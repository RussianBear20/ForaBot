import json

class ServerMessageHandler:
    def __init__(self, forams_system):
        self.forams_system = forams_system

    def runFunctionFromMessage(self, message):
        print("server in control")
        try:
            fn_name, args = self._parseMessage(message)
            fn = getattr(self.forams_system, fn_name)
            message = fn(*args)
            return message
        except:
            raise RuntimeError("Failed to call function from message: " + message)

    def _parseMessage(self, message):
        try:
            message_parsed = json.loads(message)
            fn = message_parsed["function"]
            args = message_parsed["args"]
            return fn, args
        except:
            raise RuntimeError("Failed to parse message: " + message)
