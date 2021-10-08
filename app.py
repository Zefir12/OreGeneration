import pygame
from mapRendering import MapRenderer
from mapCreator import *


pygame.init()
pygame.font.init()


# main gen settings
map_resolution = 3.5  # lower values makes
min_group_size = 5  # groups with lower field counts are removed
perlin_noise_threshold = 0.65

# press "k" to thicken

# if set to 1 entire group will thicken, if its set to 0.5 every block has 50% chance to spawn neighbour
random_spawn_chance_thickening = 0.3


class Game:
    def __init__(self):
        self.running = True
        self.events = pygame.event.get()
        self.clock = pygame.time.Clock()
        self.screen_size = [900, 900]
        self.screen = pygame.display.set_mode([900, 900])
        self.background_color = [90, 90, 90]
        self.mapContainer: MapContainer = MapContainer(40, 40)
        self.mapGen: MapGen = MapGen(perlin_noise_threshold, min_group_size, map_resolution, random_spawn_chance_thickening)
        self.mapRenderer: MapRenderer = MapRenderer(self.screen, self)
        self.initialization()

    def initialization(self):
        self.mapContainer = self.mapGen.create_map_first_pass(self.mapContainer)
        self.mapContainer = self.mapGen.second_pass(self.mapContainer)
        self.mapContainer = self.mapGen.third_pass(self.mapContainer)
        self.mapContainer = self.mapGen.group_pass(self.mapContainer)


    def handle_events(self):
        self.events = pygame.event.get()
        for evt in self.events:
            if evt.type == pygame.QUIT:
                sys.exit(0)
            if evt.type == pygame.KEYDOWN:
                if evt.key == 108:
                    self.mapContainer: MapContainer = MapContainer(40, 40)
                    self.mapGen: MapGen = MapGen(perlin_noise_threshold, min_group_size, map_resolution,
                                                 random_spawn_chance_thickening)

                    self.initialization()
                if evt.key == 107:
                    self.mapContainer = self.mapGen.thickening_pass(self.mapContainer)

    def text(self, message, x, y, font=pygame.font.Font('freesansbold.ttf', 32), color=None):
        if color is None:
            color = [0, 0, 0]
        self.screen.blit(font.render(str(message), 1, color), [x, y])

    def main_loop(self):
        while self.running:
            self.handle_events()
            pygame.Surface.fill(self.screen, self.background_color)

            #self.text('lmao', 400, 400)

            self.mapRenderer.draw_map_types()
            self.mapRenderer.draw_map_raw()

            pygame.display.update()


game = Game()
game.main_loop()
