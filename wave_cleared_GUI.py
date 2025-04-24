import pygame
from Button import Button
from setting import *
import vuot_man_GUI 
class WaveClearedGUI:
    def __init__(self, screen, wave_number):
        self.screen = screen
        self.wave_number = wave_number
        self.action = None
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.addControls()
        
    def addControls(self):
        self.continue_button = Button(self.screen, (self.screen.get_width() - 200) // 2, 
                                (self.screen.get_height() - 50) // 2 + 100, 200, 50, SILVER,
                                BLACK, 3, "CONTINUE")
        
        self.back_button = Button(
        self.screen,
        (self.screen.get_width() - 200) // 2,
        (self.screen.get_height() - 50) // 2 + 180,
        200, 50,
        SILVER, BLACK, 3,
        "BACK TO MENU"
        )
    
    def update_wave(self, wave_number):
        self.wave_number = wave_number
        
    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        # Wave cleared message
        wave_text = self.font.render(f"WAVE {self.wave_number} CLEARED!", True, (255, 255, 0))
        wave_rect = wave_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(wave_text, wave_rect)
        
        # Next wave info
        next_wave_text = self.small_font.render(f"WAVE {self.wave_number + 1} INCOMING", True, (255, 0, 0))
        next_wave_rect = next_wave_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(next_wave_text, next_wave_rect)
        
        # Draw continue button
        self.continue_button.draw()
        self.back_button.draw()
    
    def addEvents(self):
        self.action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.continue_button):
                    self.running = False
                    self.action = 1
                elif check_btn_click(mouse_pos, self.back_button):
                    self.running = False
                    self.action = 0
            
    def quit(self):
        pygame.quit()
        quit()
        
    def run(self):
        self.running = True
        while self.running:
            self.addEvents()
            self.draw()
            pygame.display.flip()
        
       