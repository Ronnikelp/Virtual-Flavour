# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 22:48:50 2022

@author: olive
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 13:23:52 2021
(INCOMPLETE) neater version of 6_cartridge_UI)
@author: olive
"""
import tkinter as tk
from tkinter import filedialog as fd
from functools import partial
from math import log, exp

import serial
import time


#Read and configure port[flavour_commands.py]:

ser = serial.Serial()
ser.port = 'COM4'
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity = serial.PARITY_NONE #not sure if 'no parity flow' means this
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False
ser.timeout=2
ser.write_timeout=None
ser.open()


def send_and_read(message):
    ser.flush()
    ser.write(bytes(message+'\n', 'utf-8'))
    time.sleep(0.1)
    lines = ser.readlines()
    string = ''
    for line in lines:
        string=string+str(line.decode('ascii'))
    print(string)
    return(string)
    #print(line.decode('ascii'))
    
    
    #print(ser.readline().decode('ascii'))
        
        
    #send_and_read(ser, 'Status\r\n')

    def read():
        ser.flush()
        lines = ser.readlines()
        for line in lines:
            print(line.decode('ascii'))

#end config



def remove_old_frame(frame):
    frame.pack_forget()


#check if string can be converted to a float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#parent class to create screens with rows and columns more neatly
class parent:

    #configure screen with only one column
    def row_config(self, i):
        self.frame.rowconfigure(i, weight=1, minsize=75)
        self.row_frame = tk.Frame(master=self.frame, borderwidth=1)
        self.row_frame = tk.Frame(master=self.frame, borderwidth=1)
        self.row_frame.grid(row=i, column=0, padx=4, pady=1, sticky='NSEW')
        
    #configure screen with columns and rows
    def rowcol_config(self, row, col):
        self.frame.rowconfigure(row, weight=1, minsize=75)
        self.frame.columnconfigure(col, weight=1, minsize=75)
        self.rowcol_frame = tk.Frame(master=self.frame, borderwidth=1)
        self.rowcol_frame.grid(row=row, column=col, padx=4, pady=1, sticky='NSEW')
        
        
    
#Manual operation commands:
    
def get_status():
    status = send_and_read("status")
    tk.messagebox.showinfo("Status",status)
    
def discharge_all():
    for i in range(1,7):
        send_and_read("Discharge "+str(i))
    tk.messagebox.showinfo("Message","All syringes emptied")
    
def reset():
    for i in range(1,7):
        send_and_read("Reset "+str(i)+"/r/n")
    tk.messagebox.showinfo("Message","All syringes reset")
        
    
def charge_or_precharge(arg):
    syr = arg[0]
    if arg[1] == 2:
        send_and_read("Charge "+str(syr))
    else:
        send_and_read("Precharge "+str(syr))

    return
    
#-------------------------------------------------------------------

#algorithm that tries to get user to go from one flavour to another by adjusting one syringe
class flavour_stepping(parent):
    def create_screen(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        #Choose start and end points
        self.rowcol_config(3,1)
        #two_to_3 = tk.Button(master = self.rowcol_frame, text = 'Juice 2 (pasteurised) to juice 3 (concentrate)', command = self.binary_search(1))
        two_to_3 = tk.Button(master = self.rowcol_frame, text = 'Juice 2 (pasteurised) to juice 3 (concentrate)', command = None)
        three_to_2 = tk.Button(master = self.rowcol_frame, text = 'Juice 3 (concentrate) to juice 2 (pasteurised)', command = None)
        two_to_3.grid(row=1,column=1,pady=50)
        three_to_2.grid(row=2,column=1,pady=50)
        
        return_btn = tk.Button(master=self.rowcol_frame, text = 'Back', command = lambda: main.create_screen(self.frame))
        return_btn.grid(row=3,column=1)
        
        
    #do a binary search to guide user from flavour a to flavour b
    def binary_search(self, which):
        if which ==1:
            #start point and end point for sol 5, in ml
            self.a = 1.4
            self.b = 0.02
        else:
            self.a = 0.02
            self.b = 1.4
            
            
        """
        Make calculation: If a > b, step halfway between a and b for first sample. use fechner's ln(S/S0) relation
        to find how low 'a' needs to for other sample.
        
        Ask user which sample was closer and repeat.
        """
            
        if which == 1:
            s.slist[0] = 2.00 # ml of Base
            s.slist[1] = 2.19 # ml of sol 2
            s.slist[2] = 1.00 # ml of sol 3 etc
            s.slist[3] = 1.2
            s.slist[4] = (self.a + self.b)/2
            s.slist[5] = 0.8
            
            fractional_difference = log(((self.a + self.b)/2)/self.a)
            
            #amount to add is exp(fractional difference (sign flipped) times initial ml value, i think.)
            #check this next week
            x = exp(-1*fractional_difference) * self.a
            
            tk.messagebox.showinfo("Message","Outputting sample 1/2...")
            s.dispense_flavours()
            
            tk.messagebox.showinfo("Message","Outputting sample 2/2...")
            s.slist[4] = 1 #FIND VALUE FOR THIS (continue here)
            s.dispense_flavours()
            
        else:
            tk.messagebox.showinfo("Haven;t done this bit yet")
            
            
            

        #Start by outputting something 25% closer to orange juice 3 in ml, and
        # equivilant of 25% further away from orange juice 3, using fechner;s law.
        
        #oj2 starts at 1.4, needs to get to 0.02. First guess at 0.7 ml.
        #Difference here is ln(0.7/1.4) = -0.69
        
        # Need ln (x/1.4) = 0.69, e^0.69 * 1.4 = 2.79 ml




#output one of the three premade orange juice solutions
class premade_sol(parent):
    def __init__(self):
        self.default_1 = [2.00,2.19,0.8,2,0.2,0.4]
        self.default_2 = [2.00,2.19,1.00,1.2,1.4,0.8]
        self.default_3 = [2.00,2.5,0.9,1.2,0.02,0]
        self.default_4 = [0,0,0,0,0,0]
        self.default_5 = [0,0,0,0,0,0]

    def dispense(self, which):
        if which == 1:
            s.slist[0] = self.default_1[0] # ml of Base
            s.slist[1] = self.default_1[1] # ml of sol 2
            s.slist[2] = self.default_1[2] # ml of sol 3 etc
            s.slist[3] = self.default_1[3]
            s.slist[4] = self.default_1[4]
            s.slist[5] = self.default_1[5]
            
        elif which == 2:
            s.slist[0] = self.default_2[0] # ml of Base
            s.slist[1] = self.default_2[1] # ml of sol 2
            s.slist[2] = self.default_2[2] # ml of sol 3 etc
            s.slist[3] = self.default_2[3]
            s.slist[4] = self.default_2[4]
            s.slist[5] = self.default_2[5]
            
        elif which == 3:
            s.slist[0] = self.default_3[0] # ml of Base
            s.slist[1] = self.default_3[1] # ml of sol 2
            s.slist[2] = self.default_3[2] # ml of sol 3 etc
            s.slist[3] = self.default_3[3]
            s.slist[4] = self.default_3[4]
            s.slist[5] = self.default_3[5]
            
        elif which == 4:
            s.slist[0] = self.default_4[0] # ml of Base
            s.slist[1] = self.default_4[1] # ml of sol 2
            s.slist[2] = self.default_4[2] # ml of sol 3 etc
            s.slist[3] = self.default_4[3]
            s.slist[4] = self.default_4[4]
            s.slist[5] = self.default_4[5]
            
        elif which == 5:
            s.slist[0] = self.default_5[0] # ml of Base
            s.slist[1] = self.default_5[1] # ml of sol 2
            s.slist[2] = self.default_5[2] # ml of sol 3 etc
            s.slist[3] = self.default_5[3]
            s.slist[4] = self.default_5[4]
            s.slist[5] = self.default_5[5]
            
        s.dispense_flavours()
        return
    
    def set(self, entries):
        #loop over all entries, check if the string is a decimal between 0 and 3, then set new thing to that
        for j in range(5):
            if j == 0:
                list_to_use = self.default_1
            elif j == 1:
                list_to_use = self.default_2
            elif j ==2:
                list_to_use = self.default_3
            elif j ==3:
                list_to_use = self.default_4
            elif j ==4:
                list_to_use = self.default_5
                
            for count,i in enumerate(entries[j]):
                if is_number(i.get()):
                    tmp = float(i.get())
                    #only accept values between 0 and 20
                    if tmp >=-0.00001 and tmp <=20:
                        list_to_use[count] = float(i.get())
                    
        self.create_screen(self.frame)
        return
    
    def custom(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        #-----------------------------MAKE TABLE-----------6 syringes for 5 customised flavours
        #Last row has either set or cancel
        self.rowcol_config(14,16)
        label1 = tk.Label(master = self.rowcol_frame, text = 'Sample 1',font=('Helvetica', 13, 'bold'))
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 1')
        entry11 = tk.Entry(master = self.rowcol_frame)
        entry11.grid(row=2,column=2, pady=10)
        lbl.grid(row=2,column=1, pady=0)
        entry12 = tk.Entry(master = self.rowcol_frame)
        entry12.grid(row=3,column=2, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 2')
        lbl.grid(row=3,column=1, pady=0)
        entry13 = tk.Entry(master = self.rowcol_frame)
        entry13.grid(row=4,column=2, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 3')
        lbl.grid(row=4,column=1, pady=0)
        entry14 = tk.Entry(master = self.rowcol_frame)
        entry14.grid(row=5,column=2, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 4')
        lbl.grid(row=5,column=1, pady=0)
        entry15 = tk.Entry(master = self.rowcol_frame)
        entry15.grid(row=6,column=2, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 5')
        lbl.grid(row=6,column=1, pady=0)
        entry16 = tk.Entry(master = self.rowcol_frame)
        entry16.grid(row=7,column=2, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 6')
        lbl.grid(row=7,column=1, pady=0)
        
        entry_list1 = [entry11,entry12,entry13,entry14,entry15,entry16]
        for i in range(6):
            tmp = str(self.default_1[i])
            entry_list1[i].insert(tk.END, tmp)
    
        
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 3')
        entry11 = tk.Entry(master = self.rowcol_frame)
        lbl.grid(row=4,column=1, pady=0)
        
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 4')
        entry11 = tk.Entry(master = self.rowcol_frame)
        lbl.grid(row=5,column=1, pady=0)
        
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 5')
        entry11 = tk.Entry(master = self.rowcol_frame)
        lbl.grid(row=6,column=1, pady=0)
        
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 6')
        entry11 = tk.Entry(master = self.rowcol_frame)
        lbl.grid(row=7,column=1, pady=0)
        
        label1.grid(row=1,column=1, pady=30)
        
    #first column done, repeat for 2nd and third
    
        label1 = tk.Label(master = self.rowcol_frame, text = 'Sample 2',font=('Helvetica', 13, 'bold'))
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 1')
        entry21 = tk.Entry(master = self.rowcol_frame)
        entry21.grid(row=2,column=4, pady=10)
        lbl.grid(row=2,column=3, pady=0)
        entry22 = tk.Entry(master = self.rowcol_frame)
        entry22.grid(row=3,column=4, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 2')
        lbl.grid(row=3,column=3, pady=0)
        entry23 = tk.Entry(master = self.rowcol_frame)
        entry23.grid(row=4,column=4, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 3')
        lbl.grid(row=4,column=3, pady=0)
        entry24 = tk.Entry(master = self.rowcol_frame)
        entry24.grid(row=5,column=4, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 4')
        lbl.grid(row=5,column=3, pady=0)
        entry25 = tk.Entry(master = self.rowcol_frame)
        entry25.grid(row=6,column=4, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 5')
        lbl.grid(row=6,column=3, pady=0)
        entry26 = tk.Entry(master = self.rowcol_frame)
        entry26.grid(row=7,column=4, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 6')
        lbl.grid(row=7,column=3, pady=0)
        
        entry_list2 = [entry21,entry22,entry23,entry24,entry25,entry26]
        for i in range(6):
            tmp = str(self.default_2[i])
            entry_list2[i].insert(tk.END, tmp)

        label1.grid(row=1,column=3, pady=30)
        
        
        #column 5 and 6
        label1 = tk.Label(master = self.rowcol_frame, text = 'Sample 3',font=('Helvetica', 13, 'bold'))
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 1')
        entry31 = tk.Entry(master = self.rowcol_frame)
        entry31.grid(row=2,column=6, pady=10)
        lbl.grid(row=2,column=5, pady=0)
        entry32 = tk.Entry(master = self.rowcol_frame)
        entry32.grid(row=3,column=6, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 2')
        lbl.grid(row=3,column=5, pady=0)
        entry33 = tk.Entry(master = self.rowcol_frame)
        entry33.grid(row=4,column=6, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 3')
        lbl.grid(row=4,column=5, pady=0)
        entry34 = tk.Entry(master = self.rowcol_frame)
        entry34.grid(row=5,column=6, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 4')
        lbl.grid(row=5,column=5, pady=0)
        entry35 = tk.Entry(master = self.rowcol_frame)
        entry35.grid(row=6,column=6, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 5')
        lbl.grid(row=6,column=5, pady=0)
        entry36 = tk.Entry(master = self.rowcol_frame)
        entry36.grid(row=7,column=6, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 6')
        lbl.grid(row=7,column=5, pady=0)
        
        entry_list3 = [entry31,entry32,entry33,entry34,entry35,entry36]
        for i in range(6):
            tmp = str(self.default_3[i])
            entry_list3[i].insert(tk.END, tmp)

        label1.grid(row=1,column=5, pady=30)
        #---------------------------------------------NEXT------------
        #column 7 and 8
        label1 = tk.Label(master = self.rowcol_frame, text = 'Sample 4',font=('Helvetica', 13, 'bold'))
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 1')
        entry41 = tk.Entry(master = self.rowcol_frame)
        entry41.grid(row=2,column=8, pady=10)
        lbl.grid(row=2,column=7, pady=0)
        entry42 = tk.Entry(master = self.rowcol_frame)
        entry42.grid(row=3,column=8, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 2')
        lbl.grid(row=3,column=7, pady=0)
        entry43 = tk.Entry(master = self.rowcol_frame)
        entry43.grid(row=4,column=8, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 3')
        lbl.grid(row=4,column=7, pady=0)
        entry44 = tk.Entry(master = self.rowcol_frame)
        entry44.grid(row=5,column=8, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 4')
        lbl.grid(row=5,column=7, pady=0)
        entry45 = tk.Entry(master = self.rowcol_frame)
        entry45.grid(row=6,column=8, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 5')
        lbl.grid(row=6,column=7, pady=0)
        entry46 = tk.Entry(master = self.rowcol_frame)
        entry46.grid(row=7,column=8, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 6')
        lbl.grid(row=7,column=7, pady=0)
        
        entry_list4 = [entry41,entry42,entry43,entry44,entry45,entry46]
        for i in range(6):
            tmp = str(self.default_4[i])
            entry_list4[i].insert(tk.END, tmp)

        label1.grid(row=1,column=7, pady=30)
         #---------------------------------------------NEXT------------
          #column 9 and 10
        label1 = tk.Label(master = self.rowcol_frame, text = 'Sample 5',font=('Helvetica', 13, 'bold'))
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 1')
        entry51 = tk.Entry(master = self.rowcol_frame)
        entry51.grid(row=2,column=10, pady=10)
        lbl.grid(row=2,column=9, pady=0)
        entry52 = tk.Entry(master = self.rowcol_frame)
        entry52.grid(row=3,column=10, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 2')
        lbl.grid(row=3,column=9, pady=0)
        entry53 = tk.Entry(master = self.rowcol_frame)
        entry53.grid(row=4,column=10, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 3')
        lbl.grid(row=4,column=9, pady=0)
        entry54 = tk.Entry(master = self.rowcol_frame)
        entry54.grid(row=5,column=10, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 4')
        lbl.grid(row=5,column=9, pady=0)
        entry55 = tk.Entry(master = self.rowcol_frame)
        entry55.grid(row=6,column=10, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 5')
        lbl.grid(row=6,column=9, pady=0)
        entry56 = tk.Entry(master = self.rowcol_frame)
        entry56.grid(row=7,column=10, pady=10)
        lbl= tk.Label(master = self.rowcol_frame, text = 'Syringe 6')
        lbl.grid(row=7,column=9, pady=0)
        
        entry_list5 = [entry51,entry52,entry53,entry54,entry55,entry56]
        for i in range(6):
            tmp = str(self.default_5[i])
            entry_list5[i].insert(tk.END, tmp)

        label1.grid(row=1,column=9, pady=30)
        
        

        
        all_entries = [entry_list1,entry_list2,entry_list3,entry_list4,entry_list5]
        return_btn = tk.Button(master=self.rowcol_frame, text = 'Cancel', command = lambda: self.create_screen(self.frame))
        set_btn = tk.Button(master=self.rowcol_frame, text = 'Set', command = lambda: self.set(all_entries))
        return_btn.grid(row=8,column=1, pady=30)
        set_btn.grid(row=8,column=2, pady=30)
        
        
    def create_screen(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        #Make syringes 1-6
        self.rowcol_config(5,1)
        oj1 = tk.Button(master = self.rowcol_frame, text = 'Dispense sample 1 (default: fresh)', command = lambda: self.dispense(1))
        oj2 = tk.Button(master = self.rowcol_frame, text = 'Dispense sample 2 (default: pasteurised)', command = lambda: self.dispense(2))
        oj3 = tk.Button(master = self.rowcol_frame, text = 'Dispense sample 3 (default: from concentrate)', command = lambda: self.dispense(3))
        oj4 = tk.Button(master = self.rowcol_frame, text = 'Dispense sample 4 (default: none)', command = lambda: self.dispense(4))
        oj5 = tk.Button(master = self.rowcol_frame, text = 'Dispense sample 5 (default: none)', command = lambda: self.dispense(5))
        cust = tk.Button(master = self.rowcol_frame, text = 'Customise premade solutions', command = lambda: self.custom(self.frame))
        
        oj1.grid(row=1,column=1, pady=20)
        oj2.grid(row=2,column=1, pady=20)
        oj3.grid(row=3,column=1, pady=20)
        oj4.grid(row=4,column=1, pady=20)
        oj5.grid(row=5,column=1, pady=20)
        cust.grid(row=6,column=1, pady=20)
        
            
        return_btn = tk.Button(master=self.rowcol_frame, text = 'Back', command = lambda: main.create_screen(self.frame))
        return_btn.grid(row=7,column=1)



#-------------------------------------------Manually adjust amounts in each syringe (entry boxes not working yet)-----------------
class adjust_flavour(parent):
    
    #save syringe values to syringe class
    def set_value(self, old_frame):
        
        #for each cartidge, set syringe value equal to that slider value and return to man op page.
        for i in range(6):
            s.slist[i] = self.slist[i].get()
        mo.create_screen(self.frame)
        
        return
    
    def create_screen(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        #Make syringes 1-6
        self.slist = []
        boxlist = []
        self.rowcol_config(7,3)
        for i in range(1,7):
            scale =(tk.Scale(self.rowcol_frame, from_=0, to=3, length=255, orient=tk.HORIZONTAL,                                                       resolution = 0.01))
            scale.grid(pady=1, row=i, column=2)
            scale.set(s.slist[i-1])
            label = tk.Label(self.rowcol_frame, text = ('Syringe: ',i))
            label.grid(row=i,column=1)
            #box = tk.Entry(self.rowcol_frame, textvariable='0')
            #box.grid(row=i,column=3)
            #boxlist.append(box)
            self.slist.append(scale)
            #self.columnconfigure(1)
            
        return_btn = tk.Button(master=self.rowcol_frame, text = 'Cancel', command = lambda: mo.create_screen(self.frame))
        set_btn = tk.Button(master=self.rowcol_frame, text = 'Set', command = lambda: self.set_value(self.frame))
        return_btn.grid(row=7,column=1)
        set_btn.grid(row=7,column=2)
        
        
        
# =============================================================================
# Features of manual operation screen:
# Status button (outputs status screen)
# Adjust syringes by steps or by inputting a value (seperate screen)
# Empty all syringes 
# Reset all syringes 
# Charge/precharge all syringes 
# Enter manual command
# Back to main menu
# =============================================================================

#Handles the manual operation screen
class man_op(parent):
    
        
    def create_screen(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.columnconfigure(0, weight=1, minsize=75)
        
        #Status button at the top
        self.row_config(0)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Status', command = get_status)
        adjust_flavour_btn.pack(pady=1)
        
        #Adjust syringes
        self.row_config(1)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Adjust flavour', command = lambda: af.create_screen(self.frame))
        adjust_flavour_btn.pack(pady=1)
        
        #Output flavour
        self.row_config(2)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Ouptut flavour', command = s.dispense_flavours)
        adjust_flavour_btn.pack(pady=1)
        
        #Empty all syringes
        self.row_config(3)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Empty all syringes', command = discharge_all)
        adjust_flavour_btn.pack(pady=1)
        
        #Charge syringes
        self.row_config(4)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Charge / precharge', command = lambda: self.charge(self.frame))
        adjust_flavour_btn.pack(pady=1)
        
        #Reset syringes
        self.row_config(5)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Reset all syringes', command = reset)
        adjust_flavour_btn.pack(pady=1)
        
        #Enter manual command
        self.row_config(6)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Manually enter command', command = lambda:self.manual_enter(self.frame))
        adjust_flavour_btn.pack(pady=1)
        
        
        #Return to main menu
        self.row_config(7)
        adjust_flavour_btn = tk.Button(master=self.row_frame, text = 'Return to main menu', command = lambda: main.create_screen(self.frame))
        adjust_flavour_btn.pack(pady=1)
        
        
    def manual_enter(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.rowcol_config(3,3)
        lbl = tk.Label(master = self.frame, text = 'Enter command')
        lbl.grid(row=1,column=1)
        entry = tk.Entry(master=self.frame)
        entry.grid(row=1,column=2)
        back_btn = tk.Button(master=self.frame, text = 'Return to main menu', command = lambda: self.create_screen(self.frame))
        back_btn.grid(row=2,column=1, pady=10)
        send_btn = tk.Button(master=self.frame, text = 'Send', command = lambda: send_and_read(entry.get()))
        send_btn.grid(row=1,column=3)
        
        
    
    def charge(self, old_frame):
        remove_old_frame(old_frame)
        self.frame = tk.Frame(master=main.window, width=200, height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.rowcol_config(7,2)
        
        charge1 = tk.Button(master = self.rowcol_frame, text = 'Charge 1', command = lambda: charge_or_discharge([1,2]))
        charge2 = tk.Button(master = self.rowcol_frame, text = 'Charge 2', command = lambda: charge_or_discharge([2,2]))
        charge3 = tk.Button(master = self.rowcol_frame, text = 'Charge 3', command = lambda: charge_or_discharge([3,2]))
        charge4 = tk.Button(master = self.rowcol_frame, text = 'Charge 4', command = lambda: charge_or_discharge([4,2]))
        charge5 = tk.Button(master = self.rowcol_frame, text = 'Charge 5', command = lambda: charge_or_discharge([5,2]))
        charge6 = tk.Button(master = self.rowcol_frame, text = 'Charge 6', command = lambda: charge_or_discharge([6,2]))
        
        precharge1 = tk.Button(master = self.rowcol_frame, text = 'Precharge 1', command = lambda: charge_or_discharge([1,1]))
        precharge2 = tk.Button(master = self.rowcol_frame, text = 'Precharge 2', command = lambda: charge_or_discharge([2,1]))
        precharge3 = tk.Button(master = self.rowcol_frame, text = 'Precharge 3', command = lambda: charge_or_discharge([3,1]))
        precharge4 = tk.Button(master = self.rowcol_frame, text = 'Precharge 4', command = lambda: charge_or_discharge([4,1]))
        precharge5 = tk.Button(master = self.rowcol_frame, text = 'Precharge 5', command = lambda: charge_or_discharge([5,1]))
        precharge6 = tk.Button(master = self.rowcol_frame, text = 'Precharge 6', command = lambda: charge_or_discharge([6,1]))
        
        charge1.grid(row=1,column=1,pady=15)
        charge2.grid(row=2,column=1,pady=15)
        charge3.grid(row=3,column=1,pady=15)
        charge4.grid(row=4,column=1,pady=15)
        charge5.grid(row=5,column=1,pady=15)
        charge6.grid(row=6,column=1,pady=15)
        
        precharge1.grid(row=1,column=2,pady=15)
        precharge2.grid(row=2,column=2,pady=15)
        precharge3.grid(row=3,column=2,pady=15)
        precharge4.grid(row=4,column=2,pady=15)
        precharge5.grid(row=5,column=2,pady=15)
        precharge6.grid(row=6,column=2,pady=15)
        
        
        
        return_btn = tk.Button(master=self.rowcol_frame, text = 'Back', command = lambda: man_op.create_screen(self, self.frame))
        return_btn.grid(row=7,column=1)
        
        
        
def charge_or_discharge(x):
    num = str(x[0])
    if x[1] == 1: #precharge
        send_and_read("Precharge "+num)
    else:
        send_and_read("Charge "+num)
    return
        
        
        
        
#Contains info about amount of liquid in each syringe
class syringes:
    def __init__(self):
        #s1-s6 variables of amount of ml needed for flavour in each syringe
        #self.s1, self.s2, self.s3, self.s4, self.s5 = 0
        self.slist = [0,0,0,0,0,0]
        self.names = ['Syringe 1', 'Syringe 2', 'Syringe 3', 'Syringe 4', 'Syringe 5', 'Syringe 6']
        
    def create_sliders(self, frame):
        for i in range(1,7):
            self.slist.append(tk.Scale(frame, from_=0, to=3, length=255, orient=tk.HORIZONTAL, 
                                                          resolution = 0.01))
        
    def dispense_flavours(self):
        for num, i in enumerate(self.slist):
            ml = float(i)
            steps = int(70/0.1 * ml)
            if steps > 0.1:
                steps = str(steps)
                send_and_read("Dispense "+str(num+1)+","+steps)
            
            
        return
    
    
    
    
#Creates main menu and contains the main window.
#To add a new option: increase no_rows, add the slider name to option_names and add the class to end of the order list.
class main_menu:
    
    def __init__(self):
        self.window=tk.Tk()
        self.window.geometry("")
        self.window.minsize(150, 100)
        
    def create_screen(self, old_frame):
        
        self.main_frame = tk.Frame(master=self.window, width=200, height=100)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        if old_frame:
            remove_old_frame(old_frame)

        
        #number of columns on intial screen
        no_columns = 3
        no_rows = 4
        option_names = ['Manual Operation', 'Output premade samples', 'Flavour stepping(not finished yet)']
    
        
        order = [mo, ps, fs]
    
        for i in range(no_rows-1):
            self.main_frame.rowconfigure(i, weight=1, minsize=100)
            self.main_frame.columnconfigure(0, weight=1, minsize=600)
            frame = tk.Frame(master=self.main_frame, borderwidth=1)
            frame.grid(row=i, column=0, padx=4, pady=1, sticky='NSEW')
            btn = tk.Button(master=frame, text = option_names[i], command = partial(order[i].create_screen,self.main_frame))
            
            btn.pack()
    
        #create the bottom panel with: close, save and load
    
        frame = tk.Frame(master=self.main_frame, borderwidth=1)
        frame.grid(row=no_rows, column=0, padx=4, pady=1)
        btn = tk.Button(master=frame, text = 'Close', command=self.window.destroy)
        btn.pack()



#-----------#init -----------------------------------------------------------------------
main = main_menu()
s = syringes()
af = adjust_flavour()
mo = man_op()
ps = premade_sol()
fs = flavour_stepping()
amounts = {"syringe1": 0, "syringe2": 0, "syringe3": 0, "syringe4": 0, "syringe5": 0, "syringe6": 0}


s.slist[1]=3
s.dispense_flavours()


    
#main.create_screen(None)




#main.window.mainloop() #removed tkinter popup
"""
ser.close()
"""