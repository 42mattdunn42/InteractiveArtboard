# InteractiveArtboard
An interactive artboard that utilizes network programming concepts.

I wrote all of the server code for this group project. This was a group project for my network programming class where we were tasked with creating a program that utilized socket programming. My group decided to create what we called an interactive artboard, which is a canvas on which people can draw and see what other people have drawn. Unfortunatly, it still has some issues and bugs that could be flushed out, such as not functioning when the server and client are on different machines, a zoom effect that can occur on the canvas, and a better solution to capturing what has been drawn.

The server code works off the client telling the server if it wants to send or receive an image, and the server responding with the appropriate action. When the server sends an image, it simply sends a copy of what it has previously received. When the server receives an image, it receives the file, turns it into a transparent version of the image, and then lays that on top of whatever has been previously sent and saves that as the most recent update of the image.
