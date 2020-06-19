#include <ros.h>
#include <ros/time.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float64.h>
#include <Servo.h>
#include <sensor_msgs/LaserScan.h>
//#include <ESP8266WiFi.h> 

//Commands for ros
//roscore
//rosrun rosserial_python serial_node.py /dev/ttyUSB0
//rosrun teleop_twist_keyboard teleop_twist_keyboard.py
//rostopic echo chatter //ultrasonik sensor icin
//rostopic echo LaserData
//rostopic echo cmd_vel
//gedit ~/Arduino/libraries/ros_lib/ros/node_handle.h //mesaj hacimleri vs. onlara erişimi sağlıyor


// Ultrasonik Sensor
int echoPin = 11;//gri
int trigPin = 12;//mor

long duration;
float distance;

//Servo
int ServoPin = 13; //beyaz

//LaserSEnsor
int laserPin = 8;//mavi

//BT HC06
int tdx = 0;//sarı
int rdx = 1;//turuncu

//motorlar
int ENA = 7; //beyaz
int ENB = 2; //sarı

int IN1 = 6; //gri
int IN2 = 5; //mor
int IN3 = 4; //mavi
int IN4 = 3; //yesil

Servo servo;

ros::NodeHandle node;
geometry_msgs::Twist msg;
std_msgs::Float64 Distance;
ros::Publisher chatter("chatter", &Distance);
//sensor_msgs::LaserScan Laser_msg;
std_msgs::Float64 Laser_msg;
ros:: Publisher pub_Laser("LaserData", &Laser_msg);



void motion(int dist) {
  if (dist == 1) {adelante();}
  else if (dist == 2) {atras();}
  else if (dist == 3) {izquierda();}
  else if (dist == 4) {derecha();}
  else if (dist == 5) {parar();}
}

void adelante() { //duz
  analogWrite(ENA, 255);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENB, 255);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void izquierda() { //sol
  analogWrite(ENA, 255);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void parar() { //dur
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void derecha() { //sag
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENB, 255);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void atras() { //geri
  analogWrite(ENA, 255);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENB, 255);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void sensorMethod() {
  digitalWrite(trigPin, LOW);// Clears the trigPin
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);// Sets the trigPin on HIGH state for 10 micro seconds
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  distance = duration * 0.034 / 2;// Calculating the distance
  Distance.data = distance;//publishing data
  chatter.publish(&Distance);
  node.spinOnce();
  servo_cb();
}




void laserData() {
     int detected = digitalRead(laserPin);// read Laser sensor
     if(detected != LOW){Laser_msg.data = 1.0;}//obstacle
     else{Laser_msg.data = 0.0;}//No obstacle
     pub_Laser.publish(&Laser_msg);
     node.spinOnce();
}

void servo_cb() {
  servo.write(135);
  int pos = 0;
  for (pos = 0; pos < 270; pos += 1) {servo.write(pos);laserData();delay(8);}
  for (pos = 270; pos >= 1; pos -= 1) {servo.write(pos);laserData(); delay(8); }
}

void velCallBack(const geometry_msgs::Twist& cmd_vel) {
  if (cmd_vel.linear.x > 0 && cmd_vel.angular.z == 0 ) {adelante();}//i
  else if (cmd_vel.linear.x < 0 && cmd_vel.angular.z == 0 ) {atras();}//,
  else {
    if (cmd_vel.linear.x == 0 && cmd_vel.angular.z > 0) {izquierda();}//j
    else {
      if (cmd_vel.linear.x == 0 && cmd_vel.angular.z == 0) {parar();}//k
      else {
        if (cmd_vel.linear.x == 0 && cmd_vel.angular.z < 0) {derecha();}//l
        else {parar();}
      }
    }
  }
}

ros::Subscriber <geometry_msgs::Twist> sub("cmd_vel", velCallBack);

void setup(){
  Serial.begin(57600);

  node.initNode();
  node.subscribe(sub);
  node.advertise(chatter);
  node.advertise(pub_Laser);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode (laserPin, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  servo.attach(ServoPin);   
}


void loop() {
  sensorMethod();
  node.spinOnce();
  delay(1);
}