import abc

import pygame

import constants
import shared
import mode
from state import State
from save import Save
from saveable import Saveable


class ModeGameMenu(mode.Mode, abc.ABC):
    MENU_CHAR_WIDTH = 20
    MENU_WIDTH = MENU_CHAR_WIDTH * constants.FONT_SIZE
    SHARED_DISP_TEXT = "Options:\nESC) Go Back\n"

    __slots__ = (
        '_previous_mode',
        '_old_screen',
    )

    def __init__(self, previous_mode, old_screen=None):
        super().__init__()
        self._previous_mode = previous_mode
        if old_screen is None:
            old_screen = self._getOldScreen()
        self._old_screen = old_screen

    def _getOldScreen(self):
        old_screen = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self._previous_mode.draw(old_screen)
        old_screen = pygame.transform.smoothscale(
            pygame.transform.smoothscale(
                old_screen,
                (constants.SCREEN_SIZE[0] * 4 // 5, constants.SCREEN_SIZE[1] * 4 // 5)
            ),
            constants.SCREEN_SIZE
        )
        return old_screen

    def _drawScreen(self, screen):
        screen.blit(self._old_screen, (0, 0))

    @classmethod
    def _drawText(cls, screen, disp_text):
        shared.font_wrap.renderToInside(
            screen,
            (0, 0),
            cls.MENU_WIDTH,
            disp_text,
            False,
            constants.WHITE,
            constants.BLACK
        )


class ModeGameMenuTop(ModeGameMenu):
    def _input(self, event):
        if event.type == pygame.QUIT:
            shared.game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_mode = self._previous_mode
            elif event.key == pygame.K_1:
                self.next_mode = ModeGameMenuSave(self._previous_mode, self._old_screen)
            elif event.key == pygame.K_2:
                self.next_mode = ModeGameMenuLoad(self._previous_mode, self._old_screen)
            elif event.key == pygame.K_3:
                self.next_mode = ModeGameMenuOptions(self._previous_mode, self._old_screen)
            elif event.key == pygame.K_4:
                self._stopMixer()
                shared.state = State()
                self._previous_mode = mode.ModeOpening0()
                pygame.mixer.music.pause()
                pygame.mixer.pause()
                self._old_screen = self._getOldScreen()
            elif event.key == pygame.K_5:
                shared.game_running = False

    def _drawScreen(self, screen):
        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        disp_text += "1) Save\n2) Load\n3) Options\n4) Restart\n5) Quit"
        self._drawText(screen, disp_text)


class ModeGameMenuSave(ModeGameMenu):
    FILE_EXT = '.sav'

    __slots__ = (
        '_save_name',
        '_cursor_position',
        '_confirm_overwrite',
        '_save_success',
        '_cursor_switch',
        '_cursor_timer',
    )

    def __init__(self, previous_mode, old_screen=None):
        super().__init__(previous_mode, old_screen)
        self._save_name = ''
        self._resetCursorBlink()
        self._cursor_position = 0
        self._confirm_overwrite = False
        self._save_success = None

    def _resetCursorBlink(self):
        self._cursor_switch = True
        self._cursor_timer = 0

    def _input(self, event):
        if event.type == pygame.QUIT:
            self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
        elif event.type == pygame.KEYDOWN:
            char = event.unicode
            length = len(self._save_name)
            if self._save_success:
                self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
            elif event.key == pygame.K_ESCAPE:
                if self._confirm_overwrite:
                    self._confirm_overwrite = False
                    self._save_success = None
                else:
                    self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
            elif event.key == pygame.K_RETURN:
                if self._save_name and isinstance(self._previous_mode, Saveable):
                    if Save.willOverwrite(self._save_name + self.FILE_EXT) and not self._confirm_overwrite:
                        self._confirm_overwrite = True
                    elif not self._save_success:
                        new_save = Save.getFromMode(self._save_name + self.FILE_EXT, self._previous_mode)
                        self._save_success = new_save.save()
            elif event.key == pygame.K_LEFT:
                self._cursor_position = max(self._cursor_position - 1, 0)
                self._resetCursorBlink()
            elif event.key == pygame.K_RIGHT:
                self._cursor_position = min(self._cursor_position + 1, length)
                self._resetCursorBlink()
            elif event.key in (pygame.K_UP, pygame.K_HOME):
                self._cursor_position = 0
                self._resetCursorBlink()
            elif event.key in (pygame.K_DOWN, pygame.K_END):
                self._cursor_position = length
                self._resetCursorBlink()
            elif event.key == pygame.K_DELETE:
                self._save_name = self._save_name[:self._cursor_position] + self._save_name[self._cursor_position + 1:]
                self._resetCursorBlink()
            elif event.key == pygame.K_BACKSPACE:
                if self._cursor_position > 0:
                    self._save_name = self._save_name[:self._cursor_position - 1] \
                        + self._save_name[self._cursor_position:]
                    self._cursor_position -= 1
                self._resetCursorBlink()
            elif (
                length < (self.MENU_CHAR_WIDTH - len(self.FILE_EXT) - 1)
                and (
                    # numbers
                    ('0' <= char <= '9')
                    # or letters
                    or (96 < event.key < 123)
                )
            ):
                self._save_name = self._save_name[:self._cursor_position] \
                    + char \
                    + self._save_name[self._cursor_position:]
                self._cursor_position += 1
                self._resetCursorBlink()

    def _update(self, dt):
        self._cursor_timer += dt
        if self._cursor_timer >= constants.CURSOR_TIME:
            self._cursor_switch = not self._cursor_switch
            self._cursor_timer -= constants.CURSOR_TIME

    def _drawScreen(self, screen):
        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        if not isinstance(self._previous_mode, Saveable):
            disp_text += "\nYou can't save now."
        elif not self._save_success:
            disp_text += "ENTER) Save\nType a file name:\n>"
            if self._save_name:
                disp_text += self._save_name
            disp_text += self.FILE_EXT
            if self._confirm_overwrite and self._save_success is None:
                disp_text += "\nThis will overwrite an existing save file." \
                    + "\nPress ENTER again to confirm, or ESC to go back."
            elif self._save_success is False:
                disp_text += "\nSave failed.\nPress ENTER to try again, or ESC to go back."
        else:
            disp_text += "\nSaved successfully.\nPress any key to go back."
        self._drawText(screen, disp_text)
        if self._cursor_switch and not self._confirm_overwrite and self._save_success is None:
            screen.fill(
                constants.WHITE,
                (
                    ((self._cursor_position + 1) * constants.FONT_SIZE, 4 * constants.FONT_HEIGHT),
                    (1, constants.FONT_HEIGHT)
                )
            )


class ModeGameMenuLoad(ModeGameMenu):
    __slots__ = (
        '_saves',
        '_save_index',
        '_loaded_save',
        '_confirm_delete',
        '_deleted_save',
    )

    def __init__(self, previous_mode, old_screen=None):
        super().__init__(previous_mode, old_screen)
        self._saves = Save.getAllFromFiles()
        self._save_index = 0
        self._loaded_save = False
        self._confirm_delete = False
        self._deleted_save = False

    def _input(self, event):
        if event.type == pygame.QUIT:
            self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or self._loaded_save:
                self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
            elif self._deleted_save:
                self._deleted_save = False
            elif self._confirm_delete:
                if event.key == pygame.K_RETURN:
                    self._confirm_delete = False
                    self._saves[self._save_index].delete()
                    del self._saves[self._save_index]
                    self._save_index = max(0, min(len(self._saves) - 1, self._save_index))
                    self._deleted_save = True
                else:
                    self._confirm_delete = False
            elif len(self._saves) > 0:
                if event.key in (pygame.K_UP, pygame.K_LEFT):
                    self._save_index = max(self._save_index - 1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                    self._save_index = min(self._save_index + 1, len(self._saves) - 1)
                elif event.key == pygame.K_RETURN:
                    self._stopMixer()
                    self._previous_mode = self._saves[self._save_index].load()
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                    self._old_screen = self._getOldScreen()
                    self._loaded_save = True
                elif event.key == pygame.K_DELETE:
                    self._confirm_delete = True

    def _drawScreen(self, screen):
        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        if len(self._saves) == 0:
            disp_text += "\nThere are no save files to select from."
        elif self._loaded_save:
            disp_text += "\nLoaded successfully.\nPress any key to go back."
        elif self._confirm_delete:
            disp_text += "\nThis will delete an existing save file." \
                + "\nPress ENTER to confirm, or any other key to go back."
        elif self._deleted_save:
            disp_text += "\nDeleted successfully.\nPress any key to continue."
        else:
            disp_text += "ENTER) Load\nDEL) Delete\nARROW KEYS) Select a file:"
            for i in range(-1, 2):
                disp_text += "\n"
                this_index = self._save_index + i
                if i == 0:
                    disp_text += ">"
                else:
                    disp_text += "_"
                if 0 <= this_index < len(self._saves):
                    disp_text += self._saves[this_index].file_name
        self._drawText(screen, disp_text)


class ModeGameMenuOptions(ModeGameMenu):
    def _input(self, event):
        if event.type == pygame.QUIT:
            self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
        elif event.type == pygame.KEYUP:
            if event.key in (
                    pygame.K_DOWN, pygame.K_s,
                    pygame.K_LEFT, pygame.K_a,
                    pygame.K_PAGEDOWN, pygame.K_MINUS,
            ):
                shared.display.changeScale(-1)
            elif event.key in (
                    pygame.K_UP, pygame.K_w,
                    pygame.K_RIGHT, pygame.K_d,
                    pygame.K_PAGEUP, pygame.K_EQUALS,
            ):
                shared.display.changeScale(1)
            elif event.key in (pygame.K_f, pygame.K_F11,):
                shared.display.toggleFullscreen()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_mode = ModeGameMenuTop(self._previous_mode, self._old_screen)
            elif '1' <= event.unicode <= '9':
                target_scale = int(event.unicode)
                shared.display.setScale(target_scale)

    def _drawScreen(self, screen):
        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        disp_text += f"ARROWS) Upscaling: {shared.display.upscale}" \
                     f"\nF) Fullscreen: {self.getTickBox(shared.display.is_fullscreen)}"
        self._drawText(screen, disp_text)

    @staticmethod
    def getTickBox(value: bool):
        inside = "X" if value else "_"
        return f"[{inside}]"
