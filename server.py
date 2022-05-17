from tkinter import *
from socket import *
import _thread
import threading

# initialize server connection
def initialize_server(portNum):
    global conn, addr, s, listenMsg
    # initialize socket
    conn =0
    addr = 0
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    host = 'localhost'  ## to use between devices in the same network eg.192.168.1.5
    port = portNum
    print("HEY IM IN INIT SERVER f{port}")

    # initialize server
    s.bind((host, port))
    # set no. of clients
    s.listen(5)
    
    listenMsg.grid(row = 8, column= 0)
    listenMsg.place(x=150, y = 35)
    
    #connection thread
    _thread.start_new_thread(handle, ())

    return conn

def handle():
    global conn,addr, successfulConnectionMsg, listenMsg
    
    while True:
        conn, addr = s.accept()
        
        #successful connection Msg:
        successfulConnectionMsg.grid(row = 8, column= 0)
        successfulConnectionMsg.place(x=120, y = 56)
        #delete listening msg
        listenMsg.after(1000, listenMsg.destroy)
    
        successfulConnectionMsg.after(2500, successfulConnectionMsg.destroy)
    
        
# update the chat log
def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    # update the message in the window
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'CLIENT: ' + msg)
    chatlog.config(state=DISABLED)
    # show the latest messages
    chatlog.yview(END)

def checkPortNum(portNum):
    if(portNum == ''):
        return "empty"
    
    portNum = int(portNum)
    if(portNum > 65536):
        portNum="incorrectPortNum"
    
    return portNum


def listen():
    global entry
    global errorMsgLabel
    global emptyErrorMsgLabel
    global conn
    global chatlog
    global emptyError
    global incorrectPortNum
    global emptyPortNum
    global successfulConnectionMsg
    
    emptyErrorMsgLabel.after(5000, emptyErrorMsgLabel.destroy)
    errorMsgLabel.after(5000, errorMsgLabel.destroy)
    userPortNum = entry.get()
    portNum = checkPortNum(userPortNum)


    if(portNum == "empty"):
        emptyErrorMsgLabel.grid(row = 8, column= 0)
        emptyErrorMsgLabel.place(x=80, y = 36)
        return
    
    if(portNum == "incorrectPortNum"):
        print(portNum)
        errorMsgLabel.grid(row = 8, column= 0)
        errorMsgLabel.place(x=70, y = 56)
        return
    
    print("BEFORE conn")
    print(type(portNum))
    #_thread.start_new_thread(initialize_server(portNum))
    #initialize_server(portNum)
    thread = threading.Thread(target = initialize_server(portNum))
    thread.start()
    
    print("AFter conn")

# function to send message
def send():
    
    global textbox
    global conn
    # get the message
    msg = textbox.get("0.0", END)
    # update the chatlog
    update_chat(msg, 0)
    # send the message
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

# function to receive message
def receive():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass

def msgPress(event):
    send()

def listenPress(event):
    listen()

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
    global successfulConnectionMsg, listenMsg
    incorrectPortNum = False #false
    emptyPortNum = False
    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Server Chat")
    # set size for the window
    gui.geometry("380x430")

    # text space to display messages
    chatlog = Text(gui, bg='white')
    chatlog.config(state=DISABLED)

    # buttons to send messages
    sendbutton = Button(gui, bg='#E3F6FF', fg='black', text='SEND', command=send)
    listenBtn = Button(gui, bg='#E3F6FF', fg= 'black', text='Start Listening', command=listen)

    portLabel = Label(gui, text="Port Number: ")
    errorMsgLabel = Label(gui, text="Incorrect Port Entered. Port no. must be < 65355")
    emptyErrorMsgLabel = Label(gui, text="No Port Entered. Try Again")
    successfulConnectionMsg = Label(gui, text="Connection Established.")
    listenMsg = Label(gui, text="Listening.")
    
    entry = Entry(gui)

    # textbox to type messages
    textbox = Text(gui, bg='white')

    # place the components in the window
    portLabel.grid(row=6, column=0)
    portLabel.place(x=1, y=4)
    entry.grid(row = 6, column=0)
    listenBtn.grid(row = 6, column= 0)
    entry.place(x=80, y=6, height=20, width=160)
    listenBtn.place(x=280, y= 3)
    
    chatlog_y = 30
    chatlog.place(x=6, y=chatlog_y, height=356, width=370)

    
   
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind textbox to use ENTER Key
    textbox.bind("<KeyRelease-Return>", msgPress)
    listenBtn.bind("<KeyRelease-Return>", listenPress)
    # create thread to capture messages continuously
    _thread.start_new_thread(receive, ())
    

    # to keep the window in loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    #conn = initialize_server(1234)
    GUI()