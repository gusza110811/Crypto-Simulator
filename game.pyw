import tkinter
import tkinter.font
import pyglet
import random
import json
import enum
import time

# Declarations
font = "Public Pixel"

pyglet.options['win32_gdi_font'] = True
fontpath = f"fonts/{font}.ttf"
pyglet.font.add_file(str(fontpath))

class gamestates(enum.Enum):
    OFF = "off"
    ON = "on"
    IDLE = 0
    MINING = 1
    SHOPPING = 3
    PROFILE = 4
    INVENTORY = 5
    PAUSED = 6

colorpalettes = {
        "classic":["#000","#FFF"],
        "classic2":["#00F","#FFF"],
        "transvibe":["#5BCEFA","#F5A9B8"],
        "bivibe":["#D60270","#0038A8"],
        "comfy":["#BF9D9D","#e6dfaf"],
        "comfy2":["#DBC09E","#8399a8"],
        "comfy3":["#BF9D9D","#a3ccbe"]
}

gpus = [
    # [Name, Seconds per cycle, Crypto per cycle]
    ["Tester Gpu",5,1],
    ["Scrapyard Gpu",20,1]
]

# Load settings and font
def load():
    global colorpalettes
    global settings
    global backgroundcolor
    global foregroundcolor
    global fontbig
    global fontnormal
    global fontmid
    global fontsmall
    global fonttiny
    global font

    with open("settings.json") as file:
        settings = json.load(file)
    
    if not settings["FlipPalette"]:
        backgroundcolor, foregroundcolor = tuple(colorpalettes[settings["ColorPalette"]])
    else:
        foregroundcolor, backgroundcolor = tuple(colorpalettes[settings["ColorPalette"]])
    fontbig = tkinter.font.Font(family=font,size=20)
    fontnormal = tkinter.font.Font(family=font,size=16)
    fontmid = tkinter.font.Font(family=font,size=12)
    fontsmall = tkinter.font.Font(family=font,size=8)
    fonttiny = tkinter.font.Font(family=font,size=6)

    return

def changepage(newpage):
    global page
    page = newpage

def game(root:tkinter.Tk,deltatime,init:bool):
    if init:
        Title = tkinter.Label(text="NO",font=fontbig,fg=foregroundcolor,bg=backgroundcolor)
        Title.pack(anchor="center")
    return

def menu(root:tkinter.Tk,dt,init:bool):
    if init:
        Title = tkinter.Label(text="Crypto Simulator",font=fontbig,fg=foregroundcolor,bg=backgroundcolor)
        PlayButton = tkinter.Button(text="Play",font=fontmid,fg=foregroundcolor,bg=backgroundcolor,command=lambda:changepage(game))

        Title.pack(anchor="center",pady=10)
        PlayButton.pack(anchor="center",pady=10)

    return

def main(root:tkinter.Tk):
    load()

    global page
    page = menu
    prevpage = None

    root.configure(background=backgroundcolor)

    dt = 0
    while True:
        begin = time.time()


        page(root,dt,not (page==prevpage))

        root.update()
        
        end = time.time()
        prevpage = page


        dt = end-begin

if __name__ == "__main__":
    root = tkinter.Tk()
    root.minsize(640,380)
    root.title("Crypto Simulator")
    main(root)