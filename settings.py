class Settings:
    ''' Klasa przeznaczona do przechowywania wszystkich ustawień gry'''

    def __init__(self):
        ''' Inicjalizacja ustawień gry'''

        # Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (47, 74, 130)  # b,c: (255, 204, 153),(25, 213, 166)

        # Ustawienia statku
        self.ship_limit = 3

        # Ustawienia pociskow
        self.bullet_width = 3  # 3
        self.bullet_height = 15  # 15
        self.bullet_color = (255, 128, 0)
        self.bullets_allowed = 3

        # Ustawienia obcych
        self.fleet_drop_speed = 10  # 10
        self.fleet_direction = 1
        self.space_between_aliens_x = 0.5
        self.space_between_aliens_y = 0.4

        # Inne
        self.lost_game_pause_time = 1.0

        # Współczynnik zmiany szybkości gry
        self.speed_up_scale = 1.1

        # Współczynnik  zmiany przyznawanych punktów
        self.score_scale = 1  # składowa +
        # self.score_scale = 1.1  # składowa *

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        ''' Inicjalizacja ustawień, które ulegają zmianie w trakcie gry '''
        self.ship_speed = 1.0
        self.bullet_speed = 1.0
        self.alien_speed = 0.1

        self.alien_points = 100

    def increase_speed(self):
        # self.ship_speed *= self.speed_up_scale
        # self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale

        self.alien_points = int(self.alien_points + self.score_scale)
        # self.alien_points = int(self.alien_points * self.score_scale)

        self.fleet_direction = 1
