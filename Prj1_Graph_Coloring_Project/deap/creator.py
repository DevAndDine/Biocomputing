# Dynamic class factory compatible with the subset of deap.creator used here.


def create(name, base_cls, **attrs):
    fitness_cls = attrs.pop("fitness", None)

    if fitness_cls is not None:
        class NewClass(base_cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fitness = fitness_cls()
    else:
        class NewClass(base_cls):
            pass

    for key, value in attrs.items():
        setattr(NewClass, key, value)

    NewClass.__name__ = name
    globals()[name] = NewClass
    return NewClass
