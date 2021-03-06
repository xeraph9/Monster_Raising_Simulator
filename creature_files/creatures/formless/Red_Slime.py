from creature_files.body_types.Body_Formless import Body_Formless as Formless
from creature_files.miscellaneous.Experience import Experience
from creature_files.elements.Fire import Fire
import configparser


class Red_Slime:

    def __init__(self, name, World):

        self.config = configparser.ConfigParser()
        self.config.read('creature_files/creatures_config/formless/' + self.__class__.__name__ + '.ini')
        config_general = self.config['CREATURE']

        self.name = name
        self.race = config_general['race']
        self.description = config_general['description']
        self.age = 1

        self.exp = Experience(self)
        self.element = Fire()
        self.body = Formless(self, World)

        self.is_destroyed = False

    # returns class name as a string with underscores replaced with spaces
    def get_class_name(self):

        class_name = self.__class__.__name__
        class_name_spaces = ""
        for char in class_name:
            if char is '_':
                char = ' '
            class_name_spaces += char
        return class_name_spaces

    # ----------------------------------------------------------------------------------------------------------------------
    #   Update Functions

    def update(self):

        self.age += (1 / 60)    # age approx 1 year every minute
        self.exp.update()
        self.body.update()

    # ----------------------------------------------------------------------------------------------------------------------
    #   Display Functions

    def display_values(self):

        print("G E N E R A L")
        print("Name: " + str(self.name))
        print("Race: " + str(self.race))
        print("Description: " + str(self.description))
        print("Age: " + str(round(self.age, 2)))
        self.exp.display_values()
        print("")
        self.body.display_values()
