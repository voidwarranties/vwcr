int Aa = 2;
int Ba = 5;
int Ca = 4;
int Da = 3;
int Ab = 6;
int Bb = 7;
int Cb = 8;
int Db = 9;
int Ac = 10;
int Bc = 11;
int Cc = 12;
int Dc = 13;
int Ad = 14;
int Bd = 15;
int Cd = 16;
int Dd = 17;
int cash = 18;
int draw_state = 19;
boolean Show_options = false;
byte Byte;
boolean Display_mode = false; // False = price True = Time
boolean Time_Set = false; //Making shure that the device knows that the clock is not set
int nummers[4];
boolean nummers_insert = false;
boolean setting_time = false;
boolean time_show = true;
boolean cashstate = false; // false = closed
int timearray[6];
int seconds;
int minutes;
int hours;

void setup()
{
pinMode(Aa,OUTPUT);
pinMode(Ba,OUTPUT);
pinMode(Ca,OUTPUT);
pinMode(Da,OUTPUT);
pinMode(Ab,OUTPUT);
pinMode(Bb,OUTPUT);
pinMode(Cb,OUTPUT);
pinMode(Db,OUTPUT);
pinMode(Dc,OUTPUT);
pinMode(Ac,OUTPUT);
pinMode(Bc,OUTPUT);
pinMode(Cc,OUTPUT);
pinMode(Dc,OUTPUT);
pinMode(Ad,OUTPUT);
pinMode(Bd,OUTPUT);
pinMode(Cd,OUTPUT);
pinMode(Dd,OUTPUT);
pinMode(cash,OUTPUT);
pinMode(draw_state,INPUT);
 test();
  Serial.begin(9600);
  cli();//stop interrupts
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 15624;// = (16*10^6) / (1*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei();//allow interrupts
}

ISR(TIMER1_COMPA_vect){

seconds ++;
if(seconds >= 59){seconds =0; minutes ++;} 
if(minutes >= 59){minutes = 0; hours ++;} 
if(hours >= 24){hours = 0;}


}
void test(){
for (int b =0; b < 5;b++){
for (int a =0; a < 11;a++){
   convert(a,b);delay(130);}
 } convert(0,1);delay(50);convert(0,2);delay(50);convert(0,3);delay(50);convert(0,4);}
   
void Check_state(){if (analogRead(draw_state) <1023){ cashstate = false;} else {cashstate = true;}}

void Show_time(){Serial.println(String(hours) + ":" + String(minutes) + ":" + String(seconds));}


void loop() 
{
 recive();
 show();
 Check_state();
 
 
}
 int convertbyte(byte Byte){int getal; switch(Byte){ case 48: getal = 0; break; case 49: getal = 1; break; case 50: getal = 2; break; case 51: getal = 3; break; case 52: getal = 4; break; 
                                                      case 53: getal = 5; break; case 54: getal = 6; break; case 55: getal = 7; break; case 56: getal = 8; break; case 57: getal = 9; break; 
                                                      default: getal = 10; 
                                                    }

return getal;
}


void show()
{

 if (Display_mode == true)
  {
  
   convert(hours/10,4);convert(hours%10,3);convert(minutes/10,2);convert(minutes%10,1); 
  }
 else{convert(nummers[3],1);convert(nummers[2],2);convert(nummers[1],3);convert(nummers[0],4);} 
}


  
void recive()
{  
  if (Serial.available() == 1) // cheking if a byte is recieved and processing the recieved data
  {
    Byte = Serial.read();
    if (Byte == 84)
         {
           Display_mode = true;  Show_options = true; Serial.println("Display set to time mode"); // react to Capital T
            Time_Set == true;
             {
              Serial.println("Set time in the hh:mm:ss format");
              
              int t = 0; //counter to exit the loop in time
              
             do
              { if (t >6){setting_time = false;} else {setting_time = true;}
                if (Serial.available() == 1){
                
                Byte = Serial.read();
                timearray [t] = convertbyte(Byte);
                if (t<6){Serial.print(convertbyte(Byte));}
                
                t++;
                }

              } while (setting_time == true);  Serial.println(""); Serial.print(timearray[0]); Serial.print(timearray[1]); Serial.print(timearray[2]); Serial.print(timearray[3]); Serial.print(timearray[4]); Serial.print(timearray[5]);
              
                if (timearray[0] == 0){hours = timearray[1];}else {hours = timearray[0]*10+timearray[1];}
                if (timearray[2] == 0){minutes = timearray[3];}else {minutes = timearray[2]*10+timearray[3];} 
                if (timearray[4] == 0){seconds = timearray[5];}else {seconds = timearray[4]*10+timearray[5];}
                
                Serial.println(""); Serial.print(hours); Serial.print(minutes); Serial.print(seconds);
                Time_Set =false;
             
                   
           }
         }
        if (Byte == 80)
         { Display_mode = false;  Serial.println("Display set to price mode");  // react to capital P aka price mode 
           nummers_insert = true;
           Serial.println("Insert Your numbers");
           int t = 0; //counter to exit the loop in time
           do
           { if (t > 3){ boolean nummers_insert = false;} else {boolean nummers_insert = true;}
             if (Serial.available() == 1)
            {  
              Byte = Serial.read();
              nummers [t] = convertbyte(Byte);
              if (t<4){Serial.print(convertbyte(Byte));}
              t++;
             
            }
                  
           }while( nummers_insert == true); Serial.println(""); Serial.print(nummers[0]); Serial.print (nummers[1]); Serial.print(nummers[2]); Serial.print(nummers[3]);
        }
       if (Byte == 116){time_show =true; Show_time(); time_show =false;} // react to t
       if (Byte == 79){digitalWrite(cash,255);delay(250);digitalWrite(cash,0);}//react to O aka open cashdrawer 
       if (Byte == 83){Serial.println(cashstate);}
       if (Byte == 63){Serial.println("T = display and set time");Serial.println("P = display and set Price");Serial.println("S = display drawer state");Serial.println("t = show internal time (terminal only");Serial.println("O = open the darwer");}           
  }
}
 void convert(int nummer,int digit){ //method for converting decimal numbers to thear coresponding bcd numbers and printing them

int A = 0;
int B = 0;
int C = 0;
int D = 0; //local variables for temp storing the nibbles

reset(digit,1);

switch (nummer){  //the conversion statement
  
 case 1: 
  A = 1;
 break;
  
 case 2: 
   B = 1; 
 break;
  
 case 3: 
  A = 1;
  B = 1;
 break;
  
 case 4: 
  C = 1;
 break;
  
 case 5:
  A = 1;
  C = 1;
 break;
  
 case 6:
  B = 1;
  C = 1;
 break;
  
 case 7:
  A = 1;
  B = 1;
  C = 1;
 break;
  
 case 8:
  D = 1;
 break;
  
 case 9:
  A = 1;
  D = 1;
 break;
  
 case 10:
  A = 1;
  B = 1;
  C = 1;
  D = 1;
  break;
  }

switch (digit){ // the printing

 case 1:
  digitalWrite(Aa,A);
  digitalWrite(Ba,B);
  digitalWrite(Ca,C);
  digitalWrite(Da,D);
 break;
 
 case 2:
  digitalWrite(Ab,A);
  digitalWrite(Bb,B);
  digitalWrite(Cb,C);
  digitalWrite(Db,D);
 break;
 
 case 3:
  digitalWrite(Ac,A);
  digitalWrite(Bc,B);
  digitalWrite(Cc,C);
  digitalWrite(Dc,D);
 break;
 
 case 4:
  digitalWrite(Ad,A);
  digitalWrite(Bd,B);
  digitalWrite(Cd,C);
  digitalWrite(Dd,D);
 break;
}}

void reset(int digit,boolean state) {

switch (digit){
  
case 1:

  digitalWrite(Aa,state);
  digitalWrite(Ba,state);
  digitalWrite(Ca,state);
  digitalWrite(Da,state);
  break;

case 2 :

  digitalWrite(Ab,state);
  digitalWrite(Bb,state);
  digitalWrite(Cb,state);
  digitalWrite(Db,state);
  break;

case 3 :

  digitalWrite(Ac,state);
  digitalWrite(Bc,state);
  digitalWrite(Cc,state);
  digitalWrite(Dc,state);
  break;

case 4 :

  digitalWrite(Ad,state);
  digitalWrite(Bd,state);
  digitalWrite(Cd,state);
  digitalWrite(Dd,state);
  break;

default:

  digitalWrite(Aa,state);
  digitalWrite(Ba,state);
  digitalWrite(Ca,state);
  digitalWrite(Da,state);
  digitalWrite(Ab,state);
  digitalWrite(Bb,state);
  digitalWrite(Cb,state);
  digitalWrite(Db,state);
  digitalWrite(Ac,state);
  digitalWrite(Bc,state);
  digitalWrite(Cc,state);
  digitalWrite(Dc,state);
  digitalWrite(Ad,state);
  digitalWrite(Bd,state);
  digitalWrite(Cd,state);
  digitalWrite(Dd,state);
break;
}}


 
    


 
 
