import random
import pygame
import sys
import json
import os
from Button import button_setting
from auto_respawn import *
from gameOverGUI import gameOverGUI
from pauseGUI import pauseGUI
from setting import *
from show_kill import show_kill
from sprites import *
from wave_cleared_GUI import WaveClearedGUI
from garageGUI import load_data
from gold_drop import GoldDropManager
from snowflake import Snowflake
from Airplane import Airplane
from vuot_man_GUI import vuot_man_GUI
class game:
    def __init__(self,screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        self.gold_list = []
        pygame.display.set_caption(TITLE)
        self.data()
        self.AddedItems()
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)  # Chọn font mặc định, cỡ 36
        self.gold_amount = 0  # Khởi tạo số vàng
        self.bg_color = random.choice(RANDOM_COLORS)  # Chọn màu nền ngẫu nhiên
        self.PLAYER = []  # Khởi tạo danh sách người chơi
         # Hiệu ứng tuyết rơi
        self.snowflakes = pygame.sprite.Group()
        if self.bg_color == LIGHT_BLUE:  # Nếu màu nền là LIGHT_BLUE
            for _ in range(100):  # Tạo 100 bông tuyết
                snowflake = Snowflake(WIDTH, HEIGHT)
                self.snowflakes.add(snowflake)
                
    def update(self):
        super().update()
        self.gold_manager.check_gold_pickup()  # Kiểm tra nhặt vàng
        
    def data(self):
        self.maze = []  # ma trận
        i=random.randint(1,5) # chọn ngẫu nhiên 1 trong 5 ma trận 
        with open(path.join(maze_forder, 'MAZE{}.txt'.format(i)),'rt') as f:  # đọc ma trận từ file
            for line in f:
                self.maze.append(line.strip())
        self.pausing = False
        self.playing = True
        self.respawn = auto_respawn_tank(self, 3)
        
        
    def spawn_gold(self, position, amount):
        self.gold_list.append(Gold(self, position, amount))
    
    def check_collect_gold(self, player):
        for gold in self.gold_list:
            if player.rect.colliderect(gold.rect):
                player.money += gold.amount  # Cộng tiền ngay vào ví
                self.gold_list.remove(gold)
                self.update_save_data()  # Cập nhật file save

        
    def AddedItems(self): #thêm giao diện vào game
        self.btn_setting=button_setting(self.screen, WIDTH - 75, -20, 100, 100)
        self.pause_screen = pauseGUI(self.screen)
        self.show_kill_player1 = show_kill(self.screen, "left") 
    
    def run(self):  # hàm này để chạy các chế độ game
        self.playing = True
        while self.playing:
            self.pausing=False
            while self.pausing == False:
                self.changing_time = self.clock.tick(FPS) / 1000 # tính thời gian trôi qua kể từ lần gọi cuối cùng(giây)
                self.events()  
                self.update()  # hàm này gọi tất cả hàm update của các sprites
                self.update_draw()
                self.auto_respawn()
                self.pause_game()
                  

    def pause_game(self): #hàm dừng game
        if self.pausing == True: #nếu bấm nút setting thì dừng game
            self.pause_screen.run() #hiển thị màn hình pause
            self.clock.tick(FPS) #đặt lại thời gian
            self.check_pause_events(self.pause_screen) #kiểm tra sự kiện của màn hình pause

    def auto_respawn(self):
        pass

    def new(self):  # hàm khởi tạo lại tất cả nhóm sprites và các đối tượng, chỉ số
        PLAYER.clear() #xóa tất cả các player
        ENEMY.clear() #xóa tất cả các enemy
        GameStatistics.reset_kill() #reset lại số lần giết
        GameStatistics.reset_death_time() #reset lại thời gian chết
        GameStatistics.reset_bullet() #reset thuộc tính đạn
        self.all_sprites = pygame.sprite.Group() #tạo nhóm tất cả các sprites
        self.bullets = pygame.sprite.Group() #tạo nhóm đạn
        self.walls = pygame.sprite.Group()  # tạo nhóm tường
    
    def grid(self):
        for x in range(0, WIDTH, SQSIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, SQSIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw(self): #vẽ các đối tượng lên màn hình
        self.screen.fill(self.bg_color)  # Sử dụng màu nền đã chọn
        # self.grid() #vẽ lưới
        self.all_sprites.draw(self.screen) #vẽ tất cả các sprites
        self.btn_setting.draw() #vẽ nút setting
        self.show_kill_player1.draw(GameStatistics.number_kill_player1,BLUE) #vẽ số lần giết của player1
         # Hiển thị bộ đếm thời gian
        font = pygame.font.SysFont(None, 40)
        elapsed_time = self.get_elapsed_time()
        time_text = font.render(f"Time: {elapsed_time}s", True, (255, 0, 0))
        self.screen.blit(time_text, (WIDTH // 2 - 50, 20))  # Đặt vị trí hiển thị
        # Vẽ hiệu ứng tuyết rơi
        if self.bg_color == LIGHT_BLUE:
            self.snowflakes.draw(self.screen)
        
    def update_draw(self): #cập nhật và vẽ các đối tượng
        self.draw() 
        pygame.display.flip() #cập nhật màn hình

    def update(self): #cập nhật tất cả các sprites
        self.all_sprites.update()
        if self.bg_color == LIGHT_BLUE:
            self.snowflakes.update()  # Cập nhật vị trí của các bông tuyết

    def check_pause_events(self,pause_screen): #kiểm tra sự kiện của màn hình pause
        if pause_screen == None or pause_screen.action == None: 
            return
        if pause_screen.action == 1: #tiếp tục
            return
        if pause_screen.action == 0: #thoát
            self.playing = False
        if pause_screen.action == 2: #restart
            self.new()
            pause_screen.action = None

    def events(self): #kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.btn_setting):
                    self.pausing =True
                    
    def quit(self):
        pygame.quit()
        quit()
    def get_elapsed_time(self):
     return (pygame.time.get_ticks() - self.start_time) // 1000  # Chuyển từ milliseconds sang giây

class mode_training(game): #chế độ huấn luyện
    def __init__(self,screen):
        super().__init__(screen)
        self.new()
        self.run()

    def new(self):
     super().new()
     global WALL_IMAGE  
     WALL_IMAGE = random.choice(WALL_IMAGES)  # Chọn hình ảnh tường ngẫu nhiên

     for row, tiles in enumerate(self.maze):
        for col, tile in enumerate(tiles):
            if tile == '1':
                wall(self, col, row)  # Tạo tường với hình ảnh đã chọn
            elif tile == '*':
                self.player1 = Player1(self, col, row)  # Tạo player1
            elif tile == '-':
                self.enemy = TankEnemy(self, col, row)  # Tạo enemy
    def auto_respawn(self): #hồi sinh
        self.respawn.respawn_player1()
        self.respawn.respawn_TankEnemy()

    def AddedItems(self):
        super().AddedItems()
        self.show_kill_player2 = show_kill(self.screen, "right") #hiển thị số lần giết của player2
    
    def draw(self):
        super().draw()
        self.show_kill_player2.draw(GameStatistics.number_kill_player2,RED) #vẽ số lần giết của player2

class mode_1v1(game):  # Chế độ 1v1
    def __init__(self, screen):
        super().__init__(screen)
        self.last_airplane_time = 0  # Thời gian lần cuối máy bay xuất hiện
        self.airplane_count = 0 
        self.spawn_airplane# Đếm số lần máy bay xuất hiện
        self.new()
        self.run()
    def spawn_airplane(self):
     current_time = pygame.time.get_ticks() / 1000  # Lấy thời gian hiện tại (giây)
     if self.airplane_count < 2 and current_time - self.last_airplane_time > 10:  # Máy bay xuất hiện mỗi 10 giây
        airplane = Airplane(self)
        self.all_sprites.add(airplane)  # Thêm máy bay vào nhóm all_sprites
        self.last_airplane_time = current_time
        self.airplane_count += 1  # Tăng số lần máy bay xuất hiện
        
        
    def show_game_over(self, losing_player):
        self.pausing = True
        font = pygame.font.SysFont(None, 80)
        if losing_player == "Player 1":
            text = font.render("Player 2 Wins!", True, BLUE)
        else:
            text = font.render("Player 1 Wins!", True, RED)

        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Dừng màn hình trong 3 giây
        self.playing = False  # Kết thúc trò chơi
        
    def addEvents(self):
     self.action = None
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.continue_Button.rect.collidepoint(mouse_pos):
                self.action = 1  # Tiếp tục
            elif self.exit_button.rect.collidepoint(mouse_pos):
                self.action = 0  # Thoát
            elif self.restart_button_Setting.rect.collidepoint(mouse_pos):
                self.action = 2  # Restart
    def new(self):
        super().new()
        if not hasattr(self, 'PLAYER'):  # Kiểm tra nếu thuộc tính chưa được khởi tạo
            self.PLAYER = []
        # Tăng thời gian giữa các lần bắn chỉ trong chế độ 1v1
        GameStatistics.bulletRate = 3 # Thời gian giữa các lần bắn là 1.5 giây
        # Khởi tạo người chơi và tường
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':  # Nếu ô là tường
                    wall(self, col, row)  # Tạo đối tượng tường
                if tile == '*':  # Người chơi 1
                    player1 = Player1_1v1(self, col, row)
                    self.PLAYER.append(player1)  # Thêm người chơi vào danh sách
                if tile == '-':  # Người chơi 2
                    player2 = Player2_1v1(self, col, row)
                    self.PLAYER.append(player2)  # Thêm người chơi vào danh sách
    def pause_game(self):
        if self.pausing:  # Nếu trò chơi đang tạm dừng
            self.pause_screen.run()  # Hiển thị màn hình tạm dừng
            self.clock.tick(FPS)  # Đặt lại thời gian
            self.check_pause_events(self.pause_screen)  # Kiểm tra sự kiện của màn hình tạm dừng
    def events(self):
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if check_btn_click(mouse_pos, self.btn_setting):  # Kiểm tra nếu nhấn nút tạm dừng
                self.pausing = True
    def check_pause_events(self, pause_screen):
        if pause_screen is None or pause_screen.action is None:
            return
        if pause_screen.action == 1:  # Tiếp tục
            self.pausing = False
        elif pause_screen.action == 0:  # Thoát
            self.playing = False
        elif pause_screen.action == 2:  # Chơi lại
            self.new()
            pause_screen.action = None       
    def update(self):
        super().update()
        self.spawn_airplane()
        self.all_sprites.update()  # Cập nhật tất cả các sprite# Gọi phương thức tạo máy bay
    def draw_health_bar(self, x, y, health, max_health, color):
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        fill = (health / max_health) * BAR_WIDTH
        outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, color, fill_rect)
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)  # Viền trắng

    def check_bullet_collision(self):
     for bullet in self.game.bullets:
        for player in self.game.PLAYER:
            if bullet.rect.colliderect(player.rect):  # Kiểm tra va chạm giữa đạn và người chơi
                # Đảm bảo đạn của Player1 không gây sát thương lên chính Player1 và ngược lại
                if (bullet.type == 'player1' and isinstance(player, Player2_1v1)) or \
                   (bullet.type == 'player2' and isinstance(player, Player1_1v1)):
                    player.take_damage(bullet.damage)  # Giảm máu của người chơi
                    bullet.kill()  # Xóa đạn sau khi va chạm
    def draw(self):
     self.screen.fill(self.bg_color)  # Làm mới màn hình
     self.all_sprites.draw(self.screen)  # Vẽ tất cả các sprite
     self.btn_setting.draw()  # Vẽ nút tạm dừng
     pygame.display.flip()  # Cập nhật màn hình
     if len(self.PLAYER) > 0:
        self.draw_health_bar(50, 50, self.PLAYER[0].health, 1000, RED)

    # Hiển thị thanh máu của Player2
     if len(self.PLAYER) > 1:
        self.draw_health_bar(WIDTH - 250, 50, self.PLAYER[1].health, 1000, BLUE)

        pygame.display.flip()  # Cập nhật màn hình
    def draw_health_bar(self, x, y, health, max_health, color):
     BAR_WIDTH = 200  # Chiều rộng thanh máu
     BAR_HEIGHT = 20  # Chiều cao thanh máu
     fill = (health / max_health) * BAR_WIDTH  # Tính phần trăm máu còn lại
     outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)  # Viền thanh máu
     fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)  # Phần máu còn lại
     pygame.draw.rect(self.screen, color, fill_rect)  # Vẽ phần máu
     pygame.draw.rect(self.screen, WHITE, outline_rect, 2)  # Vẽ viền trắng
class Player1_1v1(Player1):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.health = 1000  # Máu ban đầu
        self.damage = 20  # Sát thương ban đầu (thấp)
        self.bullet_speed = 50  # Tốc độ đạn ban đầu (chậm)

    def take_damage(self, amount):
        self.health -= amount  # Giảm máu
        if self.health <= 0:  # Nếu máu <= 0
            self.health = 0  # Đảm bảo máu không âm
            self.game.show_game_over("Player 2")  # Hiển thị thông báo Player 2 thắng


    def update(self):
        self.collide_with_bullet1vs1()  # Kiểm tra va chạm với đạn
        self.shoot()  # Gọi phương thức bắn đạn
        super().update()  # Gọi update của lớp cha


    def shoot(self):
     if self.is_shoot:
        self.last_fire += self.game.changing_time
        if self.last_fire > GameStatistics.bulletRate:  # Kiểm tra thời gian giữa các lần bắn
            self.last_fire = 0
            direction = vector(0, 1).rotate(-self.rot).normalize()
            position = self.position + turret.rotate(-self.rot)
            Bullet_1vs1(self.game, position.x, position.y, direction, 'player1', self.damage, self.bullet_speed)
            shoot_sound.play()  # Phát âm thanh bắn súng

    def collide_with_bullet1vs1(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.hit_rect):  # Kiểm tra va chạm giữa đạn và người chơi
                if bullet.type != 'player1':  # Đảm bảo đạn không phải của chính người chơi
                    Explosion(self.game, self.rect.center)  # Tạo vụ nổ tại vị trí xe
                    self.take_damage(bullet.damage)  # Giảm máu
                    bullet.kill()  # Xóa đạn


class Player2_1v1(Player2):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.health = 1000  # Máu ban đầu
        self.damage = 20  # Sát thương ban đầu (thấp)
        self.bullet_speed = 50  # Tốc độ đạn ban đầu (chậm)
    def take_damage(self, amount):
        self.health -= amount  # Giảm máu
        if self.health <= 0:  # Nếu máu <= 0
            self.health = 0  # Đảm bảo máu không âm
            self.game.show_game_over("Player 1")  # Hiển thị thông báo Player 1 thắng
    def shoot(self):
     if self.is_shoot:
        self.last_fire += self.game.changing_time
        if self.last_fire > GameStatistics.bulletRate:  # Kiểm tra thời gian giữa các lần bắn
            self.last_fire = 0
            direction = vector(0, 1).rotate(-self.rot).normalize()
            position = self.position + turret.rotate(-self.rot)
            Bullet_1vs1(self.game, position.x, position.y, direction, 'player2', self.damage, self.bullet_speed)
            shoot_sound.play()  # Phát âm thanh bắn súng
               
    def collide_with_bullet1vs1(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.hit_rect):  # Kiểm tra va chạm giữa đạn và người chơi
                if bullet.type != 'player2':  # Đảm bảo đạn không phải của chính người chơi
                    Explosion(self.game, self.rect.center)  # Tạo vụ nổ tại vị trí xe
                    self.take_damage(bullet.damage)  # Giảm máu
                    bullet.kill()  # Xóa đạn
    def draw_health_bar(self, x, y, health, max_health, color):
      BAR_WIDTH = 200
      BAR_HEIGHT = 20
      fill = (health / max_health) * BAR_WIDTH
      outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
      fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
      pygame.draw.rect(self.screen, color, fill_rect)
      pygame.draw.rect(self.screen, WHITE, outline_rect, 2)  # Viền trắng
      
     
    def update(self):
        self.collide_with_bullet1vs1()  # Kiểm tra va chạm với đạn
        self.shoot()  # Gọi phương thức bắn đạn
        super().update()  # Gọi update của lớp cha
    def shoot(self):
     if self.is_shoot:
        self.last_fire += self.game.changing_time
        if self.last_fire > GameStatistics.bulletRate:  # Kiểm tra thời gian giữa các lần bắn
            self.last_fire = 0
            direction = vector(0, 1).rotate(-self.rot).normalize()
            position = self.position + turret.rotate(-self.rot)
            Bullet_1vs1(self.game, position.x, position.y, direction, 'player2', self.damage, self.bullet_speed)
            shoot_sound.play()  # Phát âm thanh bắn súng
               
class Bullet_1vs1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction, bullet_type, damage, speed):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        self.image = pygame.image.load(BULLET_IMAGE).convert_alpha()  # Tải hình ảnh viên đạn
        self.image.set_colorkey((255, 255, 255))  # Loại bỏ màu trắng (RGB: 255, 255, 255)
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)  # Sử dụng vector để lưu vị trí
        self.rect.center = self.position
        self.speed = speed  # Tốc độ đạn
        self.damage = damage  # Sát thương của đạn
        self.direction = direction
        self.type = bullet_type  # Loại đạn (player1, player2, enemy)


    def update(self):
        # Di chuyển đạn
        self.position += self.direction * self.speed * self.game.changing_time
        self.rect.center = self.position

        # Kiểm tra va chạm với tường
        if pygame.sprite.spritecollideany(self, self.game.walls):
            Explosion(self.game, self.rect.center)  # Tạo vụ nổ tại vị trí va chạm
            self.kill()  # Xóa đạn

        # Kiểm tra nếu đạn ra khỏi màn hình
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()
class mode_zombie(game):  # Chế độ zombie
    def __init__(self, screen):
        super().__init__(screen)
        self.gold_manager = GoldDropManager(self)  # Quản lý vàng rơi
        self.all_sprites = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()  # Nhóm chứa quái vật

        self.new()  # Khởi tạo game
        self.run()  # Chạy vòng lặp game

    def draw(self):
        super().draw()  # Vẽ các thành phần khác
        for gold in self.gold_manager.gold_list:
            self.screen.blit(gold.image, gold.rect)  # Vẽ vàng rơi

    def zombie_killed(self, enemy):
        if enemy:  # Kiểm tra enemy hợp lệ
            self.gold_manager.drop_gold(enemy.rect.x, enemy.rect.y)

    def data(self):
        super().data()
        self.auto_respawn_zombie = auto_respawn_zombie(self, 0.7)

    def AddedItems(self):
        super().AddedItems()
        self.game_over_screen = gameOverGUI(self.screen)
    
    def auto_respawn(self):
        self.auto_respawn_zombie.respawn()

    def pause_game(self):
        super().pause_game()
        if not PLAYER: #nếu player chết thì dừng game
            self.pausing = True
            self.game_over_screen.run()
            self.check_pause_events(self.game_over_screen)
            
    def update(self):
        super().update()
        self.gold_manager.check_gold_pickup()  # Kiểm tra nhặt vàng
        
    def new(self):
        super().new()
        GameStatistics.bulletRate = 0.5
        GameStatistics.bulletSpeed = 1000
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':
                    data = load_data()
                    selected_tank= data.get("selected_tank","Basic Tank")
                    self.player1 = Player1(self, col, row)

    def get_elapsed_time(self):
     elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Tính thời gian đã trôi qua (giây)
     return elapsed_time
    
def update_save_data(self, gold_amount):
    save_path = os.path.join(os.path.dirname(__file__), 'save_data.json')

    # Kiểm tra xem file tồn tại không, nếu không thì tạo dữ liệu mặc định
    if os.path.exists(save_path):
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {"player_coins": 0, "garage_tanks": [], "selected_tank": "", "completed_wave": 0}
    else:
        data = {"player_coins": 0, "garage_tanks": [], "selected_tank": "", "completed_wave": 0}
    
    # Cập nhật số tiền
    data["player_coins"] = data.get("player_coins", 0) + gold_amount
    data["player_coins"] = data.get("player_coins", 0) + gold_amount

    # Ghi lại dữ liệu vào file
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
         print(f"Nhặt vàng! Số tiền hiện tại: {data['player_coins']}")  # Debugging
    except IOError:
         print("Lỗi: Không thể ghi dữ liệu vào save_data.json")

             
    
#---------------- chế độ ranked------------
class mode_Ranked(game):
    def __init__(self, screen):
        super().__init__(screen)
        self.level = 1  # Bắt đầu từ level 1
        self.enemy_spawn_rate = 3  # Số lượng enemy ban đầu
        self.game_time = 60  # Mỗi màn chơi kéo dài 60 giây
        self.game_over_screen = gameOverGUI(self.screen)  # 🔥 Thêm dòng này
        self.start_new_level()
        self.run()
    def start_new_level(self):
        self.new()
        self.start_time = pygame.time.get_ticks()  # Reset thời gian level
        self.spawn_enemies()

    def spawn_enemies(self):
        for _ in range(self.enemy_spawn_rate):
            x, y = random.choice(self.respawn.pos_respawn)
            self.enemy = TankEnemy(self, x, y)

    def auto_respawn(self):
        self.respawn.respawn_player1()

    def check_level_completion(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        if elapsed_time >= self.game_time:  # Nếu hết thời gian
            self.level_up()

    def level_up(self):
        self.level += 1  # Tăng level
        self.enemy_spawn_rate += 1  # Mỗi level thêm 1 enemy
        self.game_time += 5  # Mỗi level kéo dài hơn 5 giây
        self.start_new_level()  # Khởi động lại level mới

    def pause_game(self):
        super().pause_game()
        if not PLAYER:  # Nếu player chết, game over
            self.pausing = True
            self.game_over_screen.run()
            self.check_pause_events(self.game_over_screen)

    def update(self):
        super().update()
        self.check_level_completion()

class mode_vuot_man(game): #chế độ vượt màn
    def __init__(self, screen, current_wave, zombies_per_wave, level_menu=None):

        self.level_menu = level_menu
        self.current_wave = current_wave
        self.zombies_per_wave = zombies_per_wave

        data = load_data()
        self.completed_wave = data.get("completed_wave", 0)

        self.gold_manager = GoldDropManager(self)
        self.wave_cleared = False
        self.waiting_for_next_wave = False
        self.log_entries = []
        super().__init__(screen)
        self.new()
        self.log(f"Game started - Wave {self.current_wave} with {self.zombies_per_wave} zombies")
        self.run()

    def data(self):
        super().data()
        self.auto_respawn_zombie = auto_respawn_zombie_with_quantity(self, 0.7, self.zombies_per_wave)
        self.zombies_in_wave = []

    def AddedItems(self):
        super().AddedItems()
        self.game_over_screen = gameOverGUI(self.screen)
        self.wave_cleared_screen = WaveClearedGUI(self.screen, self.current_wave)  # New screen for wave transitions
    
    def log(self, message, level="INFO"):
        """        
        Parameters:
            message (str): The message to log
            level (str): Log level (INFO, WARNING, ERROR)
        """
        current_time = pygame.time.get_ticks() // 1000  # Time in seconds
        formatted_time = f"{current_time // 60:02d}:{current_time % 60:02d}"
        
        # Add player stats if available
        player_stats = ""
        if PLAYER:
            kills = GameStatistics.number_kill_player1
            player_stats = f" | Kills: {kills}"
        
        log_entry = f"[{formatted_time}] [{level}] Wave {self.current_wave}: {message}{player_stats}"
        
        print(log_entry)
        
        self.log_entries.append(log_entry)
        
        if len(self.log_entries) > 100:
            self.log_entries.pop(0)
    
    def auto_respawn(self):
        if not self.waiting_for_next_wave and not self.wave_cleared:
            new_zombies = self.auto_respawn_zombie.respawn()
            if new_zombies:
                self.zombies_in_wave.extend(new_zombies)
                self.waiting_for_next_wave = True
                self.log(f"Spawned {len(new_zombies)} zombies, total in wave: {len(self.zombies_in_wave)}")
    
    def check_wave_status(self):
        if self.zombies_in_wave and all(zombie.alive == False for zombie in self.zombies_in_wave):
            self.wave_cleared = True
            self.log(f"Wave {self.current_wave} cleared!")
            if (self.current_wave > self.completed_wave):
                self.completed_wave = self.current_wave
            self.show_wave_cleared_screen()
    
    def show_wave_cleared_screen(self):
        self.pausing = True
        self.wave_cleared_screen.update_wave(self.current_wave)
        self.wave_cleared_screen.run()
        update_completed_wave(self.completed_wave)
        self.check_clear_wave_events(self.wave_cleared_screen)
    
    def start_next_wave(self):
        self.zombies_in_wave = []
        self.wave_cleared = False
        self.current_wave += 1
        self.zombies_per_wave += 2  # Increase zombies per wave
        self.auto_respawn_zombie.spawn_count = self.zombies_per_wave
        
        self.waiting_for_next_wave = False
        self.pausing = False
        self.log(f"Starting wave {self.current_wave} with {self.zombies_per_wave} zombies")

        return 
    def update(self):
        super().update()
        self.check_wave_status()
    
    def pause_game(self):
        if self.pausing == True:
            self.pause_screen.run()
            self.clock.tick(FPS)
            self.check_pause_events(self.pause_screen)
        if not PLAYER: #nếu player chết thì dừng game
            self.pausing = True
            self.game_over_screen.run()
            self.check_pause_events(self.game_over_screen)

    def new(self):
        super().new()
        GameStatistics.bulletRate = 0.5
        GameStatistics.bulletSpeed = 1000
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':
                    data = load_data()
                    selected_tank = data.get("selected_tank", "Basic Tank")
                    # self.player1 = Player1(self, col, row, selected_tank)
                    self.player1 = Player1(self, col, row)
    
    def get_elapsed_time(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Tính thời gian đã trôi qua (giây)
        return elapsed_time
        
    def check_clear_wave_events(self, pause_screen):
        if pause_screen == None or pause_screen.action == None:
            return
        
        if pause_screen.action == 1:
            self.start_next_wave()
            self.playing = False

        if pause_screen.action == 0:
            
            self.playing = False
            self.running = False
            self.pausing = False
            # gui = vuot_man_GUI(self.screen)
            # gui.run()           

    def check_pause_events(self,pause_screen):
        if pause_screen == None or pause_screen.action == None: 
            return
        if pause_screen.action == 1: #tiếp tục
            return
        if pause_screen.action == 0: #thoát
            # self.playing = False
            self.playing = False
            self.running = False
            # gui = vuot_man_GUI(self.screen)
            # gui.run()
        if pause_screen.action == 2: #restart
            self.new()
            self.zombies_in_wave = []
            self.wave_cleared = False
            self.current_wave = 1
            self.zombies_per_wave = 5  # Increase zombies per wave
            self.auto_respawn_zombie.spawn_count = self.zombies_per_wave
            self.waiting_for_next_wave = False
            self.pausing = False
            self.log(f"Starting wave {self.current_wave} with {self.zombies_per_wave} zombies")
            pause_screen.action = None

def update_completed_wave(completed_wave):
    """
    Cập nhật thông tin về màn chơi đã hoàn thành vào file save_data.json
    
    Parameters:
        completed_wave (int): Số màn chơi đã hoàn thành
    
    Returns:
        bool: True nếu cập nhật thành công, False nếu có lỗi
    """
    import os
    import json
    
    save_path = os.path.join(os.path.dirname(__file__), 'save_data.json')
    
    # Đọc dữ liệu từ file save
    if os.path.exists(save_path):
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {"player_coins": 0, "garage_tanks": [], "selected_tank": "", "completed_wave": 0}
    else:
        data = {"player_coins": 0, "garage_tanks": [], "selected_tank": "", "completed_wave": 0}
    
    # Chỉ cập nhật nếu màn mới cao hơn màn đã lưu
    current_completed = data.get("completed_wave", 0)
    if completed_wave > current_completed:
        data["completed_wave"] = completed_wave
        print(f"Đã cập nhật màn vượt qua: {completed_wave}")  # Thông báo debug
        
        # Ghi lại dữ liệu vào file
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except IOError:
            print("Lỗi: Không thể ghi dữ liệu vào save_data.json")
            return False
        
    def run(self):  # hàm này để chạy các chế độ game
        self.playing = True
        while self.playing:
            self.pausing=False
            while self.pausing == False:
                self.changing_time = self.clock.tick(FPS) / 1000
                self.events()  
                self.update()
                self.update_draw()
                self.auto_respawn()
                self.pause_game()
        return
    
    return True

#-------------------------chế độ 1 vss 1---------------------------------------------------------
