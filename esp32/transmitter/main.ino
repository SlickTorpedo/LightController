#include <esp_now.h>
#include <WiFi.h>

// REPLACE WITH YOUR RECEIVER MAC Address or use broadcast
uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// Structure to send data
typedef struct struct_message {
  char a[32];  // This field can be modified to hold string data
  int b;       // This will store the command (1 or 2)
  float c;     // Additional data (unused for now)
  bool d;      // Additional data (unused for now)
} struct_message;

// Create a struct_message instance
struct_message myData;

esp_now_peer_info_t peerInfo;

// Callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Register for Send callback to get the status of transmitted packet
  esp_now_register_send_cb(OnDataSent);

  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  // Add peer
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() {
  // Check if there's serial input (from Python or other source)
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();  // Read the incoming byte

    int value = receivedChar - '0';
    myData.b = value;

    // // Set myData.b based on the input
    // if (receivedChar == '1') {
    //   myData.b = 1;
    // } else if (receivedChar == '2') {
    //   myData.b = 2;
    // } else {
    //   Serial.println("Invalid input, please enter 1 or 2");
    //   return;
    // }

    // Send the message via ESP-NOW
    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));

    if (result == ESP_OK) {
      Serial.println("Sent with success");
    } else {
      Serial.println("Error sending the data");
    }
  }
}
