#include "OrkCore.h"

int main(void)
{	
	initializeCore(); // Initializes core ORK Functionality
	/* Write other initialization code here (i.e. setting a pin data direction with a DDRx) */

	//USARTBuffer Vars
	unsigned short USARTBuffer1;
	unsigned short USARTBuffer2;
	unsigned short USARTBuffer3;
	unsigned short USARTBuffer4;
	unsigned short USARTBuffer5;
	unsigned short USARTBuffer6;
	unsigned short USARTBuffer7;

	//Servoposition Vars
	unsigned long ShoulderPosition;
	unsigned long ElbowPosition;
	unsigned long EndEffectorPosition;
	/*
	//Servo 32bit vars for math operation
	unsigned long ShoulderMath;
	unsigned long ElbowMath;
	unsigned long EndEffectorMath;
	*/
	while(1)
	{

	//USART Polling
	if(UCSR1A & (1<<RXC1))
	{
		USARTBuffer1=USART_Receive();
		if(USARTBuffer1==0xff)
		{
			ledOn();
			USARTBuffer2=USART_Receive();
			USARTBuffer3=USART_Receive();
			USARTBuffer4=USART_Receive();
			USARTBuffer5=USART_Receive();
			USARTBuffer6=USART_Receive();
			USARTBuffer7=USART_Receive();
			
			//14 bit Conversion 
			ShoulderPosition=(USARTBuffer3<<7)|(USARTBuffer2);
			ElbowPosition=(USARTBuffer5<<7)|(USARTBuffer4);
			EndEffectorPosition=(USARTBuffer7<<7)|(USARTBuffer6);
			
			
			//Mapping 14-bit input to 11-bit Resolution
			ShoulderPosition = (ShoulderPosition*4100) / 16384 + 1000;
			ElbowPosition = (ElbowPosition*3700) / 16384 + 500;
			EndEffectorPosition = (EndEffectorPosition*3700) / 16384 + 1000;
			
			//SetServos to Position
			setServo(Shoulder, ShoulderPosition);
			setServo(Elbow, ElbowPosition);
			setServo(EndEffector, EndEffectorPosition);
		}
		ledOff();
	}
	}
	return 0;
}
