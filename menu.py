import pygame.font
from button import Button


class Menu():
    def __init__(self, ai_game, title):
        ''' Inicjalizacja pojedynczej strony menu'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Zdefiniowanie wymiarów
        self.width = 400
        self.height = 600

        # Utworzenie prostokąta przycisku i wyśrodkowanie
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Czcionka
        self.menu_color = (150, 150, 150)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Utworzenie tytułu menu
        self._make_menu(ai_game, title)

    def _make_menu(self, ai_game, title):
        ''' Tworzy odpowiednie menu na podstawie nazwy'''

        # Stworzenie tytułu
        self._make_title(title)

        # Stworzenie przycisków dla odpowiedniego menu
        if title == "Main menu":
            self.buttons = {
                'Play game': Button(self, "Play game", 1),
                'Choose ship': Button(self, "Choose ship", 2),
                'Exit': Button(self, "Exit", 6)
            }
        elif title == "Game over!":
            self.buttons = {
                'Play again': Button(self, "Play again", 4),
                'Return to main menu': Button(self, "Return to main menu", 5),
                'Exit': Button(self, "Exit", 6)
            }

    def _make_title(self, title):
        ''' Stworzenie tytułu na górze menu'''
        self.title_image = self.font.render(title, True, self.text_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.midtop = self.rect.midtop
        self.title_image_rect.y += 20

    def draw_menu(self):
        ''' Wyświetlenie menu'''
        self.screen.fill(self.menu_color, self.rect)
        self.screen.blit(self.title_image, self.title_image_rect)

        # Wyświetlenie każdego przycisku
        for button in self.buttons.values():
            button.draw_button()
