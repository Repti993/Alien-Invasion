import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    ''' Klasa przeznaczona do zarządzania zasobami i sposobem działania gry '''

    def __init__(self):
        ''' Inicjalizacja gry i utworzenie jej zasobów '''
        pygame.init()
        self.settings = Settings()

        # Wyswietlanie pełnoekranowe:
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Wyswietlanie w oknie:
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))  # podwójny nawias, ten środkowy to krotka, czyli przekazujemy jeden argument - krotkę

        # Nazwa okna
        pygame.display.set_caption("Inwazja obcych")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Pociski są przechowywane w grupie
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        ''' Rozpoczęcie głównej pętli gry '''
        while True:
            self._check_events()  # Sprawdza zdarzenia generowane przez klawiaturę i mysz
            self.ship.update()  # Przesuwa odpowiednio statek
            self._update_bullets()  # Przesuwa wszystkie pociski, usuwa te poza ekranem

            self._update_screen()  # Aktualizuje wyświetlane informacje

    def _check_events(self):
        ''' Reakcja na zdarzenia generowane przez klawiaturę i mysz '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        ''' Reakcja na wciśnięcie klawisza '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        ''' Reakcja na zwolnienie klawisza '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        ''' Utworzenie nowego pocisku i dodanie go do grupy pocisków '''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        ''' Uaktualnienie położenia pocisków i usunięcie tych poza ekranem '''
        # Przesuwa odpowiednio pociski | metoda update() jest wywoływana dla każdego elemetu sprite w grupie bullets
        self.bullets.update()

        # Usunięcie pocisków, które znajdują się poza ekranem
        #   Nie możemy zmieniać wielkości listy, więc operacje przeprowadzamy na kopii...
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                #   ... ale obiekty usuwamy z oryginalnej listy
                self.bullets.remove(bullet)
        # print(len(self.bullets)) # informacja o liczbie pocisków na ekranie

    def _update_screen(self):
        ''' Uaktualnienie obrazów na ekranie i przejście do nowego ekranu '''
        self.screen.fill(self.settings.bg_color)  # Kolor tła
        self.ship.blitme()  # Pozycja statku
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Wyświelenie ostatnio zmodyfikowanego ekranu
        pygame.display.flip()

    def _create_fleet(self):
        ''' Utworzenie pełnej floty obcych '''
        # Utworzenie obcego
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size  # zwraca krotkę (w, h)

        # Określenie liczby obcych w rzędzie
        available_space_x = self.settings.screen_width - \
            (2 * alien_width)  # dwa marginesy szerokości obcego
        number_aliens_x = available_space_x // (
            (1 + self.settings.space_between_aliens_x) * alien_width)  # uwzględnienie przestrzeni między obcymi

        # Okreslenie liczby rzędów
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (4 * alien_height) - ship_height)
        number_rows = available_space_y // ((1 +
                                             self.settings.space_between_aliens_y) * alien_height)

        # Utworzenie floty obcych
        for row_number in range(int(number_rows)):
            for alien_number in range(int(number_aliens_x)):
                # Utworzenie obcego i umieszczenie go w rzędzie
                self._create_alien(alien_number, row_number)

        self.aliens.add(alien)

    def _create_alien(self, alien_number, row_number):
        ''' Utworzenie obcego i umieszczenie go w rzędzie '''
        alien = Alien(self)
        # alien_width = alien.rect.width
        alien_width, alien_height = alien.rect.size  # zwraca krotkę (w, h)
        alien.x = alien_width + \
            (1 + self.settings.space_between_aliens_x) * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height // 2) + (1 +
                                                   self.settings.space_between_aliens_y) * alien.rect.height * row_number
        self.aliens.add(alien)


if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()
