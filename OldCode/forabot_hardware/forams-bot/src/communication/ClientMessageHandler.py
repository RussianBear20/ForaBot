import json # IMPORT json LIBRARY

class ClientMessageHandler: # Define ClientMessageHandler class
    def __init__(self, ui, camera, read_queue): # Create constructor
        self.ui = ui # Assign ui variable
        self.camera = camera # Assign camera variable
        self.read_queue = read_queue # Assign read_queue variable
        self.shutdown_msg = '{"function":"shutdown","args":[]}' # Assign what the shutdown_msg is

    def runFunctionFromMessage(self, message): # Define runFunctionFromMessage Method
        print("client in control") # Prints that the client is in control
        try: 
            print(message) # Prints the message
            self.ui.enableUI() # Enables user interface
            recipient, fn_name, args = self._parseMessage(message) # Parses message using _parseMessage method
            rec_obj = getattr(self, recipient) # Extract the recipient object
            q_in = getattr(rec_obj, "read_queue") # Get the input queue 
            fn = getattr(rec_obj, fn_name) # Get the function to call
            q_in.put((fn,args)) # Add the function and arguments to the input queue
            message = self.read_queue.get() # Get the message from the read queue
            self.ui.disableUI() # Disable the user interface
            self.__checkShutdown(message) # Check if the message is a shutdown message
            return message 
        except: # Raises exception with printed message below if an error occurs above
            raise RuntimeError("Failed to call function from message: " + message)

    def _parseMessage(self, message): # Method to parse a message
        try: 
            print(message) # Prints the message to screen
            message_parsed = json.loads(message) # Parse the message using json library
            recipient = message_parsed["end_point"] # Get the recipient of the message
            fn = message_parsed["function"] # Get the function of the message
            args = message_parsed["args"] # Get the arguments of the message
            return recipient, fn, args # Return the message with all of its parts seperated
        except: # The below will raise an exception if failed to parse message with print statement below
            raise RuntimeError("Failed to parse message: " + message) 

    def __checkShutdown(self, message): # Method for checking shutdown by message ==
        if message == self.shutdown_msg: # If the message is a shutdown message then
            q_in = getattr(self.camera, "read_queue") # Get the camera input queue
            fn = getattr(self.camera, "shutdown") # get the shutdown function for the camera
            q_in.put((fn,[])) # Add the shutdown function to the camera input queue
        return message

    def checkForShutdown(self): # Method to check for a shutdown message
        if self.read_queue.empty(): # If the read queue is empty return False
            return False
        else: # Else check if the message is a shutdown message
            message = self.read_queue.get(False)
            return self.__checkShutdown(message)
