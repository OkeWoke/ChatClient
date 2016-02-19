from socket import *
from threading import *
from tkinter import *

import time,sys, json, tkinter.font, tkHyperlinkManager, webbrowser 
class chatGUI:
    def __init__(self, window):
        global chat
        #Initializing window settings
        self.window = window
        window.title("Oke's Chat Client")
        window.minsize(500,410)
        chat = Frame(window)
        self.chat = chat
        self.menu = Frame(window)
        
        #Load the first Menu
        Label(self.menu,text="Enter your username below and connect!").pack()
        self.aliasEntry = Entry(self.menu)
        self.aliasEntry.pack()
        Button(self.menu,text="Connect",command=self.switchToChat).pack()
        self.menu.pack()


    def switchToChat(self): #handles closing menu and switching to chat and calls connect function
        self.alias = self.aliasEntry.get() #Grabs alias entered at menu
        if self.alias.isspace() == False and self.alias != "" and len(self.alias) < 16:
            self.menu.pack_forget() #Remove menu
            sv= StringVar() #stringVar to hold string from Entry Widget
            sv.trace("w", lambda name, index, mode, sv=sv: self.callBack(sv)) #idk what this really does but it calls callBack whenever sv is changed
            
            
            self.scrollBar = Scrollbar(self.chat)
            self.scrollBar.pack(side=RIGHT,fill=Y)
            self.mainText = Text(self.chat, wrap=WORD)
            self.scrollBar.config(command=self.mainText.yview)
            self.mainText.pack(fill=BOTH,expand=YES)
            self.mainText.config(state=DISABLED,yscrollcommand=self.scrollBar.set)
            self.textEntry = Entry(self.chat,textvariable=sv)
            self.hyperlink = tkHyperlinkManager .HyperlinkManager(self.mainText)
            
            Button(self.chat, text="Send",command= lambda: loadNet.speak(self.alias, self.textEntry)).pack(side=RIGHT)
            self.textEntry.pack(fill=X)
            self.chat.pack(fill=BOTH, expand=YES)
            
            window.bind("<Return>", lambda event: loadNet.speak(self.alias, self.textEntry))
            try:
                loadNet.connect(self.alias)
            except:
                print("Unable to connect to server")
                self.chat.pack_forget()
                self.menu.pack()
                Label(text="Unable to connect to server").pack()
        
    def callBack(self,sv): #checks the text entry, sets it to first 1024 characters, called when ever text is entered.
        c = sv.get()[0:1000]
        sv.set(c)
        
    def openHyperLink(self, url):
        webbrowser.open(url)

    def displayData(self,data):
        self.mainText.config(state=NORMAL)
        bold_font = tkinter.font.Font(family="Helvetica",size=10,weight="bold")
        self.mainText.tag_configure("bold", font=bold_font)
        self.mainText.insert(END, time.strftime('%H:%M', time.localtime()) + " - "+str(data[0]), 'bold')
        msgSplit = data[1].split()
        print(msgSplit)
        for msgDat in msgSplit:
            if "http://" in msgDat or "www." in msgDat or "https://" in msgDat or "ftp://" in msgDat:
                self.mainText.insert(END, str(msgDat), self.hyperlink.add(lambda:self.openHyperLink(msgDat)))
                self.mainText.insert(END, " ")
            else:
                self.mainText.insert(END, str(msgDat)+" ")

        self.mainText.insert(END, "\n")        
        self.mainText.config(state=DISABLED)
        self.mainText.see("end")
        
class netMan:
    def __init__(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        
    def connect(self,alias):           
        self.s.connect(('192.168.1.97',23013))
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
                print("json error or display error")
        self.s.close()

    def speak(self, alias, textEntry, event=None): 
        if textEntry.get() != "":
            msg = textEntry.get()
            packet= json.dumps([alias+": ",msg])
            textEntry.delete(0,END)
            try:
                self.s.send(packet.encode('utf-8'))
            except:
                print("unable to reach server...?")
window = Tk()
loadNet = netMan()
loadGUI = chatGUI(window)


window.mainloop()
