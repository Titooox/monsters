import os

import pygame

import constants

class Display(object):
    __slots__ = (
        '_monitor_res',
        'upscale_max',
        '_disp_res_max',
        'fullscreen_offset',
        'upscale',
        '_disp_res',
        'is_fullscreen',
        '_disp_screen',
        '_full_screen',
        'screen',
    )

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(constants.SCREEN_CAPTION)
        # set window icon here
        # replace with a custom mouse icon or get rid of it?
        # pygame.mouse.set_visible(False)
        self._monitor_res = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )
        self.upscale_max = min(
            self._monitor_res[0] // constants.SCREEN_SIZE[0],
            self._monitor_res[1] // constants.SCREEN_SIZE[1]
        )
        self._disp_res_max = (
            constants.SCREEN_SIZE[0] * self.upscale_max,
            constants.SCREEN_SIZE[1] * self.upscale_max,
        )
        self.fullscreen_offset = (
            (self._monitor_res[0] - self._disp_res_max[0]) // 2,
            (self._monitor_res[1] - self._disp_res_max[1]) // 2,
        )
        self.upscale = self.upscale_max - 1
        self._full_screen = pygame.Surface(self._disp_res_max)
        self.screen = pygame.Surface(constants.SCREEN_SIZE)
        self.screenSet(0)

    def screenSet(self, scale_change):
        """Set the window to a new scale."""
        new_upscale = self.upscale + scale_change
        if new_upscale < 1 or new_upscale > self.upscale_max:
            return
        self.upscale = new_upscale
        self._disp_res = (
            constants.SCREEN_SIZE[0] * self.upscale,
            constants.SCREEN_SIZE[1] * self.upscale,
        )
        # center window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(
            (self._monitor_res[0] - self._disp_res[0]) // 2,
            (self._monitor_res[1] - self._disp_res[1]) // 2
        )
        pygame.display.quit()
        pygame.display.init()
        self._disp_screen = pygame.display.set_mode(
            self._disp_res,
            pygame.DOUBLEBUF
        )
        self.screen = self.screen.convert(self._disp_screen)
        self.is_fullscreen = False

    def screenSetFullscreen(self):
        """Set the window to fullscreen."""
        pygame.display.quit()
        pygame.display.init()
        self._disp_screen = pygame.display.set_mode(
            self._monitor_res,
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        # needs a separate full screen in case the largest full-multiple scale-up doesn't fit
        self._full_screen = self._full_screen.convert(self._disp_screen)
        self.screen = self.screen.convert(self._full_screen)
        self.is_fullscreen = True

    def _scaleMouseInput(self, event):
        """Scale mouse position for events in terms of the screen (as opposed to the display surface)."""
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if self.is_fullscreen:
                event_dict = {
                    'pos': (
                        (event.pos[0] - self.fullscreen_offset[0]) // self.upscale_max,
                        (event.pos[1] - self.fullscreen_offset[1]) // self.upscale_max,
                    )
                }
            else:
                event_dict = {
                    'pos': (
                        event.pos[0] // self.upscale,
                        event.pos[1] // self.upscale,
                    )
                }
            if event.type == pygame.MOUSEMOTION:
                event_dict['rel'] = event.rel
                event_dict['buttons'] = event.buttons
            else:
                event_dict['button'] = event.button
            return pygame.event.Event(event.type, event_dict)
        return event

    def scaleDraw(self):
        """Scale screen onto display surface, then flip the display."""
        if self.is_fullscreen:
            pygame.transform.scale(self.screen, self._disp_res_max, self._full_screen)
            self._disp_screen.blit(self._full_screen, self.fullscreen_offset)
        else:
            pygame.transform.scale(self.screen, self._disp_res, self._disp_screen)
        pygame.display.flip()
