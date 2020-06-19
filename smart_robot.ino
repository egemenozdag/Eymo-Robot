
// Right Motor
int enR = 9;
int inRF = 8;
int inRB = 7;
 
// Left Motor
int enL = 3;
int inLF = 5;
int inLB = 4;

//encoder
int sagDec = 10;
int solDec = 11;


// Sensor
int echoPin = 13;
int trigPin = 12;

long duration = 0;
int distance = 0;

void setup() {
  Serial.begin(9600); // Starting Serial Terminal
  // Set all the motor control pins to outputs
  pinMode(enL, OUTPUT);
  pinMode(enR, OUTPUT);
  pinMode(inLF, OUTPUT);
  pinMode(inLB, OUTPUT);
  pinMode(inRF, OUTPUT);
  pinMode(inRB, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void moveForward(int rotNum) {    
  int readSag =0;
  int readSol = 0;
  int sens = 0;
  int j = 0;
    while(j < rotNum) {
      digitalWrite(inLF, HIGH);
      digitalWrite(inRF, HIGH);
      digitalWrite(inLB, LOW);
      digitalWrite(inRB, LOW);
      readSag = digitalRead(sagDec);
      readSol = digitalRead(solDec);
      sens = sensor();
      Serial.print("sensor okudu:   ");
      Serial.println(sens);//&& sens!=1
      if((readSag==1 || readSol==1) ){
        analogWrite(enL, 50);
        analogWrite(enR, 50);
        j++;
      }else if(sens==1){
        stopNow(500);
      }
    } 
}

void turnRight(int rotNum) {
  int readSag =0;
  int readSol = 0;
  int sagParam =0;
  int solParam =0;
  int sens = 0;

    int j = 0;
    while(j < rotNum) {
      digitalWrite(inLF, HIGH);
      digitalWrite(inLB, LOW);
      digitalWrite(inRF, LOW);
      digitalWrite(inRB, LOW);
      readSag = digitalRead(sagDec);
      readSol = digitalRead(solDec);
      sens = sensor();
      if(readSol==1 ){
        j++;
      }
      else {
        analogWrite(enL, 50);
        analogWrite(enR, 50);
      }
    }
}


void turnLeft(int rotNum) {
  int readSag =0;
  int readSol = 0;
  int sagParam =0;
  int solParam =0;
  int sens = 0;

    int j = 0;
    while(j < rotNum) {
      digitalWrite(inLF, LOW);
      digitalWrite(inLB, LOW);
      digitalWrite(inRF, HIGH);
      digitalWrite(inRB, LOW);
      readSag = digitalRead(sagDec);
      readSol = digitalRead(solDec);
      sens = sensor();
      if(readSag==1 ){
        j++;
      }
      else {
        analogWrite(enL, 50);
        analogWrite(enR, 50);
      }
    }
}

void stopNow(int ne) {
  digitalWrite(inLB, LOW);
  digitalWrite(inRB, LOW);
  digitalWrite(inLF, LOW);
  digitalWrite(inRF, LOW);
  delay(ne);
}

void demoOne() {
  delay(3000);
  moveForward(6);
  delay(750);
  stopNow(250);
  turnLeft(3); //ilk sag
  stopNow(250);
  moveForward(4);
  delay(750);
  stopNow(250);
  
}

void demoTwo() {
  delay(3000);
  moveForward(6);
  delay(750);
  stopNow(250);
  turnRight(3); //ilk sag
  stopNow(250);
  moveForward(4);
  delay(750);
  stopNow(250);
  
}

void demoThree() {
  delay(3000);
  moveForward(6);
  delay(750);
  stopNow(250);
  turnRight(3); //ilk sag
  stopNow(250);
  moveForward(4);
  delay(750);
  stopNow(250);
  
}


int sensor() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);
  if(distance <= 10){
    return 1;
  }else {
    return 0;
  }
  
}

long microsecondsToInches(long microseconds) {
   return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}

void loop() {
  demoOne();
  stopNow(25000);
}
