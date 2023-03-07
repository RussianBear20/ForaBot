from communication.ForamsSerial import ForamsSerial # IMPORT ForamsSerial CLASS FROM ForamsSerial.py
import time # IMPORT THE TIME MODULE

class SerialServer(ForamsSerial): # DEFINE SerialServer CLASS THAT INHERITS FROM ForamsSerial CLASS
    def __init__(self, message_handler): # INITIALIZATION CONSTRUCTOR
        super().__init__("/dev/ttyS0", False, message_handler) # CALLS CONSTRUCTOR OF PARENT CLASS

    def run(self): # DEFINE RUN METHOD
        self.waitForConnection() # WAIT FOR CONNECTION TO BE ESTABLISHED
        self._enterStateGraph() # ENTERING THE STATE GRAPH
        
    def checkShutdownOrCancel(self): # DEFINE THE checkShutdownOrCancel METHOD
        data_left = self.ser.in_waiting # GET NUMBER OF BYTES AVAILABLE FOR READING
        if data_left > 0: # IF BYTES ARE AVAILABLE DO THE BELOW
            message_id, message, successful = self._getFullMessage() # GET THE FULL MESSAGE AND STORE IN VARS
            if message == self.shutdown_msg: # CHECK IF THE MESSAGE IS A SHUTDOWN MESSAGE
                self.message_handler.runFunctionFromMessage(message) # RUNS THE FUNCTION FROM MESSAGE
                self.shutdown() # SHUTS DOWN THE CONNECTION
                return True # RETURN TRUE TO INDICATE SHUTDOWN
            elif message == self.stop_msg: # IF MESSAGE IS A STOP MESSAGE
                return True # RETURN TRUE
            else: # IF MESSAGE IS NOT A SHUTDOWN OR STOP MESSAGE RETURN FALSE
                return False
        
    def waitForConnection(self): # DEFINE waitForConnection METHOD
        message = "" # INITIALIZE MESSAGE AS EMPTY STRING
        while message != self.request_connection_check: # LOOP UNTIL MESSAGE IS A REQUEST CONNECTION CHECK
            time.sleep(0.1) # SLEEP FOR .1 SECONDS TILL THE ABOVE IS TRUE
            message, message_id = self._getMessage() # STORE MESSAGE AND MESSAGE ID IN VARS
        self._confirmReceipt(message_id, True) # CONFIRM RECEIPT OF MESSAGE
        self._confirmControlAccepted() # CONFIRM CONTROL IS ACCEPTED
