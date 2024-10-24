#include <ESP32Servo.h>
#include <esp_now.h>
#include <WiFi.h>

// Servo setup
static const int servoPin1 = 33; // Pin for the first servo
static const int servoPin2 = 27; // Pin for the second servo

Servo servo1;
Servo servo2;

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
    char a[32];
    int b;
    float c;
    bool d;
} struct_message;

// Create a struct_message called myData
struct_message myData;

// callback function that will be executed when data is received
void OnDataRecv(const esp_now_recv_info *info, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  
  Serial.print("Bytes received: ");
  Serial.println(len);

  // Perform action based on the value of myData.b
  //Servo 2 is MIRRORED because it's upside down!
  switch(myData.b) {
    case 1:
      servo1.write(90);  // Turn servo1 to 180 degrees
      Serial.println("Servo 1 to 180 degrees");
      break;
    case 2:
      servo1.write(180);  // Turn servo1 to 0 degrees
      Serial.println("Servo 1 to 0 degrees");
      break;
    case 3:
      servo2.write(180);  // Turn servo2 to 180 degrees
      Serial.println("Servo 2 to 180 degrees");
      break;
    case 4:
      servo2.write(90);  // Turn servo2 to 0 degrees
      Serial.println("Servo 2 to 0 degrees");
      break;
    case 5:
      servo1.write(90);  // Turn both servos to 180 degrees
      servo2.write(180);
      Serial.println("Both servos to 180 degrees");
      break;
    case 6:
      servo1.write(180);  // Turn both servos to 0 degrees
      servo2.write(90);
      Serial.println("Both servos to 0 degrees");
      break;
    default:
      Serial.println("Invalid command");
  }

  Serial.println("Action performed based on received data.");
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Attach the servos
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Register the receive callback function
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // Main loop code, no changes needed here since actions are triggered by received data
}
