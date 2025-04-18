import pygame
import random
import json
import os
from sprites import Gold 
from setting import gold_pickup_sound
class GoldDropManager:
    def __init__(self, game):
        self.game = game
        self.gold_list = []  # Danh sách vàng rơi
        self.gold_drop_rate = 0.2  # Xác suất rơi vàng khi tiêu diệt quái vật (20%)

    def drop_gold(self, x, y):
        """Tạo vàng tại vị trí (x, y) nếu điều kiện rơi vàng được thỏa mãn."""
        if random.random() < self.gold_drop_rate:
            gold = Gold(x, y)
            self.gold_list.append(gold)
            self.game.all_sprites.add(gold)
            print(f"Vàng xuất hiện tại ({x}, {y})")

    def check_gold_pickup(self):
        """Kiểm tra xem người chơi có nhặt vàng không."""
        player = self.game.player1  # Lấy đối tượng người chơi
        for gold in self.gold_list[:]:  # Duyệt qua danh sách vàng
            if player.rect.colliderect(gold.rect):  # Kiểm tra va chạm
                gold_pickup_sound.play() 
                self.add_gold_to_save_data(gold.amount)  # Cộng tiền vào file JSON
                self.gold_list.remove(gold)  # Xóa vàng khỏi danh sách
                gold.kill()  # Xóa vàng khỏi màn hình
                print(f"Người chơi đã nhặt {gold.amount} vàng!")

    def add_gold_to_save_data(self, amount):
        """Cập nhật số vàng vào trường player_coins trong file save_data.json."""
        save_path = os.path.join(os.path.dirname(__file__), "save_data.json")  # Đường dẫn tuyệt đối
        print(f"Đường dẫn file: {save_path}")  # Debug

        try:
            with open(save_path, "r") as f:
                data = json.load(f)
                print(f"Dữ liệu hiện tại: {data}")  # Debug
        except (FileNotFoundError, json.JSONDecodeError):
            print("File không tồn tại hoặc không hợp lệ. Tạo dữ liệu mặc định.")  # Debug
            data = {
                "player_coins": 0,
                "garage_tanks": [],
                "selected_tank": "",
                "completed_wave": 0,
            }

        # Cộng số vàng vào player_coins
        data["player_coins"] = data.get("player_coins", 0) + amount

        with open(save_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Người chơi nhận được {amount} vàng! Tổng tiền: {data['player_coins']}")