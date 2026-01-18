class Animal: pass
class Mammal(Animal): pass
class Dog(Mammal): pass

def process_animal(a: Animal):
    if isinstance(a, Mammal):
        if isinstance(a, Animal):  # redundant subsumed type check
            print("This will always be true")
    return a