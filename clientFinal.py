# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:59:42 2019

@author: othmans1
"""
import os
import socket
import base64
from tkinter import *
import tkinter.font
import PIL
from PIL import Image
from PIL import ImageGrab
from PIL import ImageTk

class PaintApp:
    
    # Stores current drawing tool used
    drawing_tool = "pencil"

    # Tracks whether left mouse is down
    left_but = "up"

    # x and y positions for drawing with pencil
    x_pos, y_pos = None, None

    # Tracks x & y when the mouse is clicked and released
    x1_line_pt, y1_line_pt, x2_line_pt, y2_line_pt = None, None, None, None

    # ---------- CATCH MOUSE UP ----------

    def left_but_down(self, event=None):
        self.left_but = "down"

        # Set x & y when mouse is clicked
        self.x1_line_pt = event.x
        self.y1_line_pt = event.y

    # ---------- CATCH MOUSE UP ----------

    def left_but_up(self, event=None):
        self.left_but = "up"

        # Reset the line
        self.x_pos = None
        self.y_pos = None

        # Set x & y when mouse is released
        self.x2_line_pt = event.x
        self.y2_line_pt = event.y

    # ---------- CATCH MOUSE MOVEMENT ----------

    def motion(self, event=None):

        if self.drawing_tool == "pencil":
            self.pencil_draw(event)

    # ---------- DRAW PENCIL ----------

    def pencil_draw(self, event=None):
        if self.left_but == "down":

            # Make sure x and y have a value
            if self.x_pos is not None and self.y_pos is not None:
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=TRUE)

            self.x_pos = event.x
            self.y_pos = event.y

#    def save(self):
 #       self.img=ImageGrab.grab().crop((50,50,350,350))
  #      self.img.show()
        
    def __init__(self, canvas):
        self.drawing_area = canvas
        self.drawing_area.pack()
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.left_but_down)
        self.drawing_area.bind("<ButtonRelease-1>", self.left_but_up)
        
def client_program(): 
    root = Tk()    #creates root variable which is used to create the window the canvas will be displayed on
    
    #Get blank canvas from server
    
    #Gets host IP and sets the port number
    host = socket.gethostname()
    port = 5000
    #Sets parameters for communication between client and server
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    #establishes connection with server
    client_socket = socket.socket()
    client_socket.connect((host, port))
    #recieves image, decodes, and saves it as client.png
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = "client.png"
    filename = os.path.basename(filename)
    filesize = int(filesize)
    #creates an image out of the bytes then closes
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
    client_socket.close()
    
    root.title("Drawing (DO NOT MOVE)") #sets title test of the window
    bgr = ImageTk.PhotoImage(Image.open("client.png")) #make bgr = the image the server sends to client
    root.geometry('%dx%d+%d+%d' % (600,600,50,50)) #this sets the spawnpoint of the canvas
    canvas = Canvas(root,height=600,width=600) #places a canvas on the window for the client to draw on
    canvas.create_image(0,0,anchor=NW,image=bgr) #this sets the canvas background to the image
    btn = Button(root, text='Save and Exit', width=10, height=1, bd='10', command=save) #when clicked, calls save()
    btn.place(x=500, y=555) #places the button on the window
    paint_app = PaintApp(canvas) #creates a PaintApp which is the class that will allow the client to draw on the canvas
    root.mainloop() #displays the root window and all accompanying features
    
def save():
    img=ImageGrab.grab().crop((75,100,825,850)) #takes a screenshot of where the canvas should be on the screen
    
    #Send Current Drawing
    
    #re-establishes parameters for connection
    host = socket.gethostname()
    port = 5000
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    #updates client.png to the new drawing made by the client
    img.save("client.png")
    filename = "client.png"
    filesize = os.path.getsize(filename)
    #re-establishes connection
    s = socket.socket()
    s.connect((host, port))
    print(f"{filename}{SEPARATOR}{filesize}") #Will get error without this print statement :(
    s.send(f"{filename}{SEPARATOR}{filesize}".encode(encoding="utf-8"))
    #Writes the image into bytes
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
    s.close()
    
    #Receive Server Image similar to connection code in client_program
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = "client.png"
    filename = os.path.basename(filename)
    filesize = int(filesize)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)

    
    client_socket.close()
    
       
if __name__ == '__main__':
    client_program()