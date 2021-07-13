"""
GROUP 5 - TRIP PLANNER
MEMBERS:
    APIAG, MAICA
    TAGAYTAY, JOE CARLO 
    UROT, JHERYLL 
"""

from tkinter import *
from tkinter import ttk
import sqlite3
import re
from tkinter import messagebox
import tkinter.font as font
import os
from tkcalendar import DateEntry

#Starting Window
main = Tk()
main.geometry("600x710")
main.resizable(0,0)
positionRight = int((main.winfo_screenwidth()/2 - 310))
positionDown = int((main.winfo_screenheight()/2 - 389))
main.geometry("+{}+{}".format(positionRight, positionDown))

#Connects and makes a cursor to the database
dbase = sqlite3.connect('planner_data.db')
cursor = dbase.cursor()
dbase.execute("PRAGMA foreign_keys = ON;")

#Constructs table using queries
cursor.execute("""CREATE TABLE IF NOT EXISTS Trip (
    Trip_Number INTEGER PRIMARY KEY NOT NULL,
    TripName TEXT NOT NULL,
    Destination TEXT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Itinerary(
    ItineraryNumber INTEGER PRIMARY KEY NOT NULL,
    TourDate INTEGER NOT NULL,
    Location TEXT NOT NULL,
    Details TEXT NOT NULL,
    Trip_Number INTEGER NOT NULL,
    FOREIGN KEY (Trip_Number)
      REFERENCES Trip(Trip_Number)
          ON UPDATE CASCADE
          ON DELETE CASCADE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Events (
    EventNumber INTEGER PRIMARY KEY NOT NULL,
    EventName TEXT NOT NULL,
    Location TEXT NOT NULL,
    PlannedTime TEXT NOT NULL,
    Details TEXT NOT NULL,
    ItineraryNumber INTEGER NOT NULL,
    FOREIGN KEY (ItineraryNumber)
      REFERENCES Itinerary(ItineraryNumber)
          ON UPDATE CASCADE
          ON DELETE CASCADE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Bookings(
    HotelNumber INTEGER PRIMARY KEY NOT NULL,
    HotelName TEXT NOT NULL,
    ContactNumber TEXT NOT NULL,
    Address TEXT NOT NULL,
    EventNumber INTEGER NOT NULL,
    FOREIGN KEY (EventNumber)
        REFERENCES Events(EventNumber)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS HotelBooking (
    EventNumber INTEGER PRIMARY KEY NOT NULL,
    HotelNumber INTEGER NOT NULL,
    CheckIn TEXT NOT NULL,
    CheckOut TEXT NOT NULL,
    RoomType TEXT NOT NULL,
    FOREIGN KEY (EventNumber)
        REFERENCES Events(EventNumber)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    FOREIGN KEY (HotelNumber)
        REFERENCES Bookings(HotelNumber)
            ON UPDATE CASCADE
            ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Transportation (
    BookingCode INTEGER PRIMARY KEY NOT NULL,
    Departure TEXT NOT NULL,
    Arrival TEXT NOT NULL,
    CompanyName TEXT NOT NULL,
    EventNumber INTEGER NOT NULL,
    FOREIGN KEY (EventNumber)
        REFERENCES Events(EventNumber)
            ON UPDATE CASCADE
            ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS TransportationDetails (
    EventNumber INTEGER PRIMARY KEY NOT NULL,
    BookingCode INTEGER NOT NULL,
    ModeOfTransportation TEXT NOT NULL,
    FOREIGN KEY (EventNumber)
        REFERENCES Events(EventNumber)
            ON UPDATE CASCADE
            ON DELETE CASCADE
)""")

dbase.commit()    

#Function for keeping and updating a list of all the data in the database
def updateList():
    cursor.execute("SELECT * FROM Trip")
    global tripList
    tripList = cursor.fetchall()
    cursor.execute("SELECT * FROM Itinerary")
    global itiList
    itiList = cursor.fetchall()
    cursor.execute("SELECT * FROM Events")
    global eventList
    eventList = cursor.fetchall()
    cursor.execute("SELECT * FROM Bookings")
    global bookList
    bookList = cursor.fetchall()
    cursor.execute("SELECT * FROM HotelBooking")
    global hBookList
    hBookList = cursor.fetchall()
    cursor.execute("SELECT * FROM Transportation")
    global transpoList
    transpoList = cursor.fetchall()
    cursor.execute("SELECT * FROM TransportationDetails")
    global tDetailsList
    tDetailsList = cursor.fetchall()

#Function for deleting a trip in the database
def deleteTrip(trip):
    reponse = messagebox.askyesno("Travel Planner","Delete this trip?")
    if reponse == 0:
        return
    cursor.execute("DELETE from Trip WHERE Trip_Number=?",(trip[0],))
    dbase.commit()
    showTrips()

#Function for adding or editing the details of a trip
def tripDetails(comm,trip):
    def command():
        if comm == "add":
            cursor.execute("INSERT INTO Trip(Tripname,Destination,StartDate,EndDate)VALUES(?,?,?,?)",
                           (name.get(),desti.get(),sDate.get(),eDate.get()))
        else:
            cursor.execute("UPDATE Trip SET Tripname=?,Destination=?,StartDate=?,EndDate=? WHERE Trip_Number=?",
                           (name.get(),desti.get(),sDate.get(),eDate.get(),trip[0]))
        dbase.commit()
        tWindow.destroy()
        showTrips()
    
    tWindow = Toplevel(bg="#5f9ea0")
    tWindow.geometry("330x350")
    tWindow.resizable(0,0)
    tWindow.geometry("+{}+{}".format(positionRight+138, positionDown+173))
    
    this = LabelFrame(tWindow,text="Trip Details",font = ('Cinzel', 20,'bold'),labelanchor='n',bg="#5f9ea0",fg="white")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Trip Name :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=0,column=0,padx=(5,0),pady=(15,5),sticky='w')
    name = Entry(this,width=50)
    name.grid(row=1,column=0,columnspan=5,padx=(5,0),pady=5)
    Label(this,text="Destination :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=2,column=0,padx=(5,0),pady=5,sticky='w')
    desti = Entry(this,width=50)
    desti.grid(row=3,column=0,padx=(5,0),pady=5)
    Label(this,text="Start Date :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=4,column=0,padx=(5,0),pady=5,sticky='w')
    sDate = DateEntry(this,width=47,background="gray", foreground="snow")
    sDate.grid(row=5,column=0,padx=(5,0),pady=5)
    Label(this,text="End Date :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=6,column=0,padx=(5,0),pady=5,sticky='w') 
    eDate = DateEntry(this,width=47,background="gray", foreground="snow")
    eDate.grid(row=7,column=0,padx=(5,0),pady=5)
    holder = Frame(this,bg="#5f9ea0")
    holder.grid(row=8,column=0)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),height=1,width=17,bg="#264348", fg="white",command=tWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),height=1,width=17,bg="#5f9ea0", fg="white",command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        name.insert(END,trip[1])
        desti.insert(END,trip[2])
        sDate.set_date(trip[3])
        eDate.set_date(trip[4])

#Function for displaying the list of trips in the database          
def showTrips(*args):
    #Updates the main list
    updateList()
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thisEntry.get()
    #Loops thru the main list of trips and displays them
    row = 0
    for trip in tripList:
        if trip[1].lower().startswith(searchword.lower()):
            tripFrame = Frame(listFrame, highlightbackground="black", highlightthickness=1, height=110, width=570,bg="white")
            tripFrame.propagate(0)
            tripFrame.grid(row=row, column=0, padx=5, pady=(5,0))
            holder1 = Frame(tripFrame,bg="white")
            holder1.pack(side=LEFT)
            Label(holder1, text=trip[1],font = ('Tahoma', 27,'bold'),bg="white").grid(row=0,column=0,padx=5,pady=2,sticky=W)
            Label(holder1, text=trip[2]+" | "+trip[3]+" - "+trip[4],font = ('Calisto MT', 10),bg="white").grid(row=1,column=0,padx=5,pady=2)
            holder2 = Frame(tripFrame,bg="white")
            holder2.pack(side=RIGHT)
            view = Button(holder2,text="View Itineraries",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=20,command=lambda x=trip:changeTo(x))
            view.pack(side=TOP,pady=3,padx=5)
            edit = Button(holder2,text="Update Trip",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=20,command=lambda x=trip:tripDetails("edit",x))
            edit.pack(side=TOP,pady=3,padx=5)
            delete = Button(holder2,text="Delete Trip",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=20,command=lambda x=trip:deleteTrip(x))
            delete.pack(side=TOP,pady=3,padx=5)
            row += 1

    #Frame for fixing not working scrollbar        
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0)

#Function for changing back the display and some call functions to trips
def changeBack():
    tripButton.config(state=DISABLED)
    for frame in header.winfo_children():
        frame.destroy()
    Label(header, text="TRAVEL PLANNER", font = 'Century 37 bold',bg="#007575",fg="white").place(relx=.5, rely=.5, anchor='c')
    global thisEntry
    thisEntry = StringVar()
    searchBar.config(text=thisEntry)
    #Traces the changes in the thisEntry variable
    thisEntry.trace('w',showTrips)
    addButton.config(text="ADD TRIP",font = ('Bookman Old Style', 10),command=lambda:tripDetails("add",[]))
    showTrips()

#Function for changing back the display and some call functions to itineraries    
def changeTo(trip):
    tripButton.config(state=NORMAL)
    tripButton.config(command=changeBack)
    for frame in header.winfo_children():
        frame.destroy()
    Label(header, text=trip[1],font = ('Tahoma', 27,'bold'),bg="#007575",fg="white").place(relx=.5, rely=.35, anchor='c')
    Label(header, text=trip[3]+" - "+trip[4], font = ('Ink Free', 12, 'bold'),bg="#007575",fg="white").place(relx=.5, rely=.65, anchor='c')
    global thisEntry
    thisEntry = StringVar()
    searchBar.config(text=thisEntry)
    #Traces the changes in the thisEntry variable
    thisEntry.trace('w',showItinerary)
    global strain
    strain = trip[0]
    addButton.config(text="ADD ITINERARY",font = ('Bookman Old Style', 10), command=lambda:itineDetails("add",[],trip[0]))
    showItinerary()

#Function for changing some display and call function according to events
def changeFurther(itine):
    tripButton.config(state=NORMAL)
    for trip in tripList:
        if trip[0]==itine[4]:
            thisTrip=trip
    tripButton.config(command=lambda:changeTo(thisTrip))
    for frame in header.winfo_children():
        frame.destroy()
    Label(header, text=itine[3],font = ('Tahoma', 27,'bold'),bg="#007575",fg="white").place(relx=.5, rely=.35, anchor='c')
    Label(header, text=itine[2]+" | "+itine[1], font = ('Ink Free', 12, 'bold'),bg="#007575",fg="white").place(relx=.5, rely=.65, anchor='c')
    global thisEntry
    thisEntry = StringVar()
    searchBar.config(text=thisEntry)
    #Traces the changes in the thisEntry variable
    thisEntry.trace('w',showEvents)
    global strain
    strain = itine[0]
    addButton.config(text="ADD EVENT",font = ('Bookman Old Style', 10),command=lambda:eventDetails("add",[],itine[0]))
    showEvents()

#Function for deleting an itinerary
def deleteItine(itine):
    reponse = messagebox.askyesno("Travel Planner","Delete this itinerary?")
    if reponse == 0:
        return
    cursor.execute("DELETE from Itinerary WHERE ItineraryNumber=?",(itine[0],))
    dbase.commit()
    showItinerary()

#Function for adding or editing the details of an itinerary    
def itineDetails(comm,itine,nTrip):
    iWindow = Toplevel()
    iWindow.geometry("330x290")
    iWindow.resizable(0,0)
    iWindow.geometry("+{}+{}".format(positionRight+138, positionDown+173))

    def command():
        if comm == "add":
            cursor.execute("INSERT INTO Itinerary(TourDate,Location,Details,Trip_Number)VALUES(?,?,?,?)",
                           (date.get(),location.get(),details.get(),nTrip))
        else:
            cursor.execute("UPDATE Itinerary SET TourDate=?,Location=?,Details=? WHERE ItineraryNumber=?",
                           (date.get(),location.get(),details.get(),itine[0]))
        dbase.commit()
        iWindow.destroy()
        showItinerary()
        
    this = LabelFrame(iWindow,text="Itinerary Details",font = ('Cinzel', 20,'bold'),labelanchor='n',bg="#5f9ea0",fg="white")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="When?",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=0,column=0,padx=(5,0),pady=(15,5),sticky='w')
    date = DateEntry(this,width=47,background="gray", foreground="snow")
    date.grid(row=1,column=0,columnspan=5,padx=(5,0),pady=5)
    Label(this,text="Where is this located?",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=2,column=0,padx=(5,0),pady=5,sticky='w')
    location = Entry(this,width=50)
    location.grid(row=3,column=0,padx=(5,0),pady=5)
    Label(this,text="What will you be doing?",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=4,column=0,padx=(5,0),pady=5,sticky='w')
    details = Entry(this,width=50)
    details.grid(row=5,column=0,padx=(5,0),pady=5)
    holder = Frame(this,bg="#5f9ea0")
    holder.grid(row=6,column=0)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=17,command=iWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=17,command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        date.set_date(itine[1])
        location.insert(END,itine[2])
        details.insert(END,itine[3])

#Function for displaying the list of itineraries          
def showItinerary(*args):
    updateList()
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thisEntry.get()
    #Filters the list to the group of itineraries belonging to the chosen trip
    filtered = [x for x in itiList if x[4]==strain]
    #Loops thru the filtered list of itineraries and displays them    
    row = 0
    for itine in filtered:
        if itine[3].lower().startswith(searchword.lower()):
            itiFrame = Frame(listFrame, highlightbackground="black", highlightthickness=1, height=110, width=570,bg="white")
            itiFrame.propagate(0)
            itiFrame.grid(row=row, column=0, padx=5, pady=(5,0))
            holder1 = Frame(itiFrame,bg="white")
            holder1.pack(side=LEFT)
            Label(holder1, text=itine[3],font = ('Tahoma', 27,'bold'),bg="white").grid(row=0,column=0,padx=5,pady=2,sticky=W)
            Label(holder1, text=itine[2]+" | "+itine[1],anchor='w',font = ('Calisto MT', 10),bg="white").grid(row=1,column=0,padx=5,pady=2,sticky=W)
            holder2 = Frame(itiFrame,bg="white")
            holder2.pack(side=RIGHT)
            view = Button(holder2,text="View Events",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=20,command=lambda x=itine:changeFurther(x))
            view.pack(side=TOP,pady=3,padx=5)
            edit = Button(holder2,text="Update Itinerary",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=20,command=lambda x=itine:itineDetails("edit",x,strain))
            edit.pack(side=TOP,pady=3,padx=5)
            delete = Button(holder2,text="Delete Itinerary",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=20,command=lambda x=itine:deleteItine(x))
            delete.pack(side=TOP,pady=3,padx=5)
            row += 1

    #Frame for fixing not working scrollbar        
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0)

#Function for deleting an event
def deleteEvent(event):
    reponse = messagebox.askyesno("Travel Planner","Delete this event?")
    if reponse == 0:
        return
    cursor.execute("DELETE from Events WHERE EventNumber=?",(event[0],))
    dbase.commit()
    showEvents()

#Function for adding and editing details of an event
def eventDetails(comm,event,nItine):
    eWindow = Toplevel()
    eWindow.geometry("330x350")
    eWindow.resizable(0,0)
    eWindow.geometry("+{}+{}".format(positionRight+138, positionDown+173))

    def command():
        if comm=="add":
            cursor.execute("INSERT INTO Events(EventName,Location,PlannedTime,Details,ItineraryNumber)VALUES(?,?,?,?,?)",
                           (name.get(),locate.get(),pTime.get(),detail.get(),nItine))
            dbase.commit()
            eWindow.destroy()
            updateList()
            hotelDetails("add",[],eventList[-1][0])
            transpoDetails("add",[],eventList[-1][0])
        else:
            cursor.execute("UPDATE Events SET EventName=?,Location=?,PlannedTime=?,Details=? WHERE EventNumber=?",
                           (name.get(),locate.get(),pTime.get(),detail.get(),event[0]))
            dbase.commit()
            eWindow.destroy()
            showEvents()
        
    this = LabelFrame(eWindow,text="Event Details",font = ('Cinzel', 20,'bold'),labelanchor='n',bg="#5f9ea0",fg="white")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Event Name :",anchor='w',font = ('Bookman Old Style', 10),bg="#5f9ea0",fg="white").grid(row=0,column=0,padx=(5,0),pady=(15,5),sticky='w')
    name = Entry(this,width=50)
    name.grid(row=1,column=0,columnspan=5,padx=(5,0),pady=5)
    Label(this,text="Location :",anchor='w',font = ('Bookman Old Style', 10),bg="#5f9ea0",fg="white").grid(row=2,column=0,padx=(5,0),pady=5,sticky='w')
    locate = Entry(this,width=50)
    locate.grid(row=3,column=0,padx=(5,0),pady=5)
    Label(this,text="Planned Time:",anchor='w',font = ('Bookman Old Style', 10),bg="#5f9ea0",fg="white").grid(row=4,column=0,padx=(5,0),pady=5,sticky='w')
    pTime = Entry(this,width=50)
    pTime.grid(row=5,column=0,padx=(5,0),pady=5)
    Label(this,text="Details:",anchor='w',font = ('Bookman Old Style', 10),bg="#5f9ea0",fg="white").grid(row=6,column=0,padx=(5,0),pady=5,sticky='w')
    detail = Entry(this,width=50)
    detail.grid(row=7,column=0,padx=(5,0),pady=5)
    holder = Frame(this,bg="#5f9ea0")
    holder.grid(row=8,column=0)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=17,command=eWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=17,command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        name.insert(END,event[1])
        locate.insert(END,event[2])
        pTime.insert(END,event[3])
        detail.insert(END,event[4])

#Function for displaying the list of events under an itinerary
def showEvents(*args):
    updateList()
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thisEntry.get()
    #Filters the master list of events to events under the chosen itinerary
    filtered = [x for x in eventList if x[5]==strain]
    #Loops thru the filtered itineraries and displays them
    row = 0
    for event in filtered:
        if event[1].lower().startswith(searchword.lower()):
            eveFrame = Frame(listFrame, highlightbackground="black", highlightthickness=1, height=115, width=570,bg="white")
            eveFrame.propagate(0)
            eveFrame.grid(row=row, column=0, padx=5, pady=(5,0))
            holder1 = Frame(eveFrame,bg="white")
            holder1.pack(side=LEFT)
            Label(holder1, text=event[1],font = ('Tahoma', 27,'bold'),bg="white").grid(row=0,column=0,padx=5,pady=2,sticky=W)
            Label(holder1, text=event[2]+" | "+event[3],anchor='w',font = ('Calisto MT', 10),bg="white").grid(row=1,column=0,padx=5,pady=2,sticky=W)
            holder2 = Frame(eveFrame,bg="white")
            holder2.pack(side=RIGHT)
            view = Button(holder2,text="View Hotel",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=12,height=2,command=lambda x=event[0]:hotelDetails("edit",[],x))
            view.grid(row=0,column=0,pady=3,padx=5)
            look = Button(holder2,text="View Transpo",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=12,height=2,command=lambda x=event[0]:transpoDetails("edit",[],x))
            look.grid(row=0,column=1,pady=3,padx=5)
            edit = Button(holder2,text="Update Event",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=12,height=2,command=lambda x=event:eventDetails("edit",x,strain))
            edit.grid(row=1,column=0,pady=3,padx=5)
            delete = Button(holder2,text="Delete Event",font = ('Bookman Old Style', 10),bg="#5f9ea0",width=12,height=2,command=lambda x=event:deleteEvent(x))
            delete.grid(row=1,column=1,pady=3,padx=5)
            row += 1

    #Frame for fixing not working scrollbar
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0)

#Function for adding or editing the details of a hotel            
def hotelDetails(comm,hotel,nEvent):
    hWindow = Toplevel(bg="#5f9ea0")
    hWindow.geometry("330x475")
    hWindow.resizable(0,0)
    hWindow.geometry("+{}+{}".format(positionRight+300, positionDown+110))

    for x in bookList:
        if x[4]==nEvent:
            hotel = x
    
    def command():
        if comm == "add":
            cursor.execute("INSERT INTO Bookings(HotelName,ContactNumber,Address,EventNumber)VALUES(?,?,?,?)",
                           (name.get(),number.get(),address.get(),nEvent))
            dbase.commit()
            updateList()
            cursor.execute("INSERT INTO HotelBooking(EventNumber,HotelNumber,CheckIn,CheckOut,RoomType)VALUES(?,?,?,?,?)",
                           (nEvent,bookList[-1][0],iTime.get(),oTime.get(),rType.get()))
        else:
            cursor.execute("UPDATE Bookings SET HotelName=?,ContactNumber=?,Address=? WHERE HotelNumber=?",
                           (name.get(),number.get(),address.get(),hotel[0]))
            cursor.execute("UPDATE HotelBooking SET CheckIn=?,CheckOut=?,RoomType=? WHERE HotelNumber=?",
                           (iTime.get(),oTime.get(),rType.get(),hotel[0]))
        dbase.commit()
        hWindow.destroy()
        showEvents()
    
    this = LabelFrame(hWindow,text="Hotel Details",font = ('Cinzel', 20,'bold'),labelanchor='n',bg="#5f9ea0",fg="white")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Hotel Name :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=0,column=0,padx=(5,0),pady=(15,5),sticky='w')
    name = Entry(this,width=50)
    name.grid(row=1,column=0,columnspan=5,padx=(5,0),pady=5)
    Label(this,text="Contact Number :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=2,column=0,padx=(5,0),pady=5,sticky='w')
    number = Entry(this,width=50)
    number.grid(row=3,column=0,padx=(5,0),pady=5)
    Label(this,text="Address :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=4,column=0,padx=(5,0),pady=5,sticky='w')
    address = Entry(this,width=50)
    address.grid(row=5,column=0,padx=(5,0),pady=5)
    Label(this,text="Check-In Time :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=6,column=0,padx=(5,0),pady=5,sticky='w')
    iTime = Entry(this,width=50)
    iTime.grid(row=7,column=0,padx=(5,0),pady=5)
    Label(this,text="Check-Out Time :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=8,column=0,padx=(5,0),pady=5,sticky='w')
    oTime = Entry(this,width=50)
    oTime.grid(row=9,column=0,padx=(5,0),pady=5)
    Label(this,text="Room Type :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=10,column=0,padx=(5,0),pady=5,sticky='w')
    rType = Entry(this,width=50)
    rType.grid(row=11,column=0,padx=(5,0),pady=5)
    holder = Frame(this,bg="#5f9ea0")
    holder.grid(row=12,column=0)
    cancel = Button(holder,text="Close",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=17,command=hWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=17,command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        name.insert(END,hotel[1])
        number.insert(END,hotel[2])
        address.insert(END,hotel[3])
        for y in hBookList:
            if y[1]==hotel[0]:
                hBook = y
        iTime.insert(END,hBook[2])
        oTime.insert(END,hBook[3])
        rType.insert(END,hBook[4])

#Function for adding or editing the details of a transportation
def transpoDetails(comm,transpo,nEvent):
    tWindow = Toplevel(bg="#5f9ea0")
    tWindow.geometry("330x350")
    tWindow.resizable(0,0)
    tWindow.geometry("+{}+{}".format(positionRight-35, positionDown+173))

    for x in transpoList:
        if x[4]==nEvent:
            transpo = x
    
    def command():
        if comm == "add":
            cursor.execute("INSERT INTO Transportation(Departure,Arrival,CompanyName,EventNumber)VALUES(?,?,?,?)",
                           (dTime.get(),aTime.get(),name.get(),nEvent))
            dbase.commit()
            updateList()
            cursor.execute("INSERT INTO TransportationDetails(EventNumber,BookingCode,ModeOfTransportation)VALUES(?,?,?)",
                           (nEvent,transpoList[-1][0],tDrop.get()))
        else:
            cursor.execute("UPDATE Transportation SET Departure=?,Arrival=?,CompanyName=? WHERE BookingCode=?",
                           (dTime.get(),aTime.get(),name.get(),transpo[0]))
            cursor.execute("UPDATE TransportationDetails SET ModeOfTransportation=? WHERE BookingCode=?",
                           (tDrop.get(),transpo[0]))
        dbase.commit()
        tWindow.destroy()
        showEvents()
    
    this = LabelFrame(tWindow,text="Transportation Details",font = ('Cinzel', 17,'bold'),labelanchor='n',bg="#5f9ea0",fg="white")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Departure :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=0,column=0,padx=(5,0),pady=(15,5),sticky='w')
    dTime = Entry(this,width=50)
    dTime.grid(row=1,column=0,columnspan=5,padx=(5,0),pady=5)
    Label(this,text="Arrival :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=2,column=0,padx=(5,0),pady=5,sticky='w')
    aTime = Entry(this,width=50)
    aTime.grid(row=3,column=0,padx=(5,0),pady=5)
    Label(this,text="Company Name :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=4,column=0,padx=(5,0),pady=5,sticky='w')
    name = Entry(this,width=50)
    name.grid(row=5,column=0,padx=(5,0),pady=5)
    Label(this,text="Mode of Transportation :",font = ('Bookman Old Style', 10),anchor='w',bg="#5f9ea0",fg="white").grid(row=6,column=0,padx=(5,0),pady=5,sticky='w')
    tDrop = ttk.Combobox(this,state='readonly',width=30)
    tDrop['values'] = ["Plane","Boat","Car"]
    tDrop.grid(row=7,column=0,padx=(5,0),pady=5)
    holder = Frame(this,bg="#5f9ea0")
    holder.grid(row=8,column=0)
    cancel = Button(holder,text="Close",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=17,command=tWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=17,command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        dTime.insert(END,transpo[1])
        aTime.insert(END,transpo[2])
        name.insert(END,transpo[3])
        for y in tDetailsList:
            if y[1]==transpo[0]:
                mode = y[2]
        tDrop.set(mode)

#Code for creating the header display     
header = Frame(main, height=100, width=600, highlightbackground="black", highlightthickness=1,bg="#007575")
header.propagate(0)
header.grid(row=0,column=0)
Label(header, text="TRAVEL PLANNER", font = 'Century 37 bold',bg="#007575",fg="white").place(relx=.5, rely=.5, anchor='c')

#Code for creating the middle display
midFrame = Frame(main,height=50, width=1080,bg="#002929")
midFrame.propagate(0)
midFrame.grid(row=1,column=0,pady=1)
Label(midFrame, text="SEARCH:",font = ('Bookman Old Style', 10), anchor=W,bg="#002929",fg="white").grid(row=0,column=0,pady=5,padx=5)

#Declares this string as global in order to be used as a tracing method
global thisEntry
thisEntry = StringVar()
searchBar = Entry(midFrame,text=thisEntry,width=42)
searchBar.grid(row=0,column=1,padx=5,pady=5)
thisEntry.trace('w',showTrips)
addButton = Button(midFrame,text="ADD TRIP",font = ('Bookman Old Style', 10),width=14,bg="#003d3d", fg="white",command=lambda:tripDetails("add",[]))
addButton.grid(row=0,column=2,padx=5,pady=5)
tripButton = Button(midFrame,text="BACK",font = ('Bookman Old Style', 10),width=14,bg="#001414",fg="white")
tripButton.config(state=DISABLED)
tripButton.grid(row=0,column=3,padx=(0,5),pady=5)

#Code for creating a frame with a scrollbar
wrapper = LabelFrame(main)
wrapper.grid(row=2, column=0)
mycanvas = Canvas(wrapper, width=576,height=565)
listFrame= Frame(mycanvas)
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=listFrame, anchor="nw")

showTrips()
