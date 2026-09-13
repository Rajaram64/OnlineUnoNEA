import pygame as pg
import asyncio
import pygame_gui as pgui
import websockets
async def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("Online Uno | Raj B :D")
    class Text:
        def __init__(self, label, x_pos, y_pos):
            self.label = label
            self.x_pos = x_pos
            self.y_pos = y_pos
        async def draw_title(self):
            x_dimension, y_dimension = screen.get_size()
            NeueBold = pg.font.Font("NeueMetanaNext-SemiBold.otf",(int(y_dimension * 0.13)))
            image = NeueBold.render(self.label, True, (0,0,0))
            rectangle = image.get_rect(center = (x_dimension * self.x_pos, y_dimension * self.y_pos))
            screen.blit(image, rectangle)

    class button(Text):
        def __init__(self, label, x_pos, y_pos, nxtpage):
            super().__init__(label, x_pos, y_pos)
            self.nxtpage = nxtpage
            self.base = 0.08
            self.max = 0.14
            self.pace = 0.6
            self.currentsize = self.base
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
                goal = self.max
                self.currentfont = "NeueMetanaNextOutline-Black.otf"
                self.colour = (255,255,255)
            else:
                goal = self.base
                self.currentfont = "NeueMetanaNext-SemiBold.otf"
                self.colour = (0,0,0)

            if self.currentsize < goal:
                self.currentsize += self.pace * refreshrate
                self.currentsize = min(self.currentsize, goal)
            elif self.currentsize > goal:
                self.currentsize -= self.pace * refreshrate
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
            self.gui = pgui.UIManager(screen.get_size())
            self.rect = pg.Rect((self.screenx * self.xcords, self.screeny * self.ycords),(self.screenx * self.xdimension, self.screeny * self.ydimension))
            self.box = pgui.elements.UITextEntryLine(relative_rect=self.rect, manager=self.gui, object_id="#main_text_entry")

        async def draw_box(self, events, refreshrate, usrname, label):
            for event in events:
                self.gui.process_events(event)
                if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    starttime = pg.time.get_ticks()
                    usrname = event.text
                    SET = Text(label, self.xcords + 0.15, self.ycords)
                    while pg.time.get_ticks() - starttime < 2000:
                        await SET.draw_title()
                        pg.display.flip()
            self.gui.update(refreshrate)
            self.gui.draw_ui(screen)
            return usrname

    class NetworkTextinputs(textinputs):
        def __init__(self, xcords, ycords, xdimension, ydimension):
            super().__init__(xcords, ycords, xdimension, ydimension)
            self.connectionpoint = "ws://localhost:8765"
        async def send_input(self, events, refreshrate, usrname, label):
            for event in events:
                self.gui.process_events(event)
                if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    starttime = pg.time.get_ticks()
                    SET = Text(label, 0.5, 0.4)
                    usrinput = event.text
                    while pg.time.get_ticks() - starttime < 2000:
                        await SET.draw_title()
                        pg.display.flip()
                    connection = await websockets.connect(self.connectionpoint)
                    package = [usrname, usrinput]
                    await connection.send(package)
                    confirmation = await connection.recv()
                    await connection.close()
                    print(confirmation)
            self.gui.update(refreshrate)
            self.gui.draw_ui(screen)

    class page:
        def __init__(self, title, buttons, inputs, networkinputs):
            self.title = title
            self.buttons = buttons
            self.inputs = inputs
            self.networkinputs = networkinputs

        async def draw_page(self, refreshrate, events, currentpage, usrname):
            screen.fill((215, 0, 64))
            await self.title.draw_title()
            if self.buttons != None:
                for button in self.buttons:
                    currentpage = await button.draw_button(refreshrate, currentpage, events)
            if self.inputs != None:
                for input in self.inputs:
                    usrname = await input.draw_box(events, refreshrate, usrname, "Username set")
            if self.networkinputs != None:
                for netinput in self.networkinputs:
                    usrname = await netinput.send_input(events, refreshrate, usrname, "Username set")
            return currentpage, usrname

    async def gameloop():
        usrname = ""
        USERNAMEBOX = textinputs(0.3525, 0.8, 0.3, 0.07)
        ROOMCODE = NetworkTextinputs(0.3525, 0.4, 0.3, 0.07)
        fps = pg.time.Clock()
        playing = True #Boolean for controlling game loop
        currentpage = "home"
        BACK = button("HOME", 0.5, 0.8, "home")
        #this is all the objects for home
        CREATE = button("CREATE", 0.5, 0.4, "create")
        JOIN = button("JOIN", 0.5, 0.6, "test")
        UNO = Text("UNO", 0.5, 0.1)
        HOME = page(UNO, [CREATE, JOIN], [USERNAMEBOX], None)
        #this is all the objects for test
        TEST = Text("TEST", 0.5, 0.1)
        TESTPAGE = page(TEST, [BACK, CREATE, JOIN], None, None)
        #All object for create page
        CREATETITLE = Text("Enter Username", 0.5, 0.1)
        CREATEPAGE = page(CREATETITLE, [BACK], None, [ROOMCODE])

        while playing:
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    playing = False #when the user presses the X button on the tab, this will end the game loop and close the program

            refreshrate = fps.tick(60)/1000   #limits framerate to 60 fps as well as returning time elapsed (in seconds) since the previous frame

            if currentpage == "home":
                currentpage, usrname = await HOME.draw_page(refreshrate, events, currentpage, None)
            if currentpage == "test":
                currentpage, usrname = await TESTPAGE.draw_page(refreshrate, events, currentpage, None)
            if currentpage == "create":
                currentpage, usrname = await CREATEPAGE.draw_page(refreshrate, events, currentpage, usrname)
            pg.display.flip()


    await gameloop()
asyncio.run(main())
