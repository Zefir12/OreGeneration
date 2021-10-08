import sys
from opensimplex import OpenSimplex
from typing import Dict, List
import random


class Group:
    def __init__(self, idd: int):
        self.id: int = idd
        self.fields: Dict[(int, int), Field] = {}


class Field:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.value = val
        self.type = 0
        self.group_id = 0


class MapContainer:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.map_dict: Dict[(int, int), Field] = {}
        self.ore_dict: Dict[(int, int), Field] = {}

    def create_field(self, x, y, val):
        self.map_dict[(x, y)] = Field(x, y, val)


class MapGen:
    def __init__(self, threshold, min_group_size, resolution, random_spawn_chance):
        self.opSx = OpenSimplex()
        self.op_seed = [random.random() * 1000, random.random() * 1000]
        self.opSx_resolution = resolution
        self.threshold = threshold
        self.min_group_size = min_group_size
        self.rnd_spawn_chance = random_spawn_chance
        self.ids_counter = 0
        self.ore_dict = {}
        self.groups: Dict[int, Group] = {}

    def gen_value(self, x, y):
        value = 0
        value += (self.opSx.noise2d((x + self.op_seed[0]) / self.opSx_resolution, (y + self.op_seed[1]) / self.opSx_resolution) / 2 + 0.5) * 0.6
        value += (self.opSx.noise2d((x + self.op_seed[0]) * 4 / self.opSx_resolution, (y + self.op_seed[1]) * 4 / self.opSx_resolution) / 2 + 0.5) * 0.4
        return value

    def create_map_first_pass(self, map_instance: MapContainer):
        for x in range(map_instance.size_x):
            for y in range(map_instance.size_y):
                value = self.gen_value(x, y)
                map_instance.create_field(x, y, value)
        return map_instance

    def second_pass(self, map_instance: MapContainer):
        for field in map_instance.map_dict.values():
            if field.value > self.threshold:
                field.type = 1
                map_instance.ore_dict[(field.x, field.y)] = field
                field.group_id = self.ids_counter
                self.ids_counter += 1
        return map_instance

    def third_pass(self, map_instance: MapContainer):
        # get random ore field
        # check id and create group with that id
        # remove from ore dict and check neighbours and add them to that group

        while map_instance.ore_dict.__len__() > 0:
            r_field: Field = list(map_instance.ore_dict.values())[0]
            map_instance.ore_dict.pop((r_field.x, r_field.y))
            group: Group = Group(r_field.group_id)
            group.fields[(r_field.x, r_field.y)] = r_field
            self.groups[group.id] = group

            self._check_group(r_field, map_instance, group)

        return map_instance

    def group_pass(self, map_instance: MapContainer):
        for group in self.groups.values():
            if group.fields.__len__() < self.min_group_size:
                for field_key in group.fields:
                    map_instance.map_dict[field_key].type = 0
        return map_instance

    def thickening_pass(self, map_instance: MapContainer):
        fields_to_spawn = []
        for field in map_instance.map_dict.values():
            if field.type == 1:
                if (field.x + 1, field.y) in map_instance.map_dict:
                    if random.random() < self.rnd_spawn_chance:
                        fields_to_spawn.append((field.x + 1, field.y))
                if (field.x - 1, field.y) in map_instance.map_dict:
                    if random.random() < self.rnd_spawn_chance:
                        fields_to_spawn.append((field.x - 1, field.y))
                if (field.x, field.y + 1) in map_instance.map_dict:
                    if random.random() < self.rnd_spawn_chance:
                        fields_to_spawn.append((field.x, field.y + 1))
                if (field.x, field.y - 1) in map_instance.map_dict:
                    if random.random() < self.rnd_spawn_chance:
                        fields_to_spawn.append((field.x, field.y - 1))

        for f_id in fields_to_spawn:
            map_instance.map_dict[f_id].type = 1
        return map_instance

    def _check_group(self, field, map_instance, group):
        if (field.x, field.y - 1) in map_instance.ore_dict:
            n_field: Field = map_instance.ore_dict.pop((field.x, field.y - 1))
            group.fields[(field.x, field.y - 1)] = n_field
            n_field.group_id = group.id
            self._check_group(n_field, map_instance, group)
        if (field.x, field.y + 1) in map_instance.ore_dict:
            s_field: Field = map_instance.ore_dict.pop((field.x, field.y + 1))
            group.fields[(field.x, field.y + 1)] = s_field
            s_field.group_id = group.id
            self._check_group(s_field, map_instance, group)
        if (field.x + 1, field.y) in map_instance.ore_dict:
            e_field: Field = map_instance.ore_dict.pop((field.x + 1, field.y))
            group.fields[(field.x + 1, field.y)] = e_field
            e_field.group_id = group.id
            self._check_group(e_field, map_instance, group)
        if (field.x - 1, field.y) in map_instance.ore_dict:
            w_field: Field = map_instance.ore_dict.pop((field.x - 1, field.y))
            group.fields[(field.x - 1, field.y)] = w_field
            w_field.group_id = group.id
            self._check_group(w_field, map_instance, group)