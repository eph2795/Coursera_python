import csv
import os


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        root, ext = os.path.splitext(self.photo_file_name)
        return ext


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super(Car, self).__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super(Truck, self).__init__(brand, photo_file_name, carrying)
        try:
            self.body_length, self.body_width, self.body_height = map(float, body_whl.split('x'))
        except ValueError:
            # print('Got ValueError from {}'.format(body_whl))
            self.body_width, self.body_height, self.body_length = 0.0, 0.0, 0.0
        self.car_type = 'truck'

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super(SpecMachine, self).__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):
    correct_ext_list = ['.jpg', '.jpeg', '.png', '.gif']
    car_args = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']
    truck_args = ['brand', 'photo_file_name', 'carrying', 'body_whl']
    spec_args = ['brand', 'photo_file_name', 'carrying', 'extra']
    header = ['car_type', 'brand', 'passenger_seats_count',
              'photo_file_name', 'body_whl', 'carrying', 'extra']

    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        # print(header)
        for row in reader:
            attributes = {name: value for value, name in zip(row, header)}

            try:
                car_type = attributes['car_type']
                del attributes['car_type']

                def check_extra_attrs(attrs, attrs_list):
                    for k, v in attrs.items():
                        if v and (k not in attrs_list):
                            # print(k, v)
                            return True
                    return False

                def check_attrs(attrs, attrs_list):
                    for k in attrs_list:
                        if (k not in attrs) or not attrs[k]:
                            return False
                    return True

                if not any(attributes['photo_file_name'].endswith(ext) for ext in correct_ext_list):
                    continue
                if ((car_type == 'car')
                        and not check_extra_attrs(attributes, car_args)
                        and check_attrs(attributes, car_args)):
                    car_list.append(Car(**{k: attributes[k] for k in car_args}))
                elif ((car_type == 'truck')
                        and not check_extra_attrs(attributes, truck_args)
                        and check_attrs(attributes, ['brand', 'photo_file_name', 'carrying'])):
                    car_list.append(Truck(**{k: attributes[k] for k in truck_args}))
                elif ((car_type == 'spec_machine')
                        and not check_extra_attrs(attributes, spec_args)
                        and check_attrs(attributes, spec_args)):
                    car_list.append(SpecMachine(**{k: attributes[k] for k in spec_args}))
            except (KeyError, AttributeError, ValueError, TypeError):
                pass
    return car_list
