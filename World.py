# 妖怪牧場
import pygame, sys
from creature_files.creatures.formless.Blue_Slime import Blue_Slime
from creature_files.creatures.formless.Red_Slime import Red_Slime
from creature_files.creatures.formless.Yellow_Slime import Yellow_Slime
from creature_files.creatures.formless.Eldritch_Slime import Eldritch_Slime
from food.Berry import Berry
from food.Drum_Stick import Drum_Stick
from items.training.Book import Book
import time
import configparser
import random
import os

# TODO: world 'cleaning up' (removal of dead creature_files, eaten food, etc) should be controlled by World, current controlled within objects themselves

config = configparser.ConfigParser()
config.read('world_config.ini')
config_world = config['WORLD']

class World:

    def __init__(self):

        pygame.init()  # initiate pygame
        pygame.display.set_caption('Yōkai Ranch')
        pygame.key.set_repeat(500, 100)

        self.FPS = 60

        self.creature_container = []
        self.max_creatures = int(config_world['max_creatures'])

        self.name_container = []

        self.food_container = []
        self.waste_container = []
        self.item_container = []

        self.width = int(config_world['width'])
        self.height = int(config_world['height'])

        self.surface = pygame.display.set_mode((self.width, self.height))  # pygame.Surface object for the window
        self.surface_color = (245, 245, 220)
        self.surface.fill(self.surface_color)

        self.background = pygame.image.load('assets/world/grass.png')
        self.surface.blit(self.background, (0, 0))

        self.update_counter = 0
        self.display_counter = 0

        self.update_increment = 1
        self.display_increment = 1
        self.time_start = time.time()

        self.display_hitbox = False
        self.display_vision = False

    def spawn_blue_slime(self):

        self.name_tracker = len(self.creature_container)
        if self.name_tracker < self.max_creatures:
            self.creature_container.append(Blue_Slime(self.get_name(), self))

    def spawn_red_slime(self):

        self.name_tracker = len(self.creature_container)
        if self.name_tracker < self.max_creatures:
            self.creature_container.append(Red_Slime(self.get_name(), self))

    def spawn_yellow_slime(self):

        self.name_tracker = len(self.creature_container)
        if self.name_tracker < self.max_creatures:
            self.creature_container.append(Yellow_Slime(self.get_name(), self))

    def spawn_eldritch_slime(self):

        self.name_tracker = len(self.creature_container)
        if self.name_tracker < self.max_creatures:
            self.creature_container.append(Eldritch_Slime(self.get_name(), self))

    def toggle_hitbox(self):

        if self.display_hitbox:
            for each in self.creature_container:
                each.body.world_movement.display_hitbox()

    def toggle_vision(self):

        if self.display_vision:
            for each in self.creature_container:
                each.body.world_movement.display_vision_radius()

    def clean_waste(self, waste):

        if waste in self.waste_container:
            self.waste_container.remove(waste)

    def clean_food(self, food):

        if food in self.food_container:
            self.food_container.remove(food)

    def get_name(self):

        name_list = open('assets/names.txt', 'r')
        list = name_list.readlines()

        while True:
            name = list[random.randint(0, len(list) - 1)].rstrip()
            for each in self.creature_container:
                if each.name == name:
                    continue
            return name


World = World()
paused = False
day_tracker = 0

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # pause / unpause
            if event.key == pygame.K_SPACE:
                if paused is True:
                    paused = False
                    print("----------------------------------------")
                    print("         G A M E - R E S U M E D        ")
                    print("----------------------------------------")
                else:
                    paused = True
                    print("----------------------------------------")
                    print("         G A M E - P A U S E D          ")
                    print("----------------------------------------")

        if event.type == pygame.KEYDOWN and not paused:

            # spawn red slime
            if event.key == pygame.K_1:
                World.spawn_red_slime()
                print("     Spawned Red Slime!")

            # spawn blue slime
            if event.key == pygame.K_2:
                World.spawn_blue_slime()
                print("     Spawned Blue Slime!")

            # spawn yellow slime
            if event.key == pygame.K_3:
                World.spawn_yellow_slime()
                print("     Spawned Yellow Slime!")

            # spawn eldritch slime
            if event.key == pygame.K_4:
                World.spawn_eldritch_slime()
                print("     Spawned Eldritch Slime!")

            # spawn berry
            if event.key == pygame.K_9:
                x, y = pygame.mouse.get_pos()
                if len(World.food_container) < (3 + (len(World.creature_container) * 3)):
                    berry = Berry(World, x, y)
                    World.food_container.append(berry)
                    print("     Spawned Berry!")

            # spawn drum stick
            if event.key == pygame.K_0:
                x, y = pygame.mouse.get_pos()
                if len(World.food_container) < (3 + (len(World.creature_container) * 3)):
                    drum_stick = Drum_Stick(World, x, y)
                    World.food_container.append(drum_stick)
                    print("     Spawned Drum Stick!")

            # spawn book
            if event.key == pygame.K_b:
                x, y = pygame.mouse.get_pos()
                book = Book(World, x, y)
                World.item_container.append(book)
                print("     Spawned Book!")

            # clean waste
            if event.key == pygame.K_c:
                waste_deleted = False
                x, y = pygame.mouse.get_pos()
                click_radius = 10

                for waste in World.waste_container:
                    for num1 in range(-click_radius, click_radius):
                        for num2 in range(-click_radius, click_radius):
                            if waste.x == (x + num1) and waste.y == (y + num2) and waste_deleted is False:
                                print("     Waste Cleaned!")
                                World.clean_waste(waste)
                                waste_deleted = True
                waste_deleted = False

            # display hitbox
            if event.key == pygame.K_h:
                if World.display_hitbox:
                    World.display_hitbox = False
                else:
                    World.display_hitbox = True

            # display vision range
            if event.key == pygame.K_v:
                if World.display_vision:
                    World.display_vision = False
                else:
                    World.display_vision = True

            # spend stat points on str
            if event.key == pygame.K_KP1:
                for each in World.creature_container:
                    each.body.stats.increase_base_stat(each, 'str')

            # spend stat points on int
            if event.key == pygame.K_KP2:
                for each in World.creature_container:
                    each.body.stats.increase_base_stat(each, 'int')

            # spend stat points on end
            if event.key == pygame.K_KP3:
                for each in World.creature_container:
                    each.body.stats.increase_base_stat(each, 'end')

            # spend stat points on dex
            if event.key == pygame.K_KP4:
                for each in World.creature_container:
                    each.body.stats.increase_base_stat(each, 'dex')

            # spend stat points on spd
            if event.key == pygame.K_KP5:
                for each in World.creature_container:
                    each.body.stats.increase_base_stat(each, 'spd')

            # spend stat points on luk
            if event.key == pygame.K_KP6:
                for each in World.creature_container:
                    each.body.stats.increase_base_stat(each, 'luk')

            # give experience
            if event.key == pygame.K_x:
                for each in World.creature_container:
                    exp = int(config_world['exp_gain'])
                    each.exp.update_experience_current(exp)
                    print("     " + each.name + " gained " + "{:,}".format(exp) + " exp!")

            # speed / slow time
            if event.key == pygame.K_z:
                if World.update_increment == 1:
                    World.update_increment = 10
                else:
                    World.update_increment = 1

            # cripple a creature's body part, setting its stats to zero
            if event.key == pygame.K_k:
                creature = None
                creature_name = str.capitalize(input("Enter name of creature to cripple: "))

                for each in World.creature_container:

                    if each.name == creature_name:
                        creature = each
                        creature_name = each.name

                if creature is None:
                    print("  Creature not found!")
                else:
                    creature.body.display_body_parts()

                    part = input("Enter Body Part to cripple: ")
                    number_of_parts = len(each.body.get_body_parts(part))

                    if number_of_parts == 0:
                        print("Body part not found!")
                    else:
                        print(creature_name + " has " + str(number_of_parts) + " " + part + "(s)")
                        part_number = int(input("Which " + str.capitalize(part) + " you want to cripple? (Enter a number): ")) - 1

                        if part_number < 0 or part_number > number_of_parts - 1:
                            print("Body part not found!")
                        elif creature.body.get_body_parts(part)[part_number].is_crippled:
                            print("Part is already crippled!")
                        else:
                            creature.body.get_body_parts(part)[part_number].is_crippled = True
                            print(str.capitalize(part) + " crippled!")
                time.sleep(2)





    if not paused:
        World.toggle_hitbox()
        World.toggle_vision()

        if World.update_counter >= World.FPS:

            World.surface.fill(World.surface_color)
            World.surface.blit(World.background, (0,0))

            for each in World.food_container:
                each.update()

            for each in World.waste_container:
                each.update()

            for each in World.item_container:
                each.update()

            for each in World.creature_container:
                each.update()

            if config_world['display_names'] == 'True':
                for each in World.creature_container:
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text = font.render(each.name, True, (100, 100, 100))
                    textRect = text.get_rect()
                    textRect.center = (each.body.world_movement.x_center, each.body.world_movement.y_center - 40)
                    World.surface.blit(text, textRect)

            World.update_counter = 0

        if World.display_counter >= World.FPS:
            if config_world['display_data'] == 'True':
                print("----------------------------------------")
                print("          W O R L D - S T A T S         ")
                print("----------------------------------------")
                print("Time Elapsed: " + str(round(time.time() - World.time_start, 0)) + " seconds")
                print("Creatures: " + str(World.creature_container))
                print("Items: " + str(World.item_container))
                print("Food: " + str(World.food_container))
                print("Waste: " + str(World.waste_container))
                print("")

                for each in World.food_container:
                    pass

                for each in World.waste_container:
                    pass

                for each in World.creature_container:
                    each.display_values()

                print("World Actions:")


            World.display_counter = 0

        pygame.display.update()
        pygame.time.Clock().tick(World.FPS)
        World.update_counter += World.update_increment
        World.display_counter += World.display_increment
