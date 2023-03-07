import json

def parseFile(file_name):
    with open(file_name, 'r') as f: # Open the file in read mode
        config_dict = json.load(f) # Load the contents of the file into a dictionary
    return config_dict # Return the dictionary

def partitionDicts(settings_dict):
    dc_dict = getMotorDict(settings_dict) # Get dictionary for DC controller
    servo_dict = getServoDict(settings_dict) # Get dictionary for Servo controller
    light_dict = getLightDict(settings_dict) # Get dictionary for Light controller
    stepper_dict = getStepperDict(settings_dict) # Get dictionary for Stepper controller
    vibration_dict = getVibrationDict(settings_dict) # Get dictionary for Vibration controller
    return dc_dict, servo_dict, light_dict, stepper_dict, vibration_dict # Return all dictionaries as a tuple


def getMotorDict(settings_dict): # getMotorDict extracts MotorDictionary values 
    hats_dict = getHatsDict(settings_dict, "DCController")
    return hats_dict

def getServoDict(settings_dict): # getServoDict extracts ServoDictionary values 
    hats_dict = getHatsDict(settings_dict, "ServoController")
    return hats_dict

def getLightDict(settings_dict): # getLightDict extracts LightDictionary values 
    hats_dict = getHatsDict(settings_dict, "LightController")
    return hats_dict

def getStepperDict(settings_dict): # getStepperDict extracts StepperDictionary values 
    hats_dict = getHatsDict(settings_dict, "StepperController")
    return hats_dict

def getVibrationDict(settings_dict): # getVibrationDict extracts VibrationDictionary values 
    hats_dict = getHatsDict(settings_dict, "VibrationController")
    return hats_dict

def getHatsDict(settings_dict, desired_hat): # getHatsDict extracts a specific controller dictionary from a settings dictionary
    for hat_name in settings_dict.keys(): # Loop through keys of settings dictionary 
        if hat_name == desired_hat: # Check if key matches desire hat value
            return settings_dict[hat_name] # Return the corresponding dictionary value
