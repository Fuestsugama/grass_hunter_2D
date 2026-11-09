import pygame, sys, os

# run from this file's folder so the ../assets paths always work
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from settings import *
from level import Level

class Game: 
    def __init__(self):

        # general setup 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('GrassHunter')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # sounds 
        self.main_sound = pygame.mixer.Sound('../assets/audio/main.ogg')
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops = -1)

    def run(self):
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

if __name__ == '__main__':
    game = Game()
    game.run()



