import pygame

class Music():
    def __init__(self, settings):
        # self.main_menu_music = pygame.mixer.music.load(settings.music_path['menu_music'])
        # self.game_music = pygame.mixer.music.load(settings.music_path['game_music'])

        self.main_menu_music = pygame.mixer.Sound(settings.music_path['menu_music'])
        self.game_music = pygame.mixer.Sound(settings.music_path['game_music'])
        self.coin_drop = pygame.mixer.Sound(settings.sound_path['coin_drop'])

    def play(self, name):
        if name == 'game':
            self.game_music.play(-1)
        elif name == 'menu':
            self.main_menu_music.play(-1)
        elif name == 'coin_drop':
            self.coin_drop.play()
