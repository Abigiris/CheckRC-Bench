def process(self):
    if isinstance(self, DynamicClass):
        if type(self) is DynamicClass:  # redundant subsumed
            return self.value * 2
    else:
        raise TypeError("Should not happen")