import pygame, os, sys
from monster import *
class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = 1
        self.framerate = 60
        
        pygame.mouse.set_visible(False)
        #set window icon/captions here...
        self.res = (320,180)
        self.screen = pygame.Surface(self.res)
        self.monitor_res = (pygame.display.Info().current_w,pygame.display.Info().current_h)
        self.upscale_max = min(self.monitor_res[0]//self.res[0], self.monitor_res[1]//self.res[1])
        self.upscale = self.upscale_max//2
        self.disp_res_max = (self.res[0]*self.upscale_max, self.res[1]*self.upscale_max)
        self.window_set(0)
        self.fullscreen_offset = ((self.monitor_res[0]-self.disp_res_max[0])/2, (self.monitor_res[1]-self.disp_res_max[1])/2)
        self.full_screen = pygame.Surface(self.disp_res_max)
        
        self.clock = pygame.time.Clock()
        #test stuff
        self.test_mon = Monster()
        self.fill = [255, 255, 255]
        
    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()
        
    def window_set(self, scale_change):
        self.upscale += scale_change
        self.disp_res = (self.res[0]*self.upscale, self.res[1]*self.upscale)
        if not sys.platform.startswith('freebsd') and not sys.platform.startswith('darwin'):
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((self.monitor_res[0]-self.disp_res[0])//2, (self.monitor_res[1]-self.disp_res[1])//2)
        self.disp_screen = pygame.display.set_mode(self.disp_res)
        self.screen.convert()
        self.is_fullscreen = False
        
    def window_set_fullscreen(self):
        self.disp_screen = pygame.display.set_mode(self.monitor_res, pygame.FULLSCREEN)
        self.full_screen.convert()
        self.screen.convert(self.full_screen)
        self.is_fullscreen = True
        
    def run(self):
        """Run the game, and check if the game needs to end."""
        return self.running and self.input() and self.update() and self.draw() and self.time()
        
    def input(self):
        """Take inputs as needed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                #Window re-sizing stuff
                if event.key == pygame.K_PAGEUP or event.key == pygame.K_PERIOD:
                    if self.upscale == self.upscale_max:
                        continue
                    self.window_set(1)
                    continue
                if event.key == pygame.K_PAGEDOWN or event.key == pygame.K_COMMA:
                    if self.upscale == 1:
                        continue
                    self.window_set(-1)
                    continue
                if event.key == pygame.K_F11 or event.key == pygame.K_TAB:
                    if self.is_fullscreen:
                        self.window_set(0)
                    else:
                        self.window_set_fullscreen()
                    continue
                #test stuff
                if event.key == pygame.K_SPACE:
                    self.test_mon = Monster()
                if event.key == pygame.K_l:
                    self.test_mon.levelUp()
                if event.key == pygame.K_r:
                    self.fill[0] = 255*(self.fill[0]!=255)
                if event.key == pygame.K_g:
                    self.fill[1] = 255*(self.fill[1]!=255)
                if event.key == pygame.K_b:
                    self.fill[2] = 255*(self.fill[2]!=255)
        return 1
        
    def update(self):
        """Update things as needed."""
        return 1
        
    def draw(self):
        """Draw things as needed."""
        self.screen.fill(self.fill)
        self.test_mon.draw(self.screen, (136,66))
        #now scale onto display surface
        if not self.is_fullscreen:
            pygame.transform.scale(self.screen, self.disp_res, self.disp_screen)
        else:
            pygame.transform.scale(self.screen, self.disp_res_max, self.full_screen)
            self.disp_screen.blit(self.full_screen, self.fullscreen_offset)
        pygame.display.flip()
        return 1
        
    def time(self):
        """Take care of time stuff."""
        pygame.display.set_caption(str(self.clock.get_fps()))
        self.clock.tick(self.framerate)
        return 1
        