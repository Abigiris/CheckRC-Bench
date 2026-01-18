class Flyable: pass
class Swimmable: pass
class Duck(Swimmable): pass

def handle_duck(d: Duck):
    if isinstance(d, Swimmable):
        print("Can swim")
    elif isinstance(d, Duck):  # conflicting branch type check
        print("Cannot be a duck") 
    return d