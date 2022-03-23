import random
from time import sleep
from typing import List

from elevator import Elevator
from passenger import Passenger


class Program:
    last_floor: int = random.randint(5, 20)
    step: int = 1

    def __init__(self):
        self.elevator = self.create_elevator()
        self.building = self.create_building()

    def create_elevator(self) -> Elevator:
        elevator = Elevator(self.last_floor)

        return elevator

    def create_building(self) -> dict:
        building = {}
        for floor in range(1, self.last_floor + 1):
            passengers = [
                Passenger(floor, self.last_floor)
                for i in range(random.randint(0, 10))
            ]

            passengers_going_up = filter(
                lambda x: x.direction == 'UP',
                passengers
            )

            passengers_going_down = filter(
                lambda x: x.direction == 'DOWN',
                passengers
            )

            building.update({
                floor: {
                    'UP': list(passengers_going_up),
                    'DOWN': list(passengers_going_down)
                }
            })

        return building

    def next_step(self):
        passengers_to_exit = self.elevator.check_passengers_in_elevator()

        if not self.elevator.passengers:
            passengers_going_up = self.check_passengers_on_floor('UP')
            passengers_going_down = self.check_passengers_on_floor('DOWN')

            if len(passengers_going_up) >= len(passengers_going_down):
                self.elevator.direction = 'UP'
                passengers_to_enter = passengers_going_up
            else:
                self.elevator.direction = 'DOWN'
                passengers_to_enter = passengers_going_down
        else:
            passengers_to_enter = self.check_passengers_on_floor(
                self.elevator.direction
            )

        if len(passengers_to_enter) > self.elevator.available_space:
            passengers_to_enter = passengers_to_enter[
                                  :self.elevator.available_space
                                  ]

        self.elevator.enter_passengers(passengers_to_enter)
        self.remove_passengers_from_floor(passengers_to_enter)
        self.add_passengers_to_floor(passengers_to_exit.copy())
        message = self.get_step_info(passengers_to_exit, passengers_to_enter)
        self.elevator.set_next_floor()
        self.step += 1

        return message

    def add_passengers_to_floor(self, passengers: List[Passenger]):
        current_floor = self.elevator.current_floor
        for passenger in passengers:
            passenger.set_new_floor(current_floor)
            self.building.get(
                current_floor
            ).get(passenger.direction).append(passenger)

    def remove_passengers_from_floor(self, passengers: List[Passenger]):
        for passenger in passengers:
            self.building.get(
                self.elevator.current_floor
            ).get(self.elevator.direction).remove(passenger)

    def check_passengers_on_floor(self, direction):
        passengers = self.building.get(
            self.elevator.current_floor
        ).get(direction)

        return passengers.copy()

    def get_step_info(
            self,
            passengers_to_exit: list,
            passengers_to_enter: list
    ):
        current_floor = self.elevator.current_floor
        elevator_passengers = [
            passenger.target_floor
            for passenger in self.elevator.passengers]
        elevator_info = f'Лифт: \n' \
                        f'\tЭтаж: {current_floor}\n' \
                        f'\tПассажиры: {elevator_passengers}\n' \
                        f'\tНаправление: {self.elevator.direction}'

        building_info = 'Здание: \n'
        for floor in range(self.last_floor, 0, -1):
            passengers = self.building.get(floor)
            passengers_lsit = [
                passenger.target_floor
                for passenger in passengers.get('UP')
            ]
            passengers_lsit.extend([
                passenger.target_floor
                for passenger in passengers.get('DOWN')
            ])

            building_info += f'{floor} | {passengers_lsit}\n'

        message = f'*** Шаг {self.step} ***\n' \
                  f'На {current_floor} этаже ' \
                  f'вышло из лифта {len(passengers_to_exit)} человек\n' \
                  f'зашло в лифт {len(passengers_to_enter)} человек\n\n' \
                  f'{elevator_info}\n\n' \
                  f'{building_info}\n'

        return message


if __name__ == '__main__':
    program = Program()
    while True:
        command = input(
            'Введите команду ([n, next] - следующий шаг, [s, stop] - завершение)'
        )
        if command in ('n', 'next'):
            message = program.next_step()
            print(message)
        if command in ('s', 'stop'):
            break
