float temp = 27.0;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0));
}

void loop() {
temp += random(-400, 401) / 100.0; // saltos más grandes
  float current = random(50, 800) / 100.0;  // 0.50..8.00

  Serial.print("TempSensor:");
  Serial.println(temp, 2);
  Serial.print("CurrentSensor:");
  Serial.println(current, 2);

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.length()) {
      Serial.print("CMD:");
      Serial.println(cmd);
    }
  }

  delay(1000);
}


