from typing import Tuple

from pythongame.common import Millis


class VisualEffect:
    def __init__(self, max_age):
        self._age = 0
        self._max_age = max_age
        self.has_expired = False

    def notify_time_passed(self, time_passed: Millis):
        self._age += time_passed
        if self._age > self._max_age:
            self.has_expired = True


class VisualLine(VisualEffect):
    def __init__(self, color: Tuple[int, int, int], start_position: Tuple[int, int], end_position: Tuple[int, int],
                 max_age: Millis):
        super().__init__(max_age)
        self.color = color
        self.start_position = start_position
        self.end_position = end_position


class VisualCircle(VisualEffect):
    def __init__(self, color: Tuple[int, int, int], center_position: Tuple[int, int], radius: int, max_age: Millis):
        super().__init__(max_age)
        self.color = color
        self.center_position = center_position
        self.start_radius = int(radius / 2)
        self.end_radius = radius

    def circle(self):
        position = self.center_position[0], self.center_position[1]
        radius = self.start_radius + int(self._age / self._max_age * (self.end_radius - self.start_radius))
        return position, radius


class VisualRect(VisualEffect):
    def __init__(self, color: Tuple[int, int, int], center_position: Tuple[int, int], width: int, max_age: Millis):
        super().__init__(max_age)
        self.color = color
        self.center_position = center_position
        self.start_width = int(width * 0.75)
        self.end_width = width

    def rect(self):
        width = self.start_width + int(self._age / self._max_age * (self.end_width - self.start_width))
        return self.center_position[0] - width / 2, self.center_position[1] - width / 2, width, width
