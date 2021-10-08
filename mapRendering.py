import pygame
pygame.font.init()


class MapRenderer:
    def __init__(self, screen, parent_ref):
        self.screen = screen
        self.parent_ref = parent_ref
        self.rect_size = 20

    def render_field(self, field, color):
        if field.type == 1:
            pygame.draw.rect(self.screen, [0, 200, 0], [field.x * self.rect_size, field.y * self.rect_size, self.rect_size, self.rect_size])
        else:
            pygame.draw.rect(self.screen, color,
                             [field.x * self.rect_size, field.y * self.rect_size, self.rect_size, self.rect_size])
        pygame.draw.rect(self.screen, [0, 0, 0], [field.x * self.rect_size, field.y * self.rect_size, self.rect_size, self.rect_size], 1)

        if field.type == 1:
            self.text(field.group_id, (field.x * self.rect_size) + self.rect_size / 2 - 5,
                      (field.y * self.rect_size) + self.rect_size / 2 - 4, font=pygame.font.Font('freesansbold.ttf', 8),
                      color=[200, 200, 200])

    def draw_map_raw(self):
        for field in self.parent_ref.mapContainer.map_dict.values():
            self.render_field(field, [int(field.value*254), 0, 0])

    def draw_map_types(self):
        for field in self.parent_ref.mapContainer.map_dict.values():
            if field.type == 1:
                self.render_field(field, [200, 0, 0])
            else:
                self.render_field(field, [0, 0, 0])

    def text(self, message, x, y, font=pygame.font.Font('freesansbold.ttf', 32), color=None):
        if color is None:
            color = [0, 0, 0]
        self.screen.blit(font.render(str(message), 1, color), [x, y])