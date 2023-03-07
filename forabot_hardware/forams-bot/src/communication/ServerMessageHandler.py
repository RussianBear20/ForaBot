import json # IMPORT THE JSON LIBRARY

class ServerMessageHandler: # DEFINE SERVERMESSAGEHANDLER CLASS
    def __init__(self, forams_system): # DEFINE INITIALIZATION FUNCTION 
        self.forams_system = forams_system # STORES forams_system VALUE in self.forams_system
    # DEFINE A METHOD THAT TAKES IN A MESSAGE
    def runFunctionFromMessage(self, message):
        print("server in control") # PRINT A MESSAGE TO SERVER CONSOLE "server in control"
        try: # TRY-EXCEPT BLOCK THAT CATCHES EXCEPTIONS
            fn_name, args = self._parseMessage(message) # CALLS THE PARSE MESSAGE METHOD AND STORES RETURN VALUES
            fn = getattr(self.forams_system, fn_name) # GETS THE ATTRIBUTE OF fn_name AND STORES IN fn VAR
            message = fn(*args) # CALLS THE fn FUNCTION AND STORES IN THE message VAR
            return message # RETURNS THE message
        except: # IF AN EXCEPTION IS RAISED THE BELOW OCCURS
            raise RuntimeError("Failed to call function from message: " + message) # PRINTS WHICH MESSAGE FAILED

    def _parseMessage(self, message): # DEFINES A METHOD TO PARSE MESSAGES
        try: # TRY-EXCEPT BLOCK THAT CATCHES EXCEPTIONS
            message_parsed = json.loads(message) # PARSES message WITH json.loads AND STORES IN message_parsed
            fn = message_parsed["function"] # STORES function RETURNED FROM message_parse METHOD
            args = message_parsed["args"] # STORES args RETURNED FROM message_parsed METHOD 
            return fn, args # RETURNS fn AND args AS A TUPLE
        except: # IF AN EXCEPTION IS RAISED THE BELOW OCCURS
            raise RuntimeError("Failed to parse message: " + message) # PRINTS WHICH MESSAGE FAILED
