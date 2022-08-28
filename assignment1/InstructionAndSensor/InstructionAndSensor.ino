const int ledPin = 11;
const int buzzerPin = 14;
const int soilPin = 16;


#include "DHT.h"
//#include <SoftwareSerial.h>


#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11


DHT dht(DHTPIN, DHTTYPE);

void setup() {


  Serial.begin(9600); 

  // Setup DHT Sensor
  pinMode(DHTPIN, INPUT);
  dht.begin();
  
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial1.begin(9600);
  digitalWrite(ledPin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:

  if(Serial1.available() > 0){
    String str = Serial1.readString().substring(0);
    Serial.println(str);
    if(str == "LED_ON"){
      digitalWrite(ledPin, HIGH);   
    }
    if(str == "LED_OFF"){
      digitalWrite(ledPin, LOW);
    }
    if(str == "BUZZ"){
      digitalWrite(buzzerPin, HIGH);
      delay(50);
      digitalWrite(buzzerPin, LOW);
      delay(50);
      digitalWrite(buzzerPin, HIGH);
      delay(50);
      digitalWrite(buzzerPin, LOW);
    }
  }
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  int moisture = analogRead(soilPin);
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);
  
  Serial1.print(h);
  Serial1.print(F(";"));
  Serial1.print(t);
  Serial1.print(F(";"));
  Serial1.print(hic);
  Serial1.print(F(";"));
  Serial1.print(moisture);
  Serial1.println(F(""));

  delay(2000);
}
