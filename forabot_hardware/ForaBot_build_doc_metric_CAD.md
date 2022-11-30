Dangler 
Second draft documentation of building ForaBot (metric measurements)
Gabriella Dangler, Summer/Fall 2022
ARoS Lab, NC State University


This is my third draft detailing the assembly of the foram identification/sorting robot. 
Please reference the CAD file for parts needed and details on the design assembly. Place components in the same position as they are seen in the CAD file to ensure that all components work together properly. 
1. Chassis base and 3D-printed board mounts: 
   1. Take the grid plate, two 216mm goRAILs, four 6mm screws, and four hurricane nuts. Affix them with screws and hurricane nuts to the bottom of the plate, along the length of the left and right sides. They should be flush with the far side of the plate, and two holes short of the near side. The left rail should be affixed via the first column of holes on the left with two screws. The right rail should be affixed via the second column of holes in from the right, so that it is flush with the side. 
   2. Take the 384mm rails, six 6mm screws, and six hurricane nuts. Affix a 384mm rail to the far side of the grid, using three screws and hurricane nuts on the second row in from the far side. It will sit between the 216mm rails, and it will be flush with the edge. Affix the other rail so the screws are eight rows of holes in from the near side, also in between the 216mm rails and using three screws and hurricane nuts. 
   3. Add angle brackets as needed to reinforce structure. 
   4. Flip the structure over, so the rails are beneath the plate. This is the base chassis. 
   5. Take 3D-printed parts and place onto the base plate, with screws through the part screw holes and base plate holes, as follows:
      1. Take the TIC T825 Case (Bottom), three 10mm screws, and three threaded plates. The case should go in the bottom left corner. The protruding arms with the screw holes should face toward the x-axis. Place a TIC T825 USB Multi-Interface Stepper Motor Controller in each of the slots in the 3D-printed part. The side of the controllers with the green plastic pieces should be facing to the right. 
      2. Take the Maestro Case (bottom), four 18mm screws, and four threaded plates. The case should be installed near the top center of the base plate. The side of the Maestro Case with the hole cut into it should face away from the user, towards the far edge of the plate. Place the Micro Maestro 6-Channel USB Servo Controller in the case so that the USB port faces away from the user. 
      3. Take the Raspberry Pi Case (Bottom), three 22mm screws, one 18mm screw, and four threaded plates. The case is to be installed in the top left corner. The side with the wall with the large hole in it should face to the left. Place the board so that the USB ports face to the left, so that the ports can be used through the hole. The Breadboard should be installed via sliding it into the slits on the top of the Raspberry Pi case. The top white side of the board should face away from the user. Screw the 18mm screw through the hole in the thinner part of the base, and use the 22mm screws for the remaining three holes. 
      4. Take the Power Switch Case, three 18mm screws, and three threaded plates. The case should be installed on the right center side of the grid plate. The sides that are completely open should face to the left and right. Install the 20A, 12V SPST Switch Rocker. The power switch should be installed so that the switch faces to the right, with the red side of the switch closer to the user. 
      5. Take the Power Jack Case, three 18mm screws, and three threaded plates. The case should be installed slightly above the power switch case. Install it so that the vertically extruding portion is on the left. Place the power jack so that the side for the power cord comes out on the right. 
         1. *** When installing the power jack and its accompanying converter, make sure to screw the washer on the outside of the housing to the power jack. This will ensure that the converter stays in place when the jack is unplugged. 
2. Viewing Microscope: 
   1. Consists of: Base Adjustment, Middle Adjustment, and Focal Adjustment. 
   2. Base Adjustment: 
      1. Take the 200mm long lead screw, the 38mm long lead screw nut and the 144mm long open goRAIL. Screw the lead screw nut onto the lead screw until it is around the middle. Push both parts into the open goRAIL, so that the protruding part of the nut faces out through the open side of the goRAIL. 
      2. Take a flanged ball bearing, a thrust ball bearing, and a lead screw clamp collar. Screw the flanged ball bearing onto the left side of the lead screw, then the thrust ball bearing, and last, the clamp collar. Tighten the collar clamp. 
      3. Take a thrust ball bearing, a hyperhub, and a 3D-printed adjustment knob. Screw the thrust ball bearing onto the right side of the lead screw, then the hyperhub. Screw the adjustment knob onto the end of the hyperhub with four 10mm head screws. 
      4. Take the 1mm-thick shims and the 40x56mm grid plate. Place a shim over each upward-facing lead screw nut hole. Place the grid plate on top of the lead screw nut and shims so that each of the 56mm-long sides hang over the edge of the open rail by one hole. The grid plate should be screwed through the shims and into the lead screw nut along the middle row of holes, one screw hole in from each 40mm-long side. 
      5. Take the V-wheel standoff kit. Place one standoff at each grid plate corner, along the side of the open rail, and screw them into the grid plate. 
      6. Test that the base adjustment functions properly by twisting the adjustment knob. The nut and grid plate should move along the open rail in either direction. 
   3. Middle Adjustment: 
      1. Take one 168mm long goRAIL. It will be attached to the bottom side of the base plate on the side closest to the user. It should be orthogonal to the 384mm goRAIL beneath the chassis. Push it under the chassis until its far side is touching the 384mm goRAIL. Secure it with screws and hurricane nuts. 
      2. Take the other 168mm long goRAIL and attach it in a similar manner. 
      3. Take one 192mm long goRAIL. Place vertically on top of the protruding portion of the left 168mm long goRAIL. Push back so that the far edge of the 192mm goRAIL touches the base plate. Take a gusseted angle mount and place on the 90-degree angle made by the 168mm and 192mm goRAILS, facing toward the user. Secure to both of the rails with screws and hurricane nuts. 
      4. Repeat the above step on the right 168mm and 192mm goRAILs. 
      5. Take a flat grid bracket. Place flat against the left side of the leftmost surface made by the 168mm and 192mm goRAILs. The five-hole-wide portion should be beneath the grid plate, and the eight-hole-tall portion should be vertical. Secure the grid bracket to the structure with at least two screws and hurricane nuts for each of the two rails. 
      6. Repeat the above step on the right side of the rightmost surface made by the other 168mm and 192mm goRAILs. 
      7. Take two 1208 series surface mounts. Place one on top of each of the two 192mm goRAILs so that the middle portion is flat against the top of the rail, the protruding sides are facing upwards, and the protruding sides are on the far and near sides of the part (not left and right). Screw into the top of the rail. 
      8. Affix a 2-post clamping mount to the top of both surface mounts. 
      9. Take a precision shaft and push it through one of the 6mm-bore clamping mounts. Before pushing it through the second mount, add a linear ball bearing and push two 12mm-bore clamping mounts onto the ball bearing. Push the shaft through the other 6mm-bore clamping mounts and tighten both sides. The 12mm-bore clamping mounts can hang freely for now; they will be secured in another step. They will be referenced as left and right, assuming the user is closest to the edge of the chassis where the microscope mount is being attached. 
      10. Take the right clamping mount and affix a 5x5 grid plate, so that the clamping mount is on the left side of the plate. 
      11. Affix one end of a 48mm goRail to the grid plate. 
      12. Affix a quad-block pattern mount to the other end of the 48mm goRail. 
      13. Now take the left 6mm-bore clamping mount. Affix a 5x5 grid plate to it so that the clamping mount is in the middle. 
      14. Affix another 6mm-bore clamping mount to the other side of the grid plate, rotated so that the two clamping mounts would make the shape of an “x” with each other if viewed from the side. 
      15. Take the 432mm goRail. Position so that its length is vertical. Affix a surface mount to the bottom of it. 
      16. Affix the 8-hole low-sided U-channel to the 432mm rail with screws and hurricane nuts. Their tops should be flush with one another. 
      17. Affix three 2-post clamping mounts to the U-channel. Ensure that the middle clamp is 12mm bore, and the other two are 6mm bore. 
      18. Take the other 8-hole low-sided U-channel and affix three 2-post clamping mounts in a similar fashion. Set to the side. 
      19. Take the 432mm rail structure. Stand it vertically. Affix it to the quad-block pattern mount. Take a 200mm precision shaft and push it through both the 6mm-bore clamping mount that is making an “x” with the left 6mm-bore clamping mount, and then through the bottom 6mm-bore clamping mount on the U-channel that is attached to the 432mm rail. The end of the shaft should be about flush with the edge of the clamping mount on the U-channel. 
      20. On the other end of this shaft, push a linear ball bearing and a 12mm-bore clamping mount. Take the U-channel structure that has been set to the side and push the bottom 6mm-bore clamping mount onto the shaft. This clamping mount should be about flush with the other end of the shaft. 
      21.       22.    4. Focal Adjustment: 
      1. Take the 9-hole low-side U-channel and affix the two limit switches to it, using the limit switch mounts. 
      2. Affix the stepper motor to the U-channel using the focal stepper mount and focal stepper base parts. Ensure that the end of the stepper motor is between the two limit switches, and that it has some room before it would trigger either. 
      3. Affix four 1-post clamping mounts to the U-channel. 
      4. Take the 3-hole low-side U-channel and affix two 5-hole square beams, protruding out from the channel. Affix a third square beam between the first two. 
      5. Affix the 11-hole U-beam onto the ends of the protruding square beams. Keep the top of the U-beam flush with the upper edge of the top square beam. 
      6. Affix four 1-post clamping mounts to the 3-hole U-channel. Push a linear ball bearing through each of these clamping mounts and tighten. 
      7. Affix the microscope clamps to the opposite side of the 3-hole U-channel. This will clamp around the microscope’s DIN to C mount tube when installed. 
      8. Take two precision shafts and carefully insert one through the 1-post clamping mounts on one side of the structure, and another on the other side. This should connect the two structures while allowing free movement along the shafts. 
      9. Carefully push the end of the 11-hole U-beam onto the end of the stepper motor. A hole of the U-beam should be concentric with the hole at the end of the stepper motor. Screw in place. 
      10. Test the movement of the stepper motor. It should be able to freely move the microscope and its mount up and down along the shafts. Make sure the stepper motor properly stops when the limit switches are activated. 
   5. Full Microscope: 
      1. Take the base adjustment. Place on top of the ends of the protruding 168mm goRAILs. The open side of the rail should face upward, and the sides of the open rail should be almost flush with the outer edges of each of the 168mm goRAILs. 
      2. 3. Foram Storage Mount: 
   1. Take the 24-tooth servo block and affix it to the servo plate. 
   2. Take the two 2-post pattern mounts and affix one on each side of the servo plate, protruding up from the opposite side of the servo block and along its length. 
   3. Take the thru-hole pillow block and attach it to the top of the pattern mounts. 
   4. Take the set screw hub and screw it onto the top of the servo hub shaft. 
   5. Push the servo hub shaft down through the pillow block, so that it points toward the servo block. Push the hub shaft all the way down onto the servo shaft until it fits snugly. 
   6. Take two 5-hole pattern plates and affix them to the sides of the pattern mounts so that the mounts are concentric with the center holes of the pattern plates. The plates should be vertical, facing in the direction that the servo hub shaft is pointing. The motor’s sides should now be enclosed by the plates. 
   7. Take the standoffs and affix them between the plates near the top, one on each side. 
   8. Take the 1-post pillow block and affix it in between the plates at the middle of the very top. Offset each side of the pillow block with one spacer. 
   9. Take the D-shaft and push it down through the 1-post pillow block, set screw hub, and the servo hub shaft. It should be within the servo block as well, so that it rotates with the servo. 
   10. Use another set screw hub to affix the 3D-printed well plate to the top of the D-shaft. 
   11. Affix one dual block mount to the inside of each pattern plate. Use these to affix the full storage mount to the chassis. Reinforce with L-brackets if desired. 
4. Viewing Tray: 
   1. Affix the servo motor to the servo plate. 
   2. Affix the 2-post pattern mounts to the servo plate. 
   3. Affix the thru-hole pillow block to the top of the 2-post pattern mounts. 
   4. Affix the set screw hub onto the top of the servo hub shaft. 
   5. Push the servo hub shaft through the pillow block mount and onto the end of the servo motor. 
   6. Affix this full part onto the 7-hole U-channel. The pattern mount holes should be concentric with the large holes two up from the bottom on the U-channel. 
   7. Affix the 1-post pillow block to the U-channel. It should be between the fifth and sixth holes up from the bottom of the channel. 
   8. Take the angle pattern bracket and affix the pattern adaptor to it, using the appropriate spacers. 
   9. Affix the clamping mounts to the top of the pattern adaptor. 
   10. Push the aluminum tube through the clamps. Make sure the tube does not touch the angle pattern bracket. Tighten the clamps. This will hold the secondary camera. 
   11. Assemble the image isolation piece. The LED ring should go in between the top and middle pieces, facing down. A vibration motor should be placed in the pocket on the side of the middle piece. Place a small sheet of mesh in between the middle and bottom pieces, in the area next to the vibration motor where a hollow tube runs through the middle piece. This will keep the forams from being sucked up into the air pump when it is attached. 
   12. Affix the assembled isolation piece to the end of the 3-hole U-channel. 
   13. Affix the quad-block pattern mount, the set screw hub, and the air pump via its clamp to the 3-hole U-channel. 
   14. Affix the angle pattern mount to the top of the quad-block pattern mount. 
   15. Take the 7-hole U-channel and push the D-shaft down through the pillow blocks and hubs until it fits snugly into the servo hub shaft. 
   16. Affix the 3-hole U-channel by pushing the set screw hub onto the D-shaft, leaving a small amount of space between the two U-channels, so that the top portion can swivel freely. 
   17. Add tubing between the air pump and the hole on the side of the isolation piece. 
5. Viewing Funnel: 
   1. This part will function to hold the first funnel and needle/suction. This is where the forams are placed before the needle/suction picks one up and separates it for imaging/sorting in the second funnel/tower. 
   2. Main Mount: 
      1. Get the chassis structure. 
      2. Affix a 6 Hole U-Channel vertically. For reference, directions will be given as if the U-Channel opening is facing the user. Use four screws and nuts, as well as two dual block mounts. Place the dual block mounts at the bottom of the U-channel, on the inside, on the left and right. The dual block mounts should have their center bars facing inward, with the three empty holes facing toward each other. The U-channel should be attached to the chassis by screwing up into the dual block mounts from below the chassis. For the ease of the rest of the build for this component, remove the U-channel from the chassis, leaving the dual block mounts on the chassis as a place marker. The U-channel will be reattached once the viewing tray is built. 
      3. Screw one SPDT Miniature Limit Switch with Lever to one Limit Switch Mount D. Affix the limit switch mount on the inside face of the middle of the U-channel, 13 holes up from the bottom of the U-channel. Use one screw for each of the two holes in the mount. Slide the mount up so the screws rest at the bottom of the mount. 
      4. Take the 3D-printed needle coupler, vibration motors, and needle. Push two vibration motors into the side slots of the coupler, making sure that the wires face up. Thread the wires through the front slots so that they sit in the adjoining tubes and curve back downward. Screw the syringe needle luer into the top of the coupler. The front protruding hollow peg will receive a tube connected to the air pump after the viewing funnel is assembled. 
      5. Take the linear actuator and face the side with the label toward the user. Push the needle coupler onto the top of the actuator, so that the protruding hollow peg faces toward the user. 
      6. Take the linear actuator and the left and right stepper motor mounts. Push them onto each side of the silver rectangular rod in the middle of the linear actuator. The side cavities should face up and towards the back of the U-channel. The protruding edge on the left side of the left stepper motor mount should look like the letter “L” rotated counterclockwise, and it should be mirrored by the right stepper motor. 
      7. Push the stepper motor and mounts into the U-channel - they should fit snugly. The stepper motor mounts should be screwed in towards the back 10 holes up from the bottom of the U-channel, and towards the front 11 holes up. 
      8. Plug the wires for the stepper motor into the bottom of the motor and keep them safely out of the way until they get connected to the motor driver (TIC T825). 
   3. Air Pump Mount: 
      1. The channel from the previous step is used here. It should still be detached from the main chassis.
      2. Take two flange grommets and push them through the big holes on the right face of the tower, one hole two spaces up from the bottom of the U-channel, and the other hole four spaces up. 
      3. Later: On the inside face of the same side of the U-channel, for both flange grommets, place a 4mm ID hole reducer and push a screw through the washer and the flange grommet, securing it with a nut. 
      4. Take a 3-hole pattern plate, two flange grommets, and a 25mm bore clamping mount. Push the grommets into the top and bottom holes of the pattern plate. Affix the clamping mount with two screws, five holes up from the bottom. 
      5. Take an air pump and place it in the clamping mount so that the white plastic part faces up. Tighten the clamp down enough so that it holds snugly. It may be helpful to wrap one or two layers of electrical or painting tape just below the lip of the white plastic to allow the pump to fit more snugly in the clamp. 
      6. Take the 3-hole pattern plate and align it with the U-channel so that the air pump is upright and the grommets from the channel and the plate align with each other. Place a 4mm ID hole reducer on the outer-facing sides of each grommet, four in total. Push a screw into both of the hole reducer/grommet combinations from the outside going in towards the center of the U-channel. Secure the screws with nuts. 
      7. The U-channel should now be screwed back onto the chassis, in the same place as it was before. The open face of the channel should face toward the user. 
      8. Cut a length of tubing sufficient enough to reach between the air pump and the needle coupler. Push one end of the tubing onto the protruding peg of the coupler, and push the other end onto the protruding peg of the air pump. 
   4. Funnel & Latching Mechanism: 
      1. Affix a 90-Degree Pattern Plate on the middle column of the U-channel. Extended portion of the plate should be flush with and facing away from the top of the U-channel. 
      2. Affix a hinge to the top of the 90-degree pattern plate so that it is flat against the plate. The hinge side should be close to the vertical plate, so that the hinge opens toward the -y axis of the large plate. 
      3. Affix four ⅞” screws to a 15mm Bore, Face Tapped Clamping Mount, add one ¼” spacer to each screw, and screw one into each corner of a flat single pattern plate (1.5”x1.5” pattern plate). Make sure the adjustable clamp opening faces out, towards the user (towards the open edge of the vertical plate). 
      4. Place one ⅛” spacer on each of the two screws on the opposite side of the adjustable clamp. Use those two screws to affix to the single pattern plate. Affix the plate via the same screws to the outside of the unused side of the hinge, so that part covers the open area of the vertical plate when the hinge is open. 
      5. Place the 3D-printed funnel in the clamping hub and tighten until the funnel is held snugly in place. 
      6. Get both the top and bottom 3D-printed parts of the Magnetic Latch. Insert a 0.5” diameter magnet in each, making sure that one is a North pole and one is a South pole. Screw each magnet in place with a countersunk screw and a screw plate. 
      7. Attach the bottom latch at the top of the U-channel, so that the magnet faces up. The part should screw into four holes in the tower near the very top. 
      8. The top latch should be screwed into the end of the hinged metal part above the rest of the tower. The screw holes of the part should line up with the last holes on the edge of the latched piece, and the magnet should face down. The parts should fit together nicely when the hinge is closed. 
6. Isolation Funnel: 
   1. Repeat all parts of step 5 for the second tower, but flip anything that is not symmetrical over the y-axis so the air pump is on the left side of the second U-channel. This second U-channel should encircle the big circle at (5, 2).
