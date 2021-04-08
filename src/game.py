import pygame

import constants
import shared
from modegamemenu import ModeGameMenu
from modeopening import ModeOpening
#from modetest import ModeTest

class Game(object):
    __slots__ = (
        '_max_framerate',
        '_clock',
        '_current_mode',
    )

    def __init__(self, max_framerate):
        """Start and create things as needed."""
        pygame.init()
        # time
        self._max_framerate = max_framerate
        self._clock = pygame.time.Clock()
        # mode (must be set before running)
        self._current_mode = ModeOpening()
        # test stuff
        #self._current_mode = ModeTest()

    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()

    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self._current_mode:
            raise RuntimeError("error: no current mode")
        self._current_mode.input_events(
            self._filterInput(pygame.event.get())
        )
        self._current_mode.update(
            self._getTime()
        )
        self._current_mode.draw()
        shared.display.scaleDraw()
        if self._current_mode.next_mode is not None:
            self._current_mode = self._current_mode.next_mode
        return shared.game_running

    def _filterInput(self, events):
        """Take care of input that game modes should not take care of."""
        return map(self._scaleMouseInput, filter(self._stillNeedsHandling, events))

    def _stillNeedsHandling(self, event):
        """If event should be handled before all others, handle it and return False, otherwise return True.
        As an example, game-ending or display-changing events should be handled before all others.
        """
        if event.type == pygame.QUIT:
            return self._handleQuit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self._handleQuit()
            # window re-sizing stuff
            elif event.key in (pygame.K_PAGEUP, pygame.K_PERIOD):
                if not shared.display.is_fullscreen:
                    shared.display.screenSet(1)
                return False
            elif event.key in (pygame.K_PAGEDOWN, pygame.K_COMMA):
                if not shared.display.is_fullscreen:
                    shared.display.screenSet(-1)
                return False
            elif event.key in (pygame.K_F11, pygame.K_TAB):
                if shared.display.is_fullscreen:
                    shared.display.screenSet(0)
                else:
                    shared.display.screenSetFullscreen()
                return False
        return True

    def _handleQuit(self):
        # pass quit events forward to the ModeGameMenu, but not to other events
        if isinstance(self._current_mode, ModeGameMenu):
            return True
        self._current_mode = ModeGameMenu(self._current_mode)
        return False

    def _scaleMouseInput(self, event):
        """Scale mouse position for events in terms of the screen (as opposed to the display surface)."""
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if shared.display.is_fullscreen:
                event_dict = {
                    'pos': (
                        (event.pos[0] - shared.display.fullscreen_offset[0]) // shared.display.upscale_max,
                        (event.pos[1] - shared.display.fullscreen_offset[1]) // shared.display.upscale_max,
                    )
                }
            else:
                event_dict = {
                    'pos': (
                        event.pos[0] // shared.display.upscale,
                        event.pos[1] // shared.display.upscale,
                    )
                }
            if event.type == pygame.MOUSEMOTION:
                event_dict['rel'] = event.rel
                event_dict['buttons'] = event.buttons
            else:
                event_dict['button'] = event.button
            return pygame.event.Event(event.type, event_dict)
        return event

    def _getTime(self):
        """Take care of time stuff."""
        pygame.display.set_caption(str(self._clock.get_fps()))# just for debugging purposes
        return self._clock.tick(self._max_framerate)
