import pygame
import sys
from random import randint 
pygame.init()

clock = pygame.time.Clock()
window = pygame.display.set_mode((700, 500))
finish = 0

pygame.font.init()
font = pygame.font.Font(None, 70)
win = font.render('YOU WIN!', True, (0, 0, 0))
lose = font.render('YOU LOSE!', True, (0, 0, 0))

class Room(): # класс комнаты
	def __init__(self, image, w, h, chests = [], enemys = [], doors = []):
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(50, 50))
		self.ground = []
		x = 50
		y = 50
		self.chests = chests
		self.enemys = enemys
		self.doors = doors
		while x != w - 50:
			y = 50
			while y != h - 50:
				self.ground.append(Flor(image = image, x = x, y = y))
				y += 50
			x += 50

class Flor(): #класс пола
	def __init__(self, image, x, y):
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(50, 50))
		self.x = x 
		self.y = y

	def reset(self):
		window.blit(self.image, (self.x, self.y))

class Chest(): #класс сундука
	def __init__(self,  x, y, image, status, open_image, empty_image):
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(50, 50))
		self.locked_image = self.image
		self.open_image = pygame.image.load(open_image)
		self.open_image = pygame.transform.scale(self.open_image, (50, 50))
		self.empty_image = pygame.image.load(empty_image)
		self.empty_image = pygame.transform.scale(self.empty_image, (50, 50))
		self.status =  status
		self.x = x 
		self.y = y 
		self.mask = pygame.mask.from_surface(self.image)
 
	def reset(self):
		window.blit(self.image, (self.x, self.y))

class Hero():
	def __init__(self, image, x, y, health, room = None):
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(80, 80))
		self.counter = 0
		self.door_counter = 0
		self.kill_counter = 0
		self.x = x 
		self.y = y
		self.speed = 5
		self.mask = pygame.mask.from_surface(self.image)
		self.sword_sound = pygame.mixer.Sound('sword_sound.mp3')
		self.chest_sound = pygame.mixer.Sound('sunduk_sound.mp3')
		self.money_sound = pygame.mixer.Sound('money_sound.mp3')
		self.door_sound = pygame.mixer.Sound('door_sound.mp3')
		self.door_sound.set_volume(0.8)
		self.room = room
		self.speed_x = 0 
		self.speed_y = 0
		self.health = health

	def reset(self):
		window.blit(self.image, (self.x, self.y))

	def controller(self):
		keys_pressed=pygame.key.get_pressed()
		if  keys_pressed[pygame.K_SPACE]:
			print(111)
		if keys_pressed[pygame.K_w]:
			self.y -= self.speed 
			self.speed_y  = - self.speed
		if  keys_pressed[pygame.K_a]:
			self.x -= self.speed
			self.speed_x = - self.speed
		if keys_pressed[pygame.K_s]:
			self.y += self.speed
			self.speed_y = self.speed
		if  keys_pressed[pygame.K_d]:
			self.x += self.speed
			self.speed_x = self.speed
		self.check_bounds()

	def check_bounds(self): #проверка границ
		if self.x < 45:
			self.x = 45
		if self.y < 50:
			self.y = 50
		if self.y >  375:
			self.y = 375
		if self.x  > 575:
			self.x = 575

	def look_out(self, chest):
		offset = (chest.x - self.x, chest.y - self.y)
		collision = self.mask.overlap_area(chest.mask, offset)
		if chest.image == chest.open_image:
			self.counter += 1 
		if collision > 5:
			keys_pressed=pygame.key.get_pressed()
			if  keys_pressed[pygame.K_f] and chest.image == chest.locked_image:
				chest.image = chest.open_image
				self.chest_sound.play()
				return
			if  keys_pressed[pygame.K_f] and chest.image == chest.open_image and self.counter > 20:
				chest.image = chest.empty_image	
				self.money_sound.play()
				self.counter = 0	
			self.x -= self.speed_x
			self.y -= self.speed_y

	def kill_enemy(self, enemy):
		offset = (enemy.x - self.x, enemy.y - self.y)
		collision = self.mask.overlap_area(enemy.mask, offset)
		print(collision)
		if collision > 5:
			self.kill_counter += 1
			mouse_pressed = pygame.mouse.get_pressed()
			if mouse_pressed[0] == True and enemy.health == 0 and self.kill_counter > 15:
				self.kill_counter = 0
				self.room.enemys.remove(enemy)
				self.sword_sound.play()
			elif mouse_pressed[0] == True and enemy.health > 0 and self.kill_counter > 15:
				self.kill_counter = 0
				enemy.health -= 1
				self.sword_sound.play()

	def touch_door(self, door):
		offset = (door.x -  self.x, door.y - self.y)
		collision = self.mask.overlap_area(door.mask, offset)
		if collision > 20:
			self.door_counter += 1
			keys_pressed=pygame.key.get_pressed()
			if  keys_pressed[pygame.K_e] and self.door_counter > 40:
				self.door_counter = 0
				test_hero.room = door.go_to
				self.door_sound.play()

class Enemy():
	def __init__(self, x, y, image, health = 0):
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(150, 150))
		self.x = x
		self.y = y
		self.mask = pygame.mask.from_surface(self.image)
		self.health = health

	def intelect(self):
		if self.x < test_hero.x:
			self.x += 1
		else:
			self.x -= 1
		if self.y < test_hero.y:
			self.y += 1
		else:
			self.y -= 1

	def reset(self):
		window.blit(self.image, (self.x, self.y))

class Boss(Enemy):
	def __init__(self, x, y, image, health):
		super().__init__(x, y, image, health)
		self.wait = 10
		

	def intelect(self):
		if self.x < test_hero.x:
			self.x += 1.5
		else:
			self.x -= 1.5
		if self.y < test_hero.y:
			self.y += 1.5
		else:
			self.y -= 1.5
		self.minions()

	def minions(self):
		if self.wait <= 0 and len(test_room_2.enemys) <= 2 :
			mini_enemy = Enemy(image = 'enemy.png', x = 400, y = 50, health = 5)
			test_room_2.enemys.append(mini_enemy)
			self.wait = 300
		else:
			self.wait -= 1

class Final_boss(Enemy):
	def  __init__(self, x, y, image, health):
		super().__init__(x, y, image, health)
		self.punch = pygame.mixer.Sound('punch.mp3')

	def intelect(self):
		if self.x < test_hero.x:
			self.x += 2
		else:
			self.x -= 2
		if self.y < test_hero.y:
			self.y += 2
		else:
			self.y -= 2
		self.attack_hero(test_hero)

	def attack_hero(self, hero):
		offset = (hero.x - self.x, hero.y - self.y)
		collision = self.mask.overlap_area(hero.mask, offset)	
		attack = randint(0, 5)
		'''if collision > 2: 
			if attack == 0:
				hero.health -= 15
			elif attack == 1 or attack == 2:
				hero.health -= 15
			elif attack == 3:
				hero.health -= 15
			elif attack == 4:
				hero.health -= 15
			elif attack == 5:
				hero.health -= 15'''
		if collision > 25:
			hero.health -= 0.05
			self.punch.play()
	
class Door():
	def __init__(self, x, y, image, go_from = 'defolt', go_to = 'defolt'):
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(85, 90))
		self.x = x
		self.y = y
		self.go_from = go_from
		self.go_to = go_to
		self.mask = pygame.mask.from_surface(self.image)

	def reset(self):
		window.blit(self.image, (self.x, self.y))

'''plitcka = Flor(image = 'flor_rock.png',x = 0, y = 0)''' #Сделать одну плитку

test_room = Room(image = 'flor_rock.png', w = 700, h = 500)
test_room_2 = Room(image = 'red_flor_rock.png', w = 700, h = 500, doors = [], enemys = [], chests = [])
test_room_3 = Room(image = 'hell_flor.png', w = 700, h = 500, doors = [], enemys = [], chests = [])
test_door = Door(image = 'door_8bit.png', x = 300, y = 50, go_from = test_room, go_to = test_room_2)
test_chest = Chest(image = 'chest_locked.png', x = 50, y = 400, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png')
test_chest_1 = Chest(image = 'chest_locked.png', x = 100, y = 400, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png')
test_hero = Hero(image = 'character.png', x = 100, y = 250, health = 15)
test_enemy  = Enemy(image = 'enemy.png', x = 100, y = 50, health = 5) 
test_boss = Boss(image = 'demon_8bit.png', x = 100, y = 50, health = 10)
test_final_boss = Final_boss(image = 'finall_boss.png', x = 100, y = 50, health = 10)

test_room.chests.append(test_chest)
test_room.chests.append(test_chest_1)
test_room.enemys.append(test_enemy)
test_room.doors.append(test_door)
test_room_2.enemys.append(test_boss)
test_room_3.enemys.append(test_final_boss)
test_room_2.chests.append(Chest(image = 'chest_locked.png', x = 50, y = 400, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_2.chests.append(Chest(image = 'chest_locked.png', x = 50, y = 50, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_2.chests.append(Chest(image = 'chest_locked.png', x = 600, y = 400, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_2.chests.append(Chest(image = 'chest_locked.png', x = 600, y = 50, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_3.chests.append(Chest(image = 'chest_locked.png', x = 50, y = 50, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_3.chests.append(Chest(image = 'chest_locked.png', x = 100, y = 50, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_3.chests.append(Chest(image = 'chest_locked.png', x = 600, y = 50, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_3.chests.append(Chest(image = 'chest_locked.png', x = 550, y = 50, status = 'locked', open_image = 'chest.png', empty_image = 'empty_chest.png'))
test_room_2.doors.append(Door(image = 'door_8bit.png', x = 300, y = 360, go_from = test_room_2, go_to = test_room_3))
test_room_2.doors.append(Door(image = 'door_8bit.png', x = 300, y = 50, go_from = test_room_2, go_to = test_room))
test_room_3.doors.append(Door(image = 'door_8bit.png', x = 300, y = 50, go_from = test_room_3, go_to = test_room_2))
test_hero.room = test_room

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	if finish <= 1:
		pygame.display.update()
		window.fill((0, 0, 0))
		'''plitcka.reset()'''  #Отоброзить тестовую плитку
		for plitcka in test_hero.room.ground:
			plitcka.reset()
		for door in test_hero.room.doors:
			door.reset()
			test_hero.touch_door(door)
		for enemy in test_hero.room.enemys:
			enemy.intelect()
			enemy.reset() 
			test_hero.kill_enemy(enemy)
		test_hero.reset()
		if test_hero.health <= 0:
			window.blit(lose, (200, 200))
			finish += 1
		if len(test_room_3.enemys) == 0:
			window.blit(win, (200, 200))
			finish += 1
		for chest in  test_hero.room.chests:
			chest.reset()
			test_hero.look_out(chest)
		test_hero.controller()
	pygame.display.update()
	clock.tick(60) 