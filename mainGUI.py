import pygame
from Button import Button
from game import *
from setting import *

class mainGUI:
    def __init__(self):
        pygame.init()
        self.icon = pygame.image.load(r'img\logo.png')
        self.background = pygame.image.load(r'img\background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.addControls()

        bg_music.play(-1)
        self.run()

    def addControls(self):
        x = 160
        center_x = (self.screen.get_width() - 200) // 2
        center_y = (self.screen.get_height() - 50) // 2

        self.zombie_Button = Button(self.screen, center_x, center_y + x - 70, 200, 50, SILVER, BLACK, 3, "ZOMBIE WORLD")
        self.training_Button = Button(self.screen, center_x, center_y + x, 200, 50, SILVER, BLACK, 3, "TRAINING")
        self.pvp_Button = Button(self.screen, center_x, center_y + x + 70, 200, 50, SILVER, BLACK, 3, "2 PLAYERS")
        self.ranked_Button = Button(self.screen, center_x, center_y + x + 140, 200, 50, SILVER, BLACK, 3, "RANKED MODE")
        self.button_quit = Button(self.screen, center_x, center_y + x + 210, 200, 50, SILVER, BLACK, 4, "QUIT")

    def quit(self):
        pygame.quit()
        quit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.zombie_Button.draw()
        self.training_Button.draw()
        self.pvp_Button.draw()
        self.ranked_Button.draw()
        self.button_quit.draw()

    def addEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.button_quit):
                    self.quit()
                if check_btn_click(mouse_pos, self.zombie_Button):
                    self.current_display = mode_zombie(self.screen)
                if check_btn_click(mouse_pos, self.training_Button):
                    self.current_display = mode_training(self.screen)
                if check_btn_click(mouse_pos, self.pvp_Button):
                    self.current_display = mode_1v1(self.screen)
                if check_btn_click(mouse_pos, self.ranked_Button):
                    self.current_display = mode_Ranked(self.screen)

    def run(self):
        self.run = True
        while self.run:
            self.addEvents()
            self.draw()
            pygame.display.flip()
        self.quit()