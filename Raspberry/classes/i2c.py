import smbus2


class I2CProtocol:
    def __init__(self, arduino_address):
        self.arduino_address = arduino_address
        self.offset = 0
        self.block_size = 16
        self.bus = smbus2.SMBus(1)

    # Função que recebe os dados do Arduino
    # A sequência dos dados recebidos são de extrema
    # importância para o funcionamento do sistema
    def read_block_data(self, variables):
        for i in range(len(variables)):
            if variables[i].get_name() == 'KCT_START':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_PUMP1_ALARM':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_PUMP1_FAULT':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_PUMP1_START':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_PUMP2_ALARM':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_PUMP2_FAULT':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_PUMP2_START':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_T_OIL_LEVEL':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.float_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_R_OIL_LEVEL':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.float_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_R_OIL_TEMPERATURE':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.float_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_SUPERHEATED_STEAM':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_HLEVEL':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_HTEMP':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_LLEVEL':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_LTEMP':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

        for i in range(len(variables)):
            if variables[i].get_name() == 'FBK_EMERGENCY':
                received_data = self.bus.read_i2c_block_data(self.arduino_address, self.offset, self.block_size)
                variables[i].set_value(self.int_value(received_data))
                break

    # Função que envia os dados para o Arduino
    # A inicialização do vetor a ser enviado e sua sequência são
    # de extrema importância para o funcionamento do sistema
    def write_block_data(self, variables):
        send_data = [0, 0, 0]

        for variable in variables:
            if variable.get_name() == 'KCT_MODE_PUMP1':
                send_data[0] = self.char_value(variable.get_last_value())
            if variable.get_name() == 'KCT_MODE_PUMP2':
                send_data[1] = self.char_value(variable.get_last_value())
            if variable.get_name() == 'KCT_START':
                send_data[2] = self.char_value(variable.get_last_value())

        self.bus.write_i2c_block_data(self.arduino_address, self.offset, send_data)

    def char_value(self, value):
        return ord(str(value))

    def int_value(self, array_data):
        string_data = ""
        for character in array_data:
            string_data += chr(character)
        return int(float(string_data.strip()))

    def float_value(self, array_data):
        string_data = ""
        for character in array_data:
            string_data += chr(character)
        return float(string_data.strip())