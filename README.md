# ChatClient aka not a steam chat clone
A chat client written in python, with Tkinter GUI. 
I think Skype and Steam is crap, so I'm gonna try make something with features I want with 100% less stability :D

This Chat Client requires communication to a dedicated server, which I am also making @ repo: OkeWoke/ChatServer
![ChatClientScreenShot](http://www.virtualquanta.com/Images/programming/chat.PNG) 
![ChatClientScreenShot](http://www.virtualquanta.com/Images/programming/chatMenu.PNG)
## How to use
Should work on python2 and Python3.

1. Currently there's no GUI to dictate port and IP of server, so open the chatClient.py file and look for 'self.s.connect(('192.168.1.97',55557))' Change the ip and port to what ever the server you want to connect to is hosting on.
2.  Execute chatClient.py
3.  Enter alias and click connect! You're free to chat!

##Features
- 2+ person communication.. duh
- Clickable Hyperlinks that launch webbrowser
- Dedicated server software, located @ OkeWoke/ChatServer
- Custom Alias Entry
- Options Menu -change 24 hr/12 hr or no time stamp, more options to come!
- Colours!!!

## Features to come
- Notifications when window not in focus
- User Bar
- okewoke is typing a message...
- Drag n drop images?
- Voice Chat
