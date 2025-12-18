import pygame, sys, random, math
from settings import *
from dungeon import Dungeon, STAIRS
from player import Player
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
clock = pygame.time.Clock()

floor = 1
dungeon = Dungeon(floor)

explored = [[False]*MAP_WIDTH for _ in range(MAP_HEIGHT)]
visible = [[False]*MAP_WIDTH for _ in range(MAP_HEIGHT)]

sx, sy = dungeon.rooms[0].center()
player = Player(sx*TILE, sy*TILE)


def spawn_enemies():
    enemies = []
    # probability-based enemy count
    base_chance = 0.4 + (floor * 0.05)   # increases slowly per floor
    max_enemies = min(3 + floor // 2, 6)

    for _ in range(max_enemies):
        if random.random() < base_chance:
            r = random.choice(dungeon.rooms)
            x, y = r.center()
            enemies.append(Enemy(x*TILE, y*TILE))
    return enemies


enemies = spawn_enemies()


def reveal_start_room():
    room = dungeon.rooms[0]
    for y in range(room.y, room.y + room.h):
        for x in range(room.x, room.x + room.w):
            explored[y][x] = True


def compute_light(radius=6):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible[y][x] = False

    px = player.rect.x // TILE
    py = player.rect.y // TILE

    for y in range(py - radius, py + radius + 1):
        for x in range(px - radius, px + radius + 1):
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                if math.hypot(x - px, y - py) <= radius:
                    visible[y][x] = True
                    explored[y][x] = True


def regenerate(reset=False):
    global dungeon, explored, enemies, floor, player

    if reset:
        floor = 1
    else:
        floor += 1

    dungeon = Dungeon(floor)
    explored = [[False]*MAP_WIDTH for _ in range(MAP_HEIGHT)]
    reveal_start_room()

    sx, sy = dungeon.rooms[0].center()
    player = Player(sx*TILE, sy*TILE)

    enemies = spawn_enemies()
    return enemies


def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if explored[y][x]:
                tile = dungeon.map[y][x]
                if visible[y][x]:
                    color = DARK_GRAY if tile == 0 else GRAY
                    if tile == STAIRS:
                        color = YELLOW
                else:
                    color = (25, 25, 25)
                pygame.draw.rect(screen, color, (x*TILE, y*TILE, TILE, TILE))


def draw_minimap():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if explored[y][x]:
                c = GRAY if dungeon.map[y][x] != 0 else DARK_GRAY
                pygame.draw.rect(screen, c, (x*4, y*4, 4, 4))

    pygame.draw.rect(
        screen, BLUE,
        (player.rect.x//5, player.rect.y//5, 4, 4)
    )


reveal_start_room()

while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_UP]: dy = -2
    if keys[pygame.K_DOWN]: dy = 2
    if keys[pygame.K_LEFT]: dx = -2
    if keys[pygame.K_RIGHT]: dx = 2

    player.move(dx, dy, dungeon)
    player.update()

    compute_light()

    for e in enemies:
        e.update(dungeon, player)
        if e.rect.colliderect(player.rect):
            enemies = regenerate(reset=True)
            break

    if dungeon.map[player.rect.y//TILE][player.rect.x//TILE] == STAIRS:
        enemies = regenerate()

    draw_map()
    player.draw(screen)
    for e in enemies:
        e.draw(screen)

    draw_minimap()
    screen.blit(
        pygame.font.SysFont(None, 24).render(f"Floor: {floor}", True, WHITE),
        (MAP_WIDTH*TILE + 20, 20)
    )

    pygame.display.flip()
    clock.tick(FPS)
