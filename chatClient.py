try: #if python3
    from tkinter import *
    import  tkinter.font as tkFont
except: #if python2
    from Tkinter import *
    import tkFont
    
from socket import *
from threading import *
import time,sys, json,tkHyperlinkManager, webbrowser 

class chatGUI:
    def __init__(self, window):
        self.bgColour = "#2a2a2a" #First COlour was: "#607D8B"
        #Initializing window settings
        self.window = window
        window.title("Oke's Chat Client")
        window.minsize(500,500)
        window.resizable(width=FALSE, height=FALSE)
        window.configure(bg=self.bgColour)
        self.chat = Frame(window,bg=self.bgColour)
        self.menu = Frame(window,bg=self.bgColour)
        self.checkFile()
        
        menuBar = Menu(window,foreground=self.bgColour,activeforeground=self.bgColour)
        menuBar.add_command(label="Options", command=self.optionMenu)
        window.config(menu=menuBar)
        self.chatFrame()
        #Load the first Menu
        self.menuFrame()
        self.menu.place(y=0,x=0,height=500,width=500)

    def checkFile(self):
        try:
            optionFile = open("options.txt")
            self.optionData = json.loads(optionFile.read())
        except:
            print("Options Configuration File Missing.\n Creating new file...")
            optionFile = open("options.txt","w+")
            Dict = {
                "timeStamp": 1,
                "timeSet": 1
            }
            Dict = json.dumps(Dict)
            optionFile.write(Dict)
            optionFile.close()
            optionFile = open("options.txt")
            self.optionData = json.loads(optionFile.read())
        
        optionFile.close()

    def optionMenu(self):
        self.timeStamp = IntVar()
        self.hourStamp = IntVar()
        self.timeStamp.set(self.optionData["timeStamp"])
        self.hourStamp.set(self.optionData["timeSet"])
        self.optionWindow = Toplevel(bg=self.bgColour)
        self.optionWindow.title("ChatClient Options")
        Checkbutton(self.optionWindow, text="TimeStamp", variable=self.timeStamp).pack()
        Checkbutton(self.optionWindow, text="Use 24 Hour timestamp", variable=self.hourStamp).pack()
        Button(self.optionWindow,text="Apply", command=self.saveSettings).pack()

    def saveSettings(self):
        self.optionData["timeStamp"] = self.timeStamp.get()
        self.optionData["timeSet"] = self.hourStamp.get()
        optionFile = open("options.txt","w+")
        optionFile.truncate()
        optionFile.write(json.dumps(self.optionData))
        optionFile.close()        
        
    def switchToChat(self): #handles closing menu and switching to chat and calls connect function
        self.alias = self.aliasEntry.get() #Grabs alias entered at menu
        if self.alias.isspace() == False and self.alias != "" and len(self.alias) < 16:
            window.bind("<Return>", lambda event: loadNet.speak(self.alias, self.textEntry))
            try:
                    self.menu.place_forget() #Remove menu
                    self.chat.pack(fill=BOTH, expand=YES)
                    print("pack")
                    window.resizable(width=TRUE, height=TRUE)
                    window.minsize(500,410)
                    loadNet.connect(self.alias)
                    
            except:
                    print("Unable to connect to server")
                    self.chat.pack_forget()
                    self.menu.place(y=0,x=0,height=500,width=500)
                    window.resizable(width=FALSE, height=FALSE)
                    window.minsize(500,500)
                    self.Error.pack()

    def menuFrame(self):
        #BG IMAGE
        bgImg = PhotoImage(file="Images/bgImg.gif")
        bgLabel = Label(self.menu,image=bgImg,bg=self.bgColour)
        bgLabel.image=bgImg
        bgLabel.place(x=0,y=0)
        #Error
        self.Error = Label(self.menu,text="Unable to connect to server\n")
        #Label Msg
        labelImg = PhotoImage(file="Images/menu_text.gif")
        label = Label(self.menu,image=labelImg,bg=self.bgColour)
        label.image = labelImg
        label.place(y=75,x=100)
        #Entry Widget
        self.aliasEntry = Entry(self.menu)
        self.aliasEntry.place(y=100,x=190)
        #Connect Button
        buttonImg =PhotoImage(file="Images/buttonImg.gif")
        button = Button(self.menu,text="Connect",command=self.switchToChat,image=buttonImg,bg=self.bgColour,borderwidth=0)
        button.image = buttonImg
        button.place(y=235,x=200)
        
    def chatFrame(self):
        bold_font = tkFont.Font(family="Helvetica",size=10,weight="bold")
        norm_font = tkFont.Font()
        sv= StringVar() #stringVar to hold string from Entry Widget
        sv.trace("w", lambda name, index, mode, sv=sv: self.callBack(sv)) #idk what this really does but it calls callBack whenever sv is changed
        
        self.scrollBar = Scrollbar(self.chat)
        self.scrollBar.grid(column=1,row=0,sticky=N+S+E+W)
        self.mainText = Text(self.chat, wrap=WORD,bg=self.bgColour,state=DISABLED,yscrollcommand=self.scrollBar.set)
        self.mainText.grid(column=0,row=0,sticky=N+S+E+W)
        self.mainText.tag_configure("bold", font=bold_font, foreground="#7dbcc1")
        self.mainText.tag_configure("normal", font=norm_font, foreground ="white")
        self.scrollBar.config(command=self.mainText.yview)
        
        self.userBar = Text(self.chat,width=20,bg=self.bgColour,fg="white",state=DISABLED)
        self.userBar.grid(column=2, row=0,sticky=N+S+E+W)
        self.userBar.tag_configure("bold", font=bold_font, foreground="#7dbcc1")
        
        self.textEntry = Entry(self.chat,textvariable=sv,bg =self.bgColour,fg="white")
        self.textEntry.grid(row=1,column=0,sticky=N+S+E+W,rowspan=2)
        
        self.hyperlink = tkHyperlinkManager.HyperlinkManager(self.mainText)

        Button(self.chat, text="Send",command= lambda: loadNet.speak(self.alias, self.textEntry),bg=self.bgColour,fg="white").grid(column=2,row=1,sticky=NW)
        
        self.chat.columnconfigure(0,weight=1)
        self.chat.columnconfigure(2,minsize=140)
        self.chat.rowconfigure(0,weight=1)
        
        
    def callBack(self,sv): #checks the text entry, sets it to first 1024 characters, called when ever text is entered.
        c = sv.get()[0:1000]
        sv.set(c)
        
    def displayData(self,data):
        print(data)
        self.mainText.config(state=NORMAL)
        if self.optionData["timeStamp"]:
            if self.optionData["timeSet"]:
                self.mainText.insert(END, time.strftime('%H:%M', time.localtime()) + " - "+str(data[0]), 'bold')
            else:
                self.mainText.insert(END, time.strftime('%I:%M', time.localtime()) + " - "+str(data[0]), 'bold')
        else:
            self.mainText.insert(END, str(data[0]), 'bold')
        msgSplit = data[1].split()
        for msgDat in msgSplit:
            if "http://" in msgDat or "www." in msgDat or "https://" in msgDat or "ftp://" in msgDat:
                self.mainText.insert(END, str(msgDat), self.hyperlink.add(lambda:webbrowser.open(msgDat)))
                self.mainText.insert(END, " ")
            else:
                self.mainText.insert(END, str(msgDat)+" ", "normal")

        self.mainText.insert(END, "\n")        
        self.mainText.config(state=DISABLED)
        self.mainText.see("end")

    def modUserBar(self,userList):
        print("receive userBar Data")
        self.userBar.config(state=NORMAL)
        self.userBar.delete(1.0, END)
        for user in userList:
            self.userBar.insert(END, str(user)+"\n", 'bold')
        self.userBar.config(state=DISABLED)
            
        
class netMan:
    def __init__(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        
    def connect(self,alias):
        self.s.connect(('192.168.1.97',11111))#My ip is 122.57.41.49
        self.s.send(alias.encode('utf-8'))
        listenThread = Thread(target=self.listen)
        listenThread.start()
  
    def listen(self):
        while True:
            data =  self.s.recv(1024)
            if not data:
                break
            try:
                dataDecode = json.loads(data.decode('utf-8'))
                if dataDecode[0] == 1:
                    loadGUI.displayData(dataDecode[1:])
                elif dataDecode[0] == 0:
                    loadGUI.modUserBar(dataDecode[1])
            except:
                print("json error or display error\n")
        self.s.close()

    def speak(self, alias, textEntry, event=None): 
        if textEntry.get() != "":
            msg = textEntry.get()
            packet= json.dumps([1,alias+": ",msg])
            textEntry.delete(0,END)
            try:
                self.s.send(packet.encode('utf-8'))
            except:
                print("unable to reach server...?\n")
                
window = Tk()
loadNet = netMan()
loadGUI = chatGUI(window)

window.mainloop()
