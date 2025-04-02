import pygame
from Button import Button
from setting import *
from setting import button_click_sound 
from garageGUI import load_data, save_data
class pauseGUI:  # Màn hình Pause
    def __init__(self, screen):
        self.screen = screen
        self.action = None
        self.addControls()
        
        # Khởi tạo pygame mixer để phát âm thanh
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("sounds/An.wav")  # Thay bằng file âm thanh của bạn

    def addControls(self):
        k = 160
        self.continue_Button = Button(self.screen, (self.screen.get_width() - 200) // 2, (self.screen.get_height() - 50) // 2 + k - 70, 200, 50, SILVER,
                                      BLACK, 3, "CONTINUE")
        self.restart_button_Setting = Button(self.screen, (self.screen.get_width() - 200) // 2, (self.screen.get_height() - 50) // 2 + k, 200, 50, SILVER,
                                             BLACK, 3, "RESTART")
        self.exit_button = Button(self.screen, (self.screen.get_width() - 200) // 2, (self.screen.get_height() - 50) // 2 + k + 70, 200, 50, SILVER,
                                  BLACK, 3, "EXIT")
        self.select_tank_Button = Button(self.screen, (self.screen.get_width() - 200) // 2, 
                                 (self.screen.get_height() - 50) // 2 + 160, 
                                 200, 50, SILVER, BLACK, 3, "SỬ DỤNG XE")

        
    def draw(self):
        self.continue_Button.draw()
        self.restart_button_Setting.draw()
        self.exit_button.draw()

    def addEvents(self):
        self.action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.exit_button):
                    self.click_sound.play()  # Phát âm thanh khi nhấn nút
                    self.running = False
                    self.action = 0  # Thoát
                if check_btn_click(mouse_pos, self.continue_Button):
                    self.click_sound.play()  # Phát âm thanh khi nhấn nút
                    self.running = False
                    self.action = 1  # Tiếp tục
                if check_btn_click(mouse_pos, self.restart_button_Setting):
                    self.click_sound.play()  # Phát âm thanh khi nhấn nút
                    self.running = False
                    self.action = 2  # Restart
                elif check_btn_click(mouse_pos, self.select_tank_Button):
                   self.select_tank()
    def select_tank(self):
     data = load_data()
     garage_tanks = data.get("garage_tanks", [])
     if not garage_tanks:
        return  # Nếu không có xe nào thì không làm gì

     selected_tank = garage_tanks[0]  # Chọn xe đầu tiên trong danh sách
     data["selected_tank"] = selected_tank
     save_data(data)
     print(f"Xe {selected_tank} đã được chọn!")

    def quit(self):
        pygame.quit()
        quit()

    def run(self):
        self.running = True
        while self.running:
            self.addEvents()
            self.draw()
            pygame.display.flip()
