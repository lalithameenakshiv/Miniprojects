#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const char* ssid = "Hello";
const char* password = "12345678";

WebServer server(80);

// ---------- LCD ----------
LiquidCrystal_I2C lcd(0x27, 16, 2);   // If not working, try 0x3F

// ---------- PINS ----------
#define RELAY1 26
#define RELAY2 27
#define LED    2
#define IR_PIN 34

bool autoMode = true;

// ---------- LCD FUNCTION ----------
void showLCD(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

// ---------- LED FUNCTION ----------
void updateLED() {
  if (digitalRead(RELAY1) == LOW || digitalRead(RELAY2) == LOW)
    digitalWrite(LED, HIGH);
  else
    digitalWrite(LED, LOW);
}

// ---------- SETUP ----------
void setup() {
  Serial.begin(115200);

  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(IR_PIN, INPUT);

  digitalWrite(RELAY1, HIGH);
  digitalWrite(RELAY2, HIGH);
  digitalWrite(LED, LOW);

  // LCD
  Wire.begin(21, 22);   // SDA, SCL for ESP32
  lcd.begin();
  lcd.backlight();
  showLCD("Smart Home", "Connecting...");

  WiFi.begin(ssid, password);
  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  showLCD("WiFi Connected", WiFi.localIP().toString());

  server.on("/", handleRoot);
  server.on("/auto", setAuto);
  server.on("/manual", setManual);

  server.on("/r1on", relay1ON);
  server.on("/r1off", relay1OFF);
  server.on("/r2on", relay2ON);
  server.on("/r2off", relay2OFF);

  server.begin();
  delay(2000);

  if (autoMode) {
    showLCD("AUTO MODE", "Waiting...");
  } else {
    showLCD("MANUAL MODE", "All OFF");
  }
}

// ---------- LOOP ----------
void loop() {
  server.handleClient();

  if (autoMode) {
    int ir = digitalRead(IR_PIN);

    if (ir == LOW) {
      digitalWrite(RELAY1, LOW);
      digitalWrite(RELAY2, LOW);
      updateLED();

      Serial.println("Human Detected -> Bulbs ON");
      showLCD("DETECTED", "BULBS ON");
    } else {
      digitalWrite(RELAY1, HIGH);
      digitalWrite(RELAY2, HIGH);
      updateLED();

      Serial.println("No Human -> Bulbs OFF");
      showLCD("NOT DETECT", "BULBS OFF");
    }

    delay(300);
  }
}

// ---------- CONTROL ----------
void relay1ON() {
  if (!autoMode) {
    digitalWrite(RELAY1, LOW);
    updateLED();
    showLCD("MANUAL MODE", "BULB1 ON");
  }
  server.send(200, "text/html", webpage());
}

void relay1OFF() {
  if (!autoMode) {
    digitalWrite(RELAY1, HIGH);
    updateLED();

    if (digitalRead(RELAY2) == LOW)
      showLCD("MANUAL MODE", "BULB2 ON");
    else
      showLCD("MANUAL MODE", "ALL BULBS OFF");
  }
  server.send(200, "text/html", webpage());
}

void relay2ON() {
  if (!autoMode) {
    digitalWrite(RELAY2, LOW);
    updateLED();
    showLCD("MANUAL MODE", "BULB2 ON");
  }
  server.send(200, "text/html", webpage());
}

void relay2OFF() {
  if (!autoMode) {
    digitalWrite(RELAY2, HIGH);
    updateLED();

    if (digitalRead(RELAY1) == LOW)
      showLCD("MANUAL MODE", "BULB1 ON");
    else
      showLCD("MANUAL MODE", "ALL BULBS OFF");
  }
  server.send(200, "text/html", webpage());
}

void setAuto() {
  autoMode = true;
  showLCD("AUTO MODE", "Waiting...");
  server.send(200, "text/html", webpage());
}

void setManual() {
  autoMode = false;
  digitalWrite(RELAY1, HIGH);
  digitalWrite(RELAY2, HIGH);
  updateLED();
  showLCD("MANUAL MODE", "ALL BULBS OFF");
  server.send(200, "text/html", webpage());
}

void handleRoot() {
  server.send(200, "text/html", webpage());
}

// ---------- WEB UI ----------
String webpage() {
  String mode = autoMode ? "AUTO (IR)" : "MANUAL";

  return R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{
  margin:0;
  background:black;
  color:white;
  font-family:Arial;
  text-align:center;
}
.card{
  margin-top:50px;
}
button{
  width:100px;
  height:40px;
  margin:5px;
  border:none;
  border-radius:8px;
  font-size:15px;
}
.on{background:#2ecc71;}
.off{background:#e74c3c;color:white;}
.mode{background:#3498db;color:white;}
</style>
</head>

<body>
<div class="card">
<h2>Smart Home</h2>
<p>Mode: )rawliteral" + mode + R"rawliteral(</p>

<a href="/auto"><button class="mode">AUTO</button></a>
<a href="/manual"><button class="mode">MANUAL</button></a>

<h3>Bulb 1</h3>
<a href="/r1on"><button class="on">ON</button></a>
<a href="/r1off"><button class="off">OFF</button></a>

<h3>Bulb 2</h3>
<a href="/r2on"><button class="on">ON</button></a>
<a href="/r2off"><button class="off">OFF</button></a>
</div>
</body>
</html>
)rawliteral";
}
