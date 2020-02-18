#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)
SPEED_MIN = 1
SPEED_MAX = 4
SPEED_STEP = 1


def draw_help():
    """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸ ÑÐºÑ€Ð°Ð½Ð° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ñ‹"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])

    data.append(["Left MB", "Add point"])
    data.append(["Right MB", "Remove point"])
    data.append(["I", "Increase knot speed"])
    data.append(["D", "Decrease knot speed"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# ÐšÐ»Ð°ÑÑ Ð´Ð»Ñ Ñ€Ð°Ð±Ð¾Ñ‚Ñ‹ Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°Ð¼Ð¸
# =======================================================================================
class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        """"Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ñ€Ð°Ð·Ð½Ð¾ÑÑ‚ÑŒ Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ ÑÑƒÐ¼Ð¼Ñƒ Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __len__(self):
        """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð´Ð»Ð¸Ð½Ñƒ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð¿Ñ€Ð¾Ð¸Ð·Ð²ÐµÐ´ÐµÐ½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð½Ð° Ñ‡Ð¸ÑÐ»Ð¾"""
        return Vec2d(self.x * other, self.y * other)

    def int_pair(self):
        """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð¿Ð°Ñ€Ñƒ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚, Ð¾Ð¿Ñ€ÐµÐ´ÐµÐ»ÑÑŽÑ‰Ð¸Ñ… Ð²ÐµÐºÑ‚Ð¾Ñ€ (ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚Ñ‹ Ñ‚Ð¾Ñ‡ÐºÐ¸ ÐºÐ¾Ð½Ñ†Ð° Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°),
        ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚Ñ‹ Ð½Ð°Ñ‡Ð°Ð»ÑŒÐ½Ð¾Ð¹ Ñ‚Ð¾Ñ‡ÐºÐ¸ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° ÑÐ¾Ð²Ð¿Ð°Ð´Ð°ÑŽÑ‚ Ñ Ð½Ð°Ñ‡Ð°Ð»Ð¾Ð¼ ÑÐ¸ÑÑ‚ÐµÐ¼Ñ‹ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ (0, 0)"""
        return int(self.x), int(self.y)

    def __repr__(self):
        return '({:.4f}, {:.4f})'.format(self.x, self.y)

# =======================================================================================
# Ð¤ÑƒÐ½ÐºÑ†Ð¸Ð¸, Ð¾Ñ‚Ð²ÐµÑ‡Ð°ÑŽÑ‰Ð¸Ðµ Ð·Ð° Ñ€Ð°ÑÑ‡ÐµÑ‚ ÑÐ³Ð»Ð°Ð¶Ð¸Ð²Ð°Ð½Ð¸Ñ Ð»Ð¾Ð¼Ð°Ð½Ð¾Ð¹
# =======================================================================================
class Polyline:
    def __init__(self, points, speeds):
        self.points = points
        self.knot_points = []
        self.speeds = speeds

    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.knot_points) - 1
        if deg == 0:
            return self.knot_points[0]

        vec1 = self.knot_points[deg] * alpha
        vec2 = self.get_point(alpha, deg - 1)
        return vec1 + vec2 * (1 - alpha)

    def get_points(self, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(i * alpha))
        return res

    def set_points(self):
        """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¿ÐµÑ€ÐµÑ€Ð°ÑÑ‡ÐµÑ‚Ð° ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x < 0 or self.points[p].x > SCREEN_DIM[0]:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y < 0 or self.points[p].y > SCREEN_DIM[1]:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def get_knot(self, count):
        if len(self.points) < 3:
            return []

        res = []
        for i in range(-2, len(self.points)-2):
            self.knot_points = []
            self.knot_points.append((self.points[i] + self.points[i+1]) * 0.5)
            self.knot_points.append(self.points[i+1])
            self.knot_points.append((self.points[i+1] + self.points[i+2]) * 0.5)

            res.extend(self.get_points(count))
        return res

# =======================================================================================
# Ð¤ÑƒÐ½ÐºÑ†Ð¸Ð¸ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸
# =======================================================================================
class Knot(Polyline):
    def __init__(self, points, speeds, speed_coef):
        super(Knot, self).__init__(points, speeds)
        self.speed_coef = speed_coef

    @staticmethod
    def draw_points(points, style="points", width=3, color=(255, 255, 255)):
        """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸ Ñ‚Ð¾Ñ‡ÐµÐº Ð½Ð° ÑÐºÑ€Ð°Ð½Ðµ"""
        if style == "line":
            for p_n in range(-1, len(points)-1):
                pygame.draw.line(gameDisplay, color,
                                 points[p_n].int_pair(),
                                 points[p_n+1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    def change_speed(self, direction):
        delta = SPEED_STEP * direction
        if SPEED_MIN <= self.speed_coef + delta <= SPEED_MAX:
            self.speed_coef += delta
        if direction == 1:  # increase
            self.speeds = [v * self.speed_coef for v in knot.speeds]
        elif direction == -1 :  # decrease
            self.speeds = [v * (1 / self.speed_coef) for v in knot.speeds]
        print(self.speeds)


# =======================================================================================
# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    speed_coef = 3
    working = True

    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    knot = Knot(points=[], speeds=[], speed_coef=speed_coef)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot(points=[], speeds=[], speed_coef=speed_coef)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

                if event.key == pygame.K_d:
                    knot.change_speed(direction=-1)
                if event.key == pygame.K_i:
                    knot.change_speed(direction=1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Adding point on LMB click
                if event.button == 1:
                    knot.points.append(Vec2d(event.pos[0], event.pos[1]))
                    knot.speeds.append(Vec2d(random.random() * knot.speed_coef,
                                             random.random() * knot.speed_coef))
                # Removing point on RMB click
                if event.button == 3:
                    knot.points.pop()
                    knot.speeds.pop()

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        knot.draw_points(knot.points)
        knot.draw_points(knot.get_knot(steps), "line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)