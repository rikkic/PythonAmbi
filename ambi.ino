#include <Adafruit_NeoPixel.h>

// put your setup code here, to run once:
#define PIN 6
#define LEDS 30
 
// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(LEDS, PIN, NEO_GRB + NEO_KHZ800);

String inData;
int i = 0;
int offset = 0;

void setup() {
        Serial.begin(57600);     // opens serial port, sets data rate to 9600 bps
        Serial.print("Running!");
        strip.begin();
        strip.setBrightness(64);
        strip.show(); // Initialize all pixels to 'off'
}

void loop() {
    while (Serial.available() > 0)
    {
        inData = Serial.readStringUntil(';');
        //inData = "255000000255000000";
        offset = 0;
        for (i = 0; i < LEDS; i++){
          strip.setPixelColor(i, inData.substring(offset,offset+3).toInt(),inData.substring(offset+3,offset+6).toInt(),inData.substring(offset+6,offset+9).toInt());
          offset += 9;
        }
        strip.show();
    }
}
