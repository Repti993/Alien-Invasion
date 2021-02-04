import pygame


class Ship:
    ''' Klasa przeznaczona do zarządzania statkiem kosmicznym '''

    def __init__(self, ai_game):
        ''' Inicjalizacja statku kosmicznego i jego położenia początkowego '''

        #   To jest obszar (prostokąt) całego okna gry...
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta
        self.image = pygame.image.load('images/ship_1.bmp')
        #   ... a to jest obszar obiektu (statku), może raczej rozmiar,
        #   bo image wcale nie leży tam, gdzie rect. Przeniesienie image na rect
        #   odbędzie się w funkcji blitme funkcją blit
        self.rect = self.image.get_rect()

        # Każdy nowy statek pojawia się na dole ekranu
        #   Generalnie oznacza to, że punkt po lewej stronie (self.rect.midbottom)
        #   znajdzie się w punkcie po drugiej stronie (np. self.screen_rect.midbottom).
        #   Gdyby np. self.rect.midbottom = self.screen_rect.midright, to punkt dolny środkowy obrazka (midbottom)
        #   znajdzie się na środku po prawej stronie ekranu (midright).
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # Opcje wskazujące na poruszanie się statku
        self.moving_right = False
        self.moving_left = False

    def update(self):
        ''' Uaktualnienie pozycji statku na podstawie opcji wskazującej na jego ruch '''
        if self.moving_right and self.rect.right < self.screen_rect.right:  # .right to wartość współrzędnej x prawej krawędzi
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        ''' Wyświetlenie statku w jego aktualnym położeniu '''

        # Dodanie obrazka image na powierzchnię (inny obraz) screen.
        # Dodaje obraz image w miejsce rect
        # Dodaje, czyli nakłada jeden na drugi
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        ''' Umieszczenie statku na śrofku przy dolnej krawędzi ekranu '''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
