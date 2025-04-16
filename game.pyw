import tkinter
import tkinter.font
import pyglet
import random
import json
import enum
import time

# Enums
class gamestates(enum.Enum):
    OFF = "off"
    ON = "on"
    IDLE = 0
    MINING = 1
    SHOPPING = 3
    PROFILE = 4
    INVENTORY = 5
    PAUSED = 6

# Global palettes and settings
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
    ["Tester Gpu", 5, 1],
    ["Scrapyard Gpu", 20, 1]
]

# App container
class app:
    root:tkinter.Tk = None

# Style settings and font declarations
class style:
    fontname = "Public Pixel"
    colorpalettes = {}
    settings = {}

    backgroundcolor = None
    foregroundcolor = None

    fontbig = None
    fontnormal = None
    fontmid = None
    fontsmall = None
    fonttiny = None

# Set pyglet font support
pyglet.options['win32_gdi_font'] = True
fontpath = f"fonts/{style.fontname}.ttf"
pyglet.font.add_file(str(fontpath))

# Utility
def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Load settings and fonts
def load():
    with open("settings.json") as file:
        style.settings = json.load(file)

    if not style.settings["FlipPalette"]:
        style.backgroundcolor, style.foregroundcolor = tuple(colorpalettes[style.settings["ColorPalette"]])
    else:
        style.foregroundcolor, style.backgroundcolor = tuple(colorpalettes[style.settings["ColorPalette"]])
    
    style.fontbig = tkinter.font.Font(family=style.fontname, size=20)
    style.fontnormal = tkinter.font.Font(family=style.fontname, size=16)
    style.fontmid = tkinter.font.Font(family=style.fontname, size=12)
    style.fontsmall = tkinter.font.Font(family=style.fontname, size=8)
    style.fonttiny = tkinter.font.Font(family=style.fontname, size=6)

class basepage:
    def render():
        return
    
    def update(dt):
        return
# Game page
class game(basepage):
    def render():
        returnButton = tkinter.Button(text="Menu", font=style.fontsmall,
                                    fg=style.foregroundcolor, bg=style.backgroundcolor,
                                    command=lambda: changepage(menu))
        Title = tkinter.Label(text="To be implemented", font=style.fontbig,
                            fg=style.foregroundcolor, bg=style.backgroundcolor)

        returnButton.pack()
        Title.pack()

# Menu page
class menu(basepage):
    def render():
        Title = tkinter.Label(text="Crypto Simulator", font=style.fontbig,
                            fg=style.foregroundcolor, bg=style.backgroundcolor)
        PlayButton = tkinter.Button(text="Play", font=style.fontmid,
                                    fg=style.foregroundcolor, bg=style.backgroundcolor,
                                    command=lambda: changepage(game))

        Title.pack(anchor="center", pady=10)
        PlayButton.pack(anchor="center", pady=10)

# Page manager
class page:
    current:basepage = None
    previous:basepage = None
    bypassprev = 0

# Page switcher
def changepage(newpage:basepage):
    page.current = newpage
    page.bypassprev = 1
    clear(app.root)

# Main loop
def main(root:tkinter.Tk):
    load()

    page.current = menu
    page.previous = None

    app.root.configure(background=style.backgroundcolor)

    dt = 0
    while True:
        begin = time.time()

        if page.current != page.previous:
            page.current.render()
        else:
            page.current.update(dt)

        root.update()

        end = time.time()

        if page.bypassprev <= 0:
            page.previous = page.current
        else:
            page.bypassprev -= 1

        dt = end - begin

# Entry point
if __name__ == "__main__":
    app.root = tkinter.Tk()
    app.root.minsize(640, 480)
    app.root.title("Crypto Simulator")
    main(app.root)
