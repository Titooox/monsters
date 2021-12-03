import os
import random

import pygame

import constants
import shared
from personality import Personality
from skin import Skin
from animsprite import AnimSprite


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
        'personality',
        'name',
        'skin',
        'stats',
        'sprite_groups',
        'sprite_paths',
        'sprite',
        'sprite_right',
        'facing_right',
    )

    def __init__(self, in_stats: dict = None):
        """Create a new monster, setting stats, etc. as needed."""
        super().__init__()
        self.lvl = 0
        self.personality = Personality.random()
        self.name = Personality.generateName(self.personality)
        self.skin = Skin.random(self.personality)

        self.stats = {x: 2 for x in self.MAIN_STATS}
        self.stats['drv'] = self.DRV_MAX
        self._levelStats()
        if in_stats is not None:
            self.stats.update(in_stats)
        self.setHealth()

        self.rect = pygame.Rect(0, 0, 48, 48)
        self.sprite_groups = tuple(random.choice(('A', 'B', 'C')) for x in range(5))
        self._setSpritePaths()
        self._setSprites()
        self.setImage()

    def save(self):
        return {
            'super': super().save(),
            'lvl': self.lvl,
            'personality': self.personality,
            'name': self.name,
            'skin': self.skin,
            'stats': self.stats,
            'sprite_groups': self.sprite_groups,
            'sprite_paths': self.sprite_paths,
            'facing_right': self.facing_right,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.lvl = save_data['lvl']
        new_obj.personality = save_data['personality']
        new_obj.name = save_data['name']
        new_obj.skin = save_data['skin']
        new_obj.stats = save_data['stats']
        new_obj.sprite_groups = save_data['sprite_groups']
        new_obj.sprite_paths = save_data['sprite_paths']
        new_obj._setSprites()
        new_obj.setImage(save_data['facing_right'])

        super_obj = super().load(save_data['super'])
        new_obj.rect.topleft = super_obj.rect.topleft
        new_obj.anims = super_obj.anims
        new_obj.last_pos = super_obj.last_pos
        new_obj.time = super_obj.time

        return new_obj

    def fightStart(self):
        self.stats['drv'] = self.DRV_MAX
        if self.lvl == 0:
            self.stats['drv'] -= 1
        self.setHealth()

    def _drvEffect(self):
        return self.stats['drv'] - self.DRV_MAX + 2

    def _getHealthBasis(self):
        return 8 + (self.lvl * 2 + 1)**2

    def fightHit(self, action: str, is_protag: bool = False):
        hit = 0
        block = 0
        if action == 'Attack':
            hit = self.stats['atk'] // 2 + self.stats['spd'] // 2
            block = hit + random.randint(0, 1)
        elif action == 'Defend':
            hit = self.stats['vit'] // 2 + self.stats['def'] // 2
            block = hit + random.randint(0, 1)
        # 'Escape'
        else:
            hit = self.stats['atk'] // 4 - self._getHealthBasis() // 4 - random.randint(1, 4)
            block = self.stats['def'] // 2 + self.stats['spd'] // 2
        if action == self.personality.preferred_action:
            bonus = self._getHealthBasis() // 3
            if is_protag:
                bonus = self._getHealthBasis() // 2
            hit += bonus
            block += bonus
        else:
            hit -= self._getHealthBasis() // 4 + random.randint(1, 2)
        hit = max(hit + random.randint(-1, 1) + self._drvEffect(), 0)
        block = max(block + random.randint(-1, 1) + self._drvEffect(), 0)
        self.stats['drv'] = max(self.stats['drv'] - 1, 0)
        return hit, block

    def _levelStats(self):
        for stat in self.MAIN_STATS:
            self.stats[stat] += 2
        for stat in random.sample(self.MAIN_STATS, 2):
            self.stats[stat] += 1
        self.stats[self.personality.stat] += 2

    def setHealth(self):
        self.stats['hpm'] = self._getHealthBasis() + self.stats['vit']
        self.stats['hpc'] = self.stats['hpm']

    def _getSpritePath(self, section: str, group: str):
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
    def atLevel(cls, in_lvl, in_stats: dict = None):
        """Create a new monster at a given level not above the maximum level, setting stats, etc. as needed."""
        new_mon = cls(in_stats)
        for n in range(min(in_lvl, cls.LVL_MAX)):
            new_mon.levelUp()
        return new_mon
