import pygame as pg
import asyncio
async def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("Online Uno")
    class text:
        def __init__(self, label, x_pos, y_pos):
            self.label = label
            self.x_pos = x_pos
            self.y_pos = y_pos
        def draw_title(self):
            x_dimension, y_dimension = screen.get_size()
            NeueBold = pg.font.Font("NeueMetanaNext-SemiBold.otf",(int(y_dimension * 0.13)))
            image = NeueBold.render(self.label, True, (0,0,0))
            rectangle = image.get_rect(center = (x_dimension * self.x_pos, y_dimension * self.y_pos))
            screen.blit(image, rectangle)

    class button(text):
        def __init__(self, label, x_pos, y_pos, nxtpage):
            super().__init__(label, x_pos, y_pos)
            self.nxtpage = nxtpage
            self.base = 0.08
            self.max = 0.14
            self.pace = 0.6
            self.currentsize = self.base
            self.currentfont = "NeueMetanaNext-SemiBold.otf"
            self.colour = (0,0,0)

        def draw_button(self, deltatime, currentpage, events):
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
                self.currentsize += self.pace * deltatime
                self.currentsize = min(self.currentsize, goal)
            elif self.currentsize > goal:
                self.currentsize -= self.pace * deltatime
                self.currentsize = max(self.currentsize, goal)
            currenttext = pg.font.Font(self.currentfont ,(int(y_dimension * self.currentsize)))
            image = currenttext.render(self.label, True, self.colour)
            rectangle = image.get_rect(center = (x_dimension * self.x_pos, y_dimension * self.y_pos))
            screen.blit(image, rectangle)
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and hover:
                    return self.nxtpage
            return currentpage

    async def testpage():
        screen.fill((215, 0, 64))
        TEST = text("TEST", 0.4, 0.08)
        TEST.draw_title()
        return "test"

    async def homepage(deltatime, CREATE, JOIN, events):
        screen.fill((215, 0, 64))
        currentpage = "home"

        UNO = text("UNO", 0.5, 0.1)

        currentpage = JOIN.draw_button(deltatime, currentpage, events)
        currentpage = CREATE.draw_button(deltatime, currentpage, events)
        UNO.draw_title()
        #use if statements here to select what to return
        return currentpage

    async def gameloop():
        playing = True #Boolean for controlling game loop
        currentpage = "home"
        CREATE = button("CREATE", 0.5, 0.4, "test")
        JOIN = button("JOIN", 0.5, 0.6, "test")
        fps = pg.time.Clock()
        while playing:
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    playing = False #when the user presses the X button on the tab, this will end the game loop and close the program
            deltatime = fps.tick(60)/1000   #limits framerate to 60 fps as well as returning time elapsed (in seconds) since the previous frame

            if currentpage == "home":
                currentpage = await homepage(deltatime, CREATE, JOIN, events)
            if currentpage == "test":
                currentpage = await testpage()
            pg.display.flip()

    await gameloop()
asyncio.run(main())
