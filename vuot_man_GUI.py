import pygame
from Button import Button
# from game import mode_vuot_man
import  game 
from setting import *
from garageGUI import GarageGUI
from shopGUI import ShopGUI
class main2GUI:
    def __init__(self, screen=None, completed_wave=0):
        pygame.init()
        self.completed_wave = completed_wave
        self.icon = pygame.image.load(r'img/logo.png')
        self.background = pygame.image.load(r'img/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.current_display = None
        self.button_sound = pygame.mixer.Sound("sounds/An.wav")  # Âm thanh khi nhấn nút
        self.addControls()

        bg_music.play(-1)
        # self.run()

    def addControls(self):
        button_width = 200
        button_height = 50
        spacing_x = 70
        spacing_y = 50

        total_width = 3 * button_width + 2 * spacing_x
        start_x = (WIDTH - total_width) // 2
        start_y = 200

        # Thay vì dùng vòng lặp for, tạo mỗi nút riêng biệt
        # self.level_buttons = []

        # Tạo nút LV1 đến LV9
        self.level_buttons1= Button(self.screen, start_x, start_y, button_width, button_height, SILVER, BLACK, 3, "LV1")
        self.level_buttons2= Button(self.screen, start_x + button_width + spacing_x, start_y, button_width, button_height, SILVER, BLACK, 3, "LV2")
        self.level_buttons3= Button(self.screen, start_x + 2 * (button_width + spacing_x), start_y, button_width, button_height, SILVER, BLACK, 3, "LV3")
        
        self.level_buttons4= Button(self.screen, start_x, start_y + button_height + spacing_y, button_width, button_height, SILVER, BLACK, 3, "LV4")
        self.level_buttons5= Button(self.screen, start_x + button_width + spacing_x, start_y + button_height + spacing_y, button_width, button_height, SILVER, BLACK, 3, "LV5")
        self.level_buttons6= Button(self.screen, start_x + 2 * (button_width + spacing_x), start_y + button_height + spacing_y, button_width, button_height, SILVER, BLACK, 3, "LV6")
        
        self.level_buttons7= Button(self.screen, start_x, start_y + 2 * (button_height + spacing_y), button_width, button_height, SILVER, BLACK, 3, "LV7")
        self.level_buttons8= Button(self.screen, start_x + button_width + spacing_x, start_y + 2 * (button_height + spacing_y), button_width, button_height, SILVER, BLACK, 3, "LV8")
        self.level_buttons9= Button(self.screen, start_x + 2 * (button_width + spacing_x), start_y + 2 * (button_height + spacing_y), button_width, button_height, SILVER, BLACK, 3, "LV9")

    def quit(self):
        pygame.quit()
        quit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # for button in self.level_buttons:
        #     button.draw()
        self.level_buttons1.draw()
        self.level_buttons2.draw()
        self.level_buttons3.draw()
        self.level_buttons4.draw()
        self.level_buttons5.draw()
        self.level_buttons6.draw()
        self.level_buttons7.draw()
        self.level_buttons8.draw()
        self.level_buttons9.draw()

    def addEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_sound.play()
                mouse_pos = pygame.mouse.get_pos()
               
                
                def handle_wave(wave_number, zombie_count):
                    if wave_number == 1 or (self.completed_wave and wave_number <= self.completed_wave + 1):
                        self.current_display = game.mode_vuot_man(self.screen, wave_number, zombie_count)
                        
                        # Cập nhật wave hoàn thành (nếu đã vượt qua thành công thì bên mode_vuot_man sẽ cập nhật)
                        self.completed_wave = self.current_display.completed_wave
                    else:
                        print(f"⚠️ LV{wave_number} chưa được mở khóa!")

                if check_btn_click(mouse_pos, self.level_buttons1):
                    handle_wave(1, 5)
                elif check_btn_click(mouse_pos, self.level_buttons2):
                    handle_wave(2, 7)
                elif check_btn_click(mouse_pos, self.level_buttons3):
                    handle_wave(3, 9)
                elif check_btn_click(mouse_pos, self.level_buttons4):
                    handle_wave(4, 11)
                elif check_btn_click(mouse_pos, self.level_buttons5):
                    handle_wave(5, 13)
                elif check_btn_click(mouse_pos, self.level_buttons6):
                    handle_wave(6, 15)
                elif check_btn_click(mouse_pos, self.level_buttons7):
                    handle_wave(7, 17)
                elif check_btn_click(mouse_pos, self.level_buttons8):
                    handle_wave(8, 19)
                elif check_btn_click(mouse_pos, self.level_buttons9):
                    handle_wave(9, 21)
                

    def run(self):
        self.run = True
        while self.run:
            if self.current_display:  # Nếu có màn hình mới
                self.current_display.run()  # Chạy màn hình của cấp độ
            self.addEvents()
            self.draw()
            pygame.display.flip()
        self.quit()
