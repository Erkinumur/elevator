import random


class Passenger:
    def __init__(self, current_floor: int, last_floor: int):
        self.current_floor: int = current_floor
        self.last_floor: int = last_floor
        self.set_target_floor()
        self.set_direction()

    def set_target_floor(self):
        floors_list = list(range(1, self.last_floor + 1))
        floors_list.remove(self.current_floor)
        self.target_floor = random.choice(floors_list)

    def set_direction(self):
        if self.target_floor > self.current_floor:
            self.direction = 'UP'
        else:
            self.direction = 'DOWN'

    def set_new_floor(self, current_floor: int):
        self.current_floor = current_floor
        self.set_target_floor()
        self.set_direction()
