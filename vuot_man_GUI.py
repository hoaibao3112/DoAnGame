import pygame
from Button import Button
import game 
from garageGUI import load_data, save_data
from setting import *

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
        self.current_display = None
        self.button_sound = pygame.mixer.Sound("sounds/An.wav")

        self.show_notification = False
        self.notification_text = ""
        self.notification_timer = 0
        self.notification_duration = 2000 
        self.notification_font = pygame.font.Font(None, 36)
        self.notification_color = (255, 0, 0)

        self.addControls()

        bg_music.play(-1)
        self.run()

    def display_notification(self, message):
        self.notification_text = message
        self.show_notification = True
        self.notification_timer = pygame.time.get_ticks()
    
    def update_notification(self):
        if self.show_notification:
            current_time = pygame.time.get_ticks()
            if current_time - self.notification_timer > self.notification_duration:
                self.show_notification = False

    def draw_notification(self):
        if self.show_notification:
            notification_surface = pygame.Surface((WIDTH, 80))
            notification_surface.set_alpha(200)
            notification_surface.fill((0, 0, 0))
            
            text_surface = self.notification_font.render(self.notification_text, True, self.notification_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 40))
            
            self.screen.blit(notification_surface, (0, 0))
            self.screen.blit(text_surface, text_rect)

    def save_completed_wave(self):
        """Save the completed wave to the save file"""
        data = load_data()
        if self.completed_wave > data.get("completed_wave", 0):
            data["completed_wave"] = self.completed_wave
            save_data(data)
            print(f"Đã lưu màn chơi hoàn thành: {self.completed_wave}")

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

        if self.show_notification:
            self.draw_notification()

    def addEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.save_completed_wave()
                return

            if event.type == pygame.USEREVENT and event.dict.get("action") == "return_to_menu":
                self.current_display = None
                self.save_completed_wave()
                self.addControls()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_sound.play()
                mouse_pos = pygame.mouse.get_pos()
                
                if check_btn_click(mouse_pos, self.back_button):
                    self.running = False
                    self.save_completed_wave()
                    return 
               
                def handle_wave(wave_number, zombie_count):
                    if wave_number == 1 or (self.completed_wave and wave_number <= self.completed_wave + 1):
                        self.current_display = game.mode_vuot_man(self.screen, wave_number, zombie_count, self)
                        if self.current_display.completed_wave > self.completed_wave:
                            self.completed_wave = self.current_display.completed_wave
                            self.save_completed_wave()
                    else:
                        self.display_notification(f"Màn {wave_number} đang khóa!")

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
        clock = pygame.time.Clock()
        while self.running:
            if self.current_display:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.save_completed_wave()
                        return
                    if event.type == pygame.USEREVENT and event.dict.get("action") == "return_to_menu":
                        self.current_display = None
                        self.save_completed_wave()
                        self.addControls()
                
                if self.current_display:
                    self.current_display.run()
            else:
                self.addEvents()
                self.update_notification()
                self.draw()
                pygame.display.flip()
                clock.tick(60)