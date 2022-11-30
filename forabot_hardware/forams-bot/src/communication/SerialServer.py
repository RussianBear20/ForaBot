from communication.ForamsSerial import ForamsSerial
import time

class SerialServer(ForamsSerial):
    def __init__(self, message_handler): 
        super().__init__("/dev/ttyS0", False, message_handler)

    def run(self):
        self.waitForConnection()
        self._enterStateGraph()
        
    def checkShutdownOrCancel(self):
        data_left = self.ser.in_waiting
        if data_left > 0:
            message_id, message, successful = self._getFullMessage()
            if message == self.shutdown_msg:
                self.message_handler.runFunctionFromMessage(message)
                self.shutdown()
                return True
            elif message == self.stop_msg:
                return True
            else:
                return False
        
    def waitForConnection(self):
        message = ""
        while message != self.request_connection_check:
            time.sleep(0.1)
            message, message_id = self._getMessage()
        self._confirmReceipt(message_id, True)
        self._confirmControlAccepted()
