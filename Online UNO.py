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
            print("ouu shi")
    async def homepage():
        print("yooo")

    async def gameloop():
        playing = True #Boolean for controlling game loop
        currentpage = "home"
        while playing:
            screen.fill((215, 0, 64))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False #when the user presses the X button on the tab, this will end the game loop and close the program
            pg.time.Clock().tick(60)   #limits framerate to 60 fps

            if currentpage == "home":
                await homepage()
            pg.display.flip()

    await gameloop()
asyncio.run(main())
