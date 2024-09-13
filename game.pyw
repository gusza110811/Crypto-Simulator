import tkinter
import tkinter.font
import pyglet
import random
import json
import enum
import time

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
        "comfy3":["#BF9D9D","#a3ccbe"],
        "urine&feces":["#740","#FF0"]
}

gpus = [
    # [Name, Seconds per cycle, Crypto per cycle]
    ["Tester Gpu",5,1],
    ["Scrapyard Gpu",20,1]
]


# Really important function
def reload():
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


# Quite a useful command
def clear(root:tkinter.Tk|tkinter.Widget):
    widgets = root.winfo_children()

    for widget in widgets:
        widget.destroy()

    return


# Save the settings yeah
def savesetting(root,colorpalettechooser:tkinter.Listbox,flippalette:tkinter.BooleanVar):
    colorpalette = ""
    try:
        colorpalette = colorpalettechooser.get(colorpalettechooser.curselection()[0])

    except IndexError:
        with open("settings.json") as file:
            settings = json.load(file)
            colorpalette = settings["ColorPalette"]
    
    flippedpalette = flippalette.get()


    with open("settings.json",'w') as file:
        savedata = {
            "ColorPalette":colorpalette,
            "FlipPalette":flippedpalette
        }
        json.dump(savedata,file,indent=4)
    
    menu(root)

    return


# Settings (really)
def setting(root:tkinter.Tk):
    clear(root)
    root.configure(bg=backgroundcolor)
    global gamestate

    Title = tkinter.Label(root,bg=backgroundcolor,text="SETTINGS",foreground=foregroundcolor,font=fontbig)
    Title.pack(pady=10)

    ColorpalettesChooser = tkinter.Listbox(root,bg=backgroundcolor,foreground=foregroundcolor,font=fontsmall)
    for palette in colorpalettes:
        ColorpalettesChooser.insert("end",palette)
    colorpaletteskey = list(colorpalettes)
    ColorpalettesChooser.select_set(colorpaletteskey.index(settings["ColorPalette"]))
    ColorpalettesChooser.pack()

    flippedpalette = tkinter.BooleanVar()
    flippalette = tkinter.Checkbutton(root,bg=backgroundcolor,fg=foregroundcolor,text="Flip color palette", font=fontsmall,onvalue=True,offvalue=False,variable=flippedpalette,selectcolor=backgroundcolor)
    if settings["FlipPalette"]:
        flippalette.select()
    flippalette.pack()

    Save = tkinter.Button(root,bg=backgroundcolor,fg=foregroundcolor,text="Save and return to menu",font=fontmid,command=lambda:savesetting(root,ColorpalettesChooser,flippedpalette))
    Save.pack()

    Tomenu = tkinter.Button(root,bg=backgroundcolor,fg=foregroundcolor,text="Cancel",font=fontmid,command=lambda:menu(root))
    Tomenu.pack()

    root.mainloop()

    return


def mine(root:tkinter.Tk,minebutton:tkinter.Button,frame:tkinter.Frame,secondstogotk:tkinter.StringVar):
    global gamestate
    global updated

    timetilnextcycle = tkinter.Label(frame,bg=backgroundcolor,fg=foregroundcolor,textvariable=secondstogotk,font=fontnormal)

    if gamestate != gamestates.MINING:

        gamestate = gamestates.MINING
        minebutton.config(text="Stop\nMining",font=fontmid)

        timetilnextcycle.pack(side="left")
        updated = False
    
    else:
        gamestate = gamestates.IDLE
        minebutton.config(text="Mine",font=fontnormal)

        clear(frame)
        updated = False


    return


def pausemenu(root:tkinter.Tk, button:tkinter.Button, generalframe:tkinter.Frame):
    global gamestate
    global updated

    def leavegame():
        global gamestate
        gamestate = gamestates.OFF

    savebutton = tkinter.Button(generalframe,bg=backgroundcolor,fg=foregroundcolor,text="Save Game",font=fontnormal)
    exitbutton = tkinter.Button(generalframe,bg=backgroundcolor,fg=foregroundcolor,text="Quit",font=fontnormal,command=leavegame)

    if gamestate != gamestates.PAUSED:
        button.config(text="return to\ngame",font=fontmid)

        savebutton.pack()
        exitbutton.pack()

        gamestate = gamestates.PAUSED
        updated = False

    
    else:
        button.config(text="Pause",font=fontnormal)

        clear(generalframe)

        gamestate = gamestates.IDLE
        updated = False

    return

def inventoryfunc(root:tkinter.Tk, button:tkinter.Button, generalframe:tkinter.Frame, inventory:list[list[str,int,int]]):
    global gamestate
    global updated
    global gpu

    inventorynames = []

    for item in inventory:
        inventorynames.append(gpus[item][0])

    scrollbar = tkinter.Scrollbar(generalframe)
    inventorydisp = tkinter.Listbox(generalframe,bg=backgroundcolor,fg=foregroundcolor,font=fontsmall,yscrollcommand=scrollbar.set)
    scrollbar.config(command=inventorydisp.yview)
    
    def equip():
        global gpu
        gpu = inventorydisp.curselection()[0]

        return

    equipbutton = tkinter.Button(generalframe,bg=backgroundcolor,fg=foregroundcolor,text="Equip",font=fontsmall,command=equip)

    for item in inventorynames:
        inventorydisp.insert("end",item)
    
    inventorydisp.select_set(inventory.index(gpu))

    if gamestate != gamestates.INVENTORY:
        button.config(text="Close Inventory",font=fontmid,padx=0)

        scrollbar.pack(side="right",fill="y")
        inventorydisp.pack()
        equipbutton.pack()

        gamestate = gamestates.INVENTORY
        updated = False

    
    else:
        button.config(text="Inventory",font=fontnormal,padx=10)

        clear(generalframe)

        gamestate = gamestates.IDLE
        updated = False


    return


# The game itself (wow)
def game(root:tkinter.Tk):
    clear(root)

    reload()

    global gamestate
    gamestate = gamestates.IDLE

    global gpus
    global crypto
    global cash

    global secondspercycle
    global cryptopercycle

    global gpu
    
    inventory = [
        0,
        1
    ]

    gpu = inventory[1]
    crypto = 0
    cash = 0

    secondspercycle = gpus[gpu][1]
    cryptopercycle =gpus[gpu][2]

    secondstogo = secondspercycle

    GeneralFrame = tkinter.Frame(root,bg=backgroundcolor,borderwidth=3)
    GeneralFrame.grid(row=2,column=1,rowspan=3,columnspan=3)
    secondstogotk = tkinter.StringVar(GeneralFrame,"secondstogo")

    pause = tkinter.Button(root, bg=backgroundcolor, fg=foregroundcolor, text="Pause",font=fontnormal,command=lambda: pausemenu(root,pause,GeneralFrame))
    pause.grid(row=0,column=1,padx=20,pady=10)

    shopbutton = tkinter.Button(root, bg=backgroundcolor, fg=foregroundcolor, text="Store",font=fontnormal)
    shopbutton.grid(row=1,column=0,pady=10,padx=10)

    minebutton = tkinter.Button(root, bg=backgroundcolor, fg=foregroundcolor, text="Mine",font=fontnormal,command=lambda: mine(root,minebutton,GeneralFrame,secondstogotk))
    minebutton.grid(row=2,column=0,pady=10,padx=10)

    guidebutton = tkinter.Button(root, bg=backgroundcolor, fg=foregroundcolor, text="Guide",font=fontnormal)
    guidebutton.grid(row=1,column=3,pady=10,padx=10)

    invbutton = tkinter.Button(root, bg=backgroundcolor, fg=foregroundcolor, text="Inventory",font=fontnormal,command=lambda:inventoryfunc(root,invbutton,GeneralFrame,inventory))
    invbutton.grid(row=1,column=1,pady=10,padx=10)

    cryptoVar = tkinter.StringVar(root,"Cryptos: ")
    cryptodisplay = tkinter.Label(root, bg=backgroundcolor, fg=foregroundcolor,textvariable=cryptoVar,font=fontmid)
    cryptodisplay.grid(row=3,column=0,pady=10,padx=10)

    deltatime = 0
    global updated
    updated = False
    while gamestate != gamestates.OFF:
        timelastupdate = time.time()
        cryptoVar.set("Cryptos:\n"+str(crypto))
        secondstogotk.set("time til\nnext cycle: "+'{:.2f}'.format(round(secondstogo,2)))

        if gamestate == gamestates.IDLE:
            if not updated:
                shopbutton.config(state="normal",fg=foregroundcolor)
                minebutton.config(state="normal",fg=foregroundcolor)
                guidebutton.config(state="normal",fg=foregroundcolor)
                invbutton.config(state="normal",fg=foregroundcolor)
                pause.config(state="normal",fg=foregroundcolor)
                updated = True

        if gamestate == gamestates.MINING:
            if not updated:
                shopbutton.config(state="disabled",fg=backgroundcolor)
                minebutton.config(state="normal",fg=foregroundcolor)
                guidebutton.config(state="disabled",fg=backgroundcolor)
                invbutton.config(state="disabled",fg=backgroundcolor)
                pause.config(state="disabled",fg=backgroundcolor)
                updated = True
            
            if secondstogo < 0:
                # do stuff
                crypto += cryptopercycle

                secondstogo = secondspercycle
            
            secondstogo -= deltatime
        
        if gamestate == gamestates.PAUSED:
            if not updated:
                shopbutton.config(state="disabled",fg=backgroundcolor)
                minebutton.config(state="disabled",fg=backgroundcolor)
                guidebutton.config(state="disabled",fg=backgroundcolor)
                invbutton.config(state="disabled",fg=backgroundcolor)
                pause.config(state="normal",fg=foregroundcolor)
                updated = True
        
        if gamestate == gamestates.INVENTORY:
            if not updated:
                shopbutton.config(state="disabled",fg=backgroundcolor)
                minebutton.config(state="disabled",fg=backgroundcolor)
                guidebutton.config(state="disabled",fg=backgroundcolor)
                invbutton.config(state="normal",fg=foregroundcolor)
                pause.config(state="disabled",fg=backgroundcolor)
                updated = True
        
        secondspercycle = gpus[gpu][1]
        cryptopercycle =gpus[gpu][2]

        root.update()
        # get deltatime
        deltatime = time.time()-  timelastupdate
        try:
            print(1/deltatime)
        except:
            pass
    
    menu(root)

    return


# The menu
def menu(root:tkinter.Tk):
    clear(root)

    global gamestate
    gamestate = gamestates.OFF

    reload()
    root.configure(bg=backgroundcolor)

    VERSION = "unreleased"

    splashtexts = [
        "2D!",
        "New and better!",
        "Crypto!",
        "Don't buy NFTs, kids!",
        "I like cheese.",
        "Milk.",
        "It's crypto simulator!",
        "(30×30)+11",
        "60×2 = 5!",
        "r/unexpectedfactorial",
        "SUPERUNALIVING",
        "DIG&CONSTRUCT",
        "Good Game!"
    ]

    # there's an issue with quitting the game requiring a few presses
    # probably due to the way stuff are dealt with but in no way am i gonna touch a better way for that
    def hardquit():
        root.quit()

        exit()

        return

    Title = tkinter.Label(root,bg=backgroundcolor,text="CRYPTO SIMULATOR",foreground=foregroundcolor,font=fontbig)
    Title.pack(pady=10)

    spashtext = tkinter.Label(root,bg=backgroundcolor,fg="#FF0",text=random.choice(splashtexts),font=fontsmall)
    spashtext.pack()

    newgamebutton = tkinter.Button(root,bg=backgroundcolor,fg=foregroundcolor,text="New game",font=fontnormal,command=lambda: game(root))
    newgamebutton.pack(pady=10)

    settingbutton = tkinter.Button(root,bg=backgroundcolor,fg=foregroundcolor,text="Settings",font=fontnormal,command=lambda: setting(root))
    settingbutton.pack(pady=10)

    exitbutton = tkinter.Button(root,bg=backgroundcolor,fg=foregroundcolor,text="Quit",font=fontnormal,command=hardquit)
    exitbutton.pack(pady=10)

    version = tkinter.Label(root,bg=backgroundcolor,fg=foregroundcolor,text=f"version: {VERSION}",font=fonttiny)
    version.pack()
    

    root.mainloop()
    return

if __name__ == "__main__":
    root = tkinter.Tk()
    root.minsize(640,380)
    root.title("Crypto Simulator")
    menu(root)