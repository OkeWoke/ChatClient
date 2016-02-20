from socket import *
from threading import *
from tkinter import *

import time,sys, json, tkinter.font, tkHyperlinkManager, webbrowser 
class chatGUI:
    def __init__(self, window):
        self.bgColour = "#2a2a2a" #First COlour was: "#607D8B"
        #Initializing window settings
        self.window = window
        window.title("Oke's Chat Client")
        window.minsize(500,500)
        window.resizable(width=FALSE, height=FALSE)
        window.configure(bg=self.bgColour)
        self.chat = Frame(window)
        self.menu = Frame(window,bg=self.bgColour)
        
        #Load the first Menu
        self.menuFrame()
        self.menu.place(y=0,x=0,height=500,width=500)


    def switchToChat(self): #handles closing menu and switching to chat and calls connect function
        self.alias = self.aliasEntry.get() #Grabs alias entered at menu
        if self.alias.isspace() == False and self.alias != "" and len(self.alias) < 16:  
            try:
                #print("done")
                loadNet.connect(self.alias)
   
                self.menu.place_forget() #Remove menu
                self.chatFrame()
                self.chat.pack()
                
                window.resizable(width=TRUE, height=TRUE)
                window.minsize(500,410)
            except:
                print("Unable to connect to server")
                self.chat.pack_forget()
                self.menu.place(y=0,x=0,height=500,width=500)
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
        sv= StringVar() #stringVar to hold string from Entry Widget
        sv.trace("w", lambda name, index, mode, sv=sv: self.callBack(sv)) #idk what this really does but it calls callBack whenever sv is changed
        self.scrollBar = Scrollbar(self.chat)
        self.scrollBar.pack(side=RIGHT,fill=Y)
        self.mainText = Text(self.chat, wrap=WORD,bg="#2a2a2a") #Steam colour is "
        self.scrollBar.config(command=self.mainText.yview)
        self.mainText.pack(fill=BOTH,expand=YES)
        self.mainText.config(state=DISABLED,yscrollcommand=self.scrollBar.set)
        self.textEntry = Entry(self.chat,textvariable=sv,bg ="#2a2a2a",fg="white")
        self.hyperlink = tkHyperlinkManager.HyperlinkManager(self.mainText)
                
        Button(self.chat, text="Send",command= lambda: loadNet.speak(self.alias, self.textEntry),bg="#2a2a2a",fg="white").pack(side=RIGHT)
        self.textEntry.pack(fill=X,ipady=4)
        self.chat.pack(fill=BOTH, expand=YES) 
        window.bind("<Return>", lambda event: loadNet.speak(self.alias, self.textEntry))
                       
    def callBack(self,sv): #checks the text entry, sets it to first 1024 characters, called when ever text is entered.
        c = sv.get()[0:1000]
        sv.set(c)
        
    def openHyperLink(self, url):
        webbrowser.open(url)

    def displayData(self,data):
        #Fonts and text config
        self.mainText.config(state=NORMAL)
        bold_font = tkinter.font.Font(family="Helvetica",size=10,weight="bold")
        norm_font = tkinter.font.Font()
        self.mainText.tag_configure("bold", font=bold_font, foreground="#7dbcc1")
        self.mainText.tag_configure("normal", font=norm_font, foreground ="white")
        #Actual data display
        self.mainText.insert(END, time.strftime('%H:%M', time.localtime()) + " - "+str(data[0]), 'bold')
        msgSplit = data[1].split()
        print(msgSplit)
        for msgDat in msgSplit:
            if "http://" in msgDat or "www." in msgDat or "https://" in msgDat or "ftp://" in msgDat:
                self.mainText.insert(END, str(msgDat), self.hyperlink.add(lambda:self.openHyperLink(msgDat)))
                self.mainText.insert(END, " ")
            else:
                self.mainText.insert(END, str(msgDat)+" ", "normal")

        self.mainText.insert(END, "\n")        
        self.mainText.config(state=DISABLED)
        self.mainText.see("end")
        
class netMan:
    def __init__(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        
    def connect(self,alias):           
        self.s.connect(('192.168.1.97',22229))
        self.s.send(alias.encode('utf-8'))
        #My ip is 122.57.41.49
        listenThread = Thread(target=self.listen)
        listenThread.start()
  

    def listen(self):
        while True:
            data =  self.s.recv(1024)
            print(data)
            if not data:
                break
            try:
                dataDecode = json.loads(data.decode('utf-8'))
                loadGUI.displayData(dataDecode)
            except:
                print("json error or display error\n")
        self.s.close()

    def speak(self, alias, textEntry, event=None): 
        if textEntry.get() != "":
            msg = textEntry.get()
            packet= json.dumps([alias+": ",msg])
            textEntry.delete(0,END)
            try:
                self.s.send(packet.encode('utf-8'))
            except:
                print("unable to reach server...?\n")
window = Tk()
loadNet = netMan()
loadGUI = chatGUI(window)


window.mainloop()
