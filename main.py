#!/usr/bin/env python3

import math
import pygame
import sys
from enum import Enum
import random



class Box:
	def __init__(self, pos, size, color):
		self.x = pos[0]
		self.y = pos[1]
		self.w = size[0]
		self.h = size[1]
		self.color = color

	def rect(self):
		return (self.x, self.y, self.w, self.h)

class MovingBox:
	def __init__(self, box, direction, speed, max_speed):
		self.box = box
		self.direction = direction
		self.speed = speed
		self.max_speed = max_speed

	def set_moving_in_dir(self, direction):
		self.direction = direction
		self.speed = self.max_speed

	def set_not_moving(self):
		self.speed = 0

class Enemy:
	def __init__(self, moving_box, health, max_health):
		self.moving_box = moving_box
		self.health = health
		self.max_health = max_health
		self.movement_error_chance = 0.2

	def run_ai(self, box):
		dx = box.x - self.moving_box.box.x
		dy = box.y - self.moving_box.box.y
		if abs(dx) > abs(dy):
			if dx > 0:
				direction = Direction.RIGHT
			else:
				direction = Direction.LEFT
		else:
			if dy < 0:
				direction = Direction.UP
			else:
				direction = Direction.DOWN
		if random.random() < self.movement_error_chance:
			direction = random.choice(get_perpendicular_directions(direction))
		self.moving_box.set_moving_in_dir(direction)

class Direction(Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4

def get_perpendicular_directions(direction):
	if direction == direction.LEFT or direction == direction.RIGHT:
		return [Direction.UP, Direction.DOWN]
	else:
		return [Direction.LEFT, Direction.RIGHT]

class PlayerStats:
	def __init__(self, health, max_health, mana, max_mana):
		self.health = health
		self.max_health = max_health
		self.mana = mana
		self.mana_float = mana
		self.max_mana = max_mana

	def gain_health(self, amount):
		self.health = min(self.health + amount, self.max_health)

	def lose_health(self, amount):
		player_stats.health -= amount

	def gain_mana(self, amount):
		self.mana_float = min(self.mana_float + amount, self.max_mana)
		self.mana = int(math.floor(self.mana_float))

	def lose_mana(self, amount):
		self.mana_float -= amount
		self.mana = int(math.floor(self.mana_float))

def render_box(screen, box, camera_pos):
	pygame.draw.rect(screen, box.color, (box.x - camera_pos[0], box.y - camera_pos[1], box.w, box.h))

def render_circle(screen, box, camera_pos):
	pygame.draw.ellipse(screen, COLOR_BLUE, (box.x - camera_pos[0], box.y - camera_pos[1], box.w, box.h))

def ranges_overlap(a_min, a_max, b_min, b_max):
    return (a_min <= b_max) and (b_min <= a_max)

def boxes_intersect(r1, r2):
    return ranges_overlap(r1.x, r1.x + r1.w, r2.x, r2.x + r2.w) \
    	and ranges_overlap(r1.y, r1.y + r1.h, r2.y, r2.y + r2.h)

def render_stat_bar(screen, x, y, w, h, stat, max_stat, color):
	pygame.draw.rect(screen, COLOR_WHITE, (x - 2, y - 2, w + 3, h + 3), 2)
	pygame.draw.rect(screen, color, (x, y, w * stat / max_stat, h))

def update_moving_box_position(moving_box, collide_with_game_boundary):
	if moving_box.direction == Direction.LEFT:
		moving_box.box.x -= moving_box.speed
	elif moving_box.direction == Direction.RIGHT:
		moving_box.box.x += moving_box.speed
	elif moving_box.direction == Direction.UP:
		moving_box.box.y -= moving_box.speed
	elif moving_box.direction == Direction.DOWN:
		moving_box.box.y += moving_box.speed
	if collide_with_game_boundary:
		moving_box.box.x = min(max(moving_box.box.x, 0), GAME_WORLD_SIZE[0] - moving_box.box.w)
		moving_box.box.y = min(max(moving_box.box.y, 0), GAME_WORLD_SIZE[1] - moving_box.box.h)

def try_use_health_potion(number):
	if health_potions[number]:
		health_potions[number] = False
		player_stats.gain_health(10)

def render_ui_potion(screen, x, y, w, h, potion_number):
	pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h), 3)
	if health_potions[potion_number]:
		pygame.draw.rect(screen, (250, 50, 50), (x, y, w, h))
	screen.blit(FONT_LARGE.render(str(potion_number), False, COLOR_WHITE), (x + 8, y + 5))

#Returns whether or not potion was picked up (not picked up if no space for it)
def pick_up_potion():
	empty_slots = [slot for slot in health_potions if not health_potions[slot]]
	if len(empty_slots) > 0:
		slot = empty_slots[0]
		health_potions[slot] = True
		return True
	else:
		return False

COLOR_ATTACK_PROJ = (200, 5, 200)
COLOR_WHITE = (250, 250, 250)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (250, 0, 0)
COLOR_BLUE = (0, 0, 250)
BG_COLOR = (200,200,200)
SCREEN_SIZE = (700, 600)
CAMERA_SIZE = (700, 500)
UI_BOX = Box((0, CAMERA_SIZE[1]), (SCREEN_SIZE[0], SCREEN_SIZE[1] - CAMERA_SIZE[1]), (0,0,0))
GAME_WORLD_SIZE = (1000, 1000)
GAME_WORLD_BOX = Box((0, 0), GAME_WORLD_SIZE, (0,0,0))
FOOD_SIZE = (30, 30)
FOOD_COLOR = (50, 200, 50)
ENEMY_SIZE = (30, 30)
ENEMY_COLOR = COLOR_RED
ENEMY_SPEED = 0.4
MANA_REGEN = 0.03
PLAYER_SPEED = 2
ATTACK_PROJ_SIZE = (35, 35)
PYGAME_MOVEMENT_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
DIRECTION_BY_PYGAME_MOVEMENT_KEY = {
	pygame.K_LEFT: Direction.LEFT,
	pygame.K_RIGHT: Direction.RIGHT,
	pygame.K_UP: Direction.UP,
	pygame.K_DOWN: Direction.DOWN
}

pygame.init()
pygame.font.init()
FONT_LARGE = pygame.font.SysFont('Arial', 30)
FONT_SMALL = pygame.font.Font(None, 25)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

camera_pos = (0, 0)
player = MovingBox(Box((100, 100), (50, 50), (250,250,250)), Direction.RIGHT, 0, PLAYER_SPEED)
projectiles = []
food_boxes = [Box(pos, FOOD_SIZE, FOOD_COLOR) for pos in [(150, 350), (450, 300), (560, 550), (30, 520), \
	(200, 500), (300, 500), (410, 420)]]
enemies = [Enemy(MovingBox(Box(pos, ENEMY_SIZE, ENEMY_COLOR), Direction.LEFT, ENEMY_SPEED, ENEMY_SPEED), 3, 3) for pos \
	in [(320, 220), (370, 320), (420, 10)]]
player_stats = PlayerStats(3, 20, 50, 100)
heal_mana_cost = 10
attack_mana_cost = 5
ticks_since_ai_ran = 0
AI_RUN_INTERVAL = 750

health_potions = {
	1: True,
	2: False,
	3: True,
	4: True,
	5: True
}

movement_keys_down = []

while(True):

	# ------------------------------------
	#         HANDLE EVENTS
	# ------------------------------------

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key in PYGAME_MOVEMENT_KEYS:
				if event.key in movement_keys_down:
					movement_keys_down.remove(event.key)
				movement_keys_down.append(event.key)
			elif event.key == pygame.K_a:
				if player_stats.mana >= heal_mana_cost:
					player_stats.lose_mana(heal_mana_cost)
					player_stats.gain_health(10)
			elif event.key == pygame.K_f:
				if player_stats.mana >= attack_mana_cost:
					player_stats.lose_mana(attack_mana_cost)
					proj_box = Box((player.box.x + player.box.w / 2 - ATTACK_PROJ_SIZE[0] / 2, \
						player.box.y + player.box.h / 2 - ATTACK_PROJ_SIZE[1] / 2), \
						ATTACK_PROJ_SIZE, COLOR_ATTACK_PROJ)
					projectiles.append(MovingBox(proj_box, player.direction, 4, 4))
			elif event.key == pygame.K_1:
				try_use_health_potion(1)
			elif event.key == pygame.K_2:
				try_use_health_potion(2)
			elif event.key == pygame.K_3:
				try_use_health_potion(3)
			elif event.key == pygame.K_4:
				try_use_health_potion(4)
			elif event.key == pygame.K_5:
				try_use_health_potion(5)
		if event.type == pygame.KEYUP:
			if event.key in  PYGAME_MOVEMENT_KEYS:
				movement_keys_down.remove(event.key)
		if movement_keys_down:
			last_pressed_movement_key = movement_keys_down[-1]
			player.set_moving_in_dir(DIRECTION_BY_PYGAME_MOVEMENT_KEY[last_pressed_movement_key])
		else:
			player.set_not_moving()


	# ------------------------------------
	#         UPDATE MOVING ENTITIES
	# ------------------------------------

	clock.tick()
	ticks_since_ai_ran += clock.get_time()
	if(ticks_since_ai_ran > AI_RUN_INTERVAL):
		ticks_since_ai_ran = 0
		should_run_enemy_ai = True
	else:
		should_run_enemy_ai = False
	for e in enemies:
		if should_run_enemy_ai:
			e.run_ai(player.box)
		update_moving_box_position(e.moving_box, True)
	update_moving_box_position(player, True)


	# ------------------------------------
	#         HANDLE COLLISIONS
	# ------------------------------------

	projectiles_to_delete = []
	food_boxes_to_delete = []
	enemies_to_delete = []
	for projectile in projectiles:
		update_moving_box_position(projectile, False)
		if not boxes_intersect(projectile.box, GAME_WORLD_BOX):
			projectiles_to_delete.append(projectile)
	for box in food_boxes:
		if boxes_intersect(player.box, box):
			did_pick_up = pick_up_potion()
			if did_pick_up:
				food_boxes_to_delete.append(box)
	for enemy in enemies:
		box = enemy.moving_box.box
		if boxes_intersect(player.box, box):
			enemies_to_delete.append(enemy)
			player_stats.lose_health(2)
		for projectile in projectiles:
			if boxes_intersect(box, projectile.box):
				enemy.health -= 1
				if enemy.health <= 0:
					enemies_to_delete.append(enemy)
				projectiles_to_delete.append(projectile)
	projectiles = [p for p in projectiles if p not in projectiles_to_delete]
	food_boxes = [b for b in food_boxes if b not in food_boxes_to_delete]
	enemies = [b for b in enemies if b not in enemies_to_delete]


	# ------------------------------------
	#         REGEN MANA
	# ------------------------------------

	player_stats.gain_mana(MANA_REGEN)


	# ------------------------------------
	#         UPDATE CAMERA POSITION
	# ------------------------------------

	camera_pos = (min(max(player.box.x - CAMERA_SIZE[0] / 2, 0), GAME_WORLD_SIZE[0] - CAMERA_SIZE[0]), \
		min(max(player.box.y - CAMERA_SIZE[1] / 2, 0), GAME_WORLD_SIZE[1] - CAMERA_SIZE[1]))


	# ------------------------------------
	#         RENDER EVERYTHING
	# ------------------------------------

	screen.fill(BG_COLOR)
	for box in food_boxes + [e.moving_box.box for e in enemies] + [p.box for p in projectiles]:
		render_box(screen, box, camera_pos)

	render_box(screen, player.box, camera_pos)
	render_circle(screen, player.box, camera_pos)

	for enemy in enemies:
		render_stat_bar(screen, enemy.moving_box.box.x - camera_pos[0] + 1, enemy.moving_box.box.y - camera_pos[1] - 10, \
			enemy.moving_box.box.w - 2, 5, enemy.health, enemy.max_health, COLOR_RED)

	pygame.draw.rect(screen, COLOR_BLACK, (0, 0, CAMERA_SIZE[0], CAMERA_SIZE[1]), 3)
	pygame.draw.rect(screen, COLOR_BLACK, (0, CAMERA_SIZE[1], SCREEN_SIZE[0], SCREEN_SIZE[1] - CAMERA_SIZE[1]))


	screen.blit(FONT_LARGE.render("Health", False, COLOR_WHITE), (UI_BOX.x + 10, UI_BOX.y + 10))
	render_stat_bar(screen, UI_BOX.x + 10, UI_BOX.y + 40, 100, 25, player_stats.health, player_stats.max_health, COLOR_RED)
	health_text = str(player_stats.health) + "/" + str(player_stats.max_health)
	screen.blit(FONT_LARGE.render(health_text, False, COLOR_WHITE), (UI_BOX.x + 30, UI_BOX.y + 43))

	screen.blit(FONT_LARGE.render("Mana", False, COLOR_WHITE), (UI_BOX.x + 130, UI_BOX.y + 10))
	render_stat_bar(screen, UI_BOX.x + 130, UI_BOX.y + 40, 100, 25, player_stats.mana, player_stats.max_mana, COLOR_BLUE)
	mana_text = str(player_stats.mana) + "/" + str(player_stats.max_mana)
	screen.blit(FONT_LARGE.render(mana_text, False, COLOR_WHITE), (UI_BOX.x + 150, UI_BOX.y + 43))

	screen.blit(FONT_LARGE.render("Potions", False, COLOR_WHITE), (UI_BOX.x + 250, UI_BOX.y + 10))
	render_ui_potion(screen, UI_BOX.x + 250, UI_BOX.y + 39, 27, 27, 1)
	render_ui_potion(screen, UI_BOX.x + 280, UI_BOX.y + 39, 27, 27, 2)
	render_ui_potion(screen, UI_BOX.x + 310, UI_BOX.y + 39, 27, 27, 3)
	render_ui_potion(screen, UI_BOX.x + 340, UI_BOX.y + 39, 27, 27, 4)
	render_ui_potion(screen, UI_BOX.x + 370, UI_BOX.y + 39, 27, 27, 5)

	ui_text = "['A' to heal (" + str(heal_mana_cost) + ")] " + \
		"['F' to attack (" + str(attack_mana_cost) + ")]"
	text_surface = FONT_SMALL.render(ui_text, False, COLOR_WHITE)
	screen.blit(text_surface, (UI_BOX.x + 20, UI_BOX.y + 75))

	pygame.draw.rect(screen, COLOR_WHITE, UI_BOX.rect(), 1)
	
	pygame.display.update()

