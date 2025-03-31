import pygame
import random
from setting import WIDTH, HEIGHT, image_folder  # Import các hằng số cần thiết
from powerup import PowerUp  # Import lớp PowerUp để thả vật phẩm
import os.path as path

class Airplane(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(path.join(image_folder, "airplane.png")).convert_alpha()  # Hình ảnh máy bay
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width  # Máy bay bắt đầu từ ngoài màn hình bên trái
        self.rect.y = random.randint(50, HEIGHT // 2)  # Vị trí y ngẫu nhiên
        self.speed = 100  # Tốc độ bay của máy bay
        self.items_dropped = 0  # Số vật phẩm đã thả
#     
      #  self.changing_time = self.clock.tick(FPS) / 1000
    def update(self):
     self.rect.x += self.speed * self.game.changing_time  # Máy bay di chuyển sang phải
     if self.rect.left > WIDTH:  # Nếu máy bay ra khỏi màn hình
        self.kill()  # Xóa máy bay khỏi nhóm sprite
        return

    # Thả vật phẩm tại một vị trí ngẫu nhiên
     if self.items_dropped < 5 and random.random() < 0.01:  # Xác suất thả vật phẩm
        self.drop_item()

    def drop_item(self):
        x = self.rect.centerx
        y = self.rect.bottom
        item = PowerUp(self.game, x, y)  # Tạo vật phẩm
        self.game.all_sprites.add(item)  # Thêm vật phẩm vào nhóm all_sprites
        self.items_dropped += 1  # Tăng số vật phẩm đã thả