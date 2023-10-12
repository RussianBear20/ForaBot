from driver.ForamsSystem import ForamsSystem
import time

if __name__=='__main__':
    config_file_location = '/home/pi/Forams/forams-bot/configurations/config_updated.json'
    #server_config_location = '/home/pi/Forams/forams-bot/configurations/serial_commands.json'
    foramsTestSystem = ForamsSystem(config_file_location)
# This runs the foramssystem object