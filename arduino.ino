#include <Arduino.h>
#include <IRremote.h>

const int IR_PIN = 9;
IRsend irsend;

char received;
String serialBuffer;

int index;
uint16_t command;
uint16_t COMMANDS[24] = {0x2, 0x3, 0x0, 0x1, 0x4, 0x8, 0xC, 0x10, 0x14, 0x5, 0x9, 0xD, 0x7, 0x11, 0x15, 0x6, 0xA, 0xE, 0x12, 0x16, 0xB, 0xF, 0x13, 0x17};



const int IR_RECEIVE_PIN = 2;


void setup() {
  Serial.begin(9600);

  irsend.begin(IR_PIN);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);

  Serial.println("IR by Flagrate");
}

void loop() {
  // read serial
  while (Serial.available() > 0) {
    received = Serial.read();
    serialBuffer += received;
    serialBuffer.trim();

    if (serialBuffer.indexOf(".") != -1) {
      serialBuffer.replace(".", "");
      index = serialBuffer.toInt();
      command = COMMANDS[index];
      serialBuffer = "";

      irsend.sendNEC(0xEF00, command, 0);

      Serial.print("Sent 0x");
      Serial.print(COMMANDS[index], HEX);
      Serial.print(" in response to ");
      Serial.println(index);
    }
  }

  if (IrReceiver.decode()) {
    Serial.println(IrReceiver.decodedIRData.command, HEX);
    IrReceiver.resume();
  }
}
