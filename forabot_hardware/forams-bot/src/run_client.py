from user import UserInterface, UserCamera
from communication import ClientMessageHandler, SerialClient
import time
import serial.tools.list_ports
from queue import Queue
from threading import Thread
import sys
import subprocess

def getCOMPorts(): # This returns a list of the currently connected serial ports
    ports = list(serial.tools.list_ports.comports())
    result = []
    for port in ports:
        result.append(port)
    return result

def getUSBPorts(): # This returns a dictionary of the currently connected USB devices
    devices = {}
    directory = 'x64' if sys.maxsize > 2 ** 32 else 'x86'
    if sys.platform.startswith('linux'):
        df = subprocess.check_output(["v4l2-ctl",'--list-devices'])
        for i in df.split(b'\n\n'):
            if i:
                info = i.split(b'\n\t')
                try:
                    video_loc = info[1].split(b'video')[1]
                    devices[info[0].decode("utf-8") ] = int(video_loc)
                except:
                    continue
    else:
        win_devs = []
        counter = 0
        is_vid = False
        df = subprocess.run(['ffmpeg','-list_devices', 'true','-f' ,'dshow', '-hide_banner', '-i', 'dummy'], shell=True, capture_output=True)
        for i in df.stderr.split(b'\r\n'):
            i_str = str(i)
            tmp = i_str.split(']')
            if len(tmp) > 1:
                if '@' not in tmp[1]:
                    if 'DirectShow audio' in tmp[1]:
                        is_vid = False
                    if is_vid:
                        win_devs.append(tmp[1].strip().replace('"','').replace('\'',''))
                        counter+=1
                    if 'DirectShow video' in tmp[1]:
                        is_vid = True
        win_devs.reverse()
        for i,d in enumerate(win_devs.reverse()):
            devices[d] = i
    return devices

if __name__=='__main__': # This sets up the serial, USB, and UI coms 
    q_out = Queue()
    ui_q_in = Queue()
    cam_q_in = Queue()
    ports = getCOMPorts()
    webcams = getUSBPorts()
    user_interface = UserInterface.UserInterface(q_out, ui_q_in, ports, webcams)
    channel = user_interface.getChannel()
    camera = UserCamera.UserCamera(q_out, cam_q_in, webcams[user_interface.usb_cam_loc.get()], user_interface.num_focal_planes)
    message_handler = ClientMessageHandler.ClientMessageHandler(user_interface, camera, q_out)
    client = SerialClient.SerialClient(channel, message_handler)
    t1 = Thread(target=getattr(camera,"run"))
    t2 = Thread(target=getattr(client,"run"))
    t1.start()
    t2.start()
    user_interface.root.mainloop()
    t1.join()
    print('Camera Thread Closed')
    t2.join()
    print('Communication Thread Closed')
