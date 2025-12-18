import random
from settings import MAP_WIDTH, MAP_HEIGHT

WALL = 0
FLOOR = 1
STAIRS = 2


class Room:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def center(self):
        return (self.x + self.w // 2, self.y + self.h // 2)

    def intersects(self, other):
        return (
            self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y
        )


class Dungeon:
    def __init__(self, floor=1):
        self.floor = floor
        self.map = [[WALL]*MAP_WIDTH for _ in range(MAP_HEIGHT)]
        self.rooms = []
        self.generate()

    def generate(self):
        room_attempts = 20
        max_rooms = 12

        for _ in range(room_attempts):
            if len(self.rooms) >= max_rooms:
                break

            w = random.randint(6, 10)
            h = random.randint(6, 10)
            x = random.randint(1, MAP_WIDTH - w - 2)
            y = random.randint(1, MAP_HEIGHT - h - 2)

            room = Room(x, y, w, h)
            if any(room.intersects(r) for r in self.rooms):
                continue

            self.create_room(room)

            if self.rooms:
                self.connect_rooms(self.rooms[-1], room)

            self.rooms.append(room)

        cx, cy = self.rooms[-1].center()
        self.map[cy][cx] = STAIRS

    def create_room(self, room):
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                self.map[y][x] = FLOOR

    def connect_rooms(self, r1, r2):
        x1, y1 = r1.center()
        x2, y2 = r2.center()

        if random.choice([True, False]):
            self.h_corridor(x1, x2, y1)
            self.v_corridor(y1, y2, x2)
        else:
            self.v_corridor(y1, y2, x1)
            self.h_corridor(x1, x2, y2)

    def h_corridor(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[y][x] = FLOOR

    def v_corridor(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[y][x] = FLOOR

    def is_walkable(self, x, y):
        return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and self.map[y][x] != WALL
