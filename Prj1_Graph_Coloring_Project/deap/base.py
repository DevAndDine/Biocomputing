import copy
import functools


class Fitness:
    weights = ()

    def __init__(self, values=()):
        self.values = values

    @property
    def valid(self):
        return bool(self.values)

    def _weighted(self):
        if not self.values:
            return ()
        if not self.weights:
            return self.values
        return tuple(v * w for v, w in zip(self.values, self.weights))

    def __lt__(self, other):
        return self._weighted() < other._weighted()

    def __le__(self, other):
        return self._weighted() <= other._weighted()


class Toolbox:
    def __init__(self):
        self.clone = copy.deepcopy

    def register(self, alias, function, *args, **kwargs):
        partial = functools.partial(function, *args, **kwargs)
        partial.__name__ = alias
        setattr(self, alias, partial)
