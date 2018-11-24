class Variable:
    def __init__(self, id, name, description, tag, type, eng_unit, l_limit, h_limit, ll_limit, hh_limit, last_value):
        self.id = id
        self.name = name
        self.description = description
        self.tag = tag
        self.type = type
        self.eng_unit = eng_unit
        self.l_limit = l_limit
        self.h_limit = h_limit
        self.ll_limit = ll_limit
        self.hh_limit = hh_limit
        self.last_value = last_value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_tag(self):
        return self.tag

    def get_type(self):
        return self.type

    def get_eng_unit(self):
        return self.eng_unit

    def get_l_limit(self):
        return self.l_limit

    def get_h_limit(self):
        return self.h_limit

    def get_ll_limit(self):
        return self.ll_limit

    def get_hh_limit(self):
        return self.hh_limit

    def get_last_value(self):
        return self.last_value

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_tag(self, tag):
        self.tag = tag

    def set_type(self, type):
        self.type = type

    def set_eng_unit(self, eng_unit):
        self.eng_unit = eng_unit

    def set_l_limit(self, l_limit):
        self.l_limit = l_limit

    def set_h_limit(self, h_limit):
        self.h_limit = h_limit

    def set_ll_limit(self, ll_limit):
        self.ll_limit = ll_limit

    def set_hh_limit(self, hh_limit):
        self.hh_limit = hh_limit

    def set_value(self, value):
        self.last_value = value

    def print_variable_info(self):
        print('ID:', self.get_id())
        print('NAME:', self.get_name())
        print('DESCRIPTION:', self.get_description())
        print('TAG:', self.get_tag())
        print('TYPE:', self.get_type())
        print('ENG. UNIT:', self.get_eng_unit())
        print('LOW LIMIT:', self.get_l_limit())
        print('HIGH LIMIT:', self.get_h_limit())
        print('LOW LOW LIMIT:', self.get_ll_limit())
        print('HIGH HIGH LIMIT:', self.get_hh_limit())
        print('LAST VALUE:', self.get_last_value())
