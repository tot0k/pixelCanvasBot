# pixelCanvasBot
a bot that places pixels on pixelcanvas.io.

I'm leanring how to make a Server-Client communication with the socket package, and I apply this to make a bot on pixelCanvas.io

Requirements :
- socket
- requests
- addict (Dict)

you must create the "admins" file at the root of the server, and write down the admins tokens (used to send "generate" command)

clients commands :

getPixel : Request a pixel to the server, that send a pixel from the waitlist.
placed : Confirm to the server that a specific pixel is placed, and removing it from the waitlist
generate : generate a new waitlist from a file at the root of the server, and from the coordinates of the top-left corner of the image on pixelcanvas.io

sorry for my bad english :p
