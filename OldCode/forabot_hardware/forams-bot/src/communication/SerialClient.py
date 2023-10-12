from communication.ForamsSerial import ForamsSerial # IMPORT THE ForamsSerial CLASS FROM COMMUNICATION.FORAMSSERIAL

class SerialClient(ForamsSerial): # DEFINE SerialClient THAT INHERITS FROM ForamsSerial
    def __init__(self, channel, message_handler): # DEFINE INIT METHOD
        super().__init__(channel, True, message_handler) # CALLS THE CONSTRUCTOR OF PARENT CLASS
        
    def run(self): # DEFINE run METHOD
        self.requestConnection() # CALL THE requestConnection METHOD OF THIS CLASS
        self._enterStateGraph('{"end_point":"ui","function":"getNextUserCommand","args":[]}')
        # THE ABOVE CALLS THE enterStateGraph METHOD OF PARENT CLASS
    def _getMessage(self): # DEFINE THE getMessage METHOD
        successful = False # INITIALIZE THE successful VAR AS FALSE
        while not successful: # LOOP TILL successful = True
            message_id, message, successful = self._getFullMessage() # GETS FULL MESSAGE AND STORES VARS
            msg = self.message_handler.checkForShutdown() # CHECKS FOR SHUTDOWN AND STORES RESULT IN msg
            if msg == self.shutdown_msg: # IF msg IS EQUAL TO THE SHUTDOWN_msg 
                self.shutdown() # SHUTDOWN 
        return message, message_id # RETURNS THE MESSAGE AND MESSAGE_ID
        
    def requestConnection(self): # DEFINE THE requestConnection METHOD
        message, message_id = self._writeMessage(self.request_connection_check) # WRITE MESSAGE AND SAVE RESULT IN VARS
        self._waitReceiptConfirmation(message, message_id) # CHECK FOR RECEIPT CONFIRMATION
        self._acceptingControl() # ACCEPT CONTROL 
        
