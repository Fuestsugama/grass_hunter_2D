import pygame, sys, os, asyncio

# run from this file's folder so the ../assets paths always work
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from settings import WIDTH, HEIGHT, FPS, WATER_COLOR
from level import Level
from sound import load_sound

class Game: 
    """Creates the window, runs the main loop, and handles the quit, menu and restart keys."""
    def __init__(self):

        # general setup 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GrassHunter')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # sounds 
        self.main_sound = load_sound('../assets/audio/main.ogg', 0.5)
        self.main_sound.play(loops = -1)

    async def run(self):
        """Main loop: handle events, then update and draw the level, 60 times per second."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m and not self.level.game_over:
                        self.level.toggle_menu()
                    if event.key == pygame.K_r and self.level.game_over:
                        pygame.mixer.stop()                  # stops the game over music
                        self.level = Level()
                        self.main_sound.play(loops = -1)     # main music starts again

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)   # gives control back to the browser every frame (web version)

async def main():
    game = Game()
    await game.run()

if __name__ == '__main__':
    asyncio.run(main())



