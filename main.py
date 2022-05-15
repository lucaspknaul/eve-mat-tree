from os import listdir
import datetime
import math


class Component:
    def __init__(self, name, quantity, time, subcomponents):
        self.name = name
        self.quantity = quantity
        self.time = time
        self.subcomponents = subcomponents

    def print(self):
        if self.subcomponents is not None:
            return "\n\nname: " + self.name + \
                   "\nquantity: " + str(self.quantity) + \
                   "\ntime: " + str(self.time) + \
                   "\nsubcomponents: " + ''.join(str(sc) for sc in self.subcomponents)
        else:
            return "\n\n\tname: " + self.name + \
                   "\n\tquantity: " + str(self.quantity)

    def __repr__(self):
        return self.print()

    def __str__(self):
        return self.print()


def parse_component(component_data):
    component_lines = component_data.split("\n")
    time_raw = component_lines[0].split("	")[1]
    time_parts = time_raw.split(":")
    time = datetime.timedelta(hours=int(time_parts[0]), minutes=int(time_parts[1]), seconds=int(time_parts[2]))
    quantity = int(''.join(component_lines[1].split(" ")[0].split(",")))
    name = ' '.join(component_lines[1].split(" ")[2:])
    subcomponents = []
    for subcomponent in component_lines[2:]:
        subcomponent_quantity = int(''.join(subcomponent.split(" ")[0].split(",")))
        subcomponent_name = ' '.join(subcomponent.split(" ")[2:])
        subcomponents.append(Component(subcomponent_name, subcomponent_quantity, None, None))
    return Component(name, quantity, time, subcomponents)


def decode_product(product_data):
    components = product_data.split("\n\n")
    component_list = []
    for component in components:
        component_list.append(parse_component(component))
    return component_list


def build_component_tree(tree_root, tree_data, cycles):
    tree_root.quantity *= cycles
    if tree_root.time is not None:
        tree_root.time = datetime.timedelta(
            seconds=tree_root.time.total_seconds() * cycles
        )
    for component_index, component in enumerate(tree_root.subcomponents):
        if component.name in [data.name for data in tree_data]:
            component_data = [c for c in tree_data if c.name == component.name][0]
            tree_root.subcomponents[component_index] = component_data
            tree_root.subcomponents[component_index] = build_component_tree(
                tree_root.subcomponents[component_index],
                tree_data,
                cycles * component.quantity / component_data.quantity
            )
        else:
            tree_root.subcomponents[component_index].quantity *= cycles
    return tree_root


def build_materials_list(product_tree):
    materials_list = []
    for component in product_tree.subcomponents:
        if component.subcomponents is None:
            materials_list.append(component)
        else:
            materials_list += build_materials_list(component)
    return materials_list


def calculate_total_time(product_tree):
    total_seconds = 0
    if product_tree.time is not None:
        total_seconds += product_tree.time.total_seconds()
    for component in product_tree.subcomponents:
        if component.time is not None:
            total_seconds += calculate_total_time(component).total_seconds()
    return datetime.timedelta(seconds=total_seconds)


def calculate_total_materials(materials_list):
    totals_dict = {}
    for material in materials_list:
        if material.name in totals_dict:
            totals_dict[material.name] += material.quantity
        else:
            totals_dict[material.name] = material.quantity
    return totals_dict


def encode_material_list(total_time, total_materials_list):
    encoded_list = "total time : " + str(total_time) + "\n"
    for material, quantity in total_materials_list.items():
        encoded_list += material + " " + str(int(math.ceil(quantity))) + "\n"
    return encoded_list


product_names = listdir("./products")
for product_name in product_names:
    #   read product file
    product_file = open("./products/" + product_name, "r")
    product = product_file.read()
    product_file.close()
    #   decode product file
    materials = decode_product(product)
    #   build tree
    component_tree = build_component_tree(materials[0], materials[1:], 1)
    #   analyze data
    materials_list = build_materials_list(component_tree)
    total_time = calculate_total_time(component_tree)
    total_material_dict = calculate_total_materials(materials_list)
    #   encode material list
    encoded_material_list = encode_material_list(total_time, total_material_dict)
    #   write materials file
    materials_file = open("./materials/" + product_name, "w")
    materials_file.write(encoded_material_list)
    materials_file.close()
