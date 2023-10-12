# Hardware Setup

## Attaching a Needle

NOTE: Each time a needle is changed, check handoff, bottom funnel alignment, and imaging heights in applicable.

  - Open command prompt
  - Run 'ticgui'
  - Choose the stepper motor for the tower you wish to attach a needle to from the dropdown
  - Click the "Resume" buttom at the bottom of the window if it is green
  - Set the bounds of the motor to -50,000 and 1,000 in the "set target" portion of the window
    - BE CAREFUL AT THIS STEP! The stepper can break by pushing the stepper beyond it's bounds. Do not blidly trust the bounds presented here, they may be too narrow or too wide in either direction. If the motor is making a griding sound, kill the power.
    - If homing has been setup and tested, Click device -> home forward from the menu in the top left.
    - The lower bound is the scroll box next to "Set velocity" text
    - The upper bound is the right most scroll box in the same row
    - NOTE: These bounds are for a 30mm stroke motor with 1/32 microsteps as defined in the supplied configurations/tic_settings.txt file
  - If you are replacing a needle, move the slider all the way to the right and let go
    - This should lower the needle to its lowest point
  - If a funnel is on the tower, remove it.
  - Now open the latch so the top of the tower is not covered by the funnel mount.
  - Move the slider in the ticgui to the left -40,000 should be a safe number if the supplied configuration is used
  - Screw the needle onto the needle mount
  - Lower the motor to its bottom most point
  - Close the latch so the funnel can be mounted
  - Move the needle up again -40,000 should be okay
  - Mount the funnel
  - Lower the needle
  - Denergize the motor in ticgui

## Setting the needle heights

### Handoff from needle to top suction
  - Open command prompt
  - Run 'MaestroControlCenter'
  - Open a second command prompt window or tab
  - Run 'ticgui'
  - Click the "Resume" buttom at the bottom of the window if it is green
  - Set the bounds of the motor to -50,000 and 1,000 in the "set target" portion of the window
    - The lower bound is the scroll box next to "Set velocity" text
    - The upper bound is the right most scroll box in the same row
    - NOTE: These bounds are for a 30mm stroke motor with 1/32 microsteps as defined in the supplied configurations/tic_settings.txt file
  - On the Maestro Control Center window:
    - Enable the servo associated with the top suction by clicking the box in the row associated with the servo number
    - If top suction positions are set, move to isolation or imaging handoff position
    - Otherwise, move the top suction over the appropriate needle.
  - Raise the needle with the slider on ticgui until it is about 0.5cm below the top suction
    - If needed, set the bounds to -100,000 and 3000
  - Adjust the servo position if necessary to align the needle with the suction hole
  - Move the needle up so that it goes just into the suction hole
    - Note there is about 3mm of space between the bottom of the suction hole and the mesh
  - Once the position is satisfactory
      - Record the "position dict": "handoff" position in configurations/config.json
      - If the servo position is not set, record the "position dict": ("isolation_suction" or "imaging_suction") value in configurations/config.json
  - Lower the needle
  - Denergize the motor in ticgui
  - Disable the servo by clicking the checkbox in Maestro Control Center again

### Needle at bottom of funnel
  - Open command prompt
  - Run 'ticgui'
  - Choose the stepper motor for the tower you wish to attach a needle to from the dropdown
  - Click the "Resume" buttom at the bottom of the window if it is green
  - Set the bounds of the motor to -100,000 and 3,000 in the "set target" portion of the window
    - The lower bound is the scroll box next to "Set velocity" text
    - The upper bound is the right most scroll box in the same row
    - NOTE: These bounds are for a 30mm stroke motor with 1/32 microsteps as defined in the supplied configurations/tic_settings.txt file
  - Move the needle up until it is just visible in the bottom of the funnel.
    - Note the needle should still be below the bottom of the funnel about 0.5 mm so that forams fall into the hole.
  - Record the "position dict": "base" location in configurations/config.json
  - Denergize the motor in ticgui
 
### Needle imaging height
  - This will most likely need to be accomplished during the align microscope with needle step
  - To check if just the needle height needs to be realigned:
    - Connect microscope to computer with usb
    - Open amscope software so that you can view a video stream of what the microscope sees
    - Open command prompt
    - Run 'ticgui'
    - Choose the stepper motor for the imaging needle
    - Raise the needle until it is infocus
    - Move the needle to the lowest position at which the tip of the needle looks in focus
    - Record the value under the "position dict": "imaging" variable of the "imaging_pin"

## Align microscope with needle
  - Connect microscope to computer with usb
  - Open amscope software so that you can view a video stream of what the microscope sees
    - It may be helpful to turn up gain and exposure time until the needle is almost perfectly aligned
  - With servo motors off, manually move the top suction below the microscope
  - Move the microscope tube such that it is as close to the top isolation piece as possible without touching
  - Move the top isolation out of the way
  - Manually align the microscope with the center of the funnel (approximately)
  - Open command prompt
  - Run 'ticgui'
  - Choose the stepper motor for the imaging needle
  - Raise the needle such that it is in approximately the correct focal plane
    - This is a difficult step, 
      - It can be done by manually measuring how far the needle should be from the bottom of the objective
        - For the 4x nikon objective recommended, the working distance is 25mm
      - I suggest using the tip of your finger to roughly find the correct needle height
        - To do this, get your finger in the field of view
        - Move your finger up/down such that the tip of your nail is in focus
        - The needle should be raised to about the end of your nail
        - An added bonus of this is it gives you an idea of the field of view of the microscope for future position adjustments.
  - Adjust the microscope such that the needle is in the field of view
   - Note adding a light is helpful here so that the exposure time can be lowered
   - Using your finger to find how to move the microscope is helpful
  - Once the needle is in the center of the image, tighten all the screws
  - Perform the steps in needle imaging height subsection

  - Suggestions:
    - Only move the microscope in one axis at a time
    - Don't fully loosen the screws
    - Tighten a screw slightly, then alternate to another screw. Continue until all screws are fully tightened
    - Use the wiggle room of an axis to adjust perpedicular to the axis (only works a small amount)
    - Iterate many times
  

  ### Moving the microscope
  - The microscope can be move parallel to the edge of the system by:
    - Find the mount(s) which connect:
      - The single extrusion parallel with the microscope tube
      - The horizontal extrustion at the base of the single extrusion
    - Loosen the screws that connect the mount(s) to the horizontal extrustion
    - The microscope should be able to slide parallel to the edge of the system
    - Tighten these screws when alignment is satisfactory
  - The microscope can move perpendicular to the edge of the system by:
    - Find the 6 screws which connect the microscope tower to the base plate
    - Loosen all 6 screws
    - The microscope should be able to slide perpendicular to the edge of the system
    - Tighten these screws when alignment is satisfactory

## Set Servo positions

### Top suction servo positions
  - Open command prompt
  - Run 'MaestroControlCenter'
  - Enable the servo associated with the top suction
  - Find the "isolation_suction" and "imaging_suction" locations in conjunction with handoff from needle to top suction subsection
  - Find the "well_suction" position by sight such that it is over the outer ring of wells
  - For "imaging_location" position the hole of the top isolation with the microscope objective by sight
  - For "imaging_webcam" and "isolation_webcam":
    - Connect the usb webcam to your computer and view its output with your favorite webcam app
    - Move the servo such that the imaging funnel is in view and the image looks as close as possible to "imaging_funnel_aligned_example.png"
    - Adjust the focus of the webcam until the base of the funnel is in focus
    - Record "imaging_webcam" location of the servo motor
    - Move the servo to look at the isolation funnel
    - Open command prompt
    - Run 'ticgui'
    - Move the isolation needle up to half the handoff height (e.g. if handoff is at -50040 move the needle to -25020) 
    - Adjust the servo to find the position that the needle tip is at its best focus
    - Record "isolation_webcam" location of the servo motor
    - Lower the needle
  - Disable the servo motors
   

### Well servo positions
  - Open command prompt
  - Run 'MaestroControlCenter'
  - Enable the servos associated with the top suction and well by clicking the box in the row associated with the servo number
    - If top suction positions are set, move to well_suction position
    - Otherwise move the top suction such that it is over the outer ring of wells.
  - Manually move the well servo with the slider to each well index.
  - Record the well servo position in configurations/config.json under well servo "position_dict"
  - Once all positions are recorded, double and triple check that they all align by moving to random positions
    - You should check that moving to an index from adjacent indices works
    - You should also check that moving to an index from far away indices works
  - Once all of this is confirmed and recorded, disable the servo motors


















