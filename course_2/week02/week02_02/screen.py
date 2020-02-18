import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Ð¤ÑƒÐ½ÐºÑ†Ð¸Ð¸ Ð´Ð»Ñ Ñ€Ð°Ð±Ð¾Ñ‚Ñ‹ Ñ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°Ð¼Ð¸
# =======================================================================================

def sub(x, y):
    """"Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ñ€Ð°Ð·Ð½Ð¾ÑÑ‚ÑŒ Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²"""
    return x[0] - y[0], x[1] - y[1]


def add(x, y):
    """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ ÑÑƒÐ¼Ð¼Ñƒ Ð´Ð²ÑƒÑ… Ð²ÐµÐºÑ‚Ð¾Ñ€Ð¾Ð²"""
    return x[0] + y[0], x[1] + y[1]


def length(x):
    """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð´Ð»Ð¸Ð½Ñƒ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°"""
    return math.sqrt(x[0] * x[0] + x[1] * x[1])


def mul(v, k):
    """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð¿Ñ€Ð¾Ð¸Ð·Ð²ÐµÐ´ÐµÐ½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð½Ð° Ñ‡Ð¸ÑÐ»Ð¾"""
    return v[0] * k, v[1] * k


def vec(x, y):
    """Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ Ð¿Ð°Ñ€Ñƒ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚, Ð¾Ð¿Ñ€ÐµÐ´ÐµÐ»ÑÑŽÑ‰Ð¸Ñ… Ð²ÐµÐºÑ‚Ð¾Ñ€ (ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚Ñ‹ Ñ‚Ð¾Ñ‡ÐºÐ¸ ÐºÐ¾Ð½Ñ†Ð° Ð²ÐµÐºÑ‚Ð¾Ñ€Ð°),
    ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚Ñ‹ Ð½Ð°Ñ‡Ð°Ð»ÑŒÐ½Ð¾Ð¹ Ñ‚Ð¾Ñ‡ÐºÐ¸ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° ÑÐ¾Ð²Ð¿Ð°Ð´Ð°ÑŽÑ‚ Ñ Ð½Ð°Ñ‡Ð°Ð»Ð¾Ð¼ ÑÐ¸ÑÑ‚ÐµÐ¼Ñ‹ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ (0, 0)"""
    return sub(y, x)


# =======================================================================================
# Ð¤ÑƒÐ½ÐºÑ†Ð¸Ð¸ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸
# =======================================================================================
def draw_points(points, style="points", width=3, color=(255, 255, 255)):
    """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸ Ñ‚Ð¾Ñ‡ÐµÐº Ð½Ð° ÑÐºÑ€Ð°Ð½Ðµ"""
    if style == "line":
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(points[p_n][0]), int(points[p_n][1])),
                             (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

    elif style == "points":
        for p in points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p[0]), int(p[1])), width)


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
# Ð¤ÑƒÐ½ÐºÑ†Ð¸Ð¸, Ð¾Ñ‚Ð²ÐµÑ‡Ð°ÑŽÑ‰Ð¸Ðµ Ð·Ð° Ñ€Ð°ÑÑ‡ÐµÑ‚ ÑÐ³Ð»Ð°Ð¶Ð¸Ð²Ð°Ð½Ð¸Ñ Ð»Ð¾Ð¼Ð°Ð½Ð¾Ð¹
# =======================================================================================
def get_point(points, alpha, deg=None):
    if deg is None:
        deg = len(points) - 1
    if deg == 0:
        return points[0]
    return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))


def get_points(base_points, count):
    alpha = 1 / count
    res = []
    for i in range(count):
        res.append(get_point(base_points, i * alpha))
    return res


def get_knot(points, count):
    if len(points) < 3:
        return []
    res = []
    for i in range(-2, len(points) - 2):
        ptn = []
        ptn.append(mul(add(points[i], points[i + 1]), 0.5))
        ptn.append(points[i + 1])
        ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))

        res.extend(get_points(ptn, count))
    return res


def set_points(points, speeds):
    """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¿ÐµÑ€ÐµÑ€Ð°ÑÑ‡ÐµÑ‚Ð° ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº"""
    for p in range(len(points)):
        points[p] = add(points[p], speeds[p])
        if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
            speeds[p] = (- speeds[p][0], speeds[p][1])
        if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
            speeds[p] = (speeds[p][0], -speeds[p][1])


# =======================================================================================
# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
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
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                speeds.append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        draw_points(points)
        draw_points(get_knot(points, steps), "line", 3, color)
        if not pause:
            set_points(points, speeds)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)