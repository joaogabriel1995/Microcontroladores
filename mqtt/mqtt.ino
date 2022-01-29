#include <WiFi.h>
#include <PubSubClient.h>
#define RelePin 27



//Wifi 

const char* ssid = "***************";
const char* password = "*************";

//MQTT Broker
const char* mqtt_broker = "test.mosquitto.org";
const int mqtt_port = 1883;
WiFiClient wifiClient;


#define ID_MQTT  "ESP32_1705"
#define TOPIC_SUBSCRIBE  "luminaria"
PubSubClient MQTT(wifiClient);




//declaração das funções
void conectaWiFi();
void conectaMQTT();
void recebePacote(char* topic, byte* payload, unsigned int length);







void setup() {
  Serial.begin(115200);
  pinMode(RelePin, OUTPUT);
  conectaWiFi();
  MQTT.setServer(mqtt_broker, mqtt_port);
  MQTT.setCallback(recebePacote);
  conetaMQTT();
}

void loop() {
  MQTT.loop();

}


void conectaWiFi(){
  if (WiFi.status()== WL_CONNECTED){
    return;
    }
    Serial.print("Conectando-se na rede: ");
    Serial.print(ssid);
    Serial.println("Aguarde!");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED){
      delay(100);
      Serial.print(".");
      }
    Serial.println();
    Serial.println("Conectado com sucesso, na rede: "); 
    Serial.print(ssid); 
}

void recebePacote(char* topic, byte* payload, unsigned int length){
  
  String msg;


  for(int i=0; i < length; i++)
  {
    char c = (char)payload[i];
    msg+=c;
      
  }
  if (msg=="0"){
    digitalWrite(RelePin, LOW);
    Serial.println("Desligado");
    }
  if (msg=="1"){
    digitalWrite(RelePin, HIGH);
    Serial.println("Ligado");
    
    }
  
  
  
  
  }





void conetaMQTT(){
  while(!MQTT.connected()){
    Serial.print("Conectando ao Broker MQTT: ");
    Serial.print(mqtt_broker);
    if (MQTT.connect(ID_MQTT)){
      Serial.println("Conectando ao broker com sucesso!");
      MQTT.subscribe(TOPIC_SUBSCRIBE);
      }
    else{
      Serial.println("Não Foi possivel se conectar com o Broker.");
      Serial.println("Nova tentantiva de conexão em 10s");
      delay(10000);
      }
    }
  }