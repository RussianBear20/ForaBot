import serial # Import PySerial library
import random # Import random library
import time   # Import time library

'''
The following describes the message patter where %message_id% would represent the value of message_id, not the string:
"<%length_of_message_content%_x_%message_id%_x_%message_content%_x_%message_id%>".
Note the following substrings are reserved for the system to easily parse the data: "_x_", "<", ">".
Other formats may result in the message being ignored or unexpected function.
Note the message_content can be:
"Client In Control", "Server In Control, "Server Requesting Control", or any other string follwing the pattern:
function:%function_name%,vars:[%ordered_variables_for_accompanying_function%]
'''
class ForamsSerial(): # Define ForamsSerial class
    def __init__(self, channel ,is_controlling, message_handler): # Create constructor
        self.logger = None # Assign None to logger variable
        self.ser = serial.Serial(channel, 115200, timeout = 0.5) # Create Serial object and sets channel, baud rate, and timeout
        self.ser.reset_input_buffer() # Resets input buffer for Serial object
        self.ser.reset_output_buffer() # Resets output buffer for Serial object
        self._setupMessageConstants() # Sets up message constants
        self.is_controlling = is_controlling # Assign is_controlling variable
        self.message_handler = message_handler # Assign message_handler variable
        self.is_running = True # Assign is_running variable to True

    def _setupMessageConstants(self): # Define the _setupMessage Constant method
        self.message_break = '_x_' # Assign the message_break variable
        self.message_start = '<'   # Assign the message_start variable
        self.message_end = '>'     # Assign the message_end variable
        self.message_end_b = self.message_end.encode('utf-8') # Encode the message_end variable in utf-8
        self.successful_id_addon = "_True" # Assign the successful_id_addon variable to "True" string
        self.pass_control_message = 'Passing Control' # Assign pass_control_message variable to "Passing Control" string
        self.get_control_message = 'Accepting In Control' # Assign get_control_message variable to "Accepting In Control" string
        self.request_connection_check = 'Requesting Connection' # Assign the request_connection_check vairble to "Requesting Connection" string
        self.shutdown_msg = '{"function":"shutdown","args":[]}' # Assign the shutdown_msg vairable 
        self.stop_msg = '{"function":"stop","args":[]}' # Assign the stop_msg variable
        self.pass_control_len = str(len(self.pass_control_message)) # Assign the pass_control_len variable
        self.id_len = 5 # Assign the id_len variable
        self.timeout = 1 # Assign the timeout variable

    def run(self): # Define method for running ForamsSerial object (is implemented by subclasses)
        raise NotImplementedError

    def _enterStateGraph(self, message_to_run=None): # Define _enterStateGraph method
        while self.is_running: # Loop when is_running variable is True
            if self.is_controlling: # If is_controlling is True
                next_command = self.message_handler.runFunctionFromMessage(message_to_run) # Get the next message to execute
                self._passControl(next_command) # Passes the control 
                if next_command == self.shutdown_msg: # If the next command is to shutdown 
                    self.shutdown() # Then shutdown
                self.is_controlling = False # Assign false to is_controlling variable when shutting down
            else: # Else if is_controlling is False
                message_to_run = self._waitForControl() # wait for control to be passed
                self._acceptingControl() # Accept control
                self.is_controlling = True # Assign is_controlling variable to True
                if message_to_run == self.shutdown_msg: # If the message is a shutdown message
                    self.shutdown() # Then shutdown

    def _acceptingControl(self): # Define the _acceptingControl method
        message, message_id = self._writeMessage(self.get_control_message) # Write message to serial port and get the message id
        self._waitReceiptConfirmation(message, message_id) # Call method to wait for receipt confirmation

    def _waitForControl(self): # Define the _waitForControl method
        message_to_handle = None # Initialize message_to_handle to None
        while True: # Loop indefinitely 
            message, message_id = self._getMessage() # Get next message and message id
            self._confirmReceipt(message_id, True) # Confirm the receipt of the message
            if message == self.pass_control_message: # If message is pass control message return message_to_handle
                return message_to_handle
            elif message != self.get_control_message: # Else assign the message_to_handle to message
                message_to_handle = message

    def _getMessage(self): # Define _getMessage method
        successful = False # Initialize successful to False
        while not successful: # Run loop till successful set to True 
            message_id, message, successful = self._getFullMessage() # Parse message and assign variables
        return message, message_id # Return the message and message id

    def _waitReceiptConfirmation(self, rec_message, rec_message_id, fn_check = lambda x: False): # Define _waitReceiptConfirmation method
        successful = False # Initialize successful to False
        passed_by_lambda = False # Initialize passed_by_lambda to False
        while not successful: # Run loop till successful set to True
            message_id, message, successful = self._getFullMessage() # Parse the message and assign variables
            if message == rec_message_id+self.successful_id_addon: # If message matches the receipt message id + addon 
                successful = True # Set successful to True 
            elif fn_check(message): # Else if the above isn't True gets passed to lambda function
                self._confirmReceipt(message_id,True) # Run confirmReceipt method
                successful = True # Set successful and passed_by_lambda to True
                passed_by_lambda = True
            else: # If both conditions above are not true 
                self.ser.write(rec_message) # Write receipt message to serial port 
                received_data = '' # received_data is set to empty string
                successful = False # Message not successfully gotten
        return passed_by_lambda 

    def _getFullMessage(self): # Define _getFullMessage method
        start = time.time() # Assign start to current time to act as timer
        no_change = time.perf_counter() # Assign no_change to current time
        data_left = self.ser.in_waiting # Get the number of bytes available in the serial buffer
        received_data_b = self.ser.read_until(self.message_end_b,data_left) # Read received data until message end byte is encountered
        received_data = received_data_b.decode('utf-8') # Decode the received data to utf-8 format
        while self._checkDataIncomplete(received_data): # Loop till received data is complete
            time.sleep(0.01) # Sleep for 0.01 seconds
            data_left = self.ser.in_waiting # Determine amount of data available for reading
            if data_left > 0: # Check if there is any data left to read
                received_data_b = self.ser.read_until(self.message_end_b,data_left) # Decode binary data to utf-8 and append to received data
                received_data += received_data_b.decode('utf-8') # 
                no_change = time.perf_counter() # Record the current time
            elif (time.perf_counter()-no_change) > self.timeout: # If the time since last change is greater than timeout threshold
                return -1, "", False # Return these variables if timedout 
        message_id, message, successful = self._extractMessageInfo(received_data) # Extract the information from received message
        return message_id, message, successful # Return the extracted message info

    def _confirmReceipt(self, message_id, successful): # Define _confirmReceipt method
        self._writeMessage(message_id + '_' +str(successful)) # Write message with successful appended to it

    def _checkDataIncomplete(self, current_data): # Define _checkDataIncomplete method
        if len(current_data) == 0: # If the current_data is of length 0 return True it is incomplete
            return True
        return current_data[-1] != self.message_end # Else return boolean of (index to the left != message_end)

    def _extractMessageInfo(self, received_data): # Define the _extractMessageInfo method
        message = '' # Initialize message variable to empty string
        message_id = '' # Initialize message_id variable to empty string
        split_data = received_data.split(self.message_break) # Split received_data into a list using the message break value as the seperator
        try: # Try the below while catching exceptions
            msg_len = int(split_data[0].strip(self.message_start)) # Get the length of the message from the first item in split_data stripping off any leading instances of the message_start
            msg_len_offset = len(split_data[0])-1 # Caculate message offset
            message_id = split_data[1] # Get message id from second item in split_data
            message = split_data[2] # Get message from third item in split_data
            end_id = split_data[3].strip(self.message_end) # Get the end id from the fourth item in split_data
        except:
            return message_id, message, False # If error occurs return the message_id, message and False
        is_successful = len(message) == msg_len and end_id == message_id # Determine if the above try: was successful
        return message_id, message, is_successful 

    def _createMessage(self, message_content):
        message_len = str(len(message_content)) # STORES LENGTH OF MESSAGE 
        message_id = self._createMessageId() # STORES MESSAGE ID
        message = self.message_start + message_len + self.message_break + message_id + self.message_break + message_content + self.message_break + message_id + self.message_end
        # THE MESSAGE IS FORMATTED ABOVE
        return message.encode('utf-8'), message_id # RETURN TUPLE OF ENCODE MESSAGE W/ ID

    def _createMessageId(self): # DEFINES A METHOD FOR CREATING UNIQUE ID'S
        num = random.randint(1,10**(self.id_len)) - 1 # CREATES RANDOM MESSAGE ID
        return str(num).zfill(self.id_len) # CHANGES NUM TO A STRING AND PADS WITH 0'S TO ID_LEN

    def _writeMessage(self, message_base): # Define _writeMessage method
        message, message_id = self._createMessage(message_base) # Create message and assign variables
        self.ser.write(message) # Write message to the serial port
        return message, message_id 

    def _passControl(self, accompanying_message): # Define _passControl method
        if accompanying_message is not None: #
            message, message_id = self._writeMessage(accompanying_message)
            self._waitReceiptConfirmation(message, message_id)
        message, message_id = self._writeMessage(self.pass_control_message)
        passed_by_lambda = self._waitReceiptConfirmation(message, message_id, lambda x: x == self.get_control_message)
        if not passed_by_lambda:
            self._confirmControlAccepted()

    def _confirmControlAccepted(self):
        message = "" # Initialize message variable to empty string
        while message != self.get_control_message: # Loop while the message is not equall to control_message
            message, message_id = self._getMessage() #
        self._confirmReceipt(message_id,True)

    def shutdown(self): # SHUTDOWN PROGRAM BY SETTING is_running TO False
        self.is_running = False
