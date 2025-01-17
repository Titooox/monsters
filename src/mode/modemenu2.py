import jovialengine

from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin2 import ModeTalkWin2
from .modetalkelse2 import ModeTalkElse2
from .modemenu import ModeMenu


class ModeMenu2(ModeMenu):
    def _handleLoad(self):
        super()._handleLoad()
        if self._convo_key == "2":
            if jovialengine.shared.state.protag_mon.personality == Personality.Affectionate:
                self._text = "Happy and healthy."
            elif jovialengine.shared.state.protag_mon.personality == Personality.Aggressive:
                self._text = "Ready to win again."
            elif jovialengine.shared.state.protag_mon.personality == Personality.Careful:
                self._text = "Probably ready to go."
            elif jovialengine.shared.state.protag_mon.personality == Personality.Energetic:
                self._text = "Excited and ready."

    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "3a":
            self._stopMixer()
            self.next_mode = ModeFight(
                jovialengine.shared.state.protag_mon,
                Monster.atLevel(2),
                lambda: ModeTalkWin2() if jovialengine.shared.state.fight_results[-1] == 1 else ModeTalkElse2()
            )
            return True
        return False
