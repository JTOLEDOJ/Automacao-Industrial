from classes.variable import Variable
import requests
import threading
import json


class SyncVariables:
    def __init__(self):
        self.array = []
        self.access = None
        self.url = 'https://script.google.com/macros/s/AKfycbzqN6sOoA3b_Pnr1alBxt_KImuLVFBifVsjEu-A-yUs53YrtIY/exec'

    def synchronize(self, variables):
        try:
            self.access = requests.get(url=self.url)
            self.array = json.loads(self.access.text)
        except Exception as error:
            print("O programa parou de funcionar. Erro:", error)
            exit()

        for element in self.array:
            variable = Variable(element['id'],
                                element['name'],
                                element['description'],
                                element['tag'],
                                element['type'],
                                element['eng_unit'],
                                element['l_limit'],
                                element['h_limit'],
                                element['ll_limit'],
                                element['hh_limit'],
                                element['last_value'])
            variables.append(variable)


class GetRequestPLC(threading.Thread):
    def __init__(self, variables):
        self.variables = variables
        self.array = []
        self.access = None
        self.url = 'https://script.google.com/macros/s/AKfycbzcxrLfynlT1MmC_kv8AoyX-6RA8Jb1eikHWPOygetUSbYUqA/exec'
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.access = requests.get(url=self.url)
            self.array = json.loads(self.access.text)
        except Exception as error:
            print("O programa parou de funcionar. Erro:", error)
            exit()

        for i in range(len(self.array)):
            element = self.array[i]

            if element['name'] == 'KCT_MODE_PUMP1':
                self.variables[i].set_value(element['last_value'])

            if element['name'] == 'KCT_MODE_PUMP2':
                self.variables[i].set_value(element['last_value'])

            if element['name'] == 'KCT_START':
                self.variables[i].set_value(element['last_value'])


class PostRequestPLC(threading.Thread):
    def __init__(self, username, password, variables):
        self.variables = variables
        self.access = None
        self.info = {'credenciais': [{'usuario': username, 'senha': password}]}
        self.url = 'https://script.google.com/macros/s/AKfycbzcxrLfynlT1MmC_kv8AoyX-6RA8Jb1eikHWPOygetUSbYUqA/exec'
        threading.Thread.__init__(self)

    def run(self):
        array = []
        for variable in self.variables:
            array.append({
                'id': variable.get_id(),
                'name': variable.get_name(),
                'last_value': variable.get_last_value()
            })
        self.info['valores'] = array
        info = {'dados': json.dumps(self.info)}

        try:
            self.access = requests.post(url=self.url, data=info)
            print(self.access.text)
        except Exception as erro:
            print("O programa parou de funcionar. Erro:", erro)
            exit()
