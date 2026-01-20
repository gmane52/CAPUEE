#include <Wire.h>


///////////////////////////////////////////////////////////////////////////telegram
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

// ====== WIFI ======
const char* ssid = "Errelece";
const char* password = "errelecee";

// ====== TELEGRAM ======
#define BOTtoken "8545831655:AAER0JN8CRoL4a_ExiqgggCkDaggMI3zaGg"  // Token del bot de Telegram
#define CHAT_ID "8555325793"       // ID del chat

// Relay (FireBeetle D2 = IO25)
const int relayPin = 25;

// Telegram client
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

unsigned long lastTimeBotRan = 0;
const unsigned long botDelay = 1000;


//////////////////////////////////////////////////////////////////////////fin telegram
#define ADS1115_ADDRESS 0x48

//=================================================================================================================================
// VARIABLE DECLARATIONS
//=================================================================================================================================

////Temp
const int sensorPin = A0;
const float vref = 3.3;
const float offset = 17.0; // ajustar luego
///fin temp

const int outputPin = 27;  // Control salida

// Define the pins of the Arduino ADC where the current sensor is measured
const int SensorPin = A1, RefPin = A2;

// Define the data from the current sensor
const int Rshunt = 33.3;                // Resistance of the transformer: Model 50 A: 20 ohms, Model 30 A: 33.3 ohms
double n_trafo = 1000;                  // Number of turns between primary and secondary

// Variables to calculate every millisecond
unsigned long time_now = 0;
unsigned long time_ant = 0, difTime = 0, act_time = 0, reading_time = 0, dif_reading_time = 0, timer1 = 0, timer2 = 0;
 
// Define variables to calculate the RMS of a power cycle
double quadratic_sum_v = 0.0;
double quadratic_sum_rms = 0.0;       // This variable accumulates the quadratic sum of instantaneous currents
const int sampleDuration = 20;          // Number of samples that determine how often the RMS is calcu-lated
int quadratic_sum_counter = 0;       // Counter of how many times values have been accumulated in the quadratic sum
double freq = 50.0;                     // Define the frequency of the power cycle

// Define variables to calculate an average of the current
double accumulated_current = 0.0;       // Accumulator of RMS values for averaging
const int sampleAverage = 250;          // Number of samples that determine how often the RMS average is calculated
int accumulated_counter = 0;             // Counter of how many times RMS values have been accumulated
bool first_run = true;
double v_calib_acum = 0;
double v_calib = 0;
int i = 0;
byte writeBuf[3];

//=================================================================================================================================
// Helper functions: Function created to partition the problem in smaller parts
//=================================================================================================================================
void config_i2c(){
  Wire.begin(); // begin I2C

  // ASD1115
  // set config register and start conversion
  // ANC1 and GND, 4.096v, 128s/

  writeBuf[0] = 1;    // config register is 1
  
  writeBuf[1] = 0b11010010; // 0xC2 single shot off <== ORIGINAL - single conversion/ AIN1 & GND/ 4.096V/ Continuous (0)
  
  // bit 15 flag bit for single shot
  // Bits 14-12 input selection:
  // 100 ANC0; 101 ANC1; 110 ANC2; 111 ANC3
  // Bits 11-9 Amp gain. Default to 010 here 001 P19
  // Bit 8 Operational mode of the ADS1115.
  // 0 : Continuous conversion mode
  // 1 : Power-down single-shot mode (default)

  writeBuf[2] = 0b11100101; // bits 7-0  0x85 //869 SPS 
  
  // Bits 7-5 data rate default to 100 for 128SPS
  // Bits 4-0  comparator functions see spec sheet.

  // setup ADS1115
  Wire.beginTransmission(ADS1115_ADDRESS);  // ADC 
  Wire.write(writeBuf[0]); 
  Wire.write(writeBuf[1]);
  Wire.write(writeBuf[2]);  
  Wire.endTransmission();  

  delay(500);
}

float read_voltage(){
  //unsigned long start = micros();
  // Read conversion register
  Wire.beginTransmission(ADS1115_ADDRESS);
  Wire.write(0x00); // Conversion register
  Wire.endTransmission();

  Wire.requestFrom(ADS1115_ADDRESS, 2);
  int16_t result = Wire.read() << 8 | Wire.read();  // Mount the 2 byte value
  Wire.endTransmission();
  
  //unsigned long end = micros();
  //Serial.print("ADC Read Time (us): ");
  //Serial.println(end - start);

  // Convert result to voltage
  float voltage = result * 4.096 / 32768.0;  // Raw adc * reference voltage configured / maximum adc value
  return voltage;  // Voltage in V
}

//=================================================================================================================================
// setup Function: Function that runs once on startup
//=================================================================================================================================
void setup() {

  //////////////////TEMP
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  //////////FIN TEM

  //////////////////////////////////////telegram
  //Serial.begin(115200);

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);  // Relay OFF (active LOW)

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  client.setInsecure();
  bot.sendMessage(CHAT_ID, "ESP32 connected", "");

  /////////////////////////////////////fin telegram
  pinMode(outputPin, OUTPUT); // GPIO 0 como salida
  digitalWrite(outputPin, LOW); // Estado inicial apagado
  // Initialize serial communications
  //serial.begin(115200);
  // Initialize IIC communications
  config_i2c();
}

//=================================================================================================================================
// loop Function: Function that runs cyclically indefinitely
//=================================================================================================================================


//////////////////telegram

void handleNewMessages(int numNewMessages) {
  for (int i = 0; i < numNewMessages; i++) {
    String chat_id = bot.messages[i].chat_id;
    String text = bot.messages[i].text;

    if (text == "/on") {
      digitalWrite(relayPin, HIGH);
      bot.sendMessage(chat_id, "Relay ON", "");
    }
    else if (text == "/off") {
      digitalWrite(relayPin, LOW);
      bot.sendMessage(chat_id, "Relay OFF", "");
    }
  }
}

/////////////////fin telegram 
void loop() {

  //////////////////////////////////////////////////////TEMPERATURA
  int adc = analogRead(sensorPin);
  float voltaje = adc * (vref / 4095.0);
  float temperatura = (voltaje * 100.0) + offset;





  ////////////////////////////////////////////////////FIN TEMPERATURA


  //////////////////Control Salid
    if (Serial.available() > 0) {
    char command = Serial.read();  // Lee 'H' o 'L'
    
    if (command == 'H') {
      digitalWrite(outputPin, HIGH);   // Activar salida digital 0
      Serial.println("GPIO 0 ON");
    }
    else if (command == 'L') {
      digitalWrite(outputPin, LOW);    // Desactivar salida digital 0
      Serial.println("GPIO 0 OFF");
    }
    }
  ///////////fin control salida
  // Read the time in microseconds since the Arduino started
  act_time= micros();
  // Calculate the time difference between the current time and the last time the instantaneous current was updated
  difTime=act_time-time_ant; 

  
   if (difTime>=1000) {

    // Update the time record with the current time
    time_ant=act_time;
    
    // Read the voltage from the sensor check the 1.65 measuring in the circuit with AO2
    double Vinst = read_voltage()- 1.65;
    //Serial.println(Vinst);
    //delay(500);
    // Convert voltage in shunt to current measurement
     double Iinst=Vinst*30; 

    // Accumulate cuadratic sum
    quadratic_sum_rms += Iinst*Iinst*difTime/1000000;
    quadratic_sum_counter++;
   } 

   // EVERY POWER CYCLE (20 ACCUMULATED VALUES), CALCULATE RMS
if (quadratic_sum_counter>=20) {

    // Take the square root to calculate the RMS of the last power cycle
    double Irms = sqrt(50*quadratic_sum_rms);
    // Reset accumulation values to calculate the RMS of the last power cycle
    quadratic_sum_counter=0;
    quadratic_sum_rms=0;
    // Filter base error
    if (Irms<=0.35){
      Irms = 0;
    }
    // Accumulate RMS current values to calculate the average RMS
    accumulated_current+=Irms;
    accumulated_counter++;
    
    //Serial.println(Irms);
  }

  // EVERY 250 POWER CYCLES (approximately 5 seconds), CALCULATE THE AVERAGE RMS
  if (accumulated_counter >=250) {

    // Calculate the average of the RMS current
    double Irms_flt =  accumulated_current/((double)accumulated_counter);
    // Reset accumulation values to calculate the average RMS
    accumulated_current=0;
    accumulated_counter=0;
    // Print the filtered current
    Serial.print("CurrentSensor:");
    Serial.println(Irms_flt);

    Serial.print("TempSensor: ");
    Serial.println(temperatura);
  }


  /////////////////////telegram
  if (millis() - lastTimeBotRan > botDelay) {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while (numNewMessages) {
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    lastTimeBotRan = millis();
  }


  /////////////////////Fin telegram

}

