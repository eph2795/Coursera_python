import pygame
import random
import math
from copy import deepcopy

SCREEN_DIM = (800, 600)


def draw_help(gameDisplay, steps):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [
        ["F1", "Show Help"],
        ["R", "Restart"],
        ["P", "Pause/Play"],
        ["Num+", "More points"],
        ["Num-", "Less points"],
        ["", ""],
        [str(steps), "Current points"]
    ]
    pygame.draw.lines(gameDisplay,
                      color=(255, 50, 50, 255),
                      closed=True,
                      pointlist=[(0, 0), (800, 0), (800, 600), (0, 600)],
                      width=5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


class Vec2d:

    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vec2d(k * self.x, k * self.y)

    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return int(self.x), int(self.y)

    def pair(self):
        return self.x, self.y

    def __str__(self):
        return '({x:.4f}, {y:.4f})'.format(x=self.x, y=self.y)

    def __repr__(self):
        return '({x:.4f}, {y:.4f})'.format(x=self.x, y=self.y)


class Polyline:

    def __init__(self, points_, speeds_):
        self.points = points_
        self.speeds = speeds_

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for i, (point, speed) in enumerate(zip(self.points, self.speeds)):
            moved_point = point + speed
            reflected_speed = speed

            x_point, y_point = moved_point.pair()
            x_speed, y_speed = speed.pair()
            if (x_point >= SCREEN_DIM[0]) or (x_point <= 0):
                reflected_speed = Vec2d(-x_speed, y_speed)
            if (y_point >= SCREEN_DIM[1]) or (y_point <= 0):
                reflected_speed = Vec2d(x_speed, -y_speed)
            self.points[i] = moved_point
            self.speeds[i] = reflected_speed

    @staticmethod
    def draw_points(points_, style="points", width=3, color_=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points_) - 1):
                pygame.draw.line(gameDisplay, color_,
                                 points_[p_n].int_pair(),
                                 points_[p_n + 1].int_pair(),
                                 width)
        elif style == "points":
            for p in points_:
                pygame.draw.circle(gameDisplay, color_,
                                   p.int_pair(),
                                   width)
        else:
            raise ValueError('Wrong value of "style" argument!')

    def get_points(self):
        return deepcopy(self.points)


class Knot(Polyline):

    def __init__(self, points_, speeds_, smoothing_points_number_):
        super().__init__(points_, speeds_)
        self.knot_points = []
        self.smoothing_points_number = smoothing_points_number_

    def get_smoothing_points_number(self):
        return self.smoothing_points_number

    def increase_smoothing_points_number(self):
        self.smoothing_points_number += 1

    def decrease_smoothing_points_number(self):
        if self.smoothing_points_number > 0:
            self.smoothing_points_number -= 1

    @classmethod
    def _get_point(cls, points_, alpha, deg=None):
        if deg is None:
            deg = len(points_) - 1
        if deg == 0:
            return points_[0]
        return points_[deg] * alpha + cls._get_point(points_, alpha, deg - 1) * (1 - alpha)

    @classmethod
    def _get_points(cls, base_points, smoothing_points_number):
        alpha = 1 / smoothing_points_number
        res = []
        for i in range(smoothing_points_number):
            res.append(cls._get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            smoothed_knot = self._get_points(
                [
                    (self.points[i] + self.points[i + 1]) * 0.5,
                    self.points[i + 1],
                    (self.points[i + 1] + self.points[i + 2]) * 0.5
                ],
                self.smoothing_points_number
            )
            res.extend(smoothed_knot)
        return res

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.knot_points = self.get_knot()

    def set_points(self):
        super().set_points()
        self.knot_points = self.get_knot()


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    knot = Knot(points_=[], speeds_=[], smoothing_points_number_=35)
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.increase_smoothing_points_number()
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.decrease_smoothing_points_number()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                knot.add_point(Vec2d(x, y), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        if not pause:
            knot.set_points()
        knot.draw_points(knot.get_points())
        knot.draw_points(knot.get_knot(), style="line", width=3, color_=color)

        if show_help:
            draw_help(gameDisplay, knot.get_smoothing_points_number())
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
