"""PyAdhaanApp is application for Al-Adhaan which is online adhaan web-application, link - "https://aladhan.com/"
which is built using 'PyAhdaan' API module this application was built only for adhaan times
and can provide adhaan from different countries and city and can also generate whole calendar for adhaan times aswell.

Features.
1.Shows adhaan timing from different countries and city.
2.Generate calendar for adhaan times.
3.Support for both gregorian to hijri calendar.
4.Clean and intuitive UI.
5.Calendar data in CSV format.

@Note : All the module funtions with _underscore are private and rest are public.
PyAdhaan : V 1.0
written by Haseeb mir (haseebmir.hm@gmail.com)  
"""

import pyadhaan as pyadh
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import csv

fields = ("City","Country","Address","Method","Month","Year","Fajr","Dhuhr", "Asr", "Maghrib","Isha","Date")
prayer_list = ["Fajr","Dhuhr","Asr","Maghrib","Isha"]
GREG_MONTHS = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
HIJRI_MONTHS = {1:"Muharram",2:"Safar",3:"Rabi al-awwal",4:"Rabi al-thani",5:"Jumada al-awwal",6:"Jumada al-thani",7:"Rajab",8:"Sha'ban",9:"Ramadan",10:"Shawwal",11:"Dhu al-Qi'dah",12:"Dhu al-Hijjah"}

#Color constants
APP_FG = "aquamarine1"
APP_BG =  "aquamarine3"
APP_UI = "green3"

#Method to convert Gregorian months to Hijri months.
def convert_months_list():
    is_hijri = check_var.get()
    months_list = HIJRI_MONTHS if is_hijri else GREG_MONTHS
    # Reset var and delete all old options
    dd_menu['menu'].delete(0, 'end')
    month_dd.set(months_list[1])

    # Insert list of new options (tk._setit hooks them up to var)
    for choice in months_list.values():
        dd_menu['menu'].add_command(label=choice,command=tk._setit(month_dd,choice))

#Method to get adhaan timings data using PyAdhaan-API.
def get_timings_data(city,country,address,method,month,year,data_key):
    
    if address:
        address = address.replace(" ","%20")
        timings = pyadh.prayer_day_address(address,method,data_key)
    else:    
        timings = pyadh.prayer_day_city(city,country,method,data_key)
    
    timings_data = []

    if timings:
        if data_key == "timings":
            for prayer in prayer_list:
                timings_data.append(timings[prayer])
        elif data_key == "date":
            date = timings["readable"]
            timings_data = date            
    return timings_data        

#Method to generate adhaan timings calendar.
def generate_calendar(entries):
    input_list = list(range(6))
    calendar_file = ""
    time_list,timings_data,timings_date = [],[],[]

    for index in range(6):
        input_list[index] = entries[fields[index]].get()

    city,country,address,method,year = input_list[0],input_list[1],input_list[2],input_list[3],input_list[5]
    
    is_hijri = check_var.get()
    date_key = "readable" if not is_hijri else "hijri"

    month = month_dd.get()
    MONTHS = HIJRI_MONTHS if is_hijri else GREG_MONTHS
    for k,v in MONTHS.items():
        if v == month:
            month = str(k)
    
    #Show error on empty input.        
    if not city and not country and not address:
        messagebox.showinfo("Error", "Input data is missing,(city,country or address)")        
        return

    #Generate calendar by address.    
    if address:
        calendar_file += (address + "_" + "hijri" + "_calendar" + ".csv") if is_hijri else (address + "_calendar" + ".csv")
        address = address.replace(" ","%20")
        timings_date = pyadh.prayer_calendar_address(address,method,month,year,"date",date_key,is_hijri)

        for prayer in prayer_list:
            timings_data += pyadh.prayer_calendar_address(address,method,month,year,"timings",prayer,is_hijri) 

    #Generate calendar by city.          
    else:
        calendar_file += (city + "_" + country + "_" + "hijri" + "_calendar" + ".csv") if is_hijri else (city + "_" + country + "_calendar" + ".csv")	
        timings_date = pyadh.prayer_calendar_city(city,country,method,month,year,"date",date_key,is_hijri)

        for prayer in prayer_list:
            timings_data += pyadh.prayer_calendar_city(city,country,method,month,year,"timings",prayer,is_hijri)

    next_index = (len(timings_data)//5)
    next_indicies = [0,next_index,next_index*2,next_index*3,next_index*4,next_index*5]

    #Format and write all the calendar to file.
    try:
        with open(calendar_file, 'w') as csv_file:
            writer = csv.writer(csv_file)

            for i in range(0,(next_index * 5)):
                
                if i < len(timings_date):
                    writer.writerow("Date" + timings_date[i])    
                
                for index in range(0,5):
                    if i >= (len(timings_data) // 5):
                        break
                    writer.writerow(prayer_list[index] + timings_data[next_indicies[index]])
                    
                    next_indicies[index] += 1            
                writer.writerow("\n")            
        
        messagebox.showinfo("Information", "Calendar generated in file : " + calendar_file)    
    except Exception as ex:
        messagebox.showinfo("Exception occured : " + ex)        

#Clear all the entries of form.
def clear_entry(entries):
    for index in range(0,6):
        entries[fields[index+6]].config(state="normal")

    for field in fields:
        entries[field].delete(0, "end")

    for index in range(0,6):
        entries[fields[index+6]].config(state="disabled")    

#Method to update adhaan timings on UI form.
def find_timings(entries):

    input_list = list(range(4))

    for index in range(4):
        input_list[index] = entries[fields[index]].get()

    city,country,address,method = input_list[0],input_list[1],input_list[2],input_list[3]

    #Show error on empty input.
    if not city and not country and not address:
        messagebox.showinfo("Error", "Input data is missing,(city,country or address)")
        return

    data_key = "timings"    
    prayer_timings = get_timings_data(city,country,address,method,None,None,data_key)

    for index in range(0,len(prayer_timings)):
        entries[fields[index+6]].config(state="normal")
        entries[fields[index+6]].insert(0,prayer_timings[index])

    #Get the date.
    data_key = "date"
    date = get_timings_data(city,country,address,method,None,None,data_key)
    entries[fields[len(fields)-1]].config(state="normal")
    entries[fields[len(fields)-1]].insert(0,date)

    for index in range(0,len(prayer_timings)+1):
        entries[fields[index+6]].config(state="disabled")    

#Method to make form UI fields on screen.
def make_form(root, fields):
   entries = {}
   bg = APP_BG
   for index in range(len(fields)):  
      row = Frame(root)
      ent = Entry(row)

      if index >= 6:
        ent = Entry(row,state="disabled")
        bg = APP_FG

      lab = Label(row,width=10, text=fields[index], anchor="w",background = bg)      
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[fields[index]] = ent
   return entries

#Main method to initialize and render interface items on screen.
if __name__ == "__main__":
   try:     
        root = Tk()
        root.title("PyAdhaan V 1.0")
        root.configure(background=APP_BG)
        root.resizable(False, False)
        ents = make_form(root, fields)
        root.bind("<Return>", (lambda event, e = ents: fetch(e)))

        #Render all buttons.
        timings_btn = Button(root, text = "Timings",fg = APP_UI,command=(lambda e = ents: find_timings(e)))
        timings_btn.pack(side = LEFT, padx = 5, pady = 5)
        
        timings_btn = Button(root, text = "Calendar",fg = APP_UI,command=(lambda e = ents: generate_calendar(e)))
        timings_btn.pack(side = LEFT, padx = 5, pady = 5)

        clear_btn = Button(root, text="Clear",fg = APP_UI,command=(lambda e = ents: clear_entry(e)))
        clear_btn.pack(side = LEFT, padx = 5, pady = 5)

        hijri_btn = Button(root, text="Convert",fg = APP_UI,command=(lambda e = ents: convert_months_list()))
        hijri_btn.pack(side = LEFT, padx = 5, pady = 5)
   
        quit_btn = Button(root, text = "Quit",fg = APP_UI,command = root.quit)
        quit_btn.pack(side = RIGHT, padx = 5, pady = 5)

        #Render checkbox.
        check_var = IntVar()
        cb = Checkbutton(root, text = "Hijri", variable = check_var,onvalue = 1, offvalue = 0, height=1,width = 13)
        cb.pack(side = RIGHT)
        cb.place(relx=0.78, rely=0.43,anchor=CENTER)
        cb.config(background = "aquamarine3",foreground = "black")

        #Render dropdown.
        month_dd = StringVar(root)
        month_dd.set(GREG_MONTHS[1])
        dd_menu = OptionMenu(root,month_dd,*GREG_MONTHS.values())
        dd_menu.pack(side = RIGHT, expand = YES,padx = 5, pady = 5)
        dd_menu.place(relx=0.65, rely=0.35, anchor=CENTER)
        dd_menu.config(width=19,background = 'SystemButtonFace',foreground = APP_UI)

        root.mainloop()

   except Exception as ex:
   		messagebox.showinfo("Exception occured : " + ex) 



