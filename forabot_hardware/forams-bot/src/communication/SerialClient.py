from communication.ForamsSerial import ForamsSerial

class SerialClient(ForamsSerial):
    def __init__(self, channel, message_handler):
        super().__init__(channel, True, message_handler)
        
    def run(self):
        self.requestConnection()
        self._enterStateGraph('{"end_point":"ui","function":"getNextUserCommand","args":[]}')
        
    def _getMessage(self):
        successful = False
        while not successful:
            message_id, message, successful = self._getFullMessage()
            msg = self.message_handler.checkForShutdown()
            if msg == self.shutdown_msg:
                self.shutdown()
        return message, message_id
        
    def requestConnection(self):
        message, message_id = self._writeMessage(self.request_connection_check)
        self._waitReceiptConfirmation(message, message_id)
        self._acceptingControl()
        
