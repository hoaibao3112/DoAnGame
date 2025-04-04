import pygame

class Button:
    def __init__(self, screen, x, y, width, height, color, border_color, border_width, text, sound=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color 
        self.border_width = border_width
        self.text = text
        self.sound = sound  # Thêm âm thanh vào nút nếu có

    def draw(self):
        pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)
        pygame.draw.rect(self.screen, self.color, (self.x + self.border_width, self.y + self.border_width,
                                                   self.width - self.border_width * 2, self.height - self.border_width * 2))
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        """Kiểm tra xem chuột có click vào nút không"""
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            if self.sound:
                self.sound.play()  # Phát âm thanh khi nhấn nút
            return True
        return False

class button_setting: # class nút setting
    def __init__(self, screen,  x, y, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = pygame.image.load(r'img/setting.png')
        self.image = pygame.transform.scale(
            self.image, (100, 100))  # Chỉnh kích thước hình ảnh nếu cần
        # Hiển thị ở góc trên cùng bên phải
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
