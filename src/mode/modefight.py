import random
from collections import deque

import pygame

import constants
import shared
import utility
from animsprite import AnimSprite
from monster import Monster

from .mode import Mode
from .modebuttons import ModeButtons


class ModeFight(ModeButtons):
    buttons = (
        pygame.Rect(24, 24, 88, 36),
        pygame.Rect(24, 76, 88, 36),
        pygame.Rect(24, 128, 88, 36),
    )
    _back_keys = {
        pygame.K_UP,
        pygame.K_LEFT,
        pygame.K_w,
        pygame.K_a,
    }
    _forward_keys = {
        pygame.K_DOWN,
        pygame.K_RIGHT,
        pygame.K_s,
        pygame.K_d,
    }
    _health_bar = pygame.image.load(constants.HEALTHBAR_FILE).convert(shared.display.screen)
    _health_bar.set_colorkey(constants.COLORKEY)
    _PLAYER_POS = (170, 128)
    _ENEMY_POS = (262, 128)
    _ANIM_WAIT = 250
    _HEALTH_BAR_LENGTH = 60
    _BOX_CHOICES = [
        "Attack",
        "Defend",
        "Escape",
    ]

    __slots__ = (
        '_background',
        '_thunk',
        '_rooeee',
        '_bwop',
        '_player_mon',
        '_enemy_mon',
        '_player_action',
        '_enemy_action',
        '_action_display',
        '_action_set',
        '_result_displayed',
        '_result',
        '_result_mode',
    )

    def __init__(self, player_mon: Monster, enemy_mon: Monster, draw_mode: Mode, win_mode: Mode, lose_mode: Mode):
        """The functions passed in should return the next mode."""
        super().__init__()

        self._background = pygame.image.load(constants.LAYOUT_2_FILE)
        for index, choice in enumerate(self._BOX_CHOICES):
            shared.font_wrap.renderToInside(
                self._background,
                self._textStart(index),
                self._textWidth(index),
                choice,
                False,
                constants.TEXT_COLOR
            )
        self._background = self._background.convert(shared.display.screen)
        self._background.set_colorkey(constants.COLORKEY)

        pygame.mixer.music.load(constants.FIGHT_LOOP)
        pygame.mixer.music.play(-1)

        self._thunk = pygame.mixer.Sound(constants.THUNK)
        self._rooeee = pygame.mixer.Sound(constants.ROOEEE)
        self._bwop = pygame.mixer.Sound(constants.BWOP)

        self._player_mon = player_mon
        self._enemy_mon = enemy_mon

        self._player_mon.fightStart()
        self._player_mon.setImage(True)

        self._player_mon.rect.midbottom = self._PLAYER_POS
        self._enemy_mon.rect.midbottom = self._ENEMY_POS
        self.all_sprites.add(self._player_mon, self._enemy_mon)

        self._player_action = False
        self._enemy_action = False

        self._action_display = deque((), 4)
        self._action_set = False

        self._result_displayed = 0

        self._result = False
        self._result_mode = {
            'draw': draw_mode,
            'win': win_mode,
            'lose': lose_mode,
        }

    def _buttonPress(self):
        self._player_action = self._BOX_CHOICES[self._selected_button]
        self._enemy_action = random.choice(('Attack', 'Defend'))

        if self._player_action == 'Attack':
            self._setActionDisplay("I'm gonna hit 'em!")
            self._player_mon.addWait(self._ANIM_WAIT)
            self._player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0,
                                       sound=self._thunk, positional_sound=True)
            self._player_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
        elif self._player_action == 'Defend':
            self._setActionDisplay("I'm gonna block 'em!")
            self._player_mon.addWait(self._ANIM_WAIT)
            self._player_mon.addPosRel(AnimSprite.Lerp, 133, -8, 0,
                                       sound=self._bwop, positional_sound=True)
            self._player_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
            self._player_mon.addPosRel(AnimSprite.Lerp, 67, -4, 0)
        elif self._player_action == 'Escape':
            self._setActionDisplay("I'm gonna run away!")
            self._player_mon.addWait(self._ANIM_WAIT)
            self._player_mon.addWait(0, sound=self._rooeee, positional_sound=True)
            self._player_mon.addPosRel(AnimSprite.Lerp, 333, -20, 0)
            self._player_mon.addPosRel(AnimSprite.Lerp, 67, 20, 0)

        if self._enemy_action == 'Attack':
            self._enemy_mon.addWait(self._ANIM_WAIT)
            self._enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0,
                                      sound=self._thunk, positional_sound=True)
            self._enemy_mon.addPosRel(AnimSprite.Lerp, 200, 12, 0)
        elif self._enemy_action == 'Defend':
            self._enemy_mon.addWait(self._ANIM_WAIT)
            self._enemy_mon.addPosRel(AnimSprite.Lerp, 133, 8, 0,
                                      sound=self._bwop, positional_sound=True)
            self._enemy_mon.addPosRel(AnimSprite.Lerp, 200, -12, 0)
            self._enemy_mon.addPosRel(AnimSprite.Lerp, 67, 4, 0)

    def _input(self, event):
        # click forward to next mode
        if self._result:
            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                self._stopMixer()
                self.next_mode = self._result_mode[self._result]()
                return
        # in the middle of action display
        if self._player_action:
            return
        super()._input(event)
        # testing stuff, remove later
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                print("_player_mon.stats = " + str(self._player_mon.stats))
                print("_enemy_mon.stats = " + str(self._enemy_mon.stats))

    def _setActionDisplay(self, text: str):
        self._action_display.appendleft(shared.font_wrap.renderInside(200, text, False, constants.TEXT_COLOR))
        self._action_set = not self._action_set

    def _playerActionDone(self):
        player_attack_defend = self._player_mon.fightHit(self._player_action)
        enemy_attack_defend = self._enemy_mon.fightHit(self._enemy_action)
        damage_to_player = utility.reduceNumber(
            max(
                0,
                enemy_attack_defend[0] - player_attack_defend[1]
            ),
            2
        )
        damage_to_enemy = utility.reduceNumber(
            max(
                0,
                player_attack_defend[0] - enemy_attack_defend[1]
            ),
            2
        )
        if damage_to_player == 0 and damage_to_enemy == 0:
            damage_to_player = damage_to_enemy = 1
        # display results below
        self._setActionDisplay("Hit for " + str(damage_to_enemy) + "! Took " + str(damage_to_player) + "!")
        self._player_mon.stats['hpc'] -= damage_to_player
        self._enemy_mon.stats['hpc'] -= damage_to_enemy

        if self._player_mon.stats['hpc'] < 1 and self._enemy_mon.stats['hpc'] < 1:
            self._setupEnd('draw')
        elif self._enemy_mon.stats['hpc'] < 1:
            self._setupEnd('win')
        elif self._player_mon.stats['hpc'] < 1:
            self._setupEnd('lose')
        else:
            self._player_action = False
        self._enemy_action = False

    def _setupEnd(self, ending: str):
        self._player_action = ending
        self._player_mon.addWait(500)
        self._player_mon.addWait(500)
        pygame.mixer.music.fadeout(1000)

    def _update(self, dt):
        if self._player_action in self._BOX_CHOICES and not self._player_mon.stillAnimating():
            self._playerActionDone()
        elif self._player_action == 'draw':
            self._endStuff("They're both out cold.")
        elif self._player_action == 'win':
            self._endStuff("I won!!!")
        elif self._player_action == 'lose':
            self._endStuff(self._player_mon.name + "'s out cold.")

    def _endStuff(self, result_display: str):
        if len(self._player_mon.anims) < 2 and self._result_displayed < 1:
            self._setActionDisplay(result_display)
            self._result_displayed = 1
        elif not self._player_mon.stillAnimating() and self._result_displayed < 2:
            self._setActionDisplay("Click or press enter to")
            self._setActionDisplay("continue.")
            self._result_displayed = 2
            self._result = self._player_action

    def _drawScreen(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self._background, (0, 0))
        if not self._action_set and self._player_action not in self._result_mode:
            self._drawSelected(screen)

        player_bar_length = self._HEALTH_BAR_LENGTH \
            * self._player_mon.stats['hpc'] // self._player_mon.stats['hpm']
        screen.fill(self._player_mon.getLightSkin(), (138, 30, player_bar_length, 10))
        screen.blit(self._health_bar, (137, 29))

        enemy_bar_length = self._HEALTH_BAR_LENGTH \
            * self._enemy_mon.stats['hpc'] // self._enemy_mon.stats['hpm']
        screen.fill(self._enemy_mon.getLightSkin(), (294 - enemy_bar_length, 30, enemy_bar_length, 10))
        screen.blit(self._health_bar, (233, 29))
        # maybe draw health numbers / stats / etc
        for index, line in enumerate(self._action_display):
            screen.blit(line, (120, 166 - constants.FONT_HEIGHT * index))
