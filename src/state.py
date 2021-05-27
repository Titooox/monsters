from monster import Monster


class State(object):
    __slots__ = (
        'protag_mon',
    )

    def __init__(self):
        # start with a random monster
        self.protag_mon = Monster()

    def save(self):
        return {
            'protag_mon': self.protag_mon,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.protag_mon = save_data['protag_mon']
        return new_obj
