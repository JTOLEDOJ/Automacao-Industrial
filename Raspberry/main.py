# Bibliotecas
from classes.http import *
#from classes.i2c import I2CProtocol
import base64
import time

# Permissões de acesso
username = base64.b64encode(b'raspberry_001').decode('utf-8')
password = base64.b64encode(b'rasp123456').decode('utf-8')

# Instancia as variáveis
variables = []
synchronizing = SyncVariables()
synchronizing.synchronize(variables)

# Realiza as operações de controle
initial_time = time.time()
final_time = initial_time
time_interval = final_time - initial_time
refresh_rate = 2

# Endereço do arduino
arduino_address = 0x18

#receive_data = GetRequestPLC()
#save_data = PostRequestPLC(username, password)
#refresh_data = I2CProtocol(arduino_address)
cont = 0


while 1:
    final_time = time.time()
    time_interval = final_time - initial_time
    cont += 1

    if time_interval > refresh_rate:
        initial_time = final_time

        # REALIZA REQUISIÇÃO GET PARA PEGAR OS VALORES DE SETPOINT DO SERVIDOR
        receive_data = GetRequestPLC(variables)
        receive_data.start()
        receive_data.join()

        # ENVIA PRIMEIRO OS VALORES DE SETPOINT PARA O ARDUINO
        # DEPOIS RECEBE OS VALORES ATUALIZADOS DO ARDUINO
        #refresh_data.write_block_data(variables)
        #refresh_data.read_block_data(variables)

        # REALIZA REQUISIÇÃO POST PARA SALVAR OS VALORES DAS VARIÁVEIS NO SERVIDOR
        save_data = PostRequestPLC(username, password, variables)
        save_data.start()
        save_data.join()
