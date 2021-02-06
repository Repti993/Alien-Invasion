import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from menu import Menu


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

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Pociski są przechowywane w grupie
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Utworzenie przycisku "Zacznij grę"
        self.main_menu = Menu(self, "Main menu")
        self.game_over_menu = Menu(self, "Game over!")
        self.choice_menu = Menu(self, "Choose ship")
        # self.play_button = Button(self, "Zacznij grę")

    def run_game(self):
        ''' Rozpoczęcie głównej pętli gry '''
        while True:
            self._check_events()  # Sprawdza zdarzenia generowane przez klawiaturę i mysz

            if self.stats.menu_dict['game']:
                self.ship.update()  # Przesuwa odpowiednio statek
                self._update_bullets()  # Przesuwa wszystkie pociski, usuwa te poza ekranem
                self._update_aliens()  # Przesuwa obcych

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

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

    def _ship_hit(self):
        ''' Reakcja na uderzenie obcego w statek '''
        if self.stats.ships_left > 1:
            # Zmniejszenie wartości przechowywanej w ships_left i wyświetlenie
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()

            # Utworzenie nowej floty i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()

            # Pauza
            sleep(self.settings.lost_game_pause_time)

        else:
            self.stats.set_active_menu('game over')

            # Ponowne wyświetlanie kursora
            pygame.mouse.set_visible(True)

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        ''' Reakcja na kolizję między pociskiem i obcym '''
        # Sprawdzenie, czy któryś pocisk trafił obcego
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True
                                                )

        if collisions:
            for aliens in collisions.values():
                # aliens to lista trafionych obcych przez ten sam pocisk
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Sprawdzenie, czy pozostali jacyś obcy
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Inkrementacja numeru poziomu
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        ''' Uaktualnienie położenia wzystkich obcych we flocie '''
        self._check_fleet_edges()
        self.aliens.update()

        # Wykrywanie kolizji między obcym i graczem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Wyszukiwanie obcych docierających do dolnej krawędzi ekranu
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        ''' Sprawdzenie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu '''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Tak samo jak w przypadku zderzenia statku z obcym
                self._ship_hit()
                break

    def _update_screen(self):
        ''' Uaktualnienie obrazów na ekranie i przejście do nowego ekranu '''
        self.screen.fill(self.settings.bg_color)  # Kolor tła

        if self.stats.menu_dict['game'] or self.stats.menu_dict['game over']:
            self.ship.blitme()  # Pozycja statku
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            # Wyświetlenie informacji o punktacji
            self.sb.show_score()

        # Wyświetla odpowiednie menu
        if self.stats.menu_dict['main']:
            self.main_menu.draw_menu()
        elif self.stats.menu_dict['game over']:
            self.game_over_menu.draw_menu()

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

    def _check_fleet_edges(self):
        ''' Reakcja na dotarcie obcych do krawędzi'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Zmiana kierunku i ruch w dół '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_buttons(self, mouse_pos):
        ''' Sprawdza kliknięty przycisk w zależności od menu '''
        if self.stats.menu_dict['main']:
            if self.main_menu.buttons['Play game'].rect.collidepoint(mouse_pos):
                self._play_button_clicked()
            # elif self.main_menu.buttons['Choose ship'].rect.collidepoint(mouse_pos):
            #    self._choose_ship_button_clicked()
            elif self.main_menu.buttons['Exit'].rect.collidepoint(mouse_pos):
                sys.exit()
        elif self.stats.menu_dict['game over']:
            if self.game_over_menu.buttons['Play again'].rect.collidepoint(mouse_pos):
                self._play_button_clicked()
            elif self.game_over_menu.buttons['Return to main menu'].rect.collidepoint(mouse_pos):
                self._return_button_clicked()
            elif self.game_over_menu.buttons['Exit'].rect.collidepoint(mouse_pos):
                sys.exit()

    def _play_button_clicked(self):
        ''' Funkcja obsługuje przyciski Play game oraz Play again'''

        # Wyzerowanie danych statatystycznych gry
        self.stats.reset_stats()
        self.stats.set_active_menu('game')

        # Wyzerowanie ustawień dynamicznych gry
        self.settings.initialize_dynamic_settings()

        # Aktualizacja wyświetlanych informacji o wyniku i poziomie
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Usuwanie zawartości list aliens i bullets
        self.aliens.empty()
        self.bullets.empty()

        # Utworzenie nowej floty i wyśrodkowanie statku
        self._create_fleet()
        self.ship.center_ship()

        # Ukrycie kursora myszy
        pygame.mouse.set_visible(False)

    def _choose_ship_button_clicked(self):
        ''' Funkcja obsługuje przycisk Choose ship'''
        self.stats.set_active_menu('choice')

    def _return_button_clicked(self):
        ''' Funkcja obsługuje przycisk Return to the main menu'''
        self.stats.set_active_menu('main')


if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()
