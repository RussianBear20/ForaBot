# Setup for Raspberry pi

## From blank drive
- Install Raspbian OS (currently using 5.10.17 from date [2021-05-07](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip))
    - Note we do NOT recommend using OS Desktop with Recommended Software.
    - Use some flashing software to install OS on sd card e.g. [Balena Etcher](https://www.balena.io/etcher/)
    - Go through the setup setps on the raspberry Pi OS
        - Set a password
        - Skip Update Software
        - If date and time don't update due to edu security, maybe try to connect through phone hotspot, register device with university, or setup on a personal wifi.
- Check that git and python 3.7 are installed
	- git --version
		- If not installed, `sudo apt-get install git`
	- python3 --version
		- If not installed, `sudo apt-get install python==3.7`
- Enable serial port, SPI, I2C
	- From "start" button "Preferences" -> "Raspberry Pi Configuration"
	- Go to tab "Interfaces"
	- Click enable radio button associated with SPI, I2C, and Serial Port.
		- Make sure Serial Console remains Disabled
	- Click Ok
	- Reboot
	
- Set up folder structure on raspberry pi
	- Open a terminal (or if using an open one, make sure you're in the home directory).
	- Run `mkdir Forams`
	- Run `cd Forams`
	- Run `git clone https://github.ncsu.edu/trichmo/forams-bot.git`
	- sudo pip3 install pyyaml
	    - Note: Version 6.0 should be installed
	- Run `cd ~/Forams/forams-bot/configurations`
	- Run `cp config_example.json config_updated.json`
	    - Note: The config_updated.json file is where any future changes made for controlling the motors will likely take place.
- Install Tic and Maestro Drivers
	- Tic
		- Find "Tic Stepper Motor Controller User's Guide" online or [here](https://www.pololu.com/docs/0J71/all#1.2)
		- Install "Tic Software for Linux (Raspberry Pi)" under Section 3.2
			- Follow steps 1-7
			- Note: We use 1.8.1
		- Update the settings using configurations/tic_settings.txt
			- Run ticgui
			- Only plug in one tic board at a time and repeat the following steps for each
			    - Select driver board from the dropdown
			    - Based on the position of the motor connected to the board (isolation,imaging,or microscope), update the "serial_num" entry in configurations/config\_updated.json
			        - The tic board configurations are under the "StepperController" section of the config_updated.json file
			        - Isolation tower stepper will be found under "isolation_pin"
			        - Imaging tower stepper will be found under "imaging_pin"
			        - Microscope stepper will be found under "focal_stepper"
			    - File -> Open Settings File
			    - Select configurations/tic\_settings\_microscope.txt or configurations/tic\_settings\_tower.txt based on the tic board plugged in
			        - Microscope uses tic\_settings\_microscope.txt
			        - Tower steppers use tic\_settings\_tower.txt
			    - Click Apply Settings button at bottom right corner
			
	- Maestro
		- Find "Pololu Maestro Servo Controller User's Guide" online or [here](https://www.pololu.com/docs/0J40)
		- Install "Maestro Servo Controller Linux Software" under section 3.b.
			- In terminal `cd ~/Downloads`
			- Run `tar -xzvf maestro-linux-*.tar.gz`
			- Run `cd maestro-linux`
			- Follow the directions is README.txt (summarized below)
				- Run `sudo apt-get install libusb-1.0-0-dev mono-runtime libmono-system-windows-forms4.0-cil`
				- Run `sudo cp 99-pololu.rules /etc/udev/rules.d/`
				- Run `sudo udevadm control --reload-rules`
				- Connect Maestro Control Board to Raspberry pi using usb cable.
				- Run `./MaestroControlCenter` and check that the "Connected to:" dropdown at the top of the page shows a device and not "Not Connected"
			- Run `sudo visudo`
			    - Edit the line which begins with Defaults     secure_path
			    - Add `/home/pi/Downloads/maestro-linux:` after `secure_path=` and before the first `/`
			    - Save and exit

        - Add /home/pi/Downloads/maestro-linux to the PATH variable by:
		    - Run `nano ~/.profile`
		    - Add the following to the end of the file 
			```
				if [ -d "/home/pi/Downloads/maestro-linux" ] ; then
				    PATH="/home/pi/Downloads/maestro-linux:$PATH"
				fi
			```
		- Close and save

- Set up software for DC Motor Hat
	- Use setup instructions outlined by Adafruit DC and stepper motor hat for raspberry pi or found [here](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview)
	- Go to "Installing Software" Section of guide
	- I2C should already be enabled
	- Run `sudo pip3 install adafruit-circuitpython-motorkit`
- Set up software for Neopixel Light ring
	- Run `sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
	- Run `sudo python3 -m pip install --force-reinstall adafruit-blinka`
	- From rpi-ws281x pypi page found [here](https://pypi.org/project/rpi-ws281x/), follow steps under "Limitations: PWM:"
		- The steps disable analog audio which must be done due to limitations of the raspbery pi. The pypi page explains more for those interested.		
		- These include:
			- Run `sudo nano /etc/modprobe.d/snd-blacklist.conf`
			- Add `blacklist snd_bcm2835` to the empty file contents and save (ctrl+x, y, enter).
- Set up the raspberry pi to automatically start the system whenever turned on
	- Copy `~/Forams/forams-bot/setup/foramsbot.service` to `/etc/systemd/system`
		- Either through the files gui
		- Or by running `sudo cp  ~/Forams/forams-bot/setup/foramsbot.service /etc/systemd/system` in a terminal window.


## From raspberry pi 4 or raspberry pi 3 image

