class Detector:
    def __init__(self, data_picture: object):
        self.data_picture: object = data_picture

    def count_class(self, name_class: str) -> int:
        count: int = 0
        for data in self.data_picture["predictions"]:
            if data["class"] == name_class:
                count += 1
        return count

    def get_nb_beach(self) -> int:
        return self.count_class("person")

    def get_nb_sea(self) -> int:
        return self.count_class("person_in_water")

    def get_visibility(self) -> int:
        for data in self.data_picture["predictions"]:
            if data["class"] == "sea":
                width_sea: int = int(data["width"])
                height_sea: int = int(data["height"])
                width_picture: int = int(self.data_picture["image"]["width"])
                height_picture: int = int(self.data_picture["image"]["height"])
                return int(width_sea * height_sea /
                           width_picture * height_picture)
        return -1

    def get_nb_boat(self) -> int:
        return self.count_class("boat")
