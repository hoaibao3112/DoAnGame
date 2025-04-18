import pygame
from Button import Button
from game import *
from setting import *
from garageGUI import GarageGUI
from shopGUI import ShopGUI
from vuot_man_GUI import vuot_man_GUI
class mainGUI:
    def __init__(self):
        pygame.init()
        self.icon = pygame.image.load(r'img/logo.png')
        self.background = pygame.image.load(r'img/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.current_display = None
        self.button_sound = pygame.mixer.Sound("sounds/An.wav")  # Âm thanh khi nhấn nút
        self.addControls()

        bg_music.play(-1)
        self.run()

    def addControls(self):
        x_offset = 300
        y_offset = 160
        button_width = 200
        button_height = 50
        spacing = 70
        center_x_left = (self.screen.get_width() // 2) - x_offset
        center_x_right = (self.screen.get_width() // 2) + x_offset
        center_y = (self.screen.get_height() - 50) // 2

        self.mode_vuot_man = Button(self.screen, center_x_left, center_y + y_offset - 140, button_width, button_height, SILVER, BLACK, 3, "VUOT MAN WORLD")
        self.zombie_Button = Button(self.screen, center_x_right, center_y + y_offset - 140, button_width, button_height, SILVER, BLACK, 3, "ZOMBIE WORLD")
        self.training_Button = Button(self.screen, center_x_left, center_y + y_offset - 70, button_width, button_height, SILVER, BLACK, 3, "TRAINING")
        self.pvp_Button = Button(self.screen, center_x_right, center_y + y_offset - 70, button_width, button_height, SILVER, BLACK, 3, "2 PLAYERS")
        self.ranked_Button = Button(self.screen, center_x_left, center_y + y_offset, button_width, button_height, SILVER, BLACK, 3, "RANKED MODE")
        self.garage_Button = Button(self.screen, center_x_right, center_y + y_offset, button_width, button_height, SILVER, BLACK, 3, "KHO CUA TOI")
        self.shop_Button = Button(self.screen, center_x_left, center_y + y_offset + spacing, button_width, button_height, SILVER, BLACK, 3, "SHOP MUA SUNG")
        self.button_quit = Button(self.screen, center_x_right, center_y + y_offset + spacing, button_width, button_height, SILVER, BLACK, 4, "QUIT")
        
    def quit(self):
        pygame.quit()
        quit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.mode_vuot_man.draw()
        self.zombie_Button.draw()
        self.training_Button.draw()
        self.pvp_Button.draw()
        self.ranked_Button.draw()
        self.garage_Button.draw()
        self.shop_Button.draw()
        self.button_quit.draw()

    def addEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_sound.play()
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.button_quit):
                    self.quit()
                elif check_btn_click(mouse_pos, self.zombie_Button):
                    self.current_display = mode_zombie(self.screen)
                elif check_btn_click(mouse_pos, self.training_Button):
                    self.current_display = mode_training(self.screen)
                elif check_btn_click(mouse_pos, self.pvp_Button):
                    self.current_display = mode_1v1(self.screen)
                elif check_btn_click(mouse_pos, self.ranked_Button):
                    self.current_display = mode_Ranked(self.screen)
                elif check_btn_click(mouse_pos, self.mode_vuot_man):
                    vuot_man_GUI(self.screen).run()
                elif check_btn_click(mouse_pos, self.garage_Button):
                    GarageGUI(self.screen).run()
                elif check_btn_click(mouse_pos, self.shop_Button):
                    ShopGUI(self.screen).run()
    
    def run(self):
        self.run = True
        while self.run:
            self.addEvents()
            self.draw()
            pygame.display.flip()
        self.quit()
