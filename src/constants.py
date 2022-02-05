import sys
import os

import pygame


SCREEN_CAPTION = "CHIKKAI!"
SCREEN_SIZE = (320, 180)
SCREEN_CENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
SCREEN_RECT = pygame.Rect((0, 0), SCREEN_SIZE)
CURSOR_TIME = 500
FONT_SIZE = 8
FONT_HEIGHT = 10
TEXT_COLOR = (164, 162, 165)
DARK_TEXT_COLOR = (82, 81, 83)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORKEY = (255, 0, 255)
SAVE_EXT = '.sav'

_location = '.'
if getattr(sys, 'frozen', False):
    _location = sys.executable
elif __file__:
    _location = __file__
SRC_DIRECTORY = os.path.dirname(_location)

ASSETS_DIRECTORY = os.path.join(SRC_DIRECTORY, 'assets')

GRAPHICS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'gfx')
FONT = os.path.join(GRAPHICS_DIRECTORY, 'simple_mono.ttf')

ICONS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'icons')
WINDOW_ICON = os.path.join(ICONS_DIRECTORY, 'icon.png')

LOGOS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'logos')
JK_LOGO_BLACK = os.path.join(LOGOS_DIRECTORY, 'jklogo_black.png')
JK_LOGO_GREY = os.path.join(LOGOS_DIRECTORY, 'jklogo_grey.png')
JK_LOGO_LIGHT_GREY = os.path.join(LOGOS_DIRECTORY, 'jklogo_light_grey.png')
STAR = os.path.join(LOGOS_DIRECTORY, 'star.png')
TIN_LOGO = os.path.join(LOGOS_DIRECTORY, 'tin_logo.png')
CHIKKAI_LOGO = os.path.join(LOGOS_DIRECTORY, 'chikkai_logo.png')

BACKGROUNDS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'backgrounds')
BLACKBOX_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'blackbox.png')
HEALTHBAR_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'healthbar.png')
LAYOUT_1_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout1boxes.png')
LAYOUT_2_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout2boxes.png')

MONSTER_PARTS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'monster-parts')

SOUND_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'sfx')
THUNK = os.path.join(SOUND_DIRECTORY, 'thunk.wav')
SPROING = os.path.join(SOUND_DIRECTORY, 'sproing.wav')
FSSSH = os.path.join(SOUND_DIRECTORY, 'fsssh.wav')
BIP = os.path.join(SOUND_DIRECTORY, 'bip.wav')
LONGSLIDE = os.path.join(SOUND_DIRECTORY, 'longslide.wav')
ROOEEE = os.path.join(SOUND_DIRECTORY, 'rooeee.wav')
BWOP = os.path.join(SOUND_DIRECTORY, 'bwop.wav')

MUSIC_DIRECTORY = os.path.join(SOUND_DIRECTORY, 'music')
TITLE_INTRO = os.path.join(MUSIC_DIRECTORY, 'title_intro.ogg')
CHAT_LOOP = os.path.join(MUSIC_DIRECTORY, 'chat_loop.ogg')
FIGHT_LOOP = os.path.join(MUSIC_DIRECTORY, 'fight_loop.ogg')

TEXT_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'txt')
CREDITS_TEXT = os.path.join(TEXT_DIRECTORY, 'credits.txt')
CONVO_DIRECTORY = os.path.join(TEXT_DIRECTORY, 'convos')

SAVE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'saves')

IMAGE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'images')

CONFIG_FILE = os.path.join(SRC_DIRECTORY, 'config.ini')
CONFIG_SECTION = 'Game'
CONFIG_MAX_FRAMERATE = 'MaxFramerate'
CONFIG_FULLSCREEN = 'Fullscreen'
CONFIG_SCREEN_SCALE = 'ScreenScale'
CONFIG_DEFAULTS = {
    CONFIG_MAX_FRAMERATE: 0,
    CONFIG_SCREEN_SCALE: 4,
    CONFIG_FULLSCREEN: False,
}
