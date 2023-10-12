from tkinter import *
from tkinter import ttk, messagebox
import json

class UserInterface:
    # The below intializes the variables 
    def __init__(self, write_queue, read_queue, ports, usb_devs):
        self.__initializeUIVariables()
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.__onClose)
        self.root.title("Automated Forams")
        self.__setupNotebook()
        self.write_queue = write_queue
        self.read_queue = read_queue
        self.createChannelWindow(ports, usb_devs)
        self.enableUI()
    # The message below is displayed when trying to quit
    def __onClose(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.write_queue.put(self.shutdown_msg)
            self.root.destroy()
    # The below creates a run tab on the UI
    def __createRunTab(self):
        tab = self.__createTab("Run")
        self.__addRunRadioSelects(tab)
        self.__addRunStopButtons(tab)
    # 
    def __createTab(self, title):
        tab = ttk.Frame(self.notebook, name=title.lower())
        self.notebook.add(tab, text=title)
        return tab

    def __setupNotebook(self):
        self.notebook = ttk.Notebook(self.root, name="notebook")
        self.__createRunTab()
        self.notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

    def __initializeUIVariables(self):
        self.light_directions = 2
        self.num_focal_planes = 15
        self.lights_per_img = 1
        self.light_steps = 4
        self.start_focal_offset = 0
        self.shutdown_msg = '{"function":"shutdown","args":[]}'
      # THE LINE BELOW WAS NOT IN GABBY'S CODE
        self.stop_msg = '{"function":"stop","args":[]}'
        self.numWells = 16
        self.interrupt_system = False
        self.next_command = ""
        self.channel = None
        self.is_channel_set = False

    def __addRunRadioSelects(self, tab):
        self.num_forams = StringVar()
        self.run_num_forams = IntVar()
        intCmd = tab.register(self.__isInt)
        run_ct_w = ttk.Entry(tab, name="entry_autoRunCt", width=3, textvariable=self.num_forams,  validate='key', validatecommand=(intCmd,'%P'))
        run_ct_w.grid(column=3, row=1, columnspan=1, sticky=W)
        run_ct_w.insert(END, 1)
        run_ct_lbl = ttk.Label(tab, text="Samples").grid(column=4, row=1, sticky=W)
        run_ct_r = ttk.Radiobutton(tab, text="Run For", name="button_runN", variable=self.run_num_forams, value=1).grid(column=1, row=1, columnspan=2, sticky=W)
        run_indef_r = ttk.Radiobutton(tab, text="Run All", name="button_runAll", variable=self.run_num_forams, value=0).grid(column=1, row=2, columnspan=2, sticky=W)

        self.failure_threshold = StringVar()
        failure_lbl = ttk.Label(tab, text="Failure Threshold").grid(column=4, row=3, sticky=W)
        failure_w = ttk.Entry(tab, name="entry_failureThreshold", width=3, textvariable=self.failure_threshold,  validate='key', validatecommand=(intCmd,'%P'))
        failure_w.grid(column=1, row=3, columnspan=3, sticky=W)
        failure_w.insert(END,1)
        self.image_orientations = StringVar()
        image_o_lbl = ttk.Label(tab, text="Number Orientations").grid(column=4, row=4, sticky=W)
        image_o_w = ttk.Entry(tab, name="entry_imageOrientations", width=3, textvariable=self.image_orientations,  validate='key', validatecommand=(intCmd,'%P'))
        image_o_w.grid(column=1, row=4, columnspan=3, sticky=W)
        image_o_w.insert(END,1)

    def __addRunStopButtons(self, tab):
        runcmd = tab.register(self.__run)
        stopcmd = tab.register(self.__stop)
        ttk.Button(tab, text="Run", name="button_run", command=runcmd).grid(column=2, row=11, sticky=E)
        ttk.Button(tab, text="Stop", name="button_stop", command=stopcmd).grid(column=3, row=11, sticky=W)
    # The below starts the system
    def __run(self):
        focal_plane_step = self.getFocalPlaneStep()
        if self.run_num_forams.get():
            nxt_cmd = '{{"function":"startSystem", "args":[{},{},{},{},{},{},{},{},{}]}}'.format(int(self.num_forams.get()),int(self.failure_threshold.get()),int(self.image_orientations.get()),self.light_directions,self.lights_per_img,self.light_steps,self.num_focal_planes,self.start_focal_offset,focal_plane_step)
        else:
            nxt_cmd = '{{"function":"startSystem", "args":[{},{},{},{},{},{},{},{},{}]}}'.format(-1,int(self.failure_threshold.get()),int(self.image_orientations.get()),self.light_directions,self.lights_per_img,self.light_steps,self.num_focal_planes,self.start_focal_offset,focal_plane_step)
        self.__callNextCommand(nxt_cmd)

    '''
        32 micro per step
        720 um dof coverage (72 * 10 um step size)
    '''
    # The below returns the value given below
    def getFocalPlaneStep(self):
        return (32*90) // self.num_focal_planes
    # The below interrupts the system
    def __stop(self):
        self.interrupt_system = True
       # Not in Gabbys code: self.write_queue.put(self.stop_msg)

    def __callNextCommand(self, command):
        self.next_command = command
        if self.is_ui_enabled:
            self.write_queue.put(self.next_command)
    '''
    def __isValidWell(self,val):
        if self.__isInt(val):
            return int(val)<self.numWells
        else:
            return False
    '''

    def __isInt(self, val):
        return val.isdigit()

    def getNextUserCommand(self):
        self.enableUI()

    def enableUI(self):
        self.is_ui_enabled = True

    def disableUI(self):
        self.is_ui_enabled = False

    def createChannelWindow(self, channels, usb_devs):
        win = Toplevel()
        win.attributes('-topmost', 'true')
        win.wm_title("Serial Channel Input")
        l = ttk.Label(win, text="Channel")
        l.grid(row=0, column=0)
        self.channel = StringVar()
        self.channel.set(channels[0])
        w = OptionMenu(win, self.channel, *channels)
        w.grid(row=0, column=1)
        c = ttk.Label(win, text="USB Camera")
        c.grid(row=1, column=0)
        usb_keys = list(usb_devs.keys())
        self.usb_cam_loc = StringVar()
        self.usb_cam_loc.set(usb_keys[0])
        cm = OptionMenu(win, self.usb_cam_loc, *usb_keys)
        cm.grid(row=1, column=1)
        b = ttk.Button(win, text="Select", command=lambda: self.setChannel(win))
        b.grid(row=2, column=0, columnspan=2)

    def setChannel(self, win):
        self.is_channel_set = True
        win.destroy()

    def getChannel(self):
        while not self.is_channel_set:
            self.root.update_idletasks()
            self.root.update()
        c_str = self.channel.get()
        splits = c_str.split(' - ')
        return splits[0]

    def checkQueue(self):
        try:
            msg = self.read_queue.get(0)
        except Queue.Empty:
            pass
        self.root.after(200, self.checkQueue)
