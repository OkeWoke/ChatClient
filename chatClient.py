try: #if python3
    import tkinter as tk
    import  tkinter.font as tkFont
except: #if python2
    import Tkinter as tk
    import tkFont

import time, sys, json, tkHyperlinkManager, webbrowser, threading, socket

class chatGUI:
    """Handles the GUI of the chat client."""

    #CONSTANTS
    HYPER_LIST_TRIGGERS = ["http://","www.","https://","ftp://"]#Used for detection of hyperlinks in msg data
    
    BG_COLOUR = "#2a2a2a" #First Colour was: "#607D8B"
    TEXT_COLOUR = "white"
    BOLD_COLOUR = "#7dbcc1"
    
    WINDOW_TITLE = "Oke's Chat Client"
    WINDOW_HEIGHT = 500
    WINDOW_WIDTH = 500
    OPTION_TITLE = "Options"

    #Various paths to images used.
    BG_IMAGE_PATH = "Images/bgImg.gif" #Background image on main menu, 500x500.
    MENU_IMG_PATH = "Images/menu_text.gif" #Label image on main menu
    BUTTON_IMAGE_PATH = "Images/buttonImg.gif" #Button image on main menu
    
    def __init__(self):
        """Creates the window, configures the window and calls functions that load in widgets for all frames/menus"""

        #Window Config
        window.title(self.WINDOW_TITLE)
        window.configure(bg=self.BG_COLOUR)
        window.resizable(width=False, height=False)
        window.minsize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        menuBar = tk.Menu(window,foreground=self.BG_COLOUR,activeforeground=self.BG_COLOUR)
        menuBar.add_command(label=self.OPTION_TITLE, command=self.optionMenu)
        window.config(menu=menuBar)
        
        self.chat = tk.Frame(window,bg=self.BG_COLOUR)
        self.menu = tk.Frame(window,bg=self.BG_COLOUR)

        #Load widgets and check settings
        self.menuFrame()#Loads the MENU GUI into memory.
        self.chatFrame()#Loads Chat GUI into memory.
        self.checkFile() #Check for options/settings configuration

        self.menu.place(y=0,x=0,height=self.WINDOW_HEIGHT,width=self.WINDOW_WIDTH)#Place the first menu
        
    def menuFrame(self):
        """Loads tk widgets for the main menu"""
        
        #Define Images
        bgImg = tk.PhotoImage(file=self.BG_IMAGE_PATH)
        labelImg = tk.PhotoImage(file=self.MENU_IMG_PATH)
        buttonImg = tk.PhotoImage(file=self.BUTTON_IMAGE_PATH)
        
        #Define Widgets
        bgLabel = tk.Label(self.menu,image=bgImg,bg=self.BG_COLOUR)
        textLabel = tk.Label(self.menu,image=labelImg,bg=self.BG_COLOUR)
        menuButton = tk.Button(self.menu,command=self.switchToChat,image=buttonImg,bg=self.BG_COLOUR,borderwidth=0)
        self.aliasEntry = tk.Entry(self.menu)
        self.Error = tk.Label(self.menu,text="Unable to connect to server\n")
        
        #Config
        bgLabel.image=bgImg
        menuButton.image = buttonImg
        textLabel.image = labelImg
        
        #Placement
        bgLabel.place(x=0,y=0)
        menuButton.place(y=235,x=200)
        self.aliasEntry.place(y=100,x=190)
        textLabel.place(y=75,x=100)

    def chatFrame(self):
        """Loads tk widgets and related objects for chat window"""
        
        #Set up fonts and StringVars
        bold_font = tkFont.Font(family="Helvetica",size=10,weight="bold")
        norm_font = tkFont.Font()
        sv= tk.StringVar() #stringVar to hold string from Entry Widget
        sv.trace("w", lambda name, index, mode, sv=sv: self.checkEntry(sv)) #Calls self.checkEntry when ever entryStr String Var is changed.
        
        #Define Widgets
        self.scrollBar = tk.Scrollbar(self.chat)
        self.mainText = tk.Text(self.chat, wrap=tk.WORD,bg=self.BG_COLOUR,state=tk.DISABLED,yscrollcommand=self.scrollBar.set)
        self.userBar = tk.Text(self.chat,width=20,bg=self.BG_COLOUR,fg=self.TEXT_COLOUR,state=tk.DISABLED)
        self.textEntry = tk.Entry(self.chat,textvariable=sv,bg =self.BG_COLOUR,fg=self.TEXT_COLOUR)#Note, textvar set to entryStr, text entered is stored in that var.
        tk.Button(self.chat, text="Send",command= lambda: loadNet.speak(self.alias, self.textEntry),bg=self.BG_COLOUR,fg=self.TEXT_COLOUR).grid(column=2,row=1,sticky=tk.NW)
 
        #Widget Config
        self.hyperlink = tkHyperlinkManager.HyperlinkManager(self.mainText)#Must be stated after self.mainText is stated.
        
        self.mainText.tag_configure("bold", font=bold_font, foreground=self.BOLD_COLOUR)
        self.mainText.tag_configure("normal", font=norm_font, foreground =self.TEXT_COLOUR)
        self.scrollBar.config(command=self.mainText.yview)
        self.userBar.tag_configure("bold", font=bold_font, foreground=self.BOLD_COLOUR)
        
        #Place
        self.scrollBar.grid(column=1,row=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.mainText.grid(column=0,row=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.userBar.grid(column=2, row=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.textEntry.grid(row=1,column=0,sticky=tk.N+tk.S+tk.E+tk.W,rowspan=2)
        
        #Grid Geometry Config to make only chat box resizable.
        self.chat.columnconfigure(0,weight=1)
        self.chat.columnconfigure(2,minsize=140)
        self.chat.rowconfigure(0,weight=1)  
        
    def optionMenu(self):
        """Load in all widgets on option Menu"""
        
        #Setup
        self.timeStamp = tk.IntVar()
        self.hourStamp = tk.IntVar()
        self.timeStamp.set(self.optionData["timeStamp"])
        self.hourStamp.set(self.optionData["timeSet"])
        self.optionWindow = tk.Toplevel(bg=self.BG_COLOUR)
        self.optionWindow.title(self.OPTION_TITLE)
        
        #Define Widgets and pack
        tk.Checkbutton(self.optionWindow, text="TimeStamp", variable=self.timeStamp).pack()
        tk.Checkbutton(self.optionWindow, text="Use 24 Hour timestamp", variable=self.hourStamp).pack()
        tk.Button(self.optionWindow,text="Apply", command=self.saveSettings).pack()

    def switchToChat(self):
        """Handles closing menu and switching to chat and calls connect function"""
        
        self.alias = self.aliasEntry.get().strip() #Grabs alias entered at menu, removes whitespace at start/finish
        
        if 0 < len(self.alias) < 16:#make sure name is under 16 chars
            try:#Try Connect to Server.        
                    loadNet.connect(self.alias)#Replace this line with pass if you wish to run without a server.
            except Exception as error:#Unpack chat, repack menu.
                    print("Unable to connect to server")
                    print(error.message)
                    self.chat.pack_forget()
                    self.menu.place(y=0,x=0,height=self.WINDOW_HEIGHT,width=self.WINDOW_WIDTH)
                    self.Error.pack()
            else:#Called only if try works, if it connects.
                window.bind("<Return>", lambda event: loadNet.speak(self.alias, self.textEntry))
                self.menu.place_forget() #Remove menu
                self.chat.pack(fill=tk.BOTH, expand=tk.YES)#put chat GUI in.
                window.resizable(width=tk.TRUE, height=tk.TRUE)
                window.minsize(500,410)
        else:
            print("Use non whitespace characters, and must be between 0 and 16 characters.")
                    
    def checkFile(self):
        """handles reading in the settings from txt file, if try fails it meants it's unreadable or doesn't exist and makes a new file."""
        
        try:
            with open("options.txt") as optionFile: 
                self.optionData = json.load(optionFile)
        except:
            print("Options Configuration File Missing. Or Unreadable. \n Creating new file...")
            with open("options.txt","w") as optionFile:
                self.optionData = {
                    "timeStamp": 1,
                    "timeSet": 1
                }
                json.dump(self.optionData,optionFile)
            optionFile.write(self.optionData,optionFile)

    def saveSettings(self):
        """Save setting vars to txt file. Called by Apply button push."""
        
        self.optionData["timeStamp"] = self.timeStamp.get()
        self.optionData["timeSet"] = self.hourStamp.get()
        with open("options.txt", "w") as optionFile:
            json.dump(self.optionData, optionFile)      
        
    def checkEntry(self, entryStr):
        """checks the text entry,sets the contents of Entry widget to max of 1000 chars, called when ever text is entered."""
        
        c = entryStr.get()[0:1000]
        entryStr.set(c)
        
    def displayData(self,data):
        """Handles displaying message data."""
        
        print(data)
        self.mainText.config(state=tk.NORMAL)
        
        if self.optionData["timeStamp"]:#if using timestamp
            if self.optionData["timeSet"]:
                time_format = '%H:%M'#24 hr
            else:
                time_format = '%I:%M'#12 hr
                
            self.mainText.insert(tk.END, time.strftime(time_format, time.localtime()) + " - "+str(data[0]), 'bold')
        else:#No timestamp
            self.mainText.insert(tk.END, str(data[0]), 'bold')#No TimeStamp
            
        msgSplit = data[1].split()#Split message up for analysis of hyperlinks
        
        for msgDat in msgSplit:#Check message for hyperlinks.
            for hyperID in self.HYPER_LIST_TRIGGERS:# check msg for hyperlinks
                if msgDat.startswith(hyperID):
                    self.mainText.insert(tk.END, str(msgDat), self.hyperlink.add(lambda:webbrowser.open(msgDat)))#Make the message a hyperlink that opens webbrowser
                    self.mainText.insert(tk.END, " ")
                    break
            else:
                self.mainText.insert(tk.END, str(msgDat)+" ", "normal")
                
        self.mainText.insert(tk.END, "\n")        
        self.mainText.config(state=tk.DISABLED)
        self.mainText.see("end") #Makes view of text box at bottom so you don't have to scroll down. Looking at you skype >:(

    def modUserBar(self,userList):
        """Called when someone connects/disconnects. Modifies the userbar which is a text widget."""
        
        self.userBar.config(state=tk.NORMAL)
        self.userBar.delete(1.0, tk.END)#Empty it out
        for user in userList:
            self.userBar.insert(tk.END, str(user)+"\n", 'bold')
        self.userBar.config(state=tk.DISABLED)
            
        
class netMan:
    """Handles network related part of program"""
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Make socket object
        
    def connect(self,alias):
        """connects the client to the specified server"""
        
        self.s.connect(('192.168.1.97',11117))
        self.s.send(alias.encode('utf-8'))#Send alias
        listenThread = threading.Thread(target=self.listen)#Define the listening thread, required because window.mainloop :(
        listenThread.start()#Start the thread!
  
    def listen(self):
        """Called from thread creation, runs continously."""
        
        while True:
            try:
                data =  self.s.recv(3000)
            except:
                print("Disconnected from server")
                break
            try:
                dataDecode = json.loads(data.decode('utf-8'))
            except:
                print("json decoding error\n")
            else:
                if dataDecode[0] == 1:
                    loadGUI.displayData(dataDecode[1:])
                elif dataDecode[0] == 0:
                    loadGUI.modUserBar(dataDecode[1])
        self.s.close()

    def speak(self, alias, textEntry, event=None):
        """Called when ever send button pushed or Enter is pressed"""
        
        msg = textEntry.get()
        
        if msg != "": #no whitespace!
            packet= json.dumps([1,alias+": ",msg],ensure_ascii=False)
            textEntry.delete(0,tk.END)
            try:
                self.s.send(packet.encode('utf-8'))
            except:
                print("unable to reach server...?\n")
                
window = tk.Tk()
loadNet = netMan()
loadGUI = chatGUI()

window.mainloop()
