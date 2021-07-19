<<<<<<< HEAD
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
from tkcalendar import DateEntry, Calendar

main = Tk()
main.geometry("1355x710")
main.resizable(0,0)
positionRight = int((main.winfo_screenwidth()/2 - 686))
positionDown = int((main.winfo_screenheight()/2 - 389))
main.geometry("+{}+{}".format(positionRight, positionDown))

#Connects and makes a cursor to the database
dbase = sqlite3.connect('planner_data.db')
cursor = dbase.cursor()
dbase.execute("PRAGMA foreign_keys = ON;")

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

#Declares image to be used
PhotoMenu = PhotoImage(file="menubar.png")
PhotoTrips = PhotoImage(file="trips2.png")
PhotoItinerary = PhotoImage(file="itinerary2.png")
PhotoEvents = PhotoImage(file="events2.png")
PhotoTravelPlanner = PhotoImage(file="travel.png")
ButtonEdit = PhotoImage(file="edit.png")
ButtonDelete = PhotoImage(file="delete.png")
ButtonEdit1 = PhotoImage(file="edit1.png")
ButtonDe1ete1 = PhotoImage(file="delete1.png")
ButtonDelete2 = PhotoImage(file="delete2.png")
ButtonEdit2 = PhotoImage(file="edit2.png")
ButtonTranspo = PhotoImage(file="transpo.png")
ButtonHotel = PhotoImage(file="hotel.png")
ButtonView = PhotoImage(file="view.png")
ButtonView1 = PhotoImage(file="view1.png")


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

def search(title,strainer):
    for frame in head.winfo_children():
        frame.destroy()
    LabelHead = Label(head, text="TRIPS",font = ('Bookman Old Style', 20,'bold'), anchor=W, bg="#cee2e8",fg="#238099")
    LabelHead.pack(side=TOP,padx=5,pady=5)
    Label(head, text="SEARCH:",font = ('Bookman Old Style', 12,'bold'), anchor=W, bg="#cee2e8").pack(side=LEFT,padx=5,pady=5)
    global thisEntry
    thisEntry = StringVar()
    global searchBar
    searchBar = Entry(head,text=thisEntry,width=200)
    searchBar.pack(side=LEFT,padx=5,pady=5)
    global addButton
    addButton = Button(head,text="Add Trip",font = ('Bookman Old Style', 12,'bold'),fg="#31859C", bg="white",width=15,command=lambda:tripDetails("add",[]))
    addButton.pack(side=LEFT,padx=5,pady=5) 
    if title=="Main":
        thisEntry.trace('w',showTrips)
        showTrips()
        return
    searchBar.config(width=97)
    Label(head,text=title+" :",font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8").pack(side=LEFT,padx=5,pady=5)
    global cBox
    cBox = ttk.Combobox(head,state='readonly',width=30)
    cBox.pack(side=LEFT,padx=10,pady=5)
    if title=="Trip":
        LabelHead.config(text="ITINERARY")
        cBox['values']=[x[1] for x in tripList]
        if strainer != '':
            cBox.set(strainer)
        else:
            cBox.set(tripList[0][1])
        cBox.config(width=27,font = ('Bookman Old Style', 10))
        cBox.bind('<<ComboboxSelected>>',showItinerary)
        thisEntry.trace('w',showItinerary)
        showItinerary()
    elif title=="Itinerary":
        cBox['values']=[x[2] for x in itiList]
        if strainer != '':
            cBox.set(strainer)
        else:
            cBox.set(itiList[0][2])
        cBox.config(width=27,font = ('Bookman Old Style', 10))
        cBox.bind('<<ComboboxSelected>>',showEvents)
        thisEntry.trace('w',showEvents)
        showEvents()
        LabelHead.config(text="EVENTS")
    
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
    
    tWindow = Toplevel(bg="white")
    tWindow.geometry("450x258")
    tWindow.resizable(0,0)
    tWindow.geometry("+{}+{}".format(positionRight+450, positionDown+230))
    
    this = LabelFrame(tWindow,text="Trip Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Trip Name :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    name = Entry(this,width=50)
    name.place(x=115, y=22)
    Label(this,text="Destination :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    desti = Entry(this,width=50)
    desti.place(x=115, y=62)
    Label(this,text="Start Date :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    sDate = DateEntry(this,width=47,background="gray", foreground="snow")
    sDate.place(x=115, y=102)
    Label(this,text="End Date :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    eDate = DateEntry(this,width=47,background="gray", foreground="snow")
    eDate.place(x=115, y=142)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=170)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),height=1,width=23,bg="#264348", fg="white",command=tWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),height=1,width=23,bg="#5f9ea0", fg="white",command=command)
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
    searchBar.config(width=140)
    addButton.config(text="Add Trip",command=lambda:tripDetails("add",[]))
    searchword = thisEntry.get()
    #Loops thru the main list of trips and displays them
    row, column = 0, 0
    for trip in tripList:
        if trip[1].lower().startswith(searchword.lower()):
            tripFrame = Frame(listFrame, highlightbackground="#31849b", highlightthickness=1, height=175, width=265,bg="white")
            tripFrame.propagate(0)
            tripFrame.grid(row=row, column=column, padx=(10,0), pady=(10,0))
            Label(tripFrame, text=trip[1],font = ('Tahoma', 26,'bold'),bg="white",fg="#31849b").pack(side=TOP,fill='x',padx=5,pady=(10,2))
            Label(tripFrame, text=trip[2],font = ('Calisto MT', 12),bg="white",fg="#2f869e").pack(side=TOP,fill='x',padx=5,pady=2)
            Label(tripFrame, text=trip[3]+" - "+trip[4],font = ('Calisto MT', 12),bg="white",fg="#2f869e").pack(side=TOP,fill='x',padx=5,pady=2)
            holder = Frame(tripFrame,bg='white')
            holder.pack(side=TOP)
            view = Button(holder,image =ButtonView, bd =0, bg = "white", command=lambda x=trip[1]:search("Trip",x))
            view.pack(side=LEFT,pady=5,padx=5)
            edit = Button(holder,image =ButtonEdit1, bd =0, bg = "white", command=lambda x=trip:tripDetails("edit",x))
            edit.pack(side=LEFT,pady=5,padx=5)
            delete = Button(holder,image =ButtonDe1ete1, bd =0, bg = "white",command=lambda x=trip:deleteTrip(x))
            delete.pack(side=RIGHT,pady=5,padx=5)
            column += 1
            if column == 4:
                column = 0
                row += 1
    #Frame for fixing not working scrollbar        
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0,columnspan=3)     

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
    iWindow = Toplevel(bg="white")
    iWindow.geometry("465x225")
    iWindow.resizable(0,0)
    iWindow.geometry("+{}+{}".format(positionRight+440, positionDown+250))

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
        
    this = LabelFrame(iWindow,text="Itinerary Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Date :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    date = DateEntry(this,width=47,background="gray", foreground="snow")
    date.place(x=135, y=22)
    Label(this,text="Location :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    location = Entry(this,width=50)
    location.place(x=135, y=62)
    Label(this,text="Main Attraction :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    details = Entry(this,width=50)
    details.place(x=135, y=102)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=20, y=130)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=23,command=iWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=23,command=command)
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
    #Filters the list to the group of itineraries belonging to the chosen trip
    for x in tripList:
        if x[1] == cBox.get():
            strain=x[0]
    addButton.config(text="Add Itinerary",command=lambda:itineDetails("add",[],strain))
    searchword = thisEntry.get()
    filtered = [x for x in itiList if x[4]==strain]
    #Loops thru the filtered list of itineraries and displays them    
    row = 0
    
    for itine in filtered:
        if itine[3].lower().startswith(searchword.lower()):
            itiFrame = Frame(listFrame)
            itiFrame.grid(row=row, column=0)
            holder1 = Frame(itiFrame,height=100,width=120, highlightbackground="#31849b",highlightthickness=1,bg="white")
            holder1.pack(side=LEFT,pady=(10,0),padx=5)
            holder1.propagate(0)
            holder2 = Frame(itiFrame,height=100,width=965, highlightbackground="#31849b",highlightthickness=1,bg="white")
            holder2.pack(side=RIGHT,pady=(10,0),padx=5)
            holder2.propagate(0)
            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            month = months[int(itine[1].split('/')[0])-1]
            Label(holder1, text=month,font = ('Tahoma', 24,'bold'),bg="white",fg="#31849b").place(relx=.5, rely=.3, anchor='c')
            Label(holder1, text=itine[1].split('/')[1],font = ('Tahoma', 18),bg="white",fg="#31849b").place(relx=.5, rely=.75, anchor='c')
            temp=Frame(holder2,bg='white')
            temp.pack(side=LEFT)
            Label(temp, text=itine[3],font = ('Tahoma', 24,'bold'),bg="white",fg="#31849b",anchor='w').grid(row=0,column=0,padx=15,sticky='w')
            Label(temp, text=itine[2],font = ('Tahoma', 18),bg="white",fg="#2f869e",anchor='w').grid(row=1,column=0,padx=15,sticky='w')
            delete = Button(holder2,image = ButtonDelete, bd=0, bg="white",command=lambda x=itine:deleteItine(x))
            delete.pack(side=RIGHT,padx=(5,10),pady=5)
            edit = Button(holder2,image = ButtonEdit, bd=0, bg="white",command=lambda x=itine:itineDetails("edit",x,strain))
            edit.pack(side=RIGHT,padx=5,pady=5)
            view = Button(holder2,image=ButtonView1,bd=0, bg="white",command=lambda x=itine[2]:search('Itinerary',x))
            view.pack(side=RIGHT,padx=5,pady=5)
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
    eWindow = Toplevel(bg="white")
    eWindow.geometry("450x265")
    eWindow.resizable(0,0)
    eWindow.geometry("+{}+{}".format(positionRight+450, positionDown+220))

    def command():
        if comm=="add":
            cursor.execute("INSERT INTO Events(EventName,Location,PlannedTime,Details,ItineraryNumber)VALUES(?,?,?,?,?)",
                           (name.get(),locate.get(),pTime.get(),detail.get(),nItine))
            dbase.commit()
            eWindow.destroy()
            updateList()

        else:
            cursor.execute("UPDATE Events SET EventName=?,Location=?,PlannedTime=?,Details=? WHERE EventNumber=?",
                           (name.get(),locate.get(),pTime.get(),detail.get(),event[0]))
            dbase.commit()
            eWindow.destroy()
            showEvents()
        
    this = LabelFrame(eWindow,text="Event Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Event Name :",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    name = Entry(this,width=50)
    name.place(x=115, y=22)
    Label(this,text="Location :",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    locate = Entry(this,width=50)
    locate.place(x=115, y=62)
    Label(this,text="Planned Time:",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    pTime = Entry(this,width=50)
    pTime.place(x=115, y=102)
    Label(this,text="Details:",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    detail = Entry(this,width=50)
    detail.place(x=115, y=140)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=170)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=23,command=eWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=23,command=command)
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
    #Filters the list to the group of itineraries belonging to the chosen trip
    for x in itiList:
        if x[2] == cBox.get():
            strain=x[0]
    addButton.config(text="Add Event",command=lambda:eventDetails("add",[],strain))
    searchword = thisEntry.get()
    #Filters the master list of events to events under the chosen itinerary
    filtered = [x for x in eventList if x[5]==strain]
    #Loops thru the filtered itineraries and displays them
    row, column, count = 0, 0, 1
    for event in filtered:
        if event[1].lower().startswith(searchword.lower()):
            eveFrame = Frame(listFrame, highlightbackground="#31849b", highlightthickness=1, height=175, width=265,bg="white")
            eveFrame.propagate(0)
            eveFrame.grid(row=row, column=column, padx=(10,0), pady=(10,0))
            Label(eveFrame, text=event[1],font = ('Tahoma', 20,'bold'),bg="white",fg="#31849b").pack(side=TOP,fill='x',padx=5,pady=(15,2))
            Label(eveFrame, text=event[2],font = ('Calisto MT', 10),bg="white",fg="#2f869e").pack(side=TOP,fill='x',padx=5,pady=2)
            holder1 = Frame(eveFrame,bg='white')
            holder1.pack(side=TOP)
            hotel = Button(holder1,image = ButtonHotel, bg="white", bd=0,command=lambda x=event[0]:hotelDetails(x))
            hotel.pack(side=LEFT,pady=(5,0),padx=5)
            transpo = Button(holder1,image =ButtonTranspo, bg="white", bd=0,command=lambda x=event[0]:transpoDetails(x))
            transpo.pack(side=LEFT,pady=(5,0),padx=5)
            #holder2 = Frame(eveFrame,bg='white')
            #holder2.pack(side=TOP)
            edit = Button(holder1,image = ButtonEdit2, bg="white", bd=0,command=lambda x=event:eventDetails("edit",x,strain))
            edit.pack(side=LEFT,pady=(5,0),padx=5)
            delete = Button(holder1,image = ButtonDelete2, bg="white", bd=0,command=lambda x=event:deleteEvent(x))
            delete.pack(side=RIGHT,pady=(5,0),padx=5)
            Label(eveFrame,text=count,font= ('Tahoma', 16,'bold'),bg="white",fg="#31849b").place(relx=0.025,rely=0.005)
            column += 1
            count += 1
            if column == 4:
                column = 0
                row += 1

    #Frame for fixing not working scrollbar
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0)

#Function for adding or editing the details of a hotel            
def hotelDetails(nEvent):
    hWindow = Toplevel(bg="white")
    hWindow.geometry("473x340")
    hWindow.resizable(0,0)
    hWindow.geometry("+{}+{}".format(positionRight+440, positionDown+180))

    comm = "add"
    
    for x in bookList:
        if x[4]==nEvent:
            hotel = x
            comm = "edit"
    
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
    
    this = LabelFrame(hWindow,text="Hotel Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Hotel Name :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    name = Entry(this,width=50)
    name.place(x=135, y=22)
    Label(this,text="Contact Number :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    number = Entry(this,width=50)
    number.place(x=135, y=62)
    Label(this,text="Address :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    address = Entry(this,width=50)
    address.place(x=135, y=102)
    Label(this,text="Check-In Time :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    iTime = Entry(this,width=50)
    iTime.place(x=135, y=142)
    Label(this,text="Check-Out Time :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=180)
    oTime = Entry(this,width=50)
    oTime.place(x=135, y=182)
    Label(this,text="Room Type :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=220)
    rType = Entry(this,width=50)
    rType.place(x=135, y=222)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=250)
    cancel = Button(holder,text="Close",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=24,command=hWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=24,command=command)
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

def transpoDetails(nEvent):
    tWindow = Toplevel(bg="white")
    tWindow.geometry("470x260")
    tWindow.resizable(0,0)
    tWindow.geometry("+{}+{}".format(positionRight+430, positionDown+200))

    comm = "add"
    
    for x in transpoList:
        if x[4]==nEvent:
            transpo = x
            comm = "edit"
    
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
    
    this = LabelFrame(tWindow,text="Transportation Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Departure :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    dTime = Entry(this,width=50)
    dTime.place(x=135, y=22)
    Label(this,text="Arrival :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    aTime = Entry(this,width=50)
    aTime.place(x=135, y=62)
    Label(this,text="Company Name :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    name = Entry(this,width=50)
    name.place(x=135, y=102)
    Label(this,text="Mode of Transportation :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    tDrop = ttk.Combobox(this,state='readonly',width=39)
    tDrop['values'] = ["Plane","Boat","Car"]
    tDrop.place(x=180, y=142)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=170)
    cancel = Button(holder,text="Close",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=24,command=tWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=24,command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        dTime.insert(END,transpo[1])
        aTime.insert(END,transpo[2])
        name.insert(END,transpo[3])
        for y in tDetailsList:
            if y[1]==transpo[0]:
                mode = y[2]
        tDrop.set(mode)
   
header = Frame(main, height=110, width=1355, bg="white",borderwidth=3,highlightbackground="#cee2e8", highlightthickness=1)
header.propagate(0)
header.pack(side=TOP)
Label(header, image=PhotoTravelPlanner, bd=0).pack()

buttons = Frame(main,bg="#cee2e8")
buttons.pack(side=LEFT,fill='y',expand='true')
menuFrame = Label(buttons,image=PhotoMenu,bd=0,highlightbackground="white", highlightthickness=0)
menuFrame.pack(side=TOP,padx=1)
tripButton = Button(buttons,image=PhotoTrips,command=lambda:search("Main",''))
tripButton.pack(side=TOP,padx=1)
iteButton = Button(buttons, image=PhotoItinerary, command=lambda:search("Trip",''))
iteButton.pack(side=TOP,padx=1)
eventButton = Button(buttons, image=PhotoEvents, command=lambda:search("Itinerary",''))
eventButton.pack(side=TOP,padx=1)
cal = Calendar(buttons, selectmode='day', year=2021, month=7, font=("Century Gothic",7),background = "#2f869e" , disabledbackground = "orange" , borderbackground = "red" , headersbackground = "#9cc4ce" , normalbackground = "white" )
cal.place(x=8,y=350)#pack(side=TOP,padx=1)

display = Frame(main, height=800, width=1200)
display.pack(side=RIGHT)
display.propagate(0)
head = Frame(display, height=80, width=1200, bg="#cee2e8",highlightbackground="#238099", highlightthickness=1)
head.propagate(0)
head.pack(side=TOP)

wrapper = LabelFrame(display)
wrapper.pack(side=TOP)
mycanvas = Canvas(wrapper, width=1200,height=560)
listFrame= Frame(mycanvas)
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=listFrame, anchor="nw")


search("Main",'')
=======
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
from tkcalendar import DateEntry, Calendar

main = Tk()
main.geometry("1355x710")
main.resizable(0,0)
positionRight = int((main.winfo_screenwidth()/2 - 686))
positionDown = int((main.winfo_screenheight()/2 - 389))
main.geometry("+{}+{}".format(positionRight, positionDown))

#Connects and makes a cursor to the database
dbase = sqlite3.connect('planner_data.db')
cursor = dbase.cursor()
dbase.execute("PRAGMA foreign_keys = ON;")

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

#Declares image to be used
PhotoMenu = PhotoImage(file="menubar.png")
PhotoTrips = PhotoImage(file="trips2.png")
PhotoItinerary = PhotoImage(file="itinerary2.png")
PhotoEvents = PhotoImage(file="events2.png")
PhotoTravelPlanner = PhotoImage(file="travel.png")
ButtonEdit = PhotoImage(file="edit.png")
ButtonDelete = PhotoImage(file="delete.png")
ButtonEdit1 = PhotoImage(file="edit1.png")
ButtonDe1ete1 = PhotoImage(file="delete1.png")
ButtonDelete2 = PhotoImage(file="delete2.png")
ButtonEdit2 = PhotoImage(file="edit2.png")
ButtonTranspo = PhotoImage(file="transpo.png")
ButtonHotel = PhotoImage(file="hotel.png")


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

def search(title):
    for frame in head.winfo_children():
        frame.destroy()
    LabelHead = Label(head, text="TRIPS",font = ('Bookman Old Style', 20,'bold'), anchor=W, bg="#cee2e8",fg="#238099")
    LabelHead.pack(side=TOP,padx=5,pady=5)
    Label(head, text="SEARCH:",font = ('Bookman Old Style', 12,'bold'), anchor=W, bg="#cee2e8").pack(side=LEFT,padx=5,pady=5)
    global thisEntry
    thisEntry = StringVar()
    global searchBar
    searchBar = Entry(head,text=thisEntry,width=200)
    searchBar.pack(side=LEFT,padx=5,pady=5)
    global addButton
    addButton = Button(head,text="Add Trip",font = ('Bookman Old Style', 12,'bold'),fg="#31859C", bg="white",width=15,command=lambda:tripDetails("add",[]))
    addButton.pack(side=LEFT,padx=5,pady=5) 
    if title=="Main":
        thisEntry.trace('w',showTrips)
        showTrips()
        return
    searchBar.config(width=97)
    Label(head,text=title+" :",font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8").pack(side=LEFT,padx=5,pady=5)
    global cBox
    cBox = ttk.Combobox(head,state='readonly',width=30)
    cBox.pack(side=LEFT,padx=10,pady=5)
    if title=="Trip":
        LabelHead.config(text="ITINERARY")
        cBox['values']=[x[1] for x in tripList]
        cBox.set(tripList[0][1])
        cBox.config(width=27,font = ('Bookman Old Style', 10))
        cBox.bind('<<ComboboxSelected>>',showItinerary)
        thisEntry.trace('w',showItinerary)
        showItinerary()
    elif title=="Itinerary":
        cBox['values']=[x[2] for x in itiList]
        cBox.set(itiList[0][2])
        cBox.config(width=27,font = ('Bookman Old Style', 10))
        cBox.bind('<<ComboboxSelected>>',showEvents)
        thisEntry.trace('w',showEvents)
        showEvents()
        LabelHead.config(text="EVENTS")
    
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
    
    tWindow = Toplevel(bg="white")
    tWindow.geometry("450x258")
    tWindow.resizable(0,0)
    tWindow.geometry("+{}+{}".format(positionRight+450, positionDown+230))
    
    this = LabelFrame(tWindow,text="Trip Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Trip Name :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    name = Entry(this,width=50)
    name.place(x=115, y=22)
    Label(this,text="Destination :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    desti = Entry(this,width=50)
    desti.place(x=115, y=62)
    Label(this,text="Start Date :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    sDate = DateEntry(this,width=47,background="gray", foreground="snow")
    sDate.place(x=115, y=102)
    Label(this,text="End Date :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    eDate = DateEntry(this,width=47,background="gray", foreground="snow")
    eDate.place(x=115, y=142)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=170)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),height=1,width=23,bg="#264348", fg="white",command=tWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),height=1,width=23,bg="#5f9ea0", fg="white",command=command)
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
    searchBar.config(width=140)
    addButton.config(text="Add Trip",command=lambda:tripDetails("add",[]))
    searchword = thisEntry.get()
    #Loops thru the main list of trips and displays them
    row, column = 0, 0
    for trip in tripList:
        if trip[1].lower().startswith(searchword.lower()):
            tripFrame = Frame(listFrame, highlightbackground="#31849b", highlightthickness=1, height=175, width=265,bg="white")
            tripFrame.propagate(0)
            tripFrame.grid(row=row, column=column, padx=(10,0), pady=(10,0))
            Label(tripFrame, text=trip[1],font = ('Tahoma', 26,'bold'),bg="white",fg="#31849b").pack(side=TOP,fill='x',padx=5,pady=(10,2))
            Label(tripFrame, text=trip[2],font = ('Calisto MT', 12),bg="white",fg="#2f869e").pack(side=TOP,fill='x',padx=5,pady=2)
            Label(tripFrame, text=trip[3]+" - "+trip[4],font = ('Calisto MT', 12),bg="white",fg="#2f869e").pack(side=TOP,fill='x',padx=5,pady=2)
            holder = Frame(tripFrame,bg='white')
            holder.pack(side=TOP)
            edit = Button(holder,image =ButtonEdit1, bd =0, bg = "white", command=lambda x=trip:tripDetails("edit",x))
            edit.pack(side=LEFT,pady=5,padx=5)
            delete = Button(holder,image =ButtonDe1ete1, bd =0, bg = "white",command=lambda x=trip:deleteTrip(x))
            delete.pack(side=RIGHT,pady=5,padx=5)
            column += 1
            if column == 4:
                column = 0
                row += 1
    #Frame for fixing not working scrollbar        
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0,columnspan=3)     

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
    iWindow = Toplevel(bg="white")
    iWindow.geometry("465x225")
    iWindow.resizable(0,0)
    iWindow.geometry("+{}+{}".format(positionRight+440, positionDown+250))

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
        
    this = LabelFrame(iWindow,text="Itinerary Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Date :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    date = DateEntry(this,width=47,background="gray", foreground="snow")
    date.place(x=135, y=22)
    Label(this,text="Location :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    location = Entry(this,width=50)
    location.place(x=135, y=62)
    Label(this,text="Main Attraction :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    details = Entry(this,width=50)
    details.place(x=135, y=102)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=20, y=130)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=23,command=iWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=23,command=command)
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
    #Filters the list to the group of itineraries belonging to the chosen trip
    for x in tripList:
        if x[1] == cBox.get():
            strain=x[0]
    addButton.config(text="Add Itinerary",command=lambda:itineDetails("add",[],strain))
    searchword = thisEntry.get()
    filtered = [x for x in itiList if x[4]==strain]
    #Loops thru the filtered list of itineraries and displays them    
    row = 0
    
    for itine in filtered:
        if itine[3].lower().startswith(searchword.lower()):
            itiFrame = Frame(listFrame)
            itiFrame.grid(row=row, column=0)
            holder1 = Frame(itiFrame,height=100,width=120, highlightbackground="#31849b",highlightthickness=1,bg="white")
            holder1.pack(side=LEFT,pady=(10,0),padx=5)
            holder1.propagate(0)
            holder2 = Frame(itiFrame,height=100,width=965, highlightbackground="#31849b",highlightthickness=1,bg="white")
            holder2.pack(side=RIGHT,pady=(10,0),padx=5)
            holder2.propagate(0)
            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            month = months[int(itine[1].split('/')[0])-1]
            Label(holder1, text=month,font = ('Tahoma', 24,'bold'),bg="white",fg="#31849b").place(relx=.5, rely=.3, anchor='c')
            Label(holder1, text=itine[1].split('/')[1],font = ('Tahoma', 18),bg="white",fg="#31849b").place(relx=.5, rely=.75, anchor='c')
            temp=Frame(holder2,bg='white')
            temp.pack(side=LEFT)
            Label(temp, text=itine[3],font = ('Tahoma', 24,'bold'),bg="white",fg="#31849b",anchor='w').grid(row=0,column=0,padx=15,sticky='w')
            Label(temp, text=itine[2],font = ('Tahoma', 18),bg="white",fg="#2f869e",anchor='w').grid(row=1,column=0,padx=15,sticky='w')
            delete = Button(holder2,image = ButtonDelete, bd=0, bg="white",command=lambda x=itine:deleteItine(x))
            delete.pack(side=RIGHT,padx=(5,10),pady=5)
            edit = Button(holder2,image = ButtonEdit, bd=0, bg="white",command=lambda x=itine:itineDetails("edit",x,strain))
            edit.pack(side=RIGHT,padx=5,pady=5)
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
    eWindow = Toplevel(bg="white")
    eWindow.geometry("450x265")
    eWindow.resizable(0,0)
    eWindow.geometry("+{}+{}".format(positionRight+450, positionDown+220))

    def command():
        if comm=="add":
            cursor.execute("INSERT INTO Events(EventName,Location,PlannedTime,Details,ItineraryNumber)VALUES(?,?,?,?,?)",
                           (name.get(),locate.get(),pTime.get(),detail.get(),nItine))
            dbase.commit()
            eWindow.destroy()
            updateList()
            #hotelDetails("add",[],eventList[-1][0])
            #transpoDetails("add",[],eventList[-1][0])
        else:
            cursor.execute("UPDATE Events SET EventName=?,Location=?,PlannedTime=?,Details=? WHERE EventNumber=?",
                           (name.get(),locate.get(),pTime.get(),detail.get(),event[0]))
            dbase.commit()
            eWindow.destroy()
            showEvents()
        
    this = LabelFrame(eWindow,text="Event Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Event Name :",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    name = Entry(this,width=50)
    name.place(x=115, y=22)
    Label(this,text="Location :",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    locate = Entry(this,width=50)
    locate.place(x=115, y=62)
    Label(this,text="Planned Time:",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    pTime = Entry(this,width=50)
    pTime.place(x=115, y=102)
    Label(this,text="Details:",anchor='w',font = ('Bookman Old Style', 10,'bold'),bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    detail = Entry(this,width=50)
    detail.place(x=115, y=140)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=170)
    cancel = Button(holder,text="Cancel",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=23,command=eWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=23,command=command)
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
    #Filters the list to the group of itineraries belonging to the chosen trip
    for x in itiList:
        if x[2] == cBox.get():
            strain=x[0]
    addButton.config(text="Add Event",command=lambda:eventDetails("add",[],strain))
    searchword = thisEntry.get()
    #Filters the master list of events to events under the chosen itinerary
    filtered = [x for x in eventList if x[5]==strain]
    #Loops thru the filtered itineraries and displays them
    row, column, count = 0, 0, 1
    for event in filtered:
        if event[1].lower().startswith(searchword.lower()):
            eveFrame = Frame(listFrame, highlightbackground="#31849b", highlightthickness=1, height=175, width=265,bg="white")
            eveFrame.propagate(0)
            eveFrame.grid(row=row, column=column, padx=(10,0), pady=(10,0))
            Label(eveFrame, text=event[1],font = ('Tahoma', 20,'bold'),bg="white",fg="#31849b").pack(side=TOP,fill='x',padx=5,pady=(15,2))
            Label(eveFrame, text=event[2],font = ('Calisto MT', 10),bg="white",fg="#2f869e").pack(side=TOP,fill='x',padx=5,pady=2)
            holder1 = Frame(eveFrame,bg='white')
            holder1.pack(side=TOP)
            hotel = Button(holder1,image = ButtonHotel, bg="white", bd=0,command=lambda x=event[0]:hotelDetails(x))
            hotel.pack(side=LEFT,pady=(5,0),padx=5)
            transpo = Button(holder1,image =ButtonTranspo, bg="white", bd=0,command=lambda x=event[0]:transpoDetails(x))
            transpo.pack(side=LEFT,pady=(5,0),padx=5)
            #holder2 = Frame(eveFrame,bg='white')
            #holder2.pack(side=TOP)
            edit = Button(holder1,image = ButtonEdit2, bg="white", bd=0,command=lambda x=event:eventDetails("edit",x,strain))
            edit.pack(side=LEFT,pady=(5,0),padx=5)
            delete = Button(holder1,image = ButtonDelete2, bg="white", bd=0,command=lambda x=event:deleteEvent(x))
            delete.pack(side=RIGHT,pady=(5,0),padx=5)
            Label(eveFrame,text=count,font= ('Tahoma', 16,'bold'),bg="white",fg="#31849b").place(relx=0.025,rely=0.005)
            column += 1
            count += 1
            if column == 4:
                column = 0
                row += 1

    #Frame for fixing not working scrollbar
    fixFrame = Frame(listFrame,width=10,height=800)
    fixFrame.propagate(0)
    fixFrame.grid(row=row+1, column=0)

#Function for adding or editing the details of a hotel            
def hotelDetails(nEvent):
    hWindow = Toplevel(bg="white")
    hWindow.geometry("473x340")
    hWindow.resizable(0,0)
    hWindow.geometry("+{}+{}".format(positionRight+440, positionDown+180))

    comm = "add"
    
    for x in bookList:
        if x[4]==nEvent:
            hotel = x
            comm = "edit"
    
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
    
    this = LabelFrame(hWindow,text="Hotel Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Hotel Name :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    name = Entry(this,width=50)
    name.place(x=135, y=22)
    Label(this,text="Contact Number :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    number = Entry(this,width=50)
    number.place(x=135, y=62)
    Label(this,text="Address :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    address = Entry(this,width=50)
    address.place(x=135, y=102)
    Label(this,text="Check-In Time :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    iTime = Entry(this,width=50)
    iTime.place(x=135, y=142)
    Label(this,text="Check-Out Time :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=180)
    oTime = Entry(this,width=50)
    oTime.place(x=135, y=182)
    Label(this,text="Room Type :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=220)
    rType = Entry(this,width=50)
    rType.place(x=135, y=222)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=250)
    cancel = Button(holder,text="Close",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=24,command=hWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=24,command=command)
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

def transpoDetails(nEvent):
    tWindow = Toplevel(bg="white")
    tWindow.geometry("470x260")
    tWindow.resizable(0,0)
    tWindow.geometry("+{}+{}".format(positionRight+430, positionDown+200))

    comm = "add"
    
    for x in transpoList:
        if x[4]==nEvent:
            transpo = x
            comm = "edit"
    
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
    
    this = LabelFrame(tWindow,text="Transportation Details",font = ('Bookman Old Style', 20,'bold'),labelanchor='n',bg="#cee2e8",fg="#31849b")
    this.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(this,text="Departure :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=20)
    dTime = Entry(this,width=50)
    dTime.place(x=135, y=22)
    Label(this,text="Arrival :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=60)
    aTime = Entry(this,width=50)
    aTime.place(x=135, y=62)
    Label(this,text="Company Name :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=100)
    name = Entry(this,width=50)
    name.place(x=135, y=102)
    Label(this,text="Mode of Transportation :",font = ('Bookman Old Style', 10,'bold'),anchor='w',bg="#cee2e8",fg="#31849b").place(x=10, y=140)
    tDrop = ttk.Combobox(this,state='readonly',width=39)
    tDrop['values'] = ["Plane","Boat","Car"]
    tDrop.place(x=180, y=142)
    holder = Frame(this,bg="#cee2e8")
    holder.place(x=15, y=170)
    cancel = Button(holder,text="Close",font = ('Bookman Old Style', 10),bg="#264348", fg="white",height=1,width=24,command=tWindow.destroy)
    cancel.pack(side=LEFT,pady=5,padx=2)
    save = Button(holder,text="Save",font = ('Bookman Old Style', 10),bg="#5f9ea0", fg="white",height=1,width=24,command=command)
    save.pack(side=RIGHT,pady=5,padx=(5,0))

    if comm == "edit":
        dTime.insert(END,transpo[1])
        aTime.insert(END,transpo[2])
        name.insert(END,transpo[3])
        for y in tDetailsList:
            if y[1]==transpo[0]:
                mode = y[2]
        tDrop.set(mode)
   
header = Frame(main, height=110, width=1355, bg="white",borderwidth=3,highlightbackground="#cee2e8", highlightthickness=1)
header.propagate(0)
header.pack(side=TOP)
Label(header, image=PhotoTravelPlanner, bd=0).pack()

buttons = Frame(main,bg="#cee2e8")
buttons.pack(side=LEFT,fill='y',expand='true')
menuFrame = Label(buttons,image=PhotoMenu,bd=0,highlightbackground="white", highlightthickness=0)
menuFrame.pack(side=TOP,padx=1)
tripButton = Button(buttons,image=PhotoTrips,command=lambda:search("Main"))
tripButton.pack(side=TOP,padx=1)
iteButton = Button(buttons, image=PhotoItinerary, command=lambda:search("Trip"))
iteButton.pack(side=TOP,padx=1)
eventButton = Button(buttons, image=PhotoEvents, command=lambda:search("Itinerary"))
eventButton.pack(side=TOP,padx=1)
cal = Calendar(buttons, selectmode='day', year=2021, month=7, font=("Century Gothic",7),background = "#2f869e" , disabledbackground = "orange" , borderbackground = "red" , headersbackground = "#9cc4ce" , normalbackground = "white" )
cal.place(x=8,y=350)#pack(side=TOP,padx=1)

display = Frame(main, height=800, width=1200)
display.pack(side=RIGHT)
display.propagate(0)
head = Frame(display, height=80, width=1200, bg="#cee2e8",highlightbackground="#238099", highlightthickness=1)
head.propagate(0)
head.pack(side=TOP)

wrapper = LabelFrame(display)
wrapper.pack(side=TOP)
mycanvas = Canvas(wrapper, width=1200,height=560)
listFrame= Frame(mycanvas)
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=listFrame, anchor="nw")


search("Main")
>>>>>>> fecbdde7310fdac51ded7ac9d1e4bff0389331de
