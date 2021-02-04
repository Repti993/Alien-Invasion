class GameStats:
    ''' Monitorowanie danych statystycznych w grze "Inwazja obcych" '''

    def __init__(self, ai_game):
        ''' Inicjalizacja danych statystycznych '''
        self.settings = ai_game.settings
        self.reset_stats()

        # Najlepszy wynik
        self.high_score = 0

        # Uruchomienie gry w stanie aktywnym
        self.game_active = False

    def reset_stats(self):
        ''' Inicjalizacja danych statystycznych, które mogą zmieniać się w trakcie gry '''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
