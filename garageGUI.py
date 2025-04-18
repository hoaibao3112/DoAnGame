import pygame
import os
import json
from setting import TANKS
import time
# Tệp lưu dữ liệu
SAVE_FILE = "save_data.json"

# Tải dữ liệu từ file
def load_data():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"player_coins": 0, "garage_tanks": [], "selected_tank": None, "completed_wave": 0}
    
# Lưu dữ liệu vào file
def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

class GarageGUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("fonts/static/Roboto-BlackItalic.ttf", 32)
        self.running = True
        self.selected_index = 0
        self.image_folder = "img"
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.load_game_data()
        self.message = ""
        self.message_time = 0
        
        # Căn giữa các nút
        center_x = self.screen_width // 2
        button_spacing = 150
        self.button_sell = pygame.Rect(center_x - 100, 580, 200, 50)  # Dịch xuống 30px
        self.button_select = pygame.Rect(center_x - 100, 510, 200, 50)  # Dịch xuống 30px # Nút chọn xe
        self.button_next = pygame.Rect(center_x + button_spacing, 400, 80, 50)
        self.button_prev = pygame.Rect(center_x - button_spacing - 80, 400, 80, 50)
        self.button_exit = pygame.Rect(center_x - 100, 650, 200, 50)  # Dịch xuống 30px

    def load_game_data(self):
        global player_coins, garage_tanks, selected_tank
        data = load_data()
        player_coins = data["player_coins"]
        garage_tanks = data["garage_tanks"]
        selected_tank = data.get("selected_tank", None)

    def draw(self):
        self.screen.fill((255, 255, 255))

        title = self.font.render("KHO XE CỦA TÔI", True, (0, 0, 0))
        self.screen.blit(title, ((self.screen_width - title.get_width()) // 2, 50))

        coin_text = self.font.render(f"Tiền: {player_coins}", True, (0, 0, 0))
        self.screen.blit(coin_text, (20, 20))

        if not garage_tanks:
            empty_text = self.font.render("Không có xe nào!", True, (0, 0, 0))
            self.screen.blit(empty_text, ((self.screen_width - empty_text.get_width()) // 2, 200))
            pygame.display.flip()
            return

        tank_name = garage_tanks[self.selected_index]
        tank = TANKS[tank_name]
        price_text = self.font.render(f"Giá bán: {tank['cost'] // 2}", True, (0, 0, 0))
        self.screen.blit(price_text, ((self.screen_width - price_text.get_width()) // 2, 300))

        image_path = os.path.join(self.image_folder, tank["image"])
        tank_image = pygame.image.load(image_path)
        tank_image = pygame.transform.scale(tank_image, (200, 200))
        self.screen.blit(tank_image, ((self.screen_width - 200) // 2, 350))

        pygame.draw.rect(self.screen, (200, 0, 0), self.button_sell)
        pygame.draw.rect(self.screen, (0, 0, 200), self.button_select)  # Màu xanh dương
        pygame.draw.rect(self.screen, (200, 200, 200), self.button_next)
        pygame.draw.rect(self.screen, (200, 200, 200), self.button_prev)
        pygame.draw.rect(self.screen, (0, 200, 0), self.button_exit)

        sell_text = self.font.render("BÁN", True, (255, 255, 255))
        select_text = self.font.render("CHỌN XE", True, (255, 255, 255))
        next_text = self.font.render(">", True, (0, 0, 0))
        prev_text = self.font.render("<", True, (0, 0, 0))
        exit_text = self.font.render("THOÁT", True, (255, 255, 255))

        self.screen.blit(sell_text, (self.button_sell.x + 70, self.button_sell.y + 10))
        self.screen.blit(select_text, (self.button_select.x + 50, self.button_select.y + 10))
        self.screen.blit(next_text, (self.button_next.x + 30, self.button_next.y + 10))
        self.screen.blit(prev_text, (self.button_prev.x + 30, self.button_prev.y + 10))
        self.screen.blit(exit_text, (self.button_exit.x + 60, self.button_exit.y + 10))
        if self.message and time.time() - self.message_time < 3:
            message_text = self.font.render(self.message, True, (0, 200, 0))
            self.screen.blit(message_text, ((self.screen_width - message_text.get_width()) // 2, 700))
        else:
            self.message = ""
        pygame.display.flip()
    
    def run(self):
        global player_coins, garage_tanks, selected_tank
        self.load_game_data()

        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_data({"player_coins": player_coins, "garage_tanks": garage_tanks, "selected_tank": selected_tank})
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.button_next.collidepoint(mouse_pos) and garage_tanks:
                        self.selected_index = (self.selected_index + 1) % len(garage_tanks)
                    elif self.button_prev.collidepoint(mouse_pos) and garage_tanks:
                        self.selected_index = (self.selected_index - 1) % len(garage_tanks)
                    elif self.button_sell.collidepoint(mouse_pos) and garage_tanks:
                        self.sell_tank()
                    elif self.button_select.collidepoint(mouse_pos) and garage_tanks:
                        self.select_tank()
                    elif self.button_exit.collidepoint(mouse_pos):
                        save_data({"player_coins": player_coins, "garage_tanks": garage_tanks, "selected_tank": selected_tank})
                        self.running = False
    def sell_tank(self):
        global player_coins, garage_tanks, selected_tank
        if not garage_tanks:
            return

        tank_name = garage_tanks[self.selected_index]
        price = TANKS[tank_name]["cost"] // 2

        # Kiểm tra nếu xe đang chọn có bị bán không
        if selected_tank == tank_name:
            selected_tank = None

        # Xóa xe khỏi danh sách
        garage_tanks.pop(self.selected_index)
        player_coins += price

        # Cập nhật dữ liệu
        save_data({"player_coins": player_coins, "garage_tanks": garage_tanks, "selected_tank": selected_tank})

        # Điều chỉnh chỉ mục
        self.selected_index = max(0, self.selected_index - 1 if garage_tanks else 0)

        print(f"Đã bán {tank_name}, số tiền hiện tại: {player_coins}, danh sách xe còn lại: {garage_tanks}")

    def load_game_data(self):
        global player_coins, garage_tanks, selected_tank
        data = load_data()
        player_coins = data["player_coins"]
        garage_tanks = data["garage_tanks"]
        selected_tank = data.get("selected_tank", None)

    def select_tank(self):
        global selected_tank
        selected_tank = garage_tanks[self.selected_index]
        save_data({"player_coins": player_coins, "garage_tanks": garage_tanks, "selected_tank": selected_tank})
        self.message = f"Đã chọn xe {selected_tank} thành công để thi đấu!"
        self.message_time = time.time()
        print(f"Đã chọn xe: {selected_tank}")

