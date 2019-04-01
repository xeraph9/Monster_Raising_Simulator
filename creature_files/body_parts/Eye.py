# stats are Dex and Vision
from creature_files.miscellaneous.Stats import Stats


class Eye:

    def __init__(self, body):

        self.config = body.creature.config[str.upper(self.__class__.__name__)]

        self.name = str(body.creature.race) + " Eye"
        self.type = "Eye"
        self.weight = 0.5
        self.stats = Stats(self)

    # ----------------------------------------------------------------------------------------------------------------------
    #   Display Functions

    def display_values_full(self):

        self.display_values()
        self.stats.display_values()

    def display_values(self):

        print("E Y E")
        print("Name: " + str(self.name))
        print("Type: " + str(self.type))
        print("Weight: " + str(self.weight))

    # ----------------------------------------------------------------------------------------------------------------------
    #   Update Functions

    def update(self):

        pass
