# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 18:39:00 2021

@author: dunnm10
"""

import socket
import os   
from PIL import Image 
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4

# Function to send a file to the connection
def send(filename, conn):
    # Establish filesize from filename and send to conn
    print("Sending")
    filesize = os.path.getsize(filename)
    conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # Sends the file in BUFFER_SIZE chunnks to conn and then close connection
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:                
                break
            conn.sendall(bytes_read)
    conn.close()
    print("Sent")
    
# Function to call receive_help with correct parameters
def receive(conn):
    print("receiving.....")
    received = conn.recv(BUFFER_SIZE).decode()
    receive_help(conn, received)
    
# Function to call receive_help with correct parameters  
def receive2(conn, string):
    print("receiving.....")
    received = string
    receive_help(conn, received)
    
# Function to receive file from conn    
def receive_help(conn, received):
    # Create update.png with given filesize from conn
    filename, filesize = received.split(SEPARATOR)
    filename = "update.png"
    filename = os.path.basename(filename)
    filesize = int(filesize)
    #Recceives file in BUFFER_SIZE chunks and writes them to update.png; when finishes closes connection
    with open(filename, "wb") as f:
        while True:
            bytes_read = conn.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
    conn.close()
    print("received")
    
    # Takes new client image, makes all white values transparent, and 
    #  combines new image with old image
    
    # Opens update.png as rgba file type
    img = Image.open('update.png')
    rgba = img.convert("RGBA")
    datas = rgba.getdata()
    # Loops through pixel data and checks if the value is white, if it is, it makes it transparent
    #  and saves the pixel info in 'newData'
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    # Saves 'newData' as update.png
    rgba.putdata(newData)
    rgba.save("update.png", "PNG")
    # Places update.png(transparent image) on top of current.png(the most updated picture)
    background = Image.open("current.png")
    foreground = Image.open("update.png")
    background.paste(foreground, (0, 0), foreground)
    background.save("current.png")
    
# The "main" function of the program
def server_program():
    # Establishes a socket for which the server to utilize
    host = ''
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(10)
    # Creates and saves current.png from blankCanvas.png as to never alter the blank canvas
    im = Image.open("blankCanvas.png")
    im.save("current.png")
    filename = "current.png"
    # Begins constantly checking if a client has connected
    while(True):
        # Establishes connection with client
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        data = conn.recv(1024).decode()
        print("data: " + data)
        # Checks what the client requested from 'data' and applies the relevant method
        if(str(data) == "receive"):
            send(filename, conn)
        elif(str(data) == "send"):
            receive(conn)
        elif("send" in str(data)):  # Required as sometimes client does not send correct message
            receive2(conn, data)
        else:
            conn.close()
            
   
if __name__ == '__main__':
    server_program()