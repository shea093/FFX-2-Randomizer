from tabulate import tabulate

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Dressphere:
    def __init__(self, dress_name_def: str, dress_id_def: int):
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        self.__dress_name = dress_name_def
        self.__dress_id = dress_id_def
        self.__stat_variables = {}
        self.__ability_table = {}
        self.__hex_chunk = ""
        for stat_name in stat_names:
            self.__stat_variables[stat_name] = 0

    @property
    def stat_variables(self):
        return self.__stat_variables

    @stat_variables.setter
    def stats(self, value: dict):
        self.__stat_variables = value

    @property
    def hex_chunk(self):
        return self.__hex_chunk

    @hex_chunk.setter
    def hex_chunk(self, value: str):
        self.__hex_chunk = value

    @property
    def dress_name(self):
        return self.__dress_name

    def separate_stat_string(self, hex: str, hpmp=False):
        variables = {}
        if hpmp == True:
            variable_names = ["A","B","C"]
            count = 0
            for index, variable in enumerate(variable_names):
                count = count + 2
                variables[variable] = int(hex[count-2:count],16)
        else:
            variable_names = ["A","B","C","D","E"]
            count = 0
            for index, variable in enumerate(variable_names):
                count = count + 2
                variables[variable] = int(hex[count-2:count],16)
        return variables


    def stat_formula(self, type: str, tableprint=False):
        table = []
        temp_list = []
        raw_objects = []
        columns = 7
        count = 0
        stat_names = ["STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        for level in range(1, 100):
            if level == 99:
                table.append(temp_list)
            if type == "HP":
                variables = self.separate_stat_string(self.stat_variables[type],hpmp=True)
                part1 = (level * variables["A"])+variables["C"]
                part2 = (level**2) / (variables["B"]/10)
                formula_result = part1 - part2
                formula_result = "{:.2f}".format(formula_result)
                raw_objects.append(formula_result)
                formula_output = color.BOLD + color.CYAN + str(level) + color.END + ". " + str(formula_result)
                if count == columns:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
            if type == "MP":
                variables = self.separate_stat_string(self.stat_variables[type],hpmp=True)
                part1 = (level * (variables["A"]/10))+variables["C"]
                part2 = (level**2) / (variables["B"])
                formula_result = part1 - part2
                formula_result = "{:.2f}".format(formula_result)
                raw_objects.append(formula_result)
                formula_output = color.BOLD + color.CYAN + str(level) + color.END + ". " + str(formula_result)
                if count == columns:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
            if type in stat_names:
                variables = self.separate_stat_string(self.stat_variables[type])
                a_frac = variables["A"] / 10
                part1 = level * a_frac
                part2 = (level / variables["B"]) + variables["C"]
                part3 = level ** 2
                formula_result = part1 + part2 - part3 / 16 / variables["D"] / variables["E"]
                formula_result = "{:.2f}".format(formula_result)
                raw_objects.append(formula_result)
                formula_output = color.BOLD + color.CYAN + str(level)+ color.END + ". " + str(formula_result)
                if count == columns:
                    temp_list.append(formula_output)
                    table.append(temp_list)
                    count = 0
                    temp_list = []
                else:
                    count = count + 1
                    temp_list.append(formula_output)
        if tableprint == True:
            print("**************************")
            print(type)
            print("**************************")
            print(tabulate(table,tablefmt="fancy_grid"))
        else:
            return raw_objects


    def __repr__(self):
        return f'<Dressphere ID = {self.__dress_id}, Dressphere Name = {self.__dress_name}>'