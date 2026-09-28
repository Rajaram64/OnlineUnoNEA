import pygame as pg
import asyncio
import pygame_gui as pgui
import websockets
import json
async def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("Online Uno | Raj B :D")
    class Text:
        def __init__(self, label, x_pos, y_pos, size):
            self.label = label
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.size = size

        async def draw_title(self):
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

        async def draw_button(self, refreshrate, currentpage, events):
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
            self.gui = pgui.UIManager((self.screenx, self.screeny))
            self.rect = pg.Rect((self.screenx * self.xcords, self.screeny * self.ycords),(self.screenx * self.xdimension, self.screeny * self.ydimension))
            self.box = pgui.elements.UITextEntryLine(relative_rect=self.rect, manager=self.gui, object_id="#main_text_entry")

        async def draw_box(self, events, refreshrate, usrname, label):
            for event in events:
                self.gui.process_events(event)
                if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    starttime = pg.time.get_ticks()
                    usrname = event.text
                    SET = Text(label, self.xcords + 0.15, self.ycords, 0.13)
                    while pg.time.get_ticks() - starttime < 2000:
                        await SET.draw_title()
                        pg.display.flip()
            self.gui.update(refreshrate)
            self.gui.draw_ui(screen)
            return usrname

    class NetworkTextinputs(textinputs):
        def __init__(self, xcords, ycords, xdimension, ydimension, type):
            super().__init__(xcords, ycords, xdimension, ydimension)
            self.connectionpoint = "ws://localhost:8765"
            self.type = type

        async def send_input(self, events, refreshrate, usrname, label, currentpage):

            for event in events:
                self.gui.process_events(event)

                if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    usrinput = event.text
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

            self.gui.update(refreshrate)
            self.gui.draw_ui(screen)
            return usrname, None, currentpage

    class page:
        def __init__(self, title, buttons, inputs, networkinputs):
            self.title = title
            self.buttons = buttons
            self.inputs = inputs
            self.networkinputs = networkinputs

        async def draw_page(self, refreshrate, events, currentpage, usrname, roomcode):
            screen.fill((215, 0, 64))
            await self.title.draw_title()
            if self.buttons != None:
                for button in self.buttons:
                    currentpage = await button.draw_button(refreshrate, currentpage, events)

            if self.inputs != None:
                for input in self.inputs:
                    usrname = await input.draw_box(events, refreshrate, usrname, "username set")

            if self.networkinputs != None:
                for netinput in self.networkinputs:
                    usrname, roomcode, currentpage = await netinput.send_input(events, refreshrate, usrname, "Room code set", currentpage)
            return currentpage, usrname, roomcode

    async def hostmenu(refreshrate, events, currentpage, usrname, roomcode, LEAVE= button("LEAVE", 0.8, 0.1, "home", None), LOBBYMENU= Text("Lobby Menu", 0.5, 0.1, 0.05)):
        x, y = screen.get_size()
        screen.fill((222, 49, 99))
        ROOMCODE = Text(roomcode, 0.1, 0.1, 0.05)
        pg.draw.rect(screen, (192, 30, 76), (x*0.01, y*0.2, x*0.28, y*0.7), width=0, border_radius=60)
        pg.draw.rect(screen, (192, 30, 76), (x*0.30, y*0.2, x*0.32, y*0.35), width=0, border_radius=60)
        pg.draw.rect(screen, (192, 30, 76), (x*0.30, y*0.57, x*0.32, y*0.35), width=0, border_radius=60)
        pg.draw.rect(screen, (192, 30, 76), (x*0.63, y*0.2, x*0.35, y*0.35), width=0, border_radius=60)
        pg.draw.rect(screen, (192, 30, 76), (x*0.63, y*0.57, x*0.35, y*0.35), width=0, border_radius=60)


        await LOBBYMENU.draw_title()
        await ROOMCODE.draw_title()

        currentpage = await LEAVE.draw_button(refreshrate, currentpage, events)

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

        while playing:
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    playing = False #when the user presses the X button on the tab, this will end the game loop and close the program

            refreshrate = fps.tick(60)/1000   #limits framerate to 60 fps as well as returning time elapsed (in seconds) since the previous frame

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
                currentpage, usrname, roomcode = await hostmenu(refreshrate, events, currentpage, usrname, roomcode)
            if currentpage == "user":
                currentpage, usrname, roomcode = await usermenu(refreshrate, events, currentpage, usrname, roomcode)
            pg.display.flip()

    await homeloop()
asyncio.run(main())
