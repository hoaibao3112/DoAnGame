import pygame
import os
import json
import time
from setting import TANKS

# Tệp lưu dữ liệu
SAVE_FILE = "save_data.json"

def load_data():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            if "player_coins" not in data:
                data["player_coins"] = 0
            if "garage_tanks" not in data:
                data["garage_tanks"] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"player_coins": 0, "garage_tanks": []}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

class ShopGUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.running = True
        self.tank_list = list(TANKS.keys())
        self.selected_index = 0
        self.image_folder = "img"
        self.message = ""
        self.message_color = (0, 0, 0)
        self.message_time = 0
        
        # Canh giữa màn hình
        self.button_width = 200
        self.button_height = 50
        center_x = (self.screen.get_width() - self.button_width) // 2
        button_spacing = 120
        
        # Nút điều khiển
        self.button_buy = pygame.Rect(center_x, 500, self.button_width, self.button_height)
        self.button_next = pygame.Rect(center_x + button_spacing + 100, 400, 80, 50)
        self.button_prev = pygame.Rect(center_x - button_spacing, 400, 80, 50)
        self.button_exit = pygame.Rect(center_x, 600, self.button_width, self.button_height)

    def draw(self):
        self.screen.fill((255, 255, 255))
        
        title = self.font.render("CỬA HÀNG MUA XE", True, (0, 0, 0))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))
        
        coin_text = self.font.render(f"\U0001F4B0 Tiền: {data['player_coins']}", True, (0, 0, 0))
        self.screen.blit(coin_text, (20, 20))
        
        tank_name = self.tank_list[self.selected_index]
        tank = TANKS[tank_name]
        text = self.font.render(f"{tank_name} - \U0001F4B5 {tank['cost']}", True, (0, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 250))
        
        image_path = os.path.join(self.image_folder, tank["image"])
        tank_image = pygame.image.load(image_path)
        tank_image = pygame.transform.scale(tank_image, (150, 150))
        self.screen.blit(tank_image, (self.screen.get_width() // 2 - 75, 300))
        
        pygame.draw.rect(self.screen, (0, 200, 0), self.button_buy)
        pygame.draw.rect(self.screen, (200, 200, 200), self.button_next)
        pygame.draw.rect(self.screen, (200, 200, 200), self.button_prev)
        pygame.draw.rect(self.screen, (200, 0, 0), self.button_exit)
        
        buy_text = self.font.render("MUA", True, (255, 255, 255))
        next_text = self.font.render(">", True, (0, 0, 0))
        prev_text = self.font.render("<", True, (0, 0, 0))
        exit_text = self.font.render("THOÁT", True, (255, 255, 255))
        
        self.screen.blit(buy_text, (self.button_buy.x + 75, self.button_buy.y + 10))
        self.screen.blit(next_text, (self.button_next.x + 30, self.button_next.y + 10))
        self.screen.blit(prev_text, (self.button_prev.x + 30, self.button_prev.y + 10))
        self.screen.blit(exit_text, (self.button_exit.x + 60, self.button_exit.y + 10))
        
        if self.message and time.time() - self.message_time < 2.5:
            message_text = self.font.render(self.message, True, self.message_color)
            self.screen.blit(message_text, (self.screen.get_width() // 2 - message_text.get_width() // 2, 550))
        else:
            self.message = ""
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_data(data)
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_next.collidepoint(mouse_pos):
                        self.selected_index = (self.selected_index + 1) % len(self.tank_list)
                    elif self.button_prev.collidepoint(mouse_pos):
                        self.selected_index = (self.selected_index - 1) % len(self.tank_list)
                    elif self.button_buy.collidepoint(mouse_pos):
                        self.purchase_tank()
                    elif self.button_exit.collidepoint(mouse_pos):
                        save_data(data)
                        self.running = False

    def purchase_tank(self):
        tank_name = self.tank_list[self.selected_index]
        tank = TANKS[tank_name]

        if data["player_coins"] >= tank["cost"] and tank_name not in data["garage_tanks"]:
            data["player_coins"] -= tank["cost"]
            data["garage_tanks"].append(tank_name)
            save_data(data)
            print("Dữ liệu sau khi mua xe:", data)  # Kiểm tra dữ liệu sau khi mua

            self.message = f"Mua {tank_name} thành công!"
            self.message_color = (0, 200, 0)
        elif tank_name in data["garage_tanks"]:
            self.message = "Xe đã có trong kho!"
            self.message_color = (255, 165, 0)
        else:
            self.message = "Không đủ tiền!"
            self.message_color = (200, 0, 0)
        
        self.message_time = time.time()
