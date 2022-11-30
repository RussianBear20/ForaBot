import json

class ClientMessageHandler:
    def __init__(self, ui, camera, read_queue):
        self.ui = ui
        self.camera = camera
        self.read_queue = read_queue
        self.shutdown_msg = '{"function":"shutdown","args":[]}'

    def runFunctionFromMessage(self, message):
        print("client in control")
        try:
            print(message)
            self.ui.enableUI()
            recipient, fn_name, args = self._parseMessage(message)
            rec_obj = getattr(self, recipient)
            q_in = getattr(rec_obj, "read_queue")
            fn = getattr(rec_obj, fn_name)
            q_in.put((fn,args))
            message = self.read_queue.get()
            self.ui.disableUI()
            self.__checkShutdown(message)
            return message
        except:
            raise RuntimeError("Failed to call function from message: " + message)

    def _parseMessage(self, message):
        try:
            print(message)
            message_parsed = json.loads(message)
            recipient = message_parsed["end_point"]
            fn = message_parsed["function"]
            args = message_parsed["args"]
            return recipient, fn, args
        except:
            raise RuntimeError("Failed to parse message: " + message)

    def __checkShutdown(self, message):
        if message == self.shutdown_msg:
            q_in = getattr(self.camera, "read_queue")
            fn = getattr(self.camera, "shutdown")
            q_in.put((fn,[]))
        return message

    def checkForShutdown(self):
        if self.read_queue.empty():
            return False
        else:
            message = self.read_queue.get(False)
            return self.__checkShutdown(message)
