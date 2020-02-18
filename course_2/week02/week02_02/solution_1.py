import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __add__(self, vec):
        return Vec2d(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2d(self.x - vec.x, self.y - vec.y)

    def __mul__(self, k):
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self, display):
        self.points = []
        self.speeds = []
        self.gameDisplay = display

    def add_point(self, x_coord, y_coord):
        self.points.append(Vec2d(x_coord, y_coord))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(self.gameDisplay, color, self.points[p_n].int_pair(), self.points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(self.gameDisplay, color, (p.int_pair()), width)


class Knot(Polyline):
    def __init__(self, display):
        super().__init__(display)
        self.curve = []
        self.steps = 35

    def add_point(self, x_coord, y_coord):
        super().add_point(x_coord, y_coord)
        self.get_knot()

    def remove_point(self):
        self.points.pop()
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def get_knot(self):
        if len(self.points) < 3:
            self.curve = []
            return
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i+1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        self.curve = res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg]*alpha + self.get_point(points, alpha, deg - 1)*(1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.curve) - 1):
                pygame.draw.line(gameDisplay, color, self.curve[p_n].int_pair(), self.curve[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, (p.int_pair()), width)

    def reset(self):
        self.points = []
        self.speeds = []
        self.curve = []

    def speed_up(self):
        for s in range(len(self.speeds)):
            self.speeds[s] = self.speeds[s] * 1.1

    def slow_down(self):
        for s in range(len(self.speeds)):
            self.speeds[s] = self.speeds[s] * 0.9


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Left Mouse Button", "Add point"])
    data.append(["Right Mouse Button", "Remove point"])
    data.append(["Mouse Scroll Up", "Speed up"])
    data.append(["Mouse Scroll Down", "Slow down"])
    data.append(["", ""])
    data.append([str(knot.steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (400, 100 + 30 * i))

# =======================================================================================
# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    knot = Knot(gameDisplay)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot.reset()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.steps -= 1 if knot.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    knot.add_point(*event.pos)
                elif event.button == 3:
                    knot.remove_point()
                elif event.button == 4:
                    knot.speed_up()
                elif event.button == 5:
                    knot.slow_down()


        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.draw_points("line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)