import pygame


class Music():
    """Music player class."""

    def __init__(self, settings):
        """Load music and sound files."""
        self.main_menu_music = settings.music_path['menu_music']
        self.game_music = settings.music_path['game_music']
        self.coin_drop = pygame.mixer.Sound(settings.sound_path['coin_drop'])
        self.plate = pygame.mixer.Sound(settings.sound_path['plate'])
        self.bell = pygame.mixer.Sound(settings.sound_path['bell'])
        self.door_open = pygame.mixer.Sound(settings.sound_path['door_open'])
        self.door_close = pygame.mixer.Sound(settings.sound_path['door_close'])

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
        elif name == 'plate':
            self.plate.play()
        elif name == 'bell':
            self.bell.play()
        elif name == 'door_open':
            self.door_open.play()
        elif name == 'door_close':
            self.door_close.play()