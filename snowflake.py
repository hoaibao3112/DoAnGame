import pygame
import random
from setting import WHITE

class Snowflake(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((random.randint(2, 5), random.randint(2, 5)))  # Kích thước ngẫu nhiên
        self.image.fill(WHITE)  # Màu trắng cho bông tuyết
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)  # Vị trí x ngẫu nhiên
        self.rect.y = random.randint(-50, screen_height)  # Vị trí y ngẫu nhiên (bên trên màn hình)
        self.speed = random.uniform(1, 3)  # Tốc độ rơi ngẫu nhiên

    def update(self):
        self.rect.y += self.speed  # Di chuyển bông tuyết xuống dưới
        if self.rect.y > self.screen_height:  # Nếu bông tuyết rơi khỏi màn hình
            self.rect.y = random.randint(-50, -10)  # Đưa bông tuyết trở lại phía trên
            self.rect.x = random.randint(0, self.screen_width)  # Đặt lại vị trí x