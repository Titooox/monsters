import abc
from collections import deque

import pygame

import constants
import shared
from .modeopening import ModeOpening


class ModeLevelUp(ModeOpening, abc.ABC):
    __slots__ = (
        '_done',
        '_time',
        '_background',
        '_first_sprite',
        '_sprite_switches',
    )

    def _drawFontEffect(self, text: str, pos: tuple[int, int]):
        shared.font_wrap.renderToCentered(
            self._background,
            (pos[0] + 1, pos[1] + 1),
            text,
            False,
            constants.TEXT_COLOR
        )
        shared.font_wrap.renderToCentered(
            self._background,
            (pos[0], pos[1]),
            text,
            False,
            constants.DARK_TEXT_COLOR
        )

    def __init__(self):
        super().__init__()
        self._done = False
        self._time = 0
        self._background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self._background.fill(constants.WHITE)
        self._drawFontEffect("LEVEL UP", (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4))
        shared.state.protag_mon.setImage(True)
        # set up first sprite
        self._first_sprite = pygame.sprite.DirtySprite()
        self._first_sprite.image = shared.state.protag_mon.image
        self._first_sprite.rect = shared.state.protag_mon.rect
        self._first_sprite.rect.center = (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 2 // 3)
        # level up and set up second sprite
        shared.state.protag_mon.levelUp()
        shared.state.protag_mon.setImage(True)
        shared.state.protag_mon.rect.midbottom = self._first_sprite.rect.midbottom
        self.all_sprites.add(self._first_sprite, shared.state.protag_mon)

        shared.state.protag_mon.visible = 0

        self._sprite_switches = deque((
            4000,
            4100,
            6000,
            6100,
            8000,
            8100,
            10000,
            10100,
            11000,
            11100,
            12000,
            12100,
            13000,
            13100,
            14000,
            14500,
            15000,
            15750,
            16000,
        ))

    def _input(self, event):
        if self._time >= 16000:
            super()._input(event)
        pass

    def _update(self, dt):
        self._time += dt
        while self._sprite_switches and self._time >= self._sprite_switches[0]:
            self._switchVisibleSprite()
            self._sprite_switches.popleft()
        if not self._sprite_switches and not self._done:
            self._done = True
            self._drawFontEffect(
                "PRESS ANY KEY TO PROCEED",
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4 + 2 * constants.FONT_HEIGHT)
            )

    def _switchVisibleSprite(self):
        if self._first_sprite.visible:
            self._first_sprite.visible = 0
            shared.state.protag_mon.visible = 1
        else:
            self._first_sprite.visible = 1
            shared.state.protag_mon.visible = 0

    def _drawScreen(self, screen):
        screen.blit(self._background, (0, 0))