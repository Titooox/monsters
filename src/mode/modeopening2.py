import pygame
import jovialengine

import constants
from monster import Monster
from .modeopening3 import ModeOpening3
from .modeopening import ModeOpening


class ModeOpening2(ModeOpening):
    __slots__ = (
        '_time',
        '_fade',
        '_music_started',
        '_music_time',
        '_move_time',
    )

    def __init__(self):
        super().__init__()
        pygame.mixer.music.load(constants.TITLE_INTRO)
        self._music_started = False
        left_mon = Monster.atLevel(3)
        right_mon = Monster.atLevel(2)

        sproing = pygame.mixer.Sound(constants.SPROING)
        ground_level = constants.SCREEN_SIZE[1] - 32
        # starts at right
        left_mon.rect.bottomright = (constants.SCREEN_SIZE[0], ground_level)
        left_mon.setImage(True)
        # starts at left
        right_mon.rect.bottomleft = (0, ground_level)
        # move to the positions
        beat = 250
        pause = 50
        left_mon.addPosRel(Monster.Lerp, beat * 6, -constants.SCREEN_SIZE[0] // 2, 0)
        right_mon.addPosRel(Monster.Lerp, beat * 6, constants.SCREEN_SIZE[0] // 2, 0,
                            sound=sproing, positional_sound=True)
        self._music_time = beat * 6
        # back and forth
        left_mon.addWait(beat * 8 + pause * 2)
        jump = right_mon.rect.width // 8
        right_mon.addPosRel(Monster.Lerp, beat, jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, jump, jump,
                            sound=sproing, positional_sound=True)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, jump)
        right_mon.addWait(pause, sound=sproing, positional_sound=True)
        right_mon.addPosRel(Monster.Lerp, beat, jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, jump, jump,
                            sound=sproing, positional_sound=True)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, jump)
        right_mon.addWait(pause)
        # small pause
        left_mon.addWait(beat)
        right_mon.addWait(beat)
        # slash!
        left_mon.addPosRel(Monster.Lerp, 100, -jump // 2, -jump // 3)
        left_mon.addPosRel(Monster.Lerp, 200, jump + jump // 2, jump // 3,
                           sound=pygame.mixer.Sound(constants.THUNK), positional_sound=True)
        right_mon.addWait(300)
        # jump back
        left_mon.addWait(beat)
        right_mon.addPosRel(Monster.Lerp, beat // 2, jump * 2, -jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat // 2, jump * 2, jump * 2)
        # pause
        left_mon.addWait(150)
        left_mon.addPosRel(Monster.Lerp, 100, -jump, 0)
        right_mon.addWait(beat * 3,
                          sound=sproing, positional_sound=True)
        # back and forth again
        right_mon.addPosRel(Monster.Lerp, beat, -jump, -jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat, -jump, jump * 2,
                            sound=sproing, positional_sound=True)
        right_mon.addPosRel(Monster.Lerp, beat, jump, -jump * 2)
        right_mon.addPosRel(Monster.Lerp, beat, jump, jump * 2)
        # charge
        right_mon.addWait(beat)
        right_mon.addPosRel(Monster.Lerp, beat, jump // 2, jump // 2)
        # fire
        right_mon.addWait(beat * 2)
        right_mon.addPosRel(Monster.Lerp, beat, -jump * 6 - jump // 2, -jump * 2 - jump // 2,
                            sound=pygame.mixer.Sound(constants.FSSSH))

        # higher layer = draw later = "in front"
        left_mon.layer = 1
        right_mon.layer = 0
        self.all_sprites.add(right_mon, left_mon)
        self._time = 0
        self._move_time = beat * 28 + pause * 2 + 300
        self._fade = pygame.Surface(constants.SCREEN_SIZE).convert(jovialengine.shared.display.screen)
        self._fade.fill(constants.WHITE)
        self._fade.set_alpha(0)

    def _switchMode(self):
        self.next_mode = ModeOpening3()

    def _update(self, dt):
        self._time += dt
        if self._time >= self._music_time and not self._music_started:
            pygame.mixer.music.play(1, 0, 2100)
            self._music_started = True
        if self._time >= self._move_time:
            self._fade.set_alpha(
                min((self._time - self._move_time) * 255 // 750, 255)
            )
        if self._time >= self._move_time + 1500:
            self._stopMixer()
            self._switchMode()

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)

    def _drawPostSprites(self, screen):
        screen.blit(self._fade, (0, 0))
