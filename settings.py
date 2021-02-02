class Settings:
    ''' Klasa przeznaczona do przechowywania wszystkich ustawień gry'''

    def __init__(self):
        ''' Inicjalizacja ustawień gry'''

        # Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (47, 74, 130)  # b,c: (255, 204, 153),(25, 213, 166)

        # Ustawienia statku
        self.ship_speed = 1.0

        # Ustawienia pociskow
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 128, 0)
        self.bullets_allowed = 3

        # Ustawienia obcych
        self.space_between_aliens_x = 0.5
        self.space_between_aliens_y = 0.4