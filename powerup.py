import pygame
from setting import image_folder, WHITE
import os.path as path

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Kiểm tra và tải hình ảnh
        try:
            self.image = pygame.image.load(path.join(image_folder, "powerup.png")).convert_alpha()
        except pygame.error as e:
            print(f"Không thể tải hình ảnh powerup.png: {e}")
            self.image = pygame.Surface((32, 32))  # Tạo hình ảnh tạm thời
            self.image.fill((255, 0, 0))  # Đặt màu đỏ để dễ nhận biết lỗi

        # Thay đổi kích thước hình ảnh
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        # Kiểm tra va chạm với người chơi
        for player in self.game.PLAYER:
            if self.rect.colliderect(player.rect):  # Kiểm tra va chạm
                self.apply_effect(player)
                self.kill()  # Xóa vật phẩm sau khi nhặt

    def apply_effect(self, player):
     if hasattr(player, 'damage') and hasattr(player, 'bullet_speed'):
        player.damage += 10  # Tăng sát thương thêm 10
        player.bullet_speed += 20  # Tăng tốc độ đạn thêm 20
        print(f"{player} đã tăng sát thương lên {player.damage} và tốc độ đạn lên {player.bullet_speed}!")
     else:
        print(f"{player} không hỗ trợ tăng sát thương hoặc tốc độ đạn.")

    def update(self):
    # Kiểm tra va chạm với người chơi
     for player in self.game.PLAYER:  # Duyệt qua danh sách người chơi
        if self.rect.colliderect(player.rect):  # Kiểm tra va chạm
            self.apply_effect(player)
            self.kill()  # Xóa vật phẩm sau khi nhặt

    def apply_effect(self, player):
     if hasattr(player, 'increase_damage'):  # Kiểm tra nếu player có phương thức increase_damage
        player.increase_damage(20)  # Tăng sát thương lên 20
        print(f"{player} đã tăng sát thương! Sát thương hiện tại: {player.damage}")
     else:
        print(f"{player} không hỗ trợ tăng sát thương.")