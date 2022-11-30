import json

def parseFile(file_name):
    with open(file_name, 'r') as f:
        config_dict = json.load(f)
    return config_dict

def partitionDicts(settings_dict):
    dc_dict = getMotorDict(settings_dict)
    servo_dict = getServoDict(settings_dict)
    light_dict = getLightDict(settings_dict)
    stepper_dict = getStepperDict(settings_dict)
    vibration_dict = getVibrationDict(settings_dict)
    return dc_dict, servo_dict, light_dict, stepper_dict, vibration_dict


def getMotorDict(settings_dict):
    hats_dict = getHatsDict(settings_dict, "DCController")
    return hats_dict

def getServoDict(settings_dict):
    hats_dict = getHatsDict(settings_dict, "ServoController")
    return hats_dict

def getLightDict(settings_dict):
    hats_dict = getHatsDict(settings_dict, "LightController")
    return hats_dict

def getStepperDict(settings_dict):
    hats_dict = getHatsDict(settings_dict, "StepperController")
    return hats_dict

def getVibrationDict(settings_dict):
    hats_dict = getHatsDict(settings_dict, "VibrationController")
    return hats_dict

def getHatsDict(settings_dict, desired_hat):
    for hat_name in settings_dict.keys():
        if hat_name == desired_hat:
            return settings_dict[hat_name]
