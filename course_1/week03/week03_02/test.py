from solution import *
cars = get_car_list('sample.csv')
print(len(cars))

for car in cars:
     print(type(car))
     print(car.get_photo_file_ext())

print(cars[0].passenger_seats_count)
print(cars[1].get_body_volume())
