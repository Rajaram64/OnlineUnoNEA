import pygame as pg
import asyncio
import pygame_gui as pgui
import websockets
import json
async def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("Online Uno | Raj B :D")

    class images(pg.sprite.Sprite):
        def __init__(self, xcord, ycord, filename, xdimension, ydimension):
            pg.sprite.Sprite.__init__(self)
            self.xcord = xcord
            self.ycord = ycord
            self.screenx, self.screeny = screen.get_size()
            self.image = pg.image.load(filename)
            self.width = self.screenx * xdimension
            self.height = self.screeny * ydimension
            self.image = pg.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect(center = (self.screenx * self.xcord , self.screeny * self.ycord))
        def drawimage(self):
            screen.blit(self.image, self.rect)

    class Text:
        def __init__(self, label, x_pos, y_pos, size):
            self.label = label
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.size = size

        def draw_title(self):
            x_dimension, y_dimension = screen.get_size()
            NeueBold = pg.font.Font("NeueMetanaNext-SemiBold.otf",(int(y_dimension * self.size)))
            image = NeueBold.render(self.label, True, (0,0,0))
            rectangle = image.get_rect(center = (x_dimension * self.x_pos, y_dimension * self.y_pos))
            screen.blit(image, rectangle)

    class button(Text):
        def __init__(self, label, x_pos, y_pos, nxtpage, size):
            super().__init__(label, x_pos, y_pos, size)
            self.nxtpage = nxtpage
            self.currentsize = 0.08
            self.currentfont = "NeueMetanaNext-SemiBold.otf"
            self.colour = (0,0,0)

        def draw_button(self, refreshrate, currentpage, events):
            x_dimension, y_dimension = screen.get_size()
            mouspos = pg.mouse.get_pos()
            currenttext = pg.font.Font(self.currentfont ,(int(y_dimension * self.currentsize)))
            image = currenttext.render(self.label, True, self.colour)
            rectangle = image.get_rect(center = (x_dimension * self.x_pos, y_dimension * self.y_pos))
            hover = rectangle.collidepoint(mouspos)

            if hover:
                goal = 0.14
                self.currentfont = "NeueMetanaNextOutline-Black.otf"
                self.colour = (255,255,255)
            else:
                goal = 0.08
                self.currentfont = "NeueMetanaNext-SemiBold.otf"
                self.colour = (0,0,0)

            if self.currentsize < goal:
                self.currentsize += 0.6 * refreshrate
                self.currentsize = min(self.currentsize, goal)
            elif self.currentsize > goal:
                self.currentsize -= 0.6 * refreshrate
                self.currentsize = max(self.currentsize, goal)

            currenttext = pg.font.Font(self.currentfont ,(int(y_dimension * self.currentsize)))
            image = currenttext.render(self.label, True, self.colour)
            rectangle = image.get_rect(center = (x_dimension * self.x_pos, y_dimension * self.y_pos))
            screen.blit(image, rectangle)

            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and hover:
                    return self.nxtpage
            return currentpage

    class textinputs():
        def __init__(self, xcords, ycords, xdimension, ydimension):
            self.xcords = xcords
            self.ycords = ycords
            self.xdimension = xdimension
            self.ydimension = ydimension
            self.screenx, self.screeny = screen.get_size()
            self.manager = pgui.UIManager((self.screenx, self.screeny))
            self.rect = pg.Rect((self.screenx * self.xcords, self.screeny * self.ycords),(self.screenx * self.xdimension, self.screeny * self.ydimension))
            self.box = pgui.elements.UITextEntryLine(relative_rect=self.rect, manager=self.manager, object_id="#main_text_entry")

        async def draw_box(self, events, refreshrate, usrname, label):
            Sprite = images(0.7, 0.42, "noun_enterkey_6369765_@700.png", 0.08, 0.1)
            for event in events:
                self.manager.process_events(event)
                if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    starttime = pg.time.get_ticks()
                    usrname = event.text
                    SET = Text(label, self.xcords + 0.15, self.ycords, 0.13)
                    while pg.time.get_ticks() - starttime < 2000:
                        SET.draw_title()
                        pg.display.flip()
                    event.text = ""
            Sprite.drawimage()
            self.manager.update(refreshrate)
            self.manager.draw_ui(screen)
            return usrname

    class NetworkTextinputs(textinputs):
        def __init__(self, xcords, ycords, xdimension, ydimension, type):
            super().__init__(xcords, ycords, xdimension, ydimension)
            self.connectionpoint = "ws://localhost:8765"
            self.type = type

        async def send_input(self, events, refreshrate, usrname, currentpage):
            Sprite = images(0.7, 0.42, "noun_enterkey_6369765_@700.png", 0.08, 0.1)
            for event in events:
                self.manager.process_events(event)
                if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    usrinput = event.text
                    try:
                        connection = await websockets.connect(self.connectionpoint)
                        package = '''{"package": [
                            {}
                            ]}'''
                        json_package = json.loads(package)
                        json_package["package"][0]["room code"] = int(usrinput)
                        json_package["package"][0]["username"] = str(usrname)
                        json_package["package"][0]["type"] = self.type
                        newpackage = json.dumps(json_package)
                        print(newpackage)
                        await connection.send(newpackage)
                        confirmation = await connection.recv()
                        await connection.close()
                        print(confirmation)
                        currentpage = "host"
                        return usrname, usrinput, currentpage
                    except:
                        pass
            Sprite.drawimage()
            self.manager.update(refreshrate)
            self.manager.draw_ui(screen)
            return usrname, None, currentpage

    class checkbox:
        def __init__(self, xcords, ycords, xdimension, ydimension):
            self.xcords = xcords
            self.ycords = ycords
            self.xdimension = xdimension
            self.ydimension = ydimension
            self.screenx, self.screeny = screen.get_size()
            self.manager = pgui.UIManager((self.screenx, self.screeny))
            self.checkbox = pgui.elements.UICheckBox(relative_rect=(self.xcords * self.screenx, self.ycords * self.screeny, self.xdimension * self.screenx, self.ydimension * self.screeny), text="", manager=self.manager)
        def draw_checkbox(self, refreshrate, events):
            for event in events:
                self.manager.process_events(event)
            self.manager.update(refreshrate)
            self.manager.draw_ui(screen)

    class page:
        def __init__(self, title, buttons, inputs, networkinputs):
            self.title = title
            self.buttons = buttons
            self.inputs = inputs
            self.networkinputs = networkinputs

        async def draw_page(self, refreshrate, events, currentpage, usrname, roomcode):
            screen.fill((215, 0, 64))
            self.title.draw_title()
            if self.buttons != None:
                for button in self.buttons:
                    currentpage = button.draw_button(refreshrate, currentpage, events)

            if self.inputs != None:
                for input in self.inputs:
                    usrname = await input.draw_box(events, refreshrate, usrname, "Username set")

            if self.networkinputs != None:
                for netinput in self.networkinputs:
                    usrname, roomcode, currentpage = await netinput.send_input(events, refreshrate, usrname, currentpage)
            return currentpage, usrname, roomcode

    class LobbyRectangles:
        def __init__(self, xdimension, ydimension, xcord, ycord):
            self.screenx , self.screeny = screen.get_size()
            self.xdimension = xdimension
            self.ydimension = ydimension
            self.xcord = xcord
            self.ycord = ycord
            self.rectangle = pg.Rect((self.screenx * self.xcord, self.screeny * self.ycord),(self.screenx * self.xdimension, self.screeny * self.ydimension))

        def drawrects(self):
            pg.draw.rect(screen, (192, 30, 76), self.rectangle, width=0, border_radius=30)

    class LobbyButtonRects(LobbyRectangles):
        def __init__(self, xdimension, ydimension, xcord, ycord, imagelabel):
            super().__init__(xdimension, ydimension, xcord, ycord)
            self.imagelabel = imagelabel
            self.actualimagefrfr = images(self.xcord + 0.05, self.ycord + 0.12, self.imagelabel, 0.08, 0.2)
            self.colour = (159, 25, 63)
            self.selected = False

        def draw_buttonrects(self, events, allbuttons):
            mouspos = pg.mouse.get_pos()
            hover = self.rectangle.collidepoint(mouspos)
            if hover == True and self.selected == False:
                self.colour = (105, 15, 40)
            elif hover == False and self.selected == False:
                self.colour = (159, 25, 63)
            elif hover == True and self.selected == True:
                self.colour = (136, 214, 108)
            elif hover == False and self.selected == True:
                self.colour = (78, 167, 46)

            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and hover:
                    if self.selected == False:
                        for buttonrec in allbuttons:
                            buttonrec.selected = False
                        self.selected = True
                    elif self.selected == True:
                        self.selected = False

            pg.draw.rect(screen, self.colour, self.rectangle, width=0, border_radius=30)
            self.actualimagefrfr.drawimage()

    class LobbyMenu(page):
        def __init__(self, title, buttons, inputs, networkinputs, checkboxes, rects, buttonrects):
            super().__init__(title, buttons, inputs, networkinputs)
            self.checkboxes = checkboxes
            self.rects = rects
            self.buttonrects = buttonrects

        async def draw_menu(self, refreshrate, events, currentpage, usrname, roomcode):
            screen.fill((222, 49, 99))

            if self.rects != None:
                for rect in self.rects:
                    rect.drawrects()

            if self.buttonrects != None:
                for buttonrectangles in self.buttonrects:
                    buttonrectangles.draw_buttonrects(events, self.buttonrects)

            if self.title != None:
                for titles in self.title:
                    titles.draw_title()

            if self.buttons != None:
                for button in self.buttons:
                    currentpage = button.draw_button(refreshrate, currentpage, events)

            if self.inputs != None:
                for input in self.inputs:
                    usrname = await input.draw_box(events, refreshrate, usrname, "username set")

            if self.networkinputs != None:
                for netinput in self.networkinputs:
                    usrname, roomcode, currentpage = await netinput.send_input(events, refreshrate, usrname, currentpage)

            if self.checkboxes != None:
                for checkbox in self.checkboxes:
                    checkbox.draw_checkbox(refreshrate, events)

            return currentpage, usrname, roomcode

    async def usermenu(refreshrate, events, currentpage, usrname, roomcode):
        screen.fill((222, 49, 99))

        return currentpage, usrname, roomcode

    async def homeloop():
        usrname = ""
        roomcode = 0
        USERNAMEBOX = textinputs(0.3525, 0.4, 0.3, 0.07)
        fps = pg.time.Clock()
        playing = True #Boolean for controlling game loop
        currentpage = "home"
        BACK = button("HOME", 0.2, 0.9, "home", None)
        #this is all the objects for home
        CREATE = button("CREATE", 0.5, 0.8, "create", None)
        JOIN = button("JOIN", 0.5, 0.6, "join", None)
        USERNAME = button("USERNAME", 0.5, 0.4, "username", None)
        UNO = Text("UNO", 0.5, 0.1, 0.13)
        HOME = page(UNO, [CREATE, JOIN, USERNAME], None, None)
        #this is all the objects for test
        TEST = Text("TEST", 0.5, 0.1, 0.13)
        TESTPAGE = page(TEST, [BACK, CREATE, JOIN], None, None)
        #All object for create page
        CREATETITLE = Text("Enter Room Code", 0.5, 0.1, 0.13)
        CREATEROOMCODE = NetworkTextinputs(0.3525, 0.4, 0.3, 0.07, "HC")
        CREATEPAGE = page(CREATETITLE, [BACK], None, [CREATEROOMCODE])
        #This is all objects for Username page
        USERNAMETITLE = Text("Enter Username", 0.5, 0.1, 0.13)
        USERNAMEPAGE = page(USERNAMETITLE, [BACK], [USERNAMEBOX], None)
        #All objects for join page
        JOINROOMCODE = NetworkTextinputs(0.3525, 0.4, 0.3, 0.07, "JL")
        JOINPAGE = page(CREATETITLE, [BACK], None, [JOINROOMCODE])
        #all objects for settings on lobby creation page
        LEAVE = button("LEAVE", 0.8, 0.1, "home", None)
        #all text for lobby creation page
        LOBBYMENU = Text("Lobby Menu", 0.5, 0.1, 0.05)
        ROOMCODE = Text(str(roomcode), 0.1, 0.1, 0.05)
        RULES = Text("Rules", 0.11, 0.25, 0.05)
        MODES = Text("Modes", 0.46, 0.25, 0.05)
        STACKDRAW = Text("Stack Draw", 0.11, 0.33, 0.04)
        CARDS = Text("Cards", 0.11, 0.37, 0.04)
        CUTIN = Text("Cut In", 0.11, 0.425, 0.04)
        ZEROSEVENSWAP = Text("0-7 swap", 0.11, 0.48, 0.04)
        FORCEDDRAW = Text("Forced Draw", 0.11, 0.54, 0.04)
        PLAYONDRAW = Text("Play on Draw", 0.11, 0.6, 0.04)
        DEFLECTION = Text("Deflection", 0.11, 0.66, 0.04)
        SKIPTURN = Text("Skip Turn", 0.11, 0.72, 0.04)
        ONDRAW = Text("On Draw", 0.11, 0.76, 0.04)
        #all checkboxes for lobby creation page
        CHECKSTACKDRAW = checkbox(0.25, 0.32, 0.025, 0.04)
        CHECKCUTIN = checkbox(0.25, 0.395, 0.025, 0.04)
        CHECKZEROSEVENSWAP = checkbox(0.25, 0.455, 0.025, 0.04)
        CHECKFORCEDDRAW = checkbox(0.25, 0.515, 0.025, 0.04)
        CHECKPLAYONDRAW = checkbox(0.25, 0.575, 0.025, 0.04)
        CHECKDEFLECTION = checkbox(0.25, 0.635, 0.025, 0.04)
        CHECKSKIPTURN = checkbox(0.25, 0.715, 0.025, 0.04)
        #rectangles for lobby frfr
        RULESREC = LobbyRectangles(0.28, 0.7, 0.005, 0.2)
        MODESREC = LobbyRectangles(0.32, 0.35, 0.3, 0.2)
        ADDONSREC = LobbyRectangles(0.32, 0.35, 0.3, 0.57)
        USERSREC = LobbyRectangles(0.35, 0.35, 0.63, 0.2)
        CHATREC = LobbyRectangles(0.35, 0.35, 0.63, 0.57)
        #special rectangles that act like buttons idk
        NOMERCYBUTTONREC = LobbyButtonRects(0.1, 0.26, 0.305, 0.28, "NOMERCY.png")
        UNOBUTTONREC = LobbyButtonRects(0.1, 0.26, 0.41, 0.28, "UNO.jpg")
        UNOFLIPBUTTONREC = LobbyButtonRects(0.1, 0.26, 0.515, 0.28, "FLIP.png")

        HOSTMENU = LobbyMenu([LOBBYMENU, ROOMCODE, RULES, CARDS, CUTIN, ZEROSEVENSWAP, STACKDRAW, FORCEDDRAW, PLAYONDRAW, DEFLECTION, SKIPTURN, ONDRAW, MODES], [LEAVE], None, None, [CHECKSTACKDRAW, CHECKCUTIN, CHECKZEROSEVENSWAP, CHECKFORCEDDRAW, CHECKPLAYONDRAW, CHECKDEFLECTION, CHECKSKIPTURN], [RULESREC, MODESREC, ADDONSREC, USERSREC, CHATREC], [NOMERCYBUTTONREC, UNOBUTTONREC, UNOFLIPBUTTONREC])

        while playing:
            events = pg.event.get()
            refreshrate = fps.tick(60)/1000 #limits framerate to 60 fps as well as returning time elapsed (in seconds) since the previous frame
            if currentpage == "home":
                currentpage, usrname, roomcode = await HOME.draw_page(refreshrate, events, currentpage, usrname, roomcode)

            if currentpage == "test":
                currentpage, usrname, roomcode = await TESTPAGE.draw_page(refreshrate, events, currentpage, usrname, roomcode)

            if currentpage == "create":
                currentpage, usrname, roomcode = await CREATEPAGE.draw_page(refreshrate, events, currentpage, usrname, roomcode)

            if currentpage == "username":
                currentpage, usrname, roomcode = await USERNAMEPAGE.draw_page(refreshrate, events, currentpage, usrname, roomcode)

            if currentpage == "join":
                currentpage, usrname, roomcode = await JOINPAGE.draw_page(refreshrate, events, currentpage, usrname, roomcode)

            if currentpage == "host":
                HOSTMENU.title[1] = Text(str(roomcode), 0.15, 0.1, 0.05) #updates the roomcode display to be the same as the one inputted by the user, instead of the default 0 value
                currentpage, usrname, roomcode = await HOSTMENU.draw_menu(refreshrate, events, currentpage, usrname, roomcode)

            if currentpage == "user":
                ROOMCODE = Text(str(roomcode), 0.5, 0.1, 0.05)
                currentpage, usrname, roomcode = await usermenu(refreshrate, events, currentpage, usrname, roomcode)

            for event in events:
                if event.type == pg.QUIT:
                    playing = False #when the user presses the X button on the tab, this will end the game loop and close the program

            pg.display.flip()

    await homeloop()
asyncio.run(main())
