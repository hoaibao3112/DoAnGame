import pygame
from Button import Button
# from game import mode_vuot_man
import game 
from setting import *
from garageGUI import GarageGUI, load_data
from shopGUI import ShopGUI

class vuot_man_GUI:
    def __init__(self, screen, main_menu=None):
        self.screen = screen
        self.main_menu = main_menu
        self.running = True

        self.pausing = False
        self.playing = True

        data = load_data()
        self.completed_wave = data.get("completed_wave", 0)

        self.icon = pygame.image.load(r'img/logo.png')
        self.background = pygame.image.load(r'img/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        pygame.display.set_icon(self.icon)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.current_display = None
        self.button_sound = pygame.mixer.Sound("sounds/An.wav")  # Âm thanh khi nhấn nút
        self.addControls()

        bg_music.play(-1)
        self.run()

    def addControls(self):
        button_width = 200
        button_height = 50
        spacing_x = 70
        spacing_y = 50

        total_width = 3 * button_width + 2 * spacing_x
        start_x = (WIDTH - total_width) // 2
        start_y = 200
        
        UNLOCKED_COLOR = SILVER
        LOCKED_COLOR = (100, 100, 100)

        def get_button_color(level):
            if level == 1 or (self.completed_wave and level <= self.completed_wave + 1):
                return UNLOCKED_COLOR
            else:
                return LOCKED_COLOR

        self.level_buttons1 = Button(self.screen, start_x, start_y, button_width, button_height, 
                                    get_button_color(1), BLACK, 3, "LV1")
        
        self.level_buttons2 = Button(self.screen, start_x + button_width + spacing_x, start_y, button_width, button_height, 
                                    get_button_color(2), BLACK, 3, "LV2")
        
        self.level_buttons3 = Button(self.screen, start_x + 2 * (button_width + spacing_x), start_y, button_width, button_height, 
                                    get_button_color(3), BLACK, 3, "LV3")
        
        self.level_buttons4 = Button(self.screen, start_x, start_y + button_height + spacing_y, button_width, button_height, 
                                    get_button_color(4), BLACK, 3, "LV4")
        
        self.level_buttons5 = Button(self.screen, start_x + button_width + spacing_x, start_y + button_height + spacing_y, button_width, button_height, 
                                    get_button_color(5), BLACK, 3, "LV5")
        
        self.level_buttons6 = Button(self.screen, start_x + 2 * (button_width + spacing_x), start_y + button_height + spacing_y, button_width, button_height, 
                                    get_button_color(6), BLACK, 3, "LV6")
        
        self.level_buttons7 = Button(self.screen, start_x, start_y + 2 * (button_height + spacing_y), button_width, button_height, 
                                    get_button_color(7), BLACK, 3, "LV7")
        
        self.level_buttons8 = Button(self.screen, start_x + button_width + spacing_x, start_y + 2 * (button_height + spacing_y), button_width, button_height, 
                                    get_button_color(8), BLACK, 3, "LV8")
        
        self.level_buttons9 = Button(self.screen, start_x + 2 * (button_width + spacing_x), start_y + 2 * (button_height + spacing_y), button_width, button_height, 
                                    get_button_color(9), BLACK, 3, "LV9")
        
        back_button_width = 200
        back_button_height = 50
        back_button_x = (WIDTH - back_button_width) // 2
        back_button_y = start_y + 3 * (button_height + spacing_y) + 30

        self.back_button = Button(self.screen, back_button_x, back_button_y, back_button_width, back_button_height, 
                                 RED, WHITE, 4, "BACK TO MENU")

    def quit(self):
        pygame.quit()
        quit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.level_buttons1.draw()
        self.level_buttons2.draw()
        self.level_buttons3.draw()
        self.level_buttons4.draw()
        self.level_buttons5.draw()
        self.level_buttons6.draw()
        self.level_buttons7.draw()
        self.level_buttons8.draw()
        self.level_buttons9.draw()
        self.back_button.draw()

    def addEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_sound.play()
                mouse_pos = pygame.mouse.get_pos()
                
                if check_btn_click(mouse_pos, self.back_button):
                    self.running = False
                    return 
               
                def handle_wave(wave_number, zombie_count):
                    if wave_number == 1 or (self.completed_wave and wave_number <= self.completed_wave + 1):
                        self.current_display = game.mode_vuot_man(self.screen, wave_number, zombie_count, self)
                        # game_instance = game.mode_vuot_man(self.screen, wave_number, zombie_count)

                        # result = game_instance.run()

                        self.completed_wave = self.current_display.completed_wave
                        
                        # print(result)
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
        self.running = True
        while self.running:
            if self.current_display:
                self.current_display.run()
            self.addEvents()
            self.draw()
            pygame.display.flip()
            
        # return