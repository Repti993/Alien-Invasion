class GameStats:
    ''' Monitorowanie danych statystycznych w grze "Inwazja obcych" '''

    def __init__(self, ai_game):
        ''' Inicjalizacja danych statystycznych '''
        self.settings = ai_game.settings
        self.reset_stats()

        # Najlepszy wynik
        self.high_score = 0

        # 'Tryby' gry
        self.menu_dict = {
            'game': False,
            'main': True,
            'choice': False,
            'game over': False
        }

    def reset_stats(self):
        ''' Inicjalizacja danych statystycznych, które mogą zmieniać się w trakcie gry '''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def set_active_menu(self, menu_to_set):
        ''' Aktywuje podane menu lub aktywuje grę'''

        # Ogólny reset
        for menu in self.menu_dict.keys():
            self.menu_dict[menu] = False

        # Aktywacja jednego menu
        self.menu_dict[menu_to_set] = True
