from os import path
import pygame
import random


vector = pygame.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (120, 120, 120)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (120, 104, 82)
BLUE = (0, 0, 255)
SILVER = (192, 192, 192)
DARK_SEA_GREEN = (211, 211, 211)

WIDTH = 1280
HEIGHT = 800
FPS = 60
TITLE = 'TANK TROUBLE'
LIGHT_BLUE = (173, 216, 230)  # Xanh nhạt
LIGHT_YELLOW = (255, 255, 204)  # Vàng nhạt
OFF_WHITE = (255, 250, 240)  # Vàng trắng
RANDOM_COLORS = [LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE]
TANKS = {
    "Basic Tank": {"cost": 500, "image": "tank1.png"},
    "Armor Tank": {"cost": 1000, "image": "tank2.png"},
    "Speed Tank": {"cost": 800, "image": "tank3.png"},
    "Heavy Tank": {"cost": 1500, "image": "tank7.png"},
    "Sniper Tank": {"cost": 1200, "image": "tank8.png"},
    "Flame Tank": {"cost": 1800, "image": "tank6.png"}
}
SQSIZE = 32  # KÍCH THƯỚC 1 Ô LƯỚI TRONG GAME
GRIDWIDTH = WIDTH/SQSIZE  # SỐ Ô THEO CHIỀU RỘNG
GRIDHEIGHT = HEIGHT/SQSIZE  # SỐ Ô THEO CHIỀU CAO

playerSpeed = 75 # tốc độ di chuyển của player

WALL_IMAGE = 'dirt.png'  # hình tường
PLAYER_IMAGE1 = 'tank1.png'
PLAYER_IMAGE3 = 'tank1.png' # hình player1
PLAYER_IMAGE2 = 'tank2.jpg'  # hình player2
folder_of_game = path.dirname(__file__) # tạo đường dẫn đến thư mục chứa tệp chỉ định
image_folder = path.join(folder_of_game, 'img') # kết hợp thành đường dẫn đến thư mục img trong folder chứa tệp đang chạy
BULLET_IMAGE = path.join(image_folder, 'BULLET.png')
ZOMBIE_IMAGE = 'zombie.png'  # hình zombie
BOSS_IMAGE = 'boss.png'  # hình boss

player_box = pygame.Rect(0, 0, 32, 32)
bullet_box = pygame.Rect(0, 0, 10, 10)
# Tạo danh sách hình ảnh tường có sẵn
WALL_IMAGES = ['wall1.png', 'wall2.png', 'wall3.png', 'wall5.png']

# Chọn ngẫu nhiên một hình ảnh làm tường
WALL_IMAGE = random.choice(WALL_IMAGES)
# shooting setting
bulletSpeed = 200 # tốc độ đạn
bullet_rate = 1 # khoảng cách bắn 1 viên đạn là 1 giây
turret = vector(0, 30)  # vị trí đạn xuất hiện


folder_of_game = path.dirname(__file__) # tạo đường dẫn đến thư mục chứa tệp chỉ định
image_folder = path.join(folder_of_game, 'img') # kết hợp thành đường dẫn đến thư mục img trong folder chứa tệp đang chạy
maze_forder = path.join(folder_of_game, 'MAZEFOLDER') # kết hợp thành đường dẫn đến thư mục MAZEFOLDER trong folder chứa tệp đang chạy


def getImage(image, color):  # trả về hình tank
    player_image = pygame.image.load(path.join(image_folder, image)).convert()
    player_image.set_colorkey(color)
    return player_image


def getListImage(str_image, width, height, color, numbers):  # lấy danh sách ảnh của cảnh động
    list_image = []
    for i in range(numbers):
        image = pygame.image.load(
            path.join(image_folder, str_image+str(i)+'.png'))
        image = pygame.transform.scale(image, (width, height))
        image.set_colorkey(color)
        list_image.append(image)
    return list_image


def check_btn_click(mouse_pos, button): # kiểm tra xem chuột có click vào nút không
    return button.x <= mouse_pos[0] <= button.x + button.width and button.y <= mouse_pos[1] <= button.y + button.height
pygame.mixer.init()
# Define the folder containing sounds
sound_folder = path.join(path.dirname(__file__), 'sounds')

# Load sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_folder, 'TiengSung.wav'))  # Shooting sound
# Âm thanh khi bắn trúng Zombie
zombie_hit_sound = pygame.mixer.Sound(path.join(sound_folder, 'VuNo.wav'))
zombie_hit_sound.set_volume(0.5)  # Điều chỉnh âm lượng
button_click_sound = pygame.mixer.Sound(path.join(sound_folder, 'An.wav'))
button_click_sound.set_volume(0.5)  # Điều chỉnh âm lượng nếu cần
# Adjust volume if needed
shoot_sound.set_volume(0.5)
bg_music = pygame.mixer.Sound(path.join(sound_folder, 'NhacNen1.wav'))
bg_music.set_volume(0.3)  # Điều chỉnh âm lượng
game_over_sound = pygame.mixer.Sound(path.join(sound_folder, 'gameOver.wav'))
game_over_sound.set_volume(0.5)  # Điều chỉnh âm lượng
gold_pickup_sound = pygame.mixer.Sound(path.join(sound_folder, 'Vang.wav'))
gold_pickup_sound.set_volume(0.5)  # Điều chỉnh âm lượng nếu cần
