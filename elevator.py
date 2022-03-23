from typing import List

from passenger import Passenger


class Elevator:
    def __init__(self, last_floor: int):
        self.max_passengers: int = 5
        self.last_floor: int = last_floor
        self.current_floor: int = 1
        self.direction: str = 'UP'
        self.passengers: List[Passenger] = []
        self.available_space: int = 5

    def set_available_space(self):
        self.available_space = self.max_passengers - len(self.passengers)

    def enter_passengers(self, passengers: List[Passenger]):
        if self.available_space:
            if self.available_space >= len(passengers):
                self.passengers.extend(passengers)
            else:
                self.passengers.extend(passengers[:self.available_space])

            self.set_available_space()

    def exit_passengers(self):
        exit_passengers_list = filter(
            lambda x: x.target_floor == self.current_floor,
            self.passengers
        )

        for passenger in exit_passengers_list:
            self.passengers.remove(passenger)

        self.set_available_space()

    def set_max_floor(self):
        """
        Устанавливается "наибольший" этаж, на который нужно пассажирам
        """
        if self.passengers:
            target_floors = [
                passenger.target_floor
                for passenger in self.passengers
            ]

            if self.direction == 'UP':
                self.max_floor = max(target_floors)
            else:
                self.max_floor = min(target_floors)
        else:
            self.max_floor = self.last_floor if self.direction == 'UP' else 1

    def set_next_floor(self):
        if self.direction == 'UP':
            if self.current_floor == self.last_floor:
                self.current_floor = self.last_floor - 1
                self.direction = 'DOWN'
            else:
                self.current_floor += 1
        else:
            if self.current_floor == 1:
                self.current_floor = 2
                self.direction = 'UP'
            else:
                self.current_floor -= 1

    def check_passengers_in_elevator(self) -> List[Passenger]:
        exit_passengers = list(filter(
            lambda x: x.target_floor == self.current_floor,
            self.passengers
        ))

        if exit_passengers:
            for passenger in exit_passengers:
                self.passengers.remove(passenger)

            self.set_available_space()

        return exit_passengers

