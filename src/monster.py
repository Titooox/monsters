import os
import random

import pygame

import constants
import shared
from animsprite import AnimSprite
from personality import Personality
from skin import Skin
from mood import Mood


class Monster(AnimSprite):
    DRV_MAX = 4
    LVL_MAX = 3
    MAIN_STATS = (
        'atk',
        'def',
        'spd',
        'vit',
    )
    BODY_SECTIONS = (
        'tail',
        'body',
        'head',
        'legs',
        'arms',
    )

    __slots__ = (
        'lvl',
        'awr',
        'personality',
        'name',
        'skin',
        'mood',
        'stats',
        'sprite_groups',
        'sprite_paths',
        'sprite',
        'sprite_right',
        'facing_right',
    )

    def __init__(self, in_stats={}):
        """Create a new monster, setting stats, etc. as needed."""
        super().__init__()
        self.lvl = 0
        # self.awr might not even need to be a thing, remove this if it ends up not mattering
        # awareness, this is a thing for conversations / progress through the game
        self.awr = 0
        # it might make more sense to hold info for conversations flow in shared.state, but I'm not sure
        # depends on how this number interacts with monster stuff
        self.personality = Personality.random()
        self.name = Personality.generateName(self.personality)
        self.skin = Skin.random(self.personality)
        # access the SkinTone with self.skin[self.lvl]
        self.mood = Mood.Neutral# mood might only be changed by and do stuff during battles / convos? maybe

        self.stats = {x: 2 for x in self.MAIN_STATS}
        self.stats['drv'] = self.DRV_MAX//2
        self._levelStats()
        self.stats.update(in_stats)
        self.setHealth()

        self.rect = pygame.Rect(0, 0, 48, 48)
        self.sprite_groups = tuple(random.choice(('A', 'B', 'C')) for x in range(5))
        self._setSpritePaths()
        self._setSprites()
        self.setImage()

    def fightStart(self):
        self.stats['drv'] = max(min(self.stats['drv'] + self.mood.drvChange, self.DRV_MAX), 0)

    def _drvEffect(self):
        return self.stats['drv'] - self.DRV_MAX + 1

    def fightHit(self, action):
        # todo: make speed affect more things
        attack = self.stats['atk']
        defend = self.stats['def']
        if action == 'attack':
            attack += self.stats['atk']//2 + self.stats['spd'] + random.randint(0, 1)
            defend += self.stats['def']//2 + self.stats['atk']//2
        elif action == 'defend':
            attack += self.stats['atk']//2 + self.stats['def']//2
            defend += self.stats['atk']//2 + self.stats['spd'] + random.randint(0, 1)
        # 'escape'
        else:
            attack = attack//2 + self.stats['spd']//2
            defend = defend//2 + self.stats['spd']//2
        attack = max(attack + random.randint(-1, 1) + self._drvEffect(), 0)
        defend = max(defend + random.randint(-1, 1) + self._drvEffect(), 0)
        return attack, defend

    def _levelStats(self):
        for stat in self.MAIN_STATS:
            self.stats[stat] += 2
        for stat in random.sample(self.MAIN_STATS, 2):
            self.stats[stat] += 1
        self.stats[self.personality.stat] += 2

    def setHealth(self):
        self.stats['hpm'] = self.stats['vit'] * 2 + self.stats['vit'] // 2 + self.stats['vit'] // 4
        self.stats['hpc'] = self.stats['hpm']

    def _getSpritePath(self, section, group):
        part = ''
        if self.lvl > 0:
            part = random.randint(0, 2)
        return os.path.join(
            constants.MONSTER_PARTS_DIRECTORY,
            '{}-{}-{}{}.png'.format(self.lvl, section, group, part)
        )

    def _setSpritePaths(self):
        self.sprite_paths = tuple(
            self._getSpritePath(self.BODY_SECTIONS[i], self.sprite_groups[i]) for i in range(5)
        )
        if self.lvl == 0:
            self.sprite_paths = self.sprite_paths[1:4]

    def getDarkSkin(self):
        return self.skin[self.lvl].dark

    def getLightSkin(self):
        return self.skin[self.lvl].light

    def _setSprites(self):
        self.sprite = pygame.image.load(self.sprite_paths[0]).convert(shared.display.screen)
        self.sprite.set_colorkey(constants.COLORKEY)
        for sprite_path in self.sprite_paths[1:]:
            new_part = pygame.image.load(sprite_path).convert(self.sprite)
            new_part.set_colorkey(constants.COLORKEY)
            self.sprite.blit(new_part, (0, 0))
        if self.lvl > 0:
            pix_array = pygame.PixelArray(self.sprite)
            pix_array.replace(self.skin[0].dark, self.getDarkSkin())
            pix_array.replace(self.skin[0].light, self.getLightSkin())
            del pix_array
        self.sprite_right = pygame.transform.flip(self.sprite, True, False)

    def setImage(self, face_right=False):
        self.facing_right = face_right
        if face_right:
            self.image = self.sprite_right
        else:
            self.image = self.sprite
        standing_pos = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = standing_pos

    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= self.LVL_MAX:
            return False
        self.lvl += 1
        self._levelStats()
        self.setHealth()
        self._setSpritePaths()
        self._setSprites()
        self.setImage()
        return True

    @classmethod
    def atLevel(cls, in_lvl, in_stats={}):
        """Create a new monster at a given level not above the maximum level, setting stats, etc. as needed."""
        new_mon = cls(in_stats)
        for n in range(min(in_lvl, cls.LVL_MAX)):
            new_mon.levelUp()
        return new_mon
