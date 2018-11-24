#include <Wire.h>
#include <Ultrasonic.h>
#define pino_start_p1 40
#define pino_start_p2 41
#define pino_trigger 44
#define pino_echo 45
#define pino_potentiometer A5
#define pino_button A7
#define pino_buzzer A9
#define arduino_address 0x18

// Inicialização dos pinos
Ultrasonic ultrasonic(pino_trigger, pino_echo);

// Parâmetros do sistema
const int BLOCK_SIZE = 16;
const int DECIMAL = 4;
char block_data[BLOCK_SIZE];
String received_data;
int item_sequence = 1;

// Variáveis de controle recebidas
int KCT_MODE_PUMP1;
int KCT_MODE_PUMP2;
bool KCT_START;

// Variáveis de controle enviadas
bool FBK_PUMP1_ALARM;
bool FBK_PUMP1_FAULT;
bool FBK_PUMP1_START;
bool FBK_PUMP2_ALARM;
bool FBK_PUMP2_FAULT;
bool FBK_PUMP2_START;
float FBK_T_OIL_LEVEL;
float FBK_R_OIL_LEVEL;
float FBK_R_OIL_TEMPERATURE;
bool FBK_SUPERHEATED_STEAM;
bool FBK_HLEVEL;
bool FBK_HTEMP;
bool FBK_LLEVEL;
bool FBK_LTEMP;
bool FBK_EMERGENCY;

// Variáveis de controle internas
bool LOS_EMERGENCY;
bool POS_EMERGENCY;
bool FBK_OK_SYSTEM;
bool KYV_PUMP1_START;
bool KYV_PUMP2_START;
float SNS_R_OIL_LEVEL;
int SNS_R_OIL_TEMPERATURE;

// Função para receber dados do Raspberry
// A ordem que as informações chegam aqui é
// importante para o correto funcionamento do sistema
void receive_data(int byte_count) {
  received_data = "";
  Wire.read();
  while(Wire.available()) {
    received_data += (char)Wire.read();
  }
  
  KCT_MODE_PUMP1 = String(received_data[0]).toInt();
  KCT_MODE_PUMP2 = String(received_data[1]).toInt();
  KCT_START = String(received_data[2]).toInt();

  //Serial.println(KCT_MODE_PUMP1);
  //Serial.println(KCT_MODE_PUMP2);
  //Serial.println(KCT_START);
}

// Função para enviar dados para o Raspberry
// A ordem que as informações saem daqui é
// importante para o correto funcionamento do sistema
void send_data() {
  if(item_sequence == 1) {
    dtostrf(KCT_START, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 2) {
    dtostrf(FBK_PUMP1_ALARM, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 3) {
    dtostrf(FBK_PUMP1_FAULT, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 4) {
    dtostrf(FBK_PUMP1_START, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 5) {
    dtostrf(FBK_PUMP2_ALARM, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 6) {
    dtostrf(FBK_PUMP2_FAULT, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 7) {
    dtostrf(FBK_PUMP2_START, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 8) {
    dtostrf(FBK_T_OIL_LEVEL, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 9) {
    dtostrf(FBK_R_OIL_LEVEL, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 10) {
    dtostrf(FBK_R_OIL_TEMPERATURE, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 11) {
    dtostrf(FBK_SUPERHEATED_STEAM, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 12) {
    dtostrf(FBK_HLEVEL, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 13) {
    dtostrf(FBK_HTEMP, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 14) {
    dtostrf(FBK_LLEVEL, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 15) {
    dtostrf(FBK_LTEMP, BLOCK_SIZE, DECIMAL, block_data);
  } else if(item_sequence == 16) {
    dtostrf(FBK_EMERGENCY, BLOCK_SIZE, DECIMAL, block_data);
  }

  item_sequence++;
  Wire.write(block_data);
}

float sensor_ultrassonico() {
  long microsec = ultrasonic.timing();
  float distance_mm = 10 * ultrasonic.convert(microsec, Ultrasonic::CM);
  
  return distance_mm;
}

bool botao_emergencia() {
  int value = analogRead(pino_button);
  Serial.println(value);
  if (value < 1000) {
    return false;
  } else {
    return true;
  }
}

void buzzer_emergencia() {
  if (LOS_EMERGENCY == true) {
    digitalWrite(pino_buzzer, HIGH);
  } else {
    digitalWrite(pino_buzzer, LOW);
  }
}

void start_bomba1() {
  if (KYV_PUMP1_START == true) {
  digitalWrite(pino_start_p1, HIGH);
  } else {
    digitalWrite(pino_start_p1, LOW);
  }
}

void start_bomba2() {
  if (KYV_PUMP2_START == true) {
  digitalWrite(pino_start_p2, HIGH);
  } else {
    digitalWrite(pino_start_p2, LOW);
  }
}

void torre() {
  // Torre - linhas 0 e 1
  FBK_T_OIL_LEVEL = ((1600.0 - FBK_R_OIL_TEMPERATURE)*(1600.0*4000.0))/(3000.0*3000.0);
  if(FBK_T_OIL_LEVEL <= 230.0 && FBK_PUMP2_START == true) {
    FBK_PUMP2_ALARM = true;
  } else {
    FBK_PUMP2_ALARM = false;
  }
}

void reservatorio() {
  // Reservatorio - linha 0
  SNS_R_OIL_TEMPERATURE = analogRead(pino_potentiometer);
  FBK_R_OIL_TEMPERATURE = (20.0*SNS_R_OIL_TEMPERATURE + 81240.0)/1023.0;

  // Reservatorio - linha 1
  SNS_R_OIL_LEVEL = sensor_ultrassonico();
  FBK_R_OIL_LEVEL = 2400.0 - 8.0*SNS_R_OIL_LEVEL;

  // Reservatorio - linhas 2, 3 e 4
  // Controle de alarmes de temperatura do reservatorio
  if(FBK_R_OIL_TEMPERATURE > 95.0) {
    FBK_HTEMP = true;
    FBK_LTEMP = false;
    FBK_SUPERHEATED_STEAM = false;
  } else if(FBK_R_OIL_TEMPERATURE <= 85.0) {
    FBK_HTEMP = false;
    FBK_LTEMP = true;
    FBK_SUPERHEATED_STEAM = true;
  } else {
    FBK_HTEMP = false;
    FBK_LTEMP = false;
    FBK_SUPERHEATED_STEAM = true;
  }

  // Reservatorio - linha 5, 6 e 7
  // Controle de alarmes de nivel do reservatorio
  if(FBK_R_OIL_LEVEL < 250.0) {
    FBK_LLEVEL = true;
    if(FBK_PUMP1_START == true) {
      FBK_PUMP1_ALARM = true;
    }
    FBK_HLEVEL = false;
  } else if(FBK_R_OIL_LEVEL > 1350.0) {
    FBK_LLEVEL = false;
    FBK_PUMP1_ALARM = false;
    FBK_HLEVEL = true;
  } else {
    FBK_LLEVEL = false;
    FBK_PUMP1_ALARM = false;
    FBK_HLEVEL = false;
  }
}

void acionamento() {
  // Bomba 1 - Acionamento
  // Acionamento - linhas 0 e 1
  if((KCT_MODE_PUMP1 == 0.0 && (FBK_R_OIL_TEMPERATURE > 85.0 && FBK_R_OIL_TEMPERATURE < 95.0)) || KCT_MODE_PUMP1 == 1.0) {
    if(FBK_PUMP1_FAULT == false && FBK_OK_SYSTEM == true) {
      FBK_PUMP1_START = true;
    } else {
      FBK_PUMP1_START = false;
    }
  } else if(KCT_MODE_PUMP1 == 2.0) {
    FBK_PUMP1_START = false;
  }

  // Acionamento - linha 2
  if(FBK_OK_SYSTEM == true && FBK_R_OIL_LEVEL < 150.0) {
    FBK_PUMP1_FAULT = true;
  } else {
    FBK_PUMP1_FAULT = false;
  }

  // Acionamento - linha 3
  if(FBK_PUMP1_FAULT == true) {
    FBK_PUMP1_START = false;
  }

  // Acionamento - linha 4
  if(FBK_PUMP1_START == true) {
    KYV_PUMP1_START = true;
  } else {
    KYV_PUMP1_START = false;
  }
  start_bomba1();

  // Bomba 2 - Acionamento
  // Acionamento - linhas 5 e 6
  if(KCT_MODE_PUMP2 == 0.0) {
    if(FBK_PUMP2_FAULT == false && FBK_OK_SYSTEM == true) {
      FBK_PUMP2_START = true;
    } else {
      FBK_PUMP2_START = false;
    }
  } else if(KCT_MODE_PUMP2 == 1.0) {
    FBK_PUMP2_START = false;
  }

  // Acionamento - linha 7
  if(FBK_OK_SYSTEM == true && FBK_T_OIL_LEVEL < 100.0) {
    FBK_PUMP2_FAULT = true;
  } else {
    FBK_PUMP2_FAULT = false;
  }

  // Acionamento - linha 8
  if(FBK_PUMP2_FAULT == true) {
    FBK_PUMP2_START = false;
  }

  // Acionamento - linha 9
  if(FBK_PUMP2_START == true) {
    KYV_PUMP2_START = true;
  } else {
    KYV_PUMP2_START = false;
  }
  start_bomba2();
}

void main_routine() {
  POS_EMERGENCY = botao_emergencia();
  // MainRoutine - linha 0
  if(KCT_START == true && POS_EMERGENCY == false) {
    FBK_OK_SYSTEM = true;
    KCT_START = true;
  } else {
    FBK_OK_SYSTEM = false;
    KCT_START = false;
  }

  // MainRoutine - linha 1
  if(POS_EMERGENCY == true) {
    FBK_EMERGENCY = true;
    LOS_EMERGENCY = true;
    FBK_PUMP1_START = false;
    FBK_PUMP2_START = false;
  } else {
    FBK_EMERGENCY = false;
    LOS_EMERGENCY = false;
  }
  buzzer_emergencia();
}

void setup()
{
  Serial.begin(9600);
  pinMode(pino_potentiometer, INPUT);
  pinMode(pino_button, INPUT);
  pinMode(pino_buzzer, OUTPUT);
  pinMode(pino_start_p1, OUTPUT);
  pinMode(pino_start_p2, OUTPUT);
  Wire.begin(arduino_address);
  Wire.onReceive(receive_data);
  Wire.onRequest(send_data);
}

void loop()
{
  reservatorio();
  torre();
  main_routine();
  acionamento();
  
  delay(50);
}
