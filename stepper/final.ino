#include <Servo.h>
Servo myservo;

int x,y,z;
void setup() {
  Serial.begin(9600);
  pinMode(12,OUTPUT);//inp a1
  pinMode(13, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(4,OUTPUT);
  myservo.attach(3);
 //myservo.write(85);
  
}

void loop() 
{
  digitalWrite(4,HIGH);
  if (Serial.available()>0)
 {
    if (Serial.read()=='X')
    {
       x=Serial.parseInt();
       if (Serial.read()=='Y')
       {
          y=Serial.parseInt();
          if (Serial.read()=='Z')
          { z=Serial.parseInt();
          
          if(x<=220)
         {
           digitalWrite(13,HIGH);
           digitalWrite(12,LOW);
           digitalWrite(8,LOW);
           digitalWrite(7,LOW);
           delay(50);
         } 
         
         else if(x>=470) 
         {
           digitalWrite(8,HIGH);
           digitalWrite(7,LOW);
           digitalWrite(13,LOW);
           digitalWrite(12,LOW);
           delay(50);
           
         } 
         else if((x>=220) && (x<=470))
         {
           if((z>=106) && (z<=190))   // 38and50
           {
             digitalWrite(13,LOW);
             digitalWrite(12,LOW);
             digitalWrite(8,LOW);
             digitalWrite(7,LOW);
                     
             myservo.write(85);
             delay(2000);
             myservo.write(0);
             delay(2000);
           }
           else
           {
             digitalWrite(13,HIGH);
             digitalWrite(12,LOW);
             digitalWrite(8,HIGH);
             digitalWrite(7,LOW);
           }
         }
          }
          else
          {
            delay(10);
          }
         
       }
     }
    } 
  
  while (Serial.available()>0)
  {
    Serial.read();
   }
  
}
