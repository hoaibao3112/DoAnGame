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
        self.screen.fill(DARK_SEA_GREEN) #tô màu màn hình
        # self.grid() #vẽ lưới
        self.all_sprites.draw(self.screen) #vẽ tất cả các sprites
        self.btn_setting.draw() #vẽ nút setting
        self.show_kill_player1.draw(GameStatistics.number_kill_player1,BLUE) #vẽ số lần giết của player1
         # Hiển thị bộ đếm thời gian
        font = pygame.font.SysFont(None, 40)
        elapsed_time = self.get_elapsed_time()
        time_text = font.render(f"Time: {elapsed_time}s", True, (255, 0, 0))
        self.screen.blit(time_text, (WIDTH // 2 - 50, 20))  # Đặt vị trí hiển thị
        
    def update_draw(self): #cập nhật và vẽ các đối tượng
        self.draw() 
        pygame.display.flip() #cập nhật màn hình

    def update(self): #cập nhật tất cả các sprites
        self.all_sprites.update()

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
        self.new()
        self.run()

    def new(self):
        super().new()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':  # Người chơi 1
                    self.player1 = Player1(self, col, row)  
                if tile == '-':  # Người chơi 2
                    self.player2 = Player2(self, col, row)

    def AddedItems(self):
        super().AddedItems()
        self.show_kill_player1 = show_kill(self.screen, "left")  # Hiển thị kill của Player 3
        self.show_kill_player2 = show_kill(self.screen, "right") # Hiển thị kill của Player 2

    def draw(self):
        super().draw()
        self.show_kill_player1.draw(GameStatistics.number_kill_player1, BLUE)  
        self.show_kill_player2.draw(GameStatistics.number_kill_player2, RED)   

    def auto_respawn(self):
        """ Tự động hồi sinh cả hai người chơi """
        self.respawn.respawn_player1()
        self.respawn.respawn_player2()

        
  
class mode_zombie(game):  # Chế độ zombie
    def __init__(self, screen):
        super().__init__(screen)
        self.gold_manager = GoldDropManager(self)  # Quản lý vàng rơi
        self.all_sprites = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()  # Nhóm chứa quái vật
        self.wave_cleared_screen = None

        
        self.current_wave = 1
        self.zombies_per_wave = 5  # Số zombie ban đầu
        self.unlocked_levels = [1]  # Danh sách các màn đã mở khóa
        self.wave_cleared_screen = WaveClearedGUI(self.screen, self.current_wave)  # Màn thông báo qua màn
        
        self.zombie_wave_data = {1: 5}  # Màn đầu có 5 zombie


        self.new()  # Khởi tạo game
        self.run()  # Chạy vòng lặp game

    
    def check_wave_completion(self):#kiểm tra điều kiện qua mànmàn
        print(f"Số zombie đã giết: {GameStatistics.number_kill_player1} / {self.zombies_per_wave}")  # Debug
        if GameStatistics.number_kill_player1 >= self.zombies_per_wave:
            self.current_wave += 1
            self.wave_cleared_screen = WaveClearedGUI(self.screen, (self.current_wave - 1))  # Cập nhật màn hình qua màn

            self.wave_cleared = True
            if self.wave_cleared_screen:
                self.wave_cleared_screen.run()

            
            # Mở khóa màn tiếp theo nếu chưa mở khóa
            if self.current_wave not in self.unlocked_levels:
                self.unlocked_levels.append(self.current_wave )

            if self.wave_cleared:
                pygame.time.delay(500)  # Đợi một chút trước khi hiển thị menu chọn màn
                self.show_level_selection()
            
           
    def show_level_selection(self):#giao diện chọn level
        self.pausing = True
        self.screen.fill((0, 0, 0))  # Tô màu nền đen

        font = pygame.font.Font(None, 50)
        title_text = font.render("Chọn màn chơi", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 4 - 50))

        button_width = 200
        button_height = 50
        button_margin = 20
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 4

        level_buttons = []  # Danh sách lưu các nút màn chơi

        for level in self.unlocked_levels:
            btn_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (0, 255, 0), btn_rect)
            text = font.render(f"Màn {level}", True, (0, 0, 0))
            self.screen.blit(text, (button_x + 50, button_y + 10))
            level_buttons.append((btn_rect, level))
            button_y += button_height + button_margin

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for btn_rect, level in level_buttons:
                        if btn_rect.collidepoint(mouse_pos):
                            self.current_wave = level
                            self.start_new_wave()
                            self.pausing = False
                            waiting = False


    def start_new_wave(self):
        # self.zombies_per_wave += 2  # Mỗi màn tăng số lượng zombie
        if self.current_wave not in self.zombie_wave_data:
            self.zombie_wave_data[self.current_wave] = 5 + (self.current_wave - 1) * 2
        self.zombies_per_wave = self.zombie_wave_data[self.current_wave]
        self.new()  # Reset màn
        self.playing = True  # Đảm bảo game tiếp tục chạy
        self.pausing = False  # Hủy trạng thái pause
        self.wave_cleared = False  # Reset trạng thái qua màn





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
        self.check_wave_completion()
        
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
            data = {"player_coins": 0, "garage_tanks": [], "selected_tank": ""}
    else:
        data = {"player_coins": 0, "garage_tanks": [], "selected_tank": ""}
    
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
    def __init__(self, screen):
        self.current_wave = 1
        self.zombies_per_wave = 5  # Starting number of zombies
        self.wave_cleared = False
        self.waiting_for_next_wave = False
        self.log_entries = []  # Store log entries
        super().__init__(screen)
        self.new()
        self.log(f"Game started - Wave {self.current_wave} with {self.zombies_per_wave} zombies")
        self.run()

    def data(self):
        super().data()
        self.auto_respawn_zombie = auto_respawn_zombie_with_quantity(self, 0.7, self.zombies_per_wave)
        self.zombies_in_wave = []  # Track zombies in current wave

    def AddedItems(self):
        super().AddedItems()
        self.game_over_screen = gameOverGUI(self.screen)
        self.wave_cleared_screen = WaveClearedGUI(self.screen, self.current_wave)  # New screen for wave transitions
    
    def log(self, message, level="INFO"):
        """
        Log game events with timestamp and current wave information
        
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
        
        # Create formatted log entry
        log_entry = f"[{formatted_time}] [{level}] Wave {self.current_wave}: {message}{player_stats}"
        
        # Print to console
        print(log_entry)
        
        # Store log entry for possible display or saving
        self.log_entries.append(log_entry)
        
        # Limit log size
        if len(self.log_entries) > 100:
            self.log_entries.pop(0)
    
    def auto_respawn(self):
        # Only spawn zombies if not waiting between waves
        if not self.waiting_for_next_wave and not self.wave_cleared:
            # Track all zombies spawned
            new_zombies = self.auto_respawn_zombie.respawn()
            if new_zombies:
                self.zombies_in_wave.extend(new_zombies)
                self.waiting_for_next_wave = True  # Stop spawning after wave is created
                self.log(f"Spawned {len(new_zombies)} zombies, total in wave: {len(self.zombies_in_wave)}")
    
    def check_wave_status(self):
        # Check if all zombies in the current wave are dead
        if self.zombies_in_wave and all(zombie.alive == False for zombie in self.zombies_in_wave):
            self.wave_cleared = True
            self.log(f"Wave {self.current_wave} cleared!")
            self.show_wave_cleared_screen()
    
    def show_wave_cleared_screen(self):
        self.pausing = True
        self.wave_cleared_screen.update_wave(self.current_wave)
        self.wave_cleared_screen.run()
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
                    self.player1 = Player1(self, col, row, selected_tank)
    
    def get_elapsed_time(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Tính thời gian đã trôi qua (giây)
        return elapsed_time
        
    def check_clear_wave_events(self, pause_screen):
        if pause_screen == None or pause_screen.action == None:
            return
        if pause_screen.action == 1:
            self.start_next_wave()
    def check_pause_events(self,pause_screen): #kiểm tra sự kiện của màn hình pause
        if pause_screen == None or pause_screen.action == None: 
            return
        if pause_screen.action == 1: #tiếp tục
            return
        if pause_screen.action == 0: #thoát
            self.playing = False
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
#----------------------------------------------------------------------------------
