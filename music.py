import pygame


class Music():
    def __init__(self, settings):
        self.main_menu_music = settings.music_path['menu_music']
        self.game_music = settings.music_path['game_music']
        self.coin_drop = pygame.mixer.Sound(settings.sound_path['coin_drop'])


    def play(self, name):
        if name == 'game':
            # Stop the current music if there is any,
            # and overwrite the mixer_music (music player) with new music
            pygame.mixer_music.stop()
            pygame.mixer_music.load(self.game_music)
            pygame.mixer_music.play(-1)
        elif name == 'menu':
            pygame.mixer_music.stop()
            pygame.mixer_music.load(self.main_menu_music)
            pygame.mixer_music.play(-1)
        elif name == 'coin_drop':
            self.coin_drop.play()