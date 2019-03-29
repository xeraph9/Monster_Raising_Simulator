# Class for Formless body types
# Slimes, etc
from creature_files.miscellaneous.Resources import Resources
from creature_files.body_parts.Eye import Eye
from creature_files.body_parts.Brain import Brain
from creature_files.body_parts.Heart import Heart
from creature_files.body_parts.Stomach import Stomach
from creature_files.body_parts.Lung import Lung
from creature_files.miscellaneous.Psychology import Psychology
from creature_files.miscellaneous.Stats import Stats
from creature_files.behaviour.World_Movement import World_Movement as World_Movement
import creature_files.miscellaneous.Weight as Weight


class Body_Formless:

    def __init__(self, whole_body, world):

        self.whole_body = whole_body
        self.world = world

        # Body Parts
        # TODO: Each bodypart should come with their own resources and base stats (partially done)
        #  which will all contribute to the body's overall stats
        self.eye_l = Eye(self)
        self.eye_r = Eye(self)
        self.brain = Brain(self)
        self.heart = Heart(self)
        self.stomach = Stomach(self, world)
        self.lung_l = Lung(self)
        self.lung_r = Lung(self)
        self.body_parts = [self.eye_l,
                           self.eye_r,
                           self.brain,
                           self.heart,
                           self.stomach,
                           self.lung_l,
                           self.lung_r]    # add all body parts into an array


        # Stats
        # add up stats of all individual body parts to get totals
        # TODO: Look into a better way of doing stats
        self.stats = Stats(0, 0, 1, 0, 0, 2,
                           0, 0, 0, 0)  # body base stats
        self.stats = Stats.combine_stats(self.stats, self.body_parts)
        self.weight = Weight.calculate_weight(10, self.body_parts)

        # Resources
        self.health = Resources.Health(self, 100, 75, 2)
        self.aether = Resources.Aether(self, 150, 75, 2)
        self.stamina = Resources.Stamina(self, 100, 20)

        # Behaviours
        self.world_movement = World_Movement(self, world)
        self.psychology = Psychology()

    # ----------------------------------------------------------------------------------------------------------------------
    #   Display Functions

    def display_body_parts(self):

        print("B O D Y - P A R T S")
        for part in self.body_parts:
            print(" " + part.type)

    def display_body_part_values(self):

        for part in self.body_parts:
            part.display_values()
            print("")

    def display_miscellaneous_values(self):
        print("Weight: " + str(self.weight))

    def display_values(self):
        print("Weight: " + str(self.weight))
        print("")
        print("R E S O U R C E S")
        self.health.display_values()
        self.aether.display_values()
        self.stamina.display_values()
        self.stamina.display_activity_level()
        print("")
        self.stomach.display_values()
        self.stomach.display_hunger_values_full()
        print("")
        self.world_movement.display_closest_food()
        #print("")
        #print("M I S C E L L A N E O U S")
        #self.display_miscellaneous_values()
        #print("")


    # ----------------------------------------------------------------------------------------------------------------------
    #   Update Functions

    # TODO: might make more sense to move this to miscellaneous.Weight module
    def update_weight(self):

        self.weight = Weight.calculate_weight(10, self.body_parts)

    def update_resources(self):

        self.health.update()
        self.aether.update()
        self.stamina.update()

    def update_body_parts(self):

        for part in self.body_parts:
            part.update()

    def update(self):

        self.update_resources()
        self.update_body_parts()
        self.world_movement.update()
        self.update_weight()