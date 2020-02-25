import pygame
import random
import math

"""
ScreenSaver with following features:
1. multi polylines, configure each separately (selected polyline is marked by yellow points, others - white points)
2. add a new polyline. support two classes: Polyline(pure base)/Knot
3. different polylines can have a different classes at the same time
4. delete polyline (currently selected). there should be at least one.
5. adjust speed (can be stopped for speed=0), knot points per each polyline separately
6. navigate/switch by Prev/Next actions
7. remove polyline point by mouse click (switch mouse click mode=add/delete)
"""

"""
Classes structure:
class Vec2d() - vector processing
class Polyline() - base polyline class, draw in a given surface screen, standalone work
class Knot(Polyline) - advanced polyline with knots
class ScreenSaverHelp() - UI help processing, draw in a given surface screen
class ScreenSaver() - main program to execute
"""


class Vec2d():
    """2d zero-based vector"""

    def __init__(self, p):
        """Initialize from point (x, y)"""
        self.x, self.y = p

    def __add__(self, other):
        """Vectors addition"""
        return Vec2d((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        """Vectors subtraction"""
        return Vec2d((self.x - other.x, self.y - other.y))

    def __mul__(self, alpha):
        """Scalar multiplication"""
        return Vec2d((self.x * alpha, self.y * alpha))

    def __len__(self):
        """Vector length"""
        return int(math.sqrt(self.x**2 + self.y**2))

    def int_pair(self):
        """As an integer pair tuple (int, int)"""
        return (int(self.x), int(self.y))


class Polyline():
    """Base polyline"""

    def __init__(self, surface_screen, steps=1, speed_factor=1):
        self.surface = surface_screen
        self.surface_sz = Vec2d(surface_screen.get_size())
        self.points = []
        self.polyline_points = None
        self.is_draw_polyline = True
        self.polyline_steps = steps
        self.speeds = []
        self.speed_factor = speed_factor  # 0-stop, >1 - accelerate
        self.width = 3
        self.points_color = (255, 255, 255)
        self.lines_color = pygame.Color(0)

    def update_steps(self, delta):
        """Safety update polylines steps"""
        self.polyline_steps += delta
        if self.polyline_steps < 1:
            self.polyline_steps = 1

    def update_speed_factor(self, delta):
        """Safety update speed factor"""
        self.speed_factor += delta
        if self.speed_factor < 0:
            self.speed_factor = 0

    def reset(self):
        """Clear all points"""
        self.points = []
        self.speeds = []

    def add_point(self, v, s):
        """Add a new point"""
        self.points.append(Vec2d(v))
        self.speeds.append(Vec2d(s))

    def set_points(self, move=True):
        """Recalculate points"""
        for p in range(len(self.points)):
            if move:
                self.points[p] += self.speeds[p] * self.speed_factor
            if self.points[p].x > self.surface_sz.x or self.points[p].x < 0:
                self.speeds[p].x = -self.speeds[p].x
            if self.points[p].y > self.surface_sz.y or self.points[p].y < 0:
                self.speeds[p].y = -self.speeds[p].y

    def draw_points(self, line_width=None, line_color=None):
        """Draw points and polyline"""
        self.draw_points_only()
        self.draw_polyline_only(line_width, line_color)

    def draw_points_only(self):
        """Draw points"""
        for p in self.points:
            pygame.draw.circle(
                self.surface, self.points_color, p.int_pair(), self.width)

    def draw_polyline_only(self, width=None, color=None):
        """Draw polyline"""
        if not self.is_draw_polyline:
            return

        points = self.polyline_points or self.points
        width = width or self.width
        color = color or self.lines_color
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(
                self.surface, color,
                points[p_n].int_pair(), points[p_n + 1].int_pair(), width)


class Knot(Polyline):
    """Knot-points for the Polyline"""

    def set_points(self, move=True):
        """Override Polyline.set_points()"""
        super().set_points(move)
        self.get_knot()

    def get_knot(self):
        """Recalculate polyline points"""
        self.polyline_points = []
        self.is_draw_polyline = len(self.points) >= 3
        if not self.is_draw_polyline:
            return

        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            self.polyline_points.extend(
                self.__get_points(ptn, self.polyline_steps))

    def __get_points(self, points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(points, i * alpha))
        return res

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + \
            self.__get_point(points, alpha, deg - 1) * (1 - alpha)


class ScreenSaverHelp():
    """Help screen for Polyline"""

    def __init__(self, screen_surface, polylines):
        self.surface = screen_surface
        self.polylines = polylines
        self.selected = 0
        self.mouse_mode_deletion = False

    def draw(self):
        self.surface.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        mouse_mode_str = 'delete' if self.mouse_mode_deletion else 'add'
        data.append(["C", f"Change mouse click mode (current={mouse_mode_str})"])
        data.append(["A", "Add new polyline (class Polyline)"])
        data.append(["S", "Add new polyline (class Knot)"])
        data.append(["D", "Delete currently selected polyline"])
        data.append(["N", "Select next polyline"])
        data.append(["B", "Select previous polyline"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["X", "Faster"])
        data.append(["Z", "Slower"])
        data.append(["", ""])
        data.append(
            [f'{str(self.selected + 1)}/{len(self.polylines)}',
             "Currently selected polyline (yellow points)"])
        data.append(
            [f'{self.polylines[self.selected].__class__.__name__}',
             "Selected polyline's class"])
        data.append(
            [str(self.polylines[self.selected].polyline_steps),
             "Selected polyline's points"])
        data.append(
            [str(self.polylines[self.selected].speed_factor),
             "Selected polyline's speed factor (0=stop)"])

        pygame.draw.lines(self.surface, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.surface.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 30 + 30 * i))
            self.surface.blit(font2.render(
                text[1], True, (128, 128, 255)), (220, 30 + 30 * i))


class ScreenSaver():
    """ScreenSaver"""

    def __init__(self, screen_dim=(800, 600), polyline_steps_default=5, speed_factor_default=1):
        pygame.init()
        self.surface = pygame.display.set_mode(screen_dim)
        pygame.display.set_caption("Anton Senyuta Screen Saver")
        self.polyline_steps_default = polyline_steps_default
        self.speed_factor_default = speed_factor_default
        self.polylines = []
        self.selected = -1
        self.points_color = (255, 255, 255)
        self.selected_points_color = (255, 255, 0)
        self.show_help = False
        self.help = ScreenSaverHelp(self.surface, self.polylines)
        self.pause = True
        self.mouse_precision = 10
        self.mouse_mode_deletion = False
        self.reset()

    def __del__(self):
        pygame.display.quit()
        pygame.quit()

    def add_polyline(self, class_, steps=None, speed_factor=None):
        steps = steps or self.polyline_steps_default
        speed_factor = speed_factor or self.speed_factor_default
        self.polylines.append(class_(self.surface, steps, speed_factor))
        self.selected = len(self.polylines) - 1
        self.polylines[self.selected].set_points()

    def run_till_exit(self):
        while True:
            if not self.__process_events():
                break

            self.__draw()

            if not self.pause:
                self.__set_points()
            if self.show_help:
                self.help.selected = self.selected
                self.help.mouse_mode_deletion = self.mouse_mode_deletion
                self.help.draw()

            pygame.display.flip()

    def __draw(self):
        self.surface.fill((0, 0, 0))
        self.__draw_polylines()

    def __draw_polylines(self):
        if not len(self.polylines):
            return

        for i, p in enumerate(self.polylines):
            p.lines_color = self.__recalculate_line_color(p.lines_color)
            p.points_color = self.selected_points_color \
                if i == self.selected else self.points_color
            p.draw_points()

    def __recalculate_line_color(self, color):
        hue = (color.hsla[0] + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        return color

    def __set_points(self):
        for p in self.polylines:
            p.set_points()

    def __process_events(self):
        force_setpoints = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_c:
                    self.mouse_mode_deletion = not self.mouse_mode_deletion
                if event.key == pygame.K_a:
                    self.add_polyline(Polyline)
                if event.key == pygame.K_s:
                    self.add_polyline(Knot)
                if event.key == pygame.K_d:
                    if len(self.polylines) > 1:
                        self.polylines.pop(self.selected)
                        self.selected -= 1 \
                            if self.selected >= len(self.polylines) else 0
                if event.key == pygame.K_KP_PLUS:
                    self.polylines[self.selected].update_steps(1)
                    force_setpoints = True
                if event.key == pygame.K_KP_MINUS:
                    self.polylines[self.selected].update_steps(-1)
                    force_setpoints = True
                if event.key == pygame.K_z:
                    self.polylines[self.selected].update_speed_factor(-0.25)
                if event.key == pygame.K_x:
                    self.polylines[self.selected].update_speed_factor(0.25)
                if event.key == pygame.K_b:
                    self.selected -= 1 if self.selected > 0 else 0
                if event.key == pygame.K_n:
                    self.selected += 1 \
                        if self.selected < len(self.polylines) - 1 else 0
                if event.key == pygame.K_F1:
                    self.show_help = not self.show_help

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_mode_deletion:
                    self.remove_point(event.pos)
                else:
                    self.polylines[self.selected].add_point(
                        event.pos, (random.random() * 2, random.random() * 2))
                    force_setpoints = True

        if force_setpoints and self.pause:
            self.polylines[self.selected].set_points(False)
        return True

    def remove_point(self, mouse_p):
        """Collect all candidate points by mouse precision and remove the nearest one"""
        mouse_p = Vec2d(mouse_p)
        candidates = []
        for poly_i, poly in enumerate(self.polylines):
            for p_i, p in enumerate(poly.points):
                if len(mouse_p - p) <= self.mouse_precision:
                    candidates.append((len(mouse_p - p), poly_i, p_i))
        if len(candidates) > 0:
            poly_i, p_i = sorted(candidates)[0][1:3]
            self.polylines[poly_i].points.pop(p_i)
            if self.pause:
                self.__set_points()

    def reset(self):
        self.polylines.clear()
        self.add_polyline(Knot)


if __name__ == "__main__":
    screen_saver = ScreenSaver()
    screen_saver.run_till_exit()
    exit(0)