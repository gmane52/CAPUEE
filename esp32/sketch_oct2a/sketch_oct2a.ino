// Este programa quiere usar el ADC con un sensor de temperatura.

#define T_SENSOR A0
double T = 0.0;
double V_sens = 0;
double T_offset = 11.7; // epirically calculated


void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(1000);
  
  Serial.print(" ADC:");
  Serial.print(analogRead(T_SENSOR));

  V_sens = (double)analogRead(T_SENSOR) * 3.3 / 4096.0;
  Serial.print(" V_Sens:");
  Serial.print(V_sens);
  Serial.print("V");
  
if (V_sens == 0)
{
  Serial.print(" TEMP ERROR.");
}
else
{
  T = V_sens / 0.01 + T_offset;
  Serial.print(" T:");
  Serial.print(T);
  Serial.print("ºC");
}
  Serial.println(" ");
  /modifico algo
}

