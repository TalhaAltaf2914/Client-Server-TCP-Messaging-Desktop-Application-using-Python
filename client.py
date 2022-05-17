from tkinter import *
from socket import *
import _thread
import nmap

# from server import checkPortNum

def checkServerAlive(port,s):
            return s.connect_ex(('localhost', port)) == 0
    

# initialize server connection
def initialize_client(userIP, userPortNum):
    global ip, s, serverAliveMsg, successfulConnectionMsg
    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    #host = 'localhost'  ## to use between devices in the same network eg.192.168.1.5
    ip = userIP
    port = userPortNum
    if(checkServerAlive(port, s) == False):#check if true is returned or not
        serverAliveErrorMsg.grid(row = 8, column= 0)
        serverAliveErrorMsg.place(x=80, y = 36) 
        serverAliveErrorMsg.after(2500, serverAliveErrorMsg.destroy)
        return     
    else:
         #successful connection Msg:
        successfulConnectionMsg.grid(row = 8, column= 0)
        successfulConnectionMsg.place(x=120, y = 56) 
        successfulConnectionMsg.after(2500, successfulConnectionMsg.destroy)
    
    
     # connect to server
    s.connect((userIP, port))
    
   
    print("Junya")
    return s

def checkPortNum(portNum):
    if(portNum == ''):
        return "empty"
    
    portNum = int(portNum)
    if(portNum > 65536):
        portNum="incorrectPortNum"
    
    return portNum

def checkIP(userIP):
    if(userIP == ''):
        return "empty"

def connect():
    global emptyIPErrorMsgLabel, emptyIPPortErrorMsgLabel, successfulConnectionMsg
    userIP = ''
    emptyIPPortErrorMsgLabel.after(5000, emptyIPPortErrorMsgLabel.destroy)
    errorMsgLabel.after(5000, errorMsgLabel.destroy)
    emptyErrorMsgLabel.after(5000, emptyErrorMsgLabel.destroy)
    emptyIPErrorMsgLabel.after(5000, emptyIPErrorMsgLabel.destroy)

    user_IP_port = entry.get()
    if(user_IP_port == ''):
        emptyIPPortErrorMsgLabel.grid(row = 8, column= 0)
        emptyIPPortErrorMsgLabel.place(x=80, y = 36)
        return
    user_IP = user_IP_port.split(':')[0]
    user_Port = user_IP_port.split(':')[1]
    user_Port = int(user_Port)
    print(user_IP)
    print( user_Port)
    
    ip_check = checkIP(user_IP)
    portNum = checkPortNum(user_Port)    

   
    
    if(portNum == "empty"):
        emptyErrorMsgLabel.grid(row = 8, column= 0)
        emptyErrorMsgLabel.place(x=80, y = 36)
        return
    
    if(portNum == "incorrectPortNum"):
        portNum = 1234;#will assign default port no.
        entry.delete("0", END)
        entry.insert(0, "127.0.0.1:1234")
        #chatlog.delete("0", END)
        print(portNum)
        errorMsgLabel.grid(row = 8, column= 0)
        errorMsgLabel.place(x=80, y = 56)

    if(ip_check == "empty"):
        emptyIPErrorMsgLabel.grid(row = 8, column= 0)
        emptyIPErrorMsgLabel.place(x=80, y = 36)

    initialize_client(user_IP, portNum) 
    

# update the chat log
def update_chat(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)
    # update the message in the window
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'SERVER: ' + msg)
    chatlog.config(state=DISABLED)
    # show the latest messages
    chatlog.yview(END)

# function to send message
def send():
    global textbox
    global s
    # get the message
    msg = textbox.get("0.0", END)
    # update the chatlog
    update_chat(msg, 0)
    # send the message
    s.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

# function to receive message
def receive():
    while 1:
        try:
            data = s.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass

def press(event):
    send()

# GUI function
def GUI():
    global chatlog
    global textbox
    global entry
    global errorMsgLabel
    global incorrectPortNum
    global conn
    global emptyPortNum
    global emptyErrorMsgLabel
    global emptyIPErrorMsgLabel, emptyIPPortErrorMsgLabel, serverAliveErrorMsg
    global successfulConnectionMsg

    incorrectPortNum = False #false
    emptyPortNum = False
    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Client Chat")
    # set size for the window
    gui.geometry("380x430")

    # text space to display messages
    chatlog = Text(gui, bg='white')
    chatlog.config(state=DISABLED)

    # buttons to send messages
    sendbutton = Button(gui, bg='#E3F6FF', fg='black', text='SEND', command=send)
    connectBtn = Button(gui, bg='#E3F6FF', fg= 'black', text='Connect', command=connect)

    portLabel = Label(gui, text="Enter IP and Port: ")
    errorMsgLabel = Label(gui, text="Incorrect Port Entered | Port Assigned: 1234")
    emptyErrorMsgLabel = Label(gui, text="No Port Entered. Try Again")
    emptyIPErrorMsgLabel = Label(gui, text="No IP Entered. Try Again")
    emptyIPPortErrorMsgLabel = Label(gui, text="Nothing Entered. Try Again")
    serverAliveErrorMsg = Label(gui, text="Server is not listening at port. Try Again")
    
    successfulConnectionMsg = Label(gui, text="Connection Established.")
    

    entry = Entry(gui)

    # textbox to type messages
    textbox = Text(gui, bg='white')

    # place the components in the window
    portLabel.grid(row=6, column=0)
    portLabel.place(x=1, y=4)
    entry.grid(row = 6, column=0)
    connectBtn.grid(row = 6, column= 0)
    entry.place(x=110, y=6, height=20, width=160)
    connectBtn.place(x=300, y= 3)
    
    chatlog_y = 30
    chatlog.place(x=6, y=chatlog_y, height=356, width=370)
    #if incorrect port entered:
    print(incorrectPortNum)
    if(incorrectPortNum == True):
        print("Inside incorrect portnum check: value =  " + incorrectPortNum)    
        errorMsgLabel.grid(row = 8, column= 0)
        errorMsgLabel.place(x=80, y = 36)
        chatlog_y = 100
        
    if(emptyPortNum):
        emptyErrorMsgLabel.grid(row = 8, column= 0)
        emptyErrorMsgLabel.place(x=80, y = 36)
        chatlog_y = 100

    
   
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind textbox to use ENTER Key
    textbox.bind("<KeyRelease-Return>", press)

    # create thread to capture messages continuously
    _thread.start_new_thread(receive, ())
    #_thread.start_new_thread(initialize_server(1234))

    # to keep the window in loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    #s = initialize_client()
    GUI()