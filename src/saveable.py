import abc


class Saveable(abc.ABC):
    @abc.abstractmethod
    def save(self):
        """Return an object represented all the information that should be saved from this mode."""
        raise NotImplementedError(
            type(self).__name__ + ".saveMode(self)"
        )

    @classmethod
    @abc.abstractmethod
    def load(cls, saveData):
        """Take in an object equivalent to the result of a call to saveMode(), and return an instance of this mode."""
        raise NotImplementedError(
            cls.__name__ + ".loadMode(cls, saveData)"
        )
