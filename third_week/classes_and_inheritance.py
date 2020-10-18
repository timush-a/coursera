import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def __repr__(self):
        return str(self.__dict__)

    valid_extensions = ['jpg', 'png', 'jpeg', 'gif']

    def get_photo_file_ext(file_name):
        """
        check extension of file
        """
        if os.path.splittext(file_name)[1] in valid_extensions:
            return os.path.splittext(file_name)[1]
        else:
            return None


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self.car_type = 'truck'
        try:
            body = self.body_whl.split('x')
            self.body_width = float(body[0])
            self.body_height = float(body[1])
            self.body_length = float(body[2])
        except (IndexError, ValueError):
            self.body_width = 0
            self.body_height = 0
            self.body_length = 0

    def get_body_volume():
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def class_selector(car_type, *args):
    if car_type == 'car':
        return Car(*args)
    elif car_type == 'truck':
        return Truck(*args)
    elif car_type == 'spec_machine':
        return SpecMachine(*args)

def get_car_list(file):
    car_list = []
    with open(file) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            if row:
                try:
                    car_list.append(class_selector(row[0], *list(filter(None, row))[1:]))
                except TypeError:
                    pass

    return car_list
