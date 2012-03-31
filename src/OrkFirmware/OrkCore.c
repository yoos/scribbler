
 #include "OrkCore.h"
 
 void initializeCore()
 {
	// Initialize Clock Setting for 16.000 MHz Operation
	cli();
	CPU_PRESCALE(CPU_16MHz);
	sei();
	
	//USART Initialization
	
	/* Set baud rate */
	UBRR1 = 25; //38.4k
	
	/* Enable receiver and transmitter */
	UCSR1B = (1<<RXEN1)|(1<<TXEN1);
	/* Set frame format: 8data, 2stop bit */
	UCSR1C = (1<<USBS1)|(3<<UCSZ10);
	
	//PWM Initialization (Timer1)
	TCCR1A = 0b10101010; //Non-Inverting Channel A,B,C
	TCCR1B = 0b00011010; //16-bit Fast PWM (Pre-Scalar=8)
	TCCR1C = 0b00000000; //For Non-Pwm modes
	
	//Set IO Data Direction for Motor Outputs
	DDRB |= (1<<5) | (1<<6) | (1<<7);
	
	ICR1=39999; //Counter Top Value (Freq:50Hz)

	// Set Outputs
	DDRB |= (1<<0); // LED output

 }
 
 void ledOff()
 {
	PORTB &= ~(1<<0);
 }
 
 void ledOn()
 {
	PORTB |= (1<<0);
 }

//USART Receive 
unsigned char USART_Receive( void )
	{
	//Wait for data to be received
	while ( !(UCSR1A & (1<<RXC1)) );
	//Get and return received data from buffer
	return UDR1;
	}

//USART Transmit
void USART_Transmit( unsigned char data )
	{
	//Wait for empty transmit buffer 
	while ( !( UCSR1A & (1<<UDRE1)) );
	
	// Put data into buffer, sends the data 
	UDR1 = data;
	}


//Set Servo Position
void setServo(unsigned char joint, unsigned long angle)
 {
	if(joint == Shoulder)
	{
		OCR1B = angle;
	} 
	else if(joint == Elbow)
	{
		OCR1A = angle;
	}
	else if(joint == EndEffector)
	{
		OCR1C = angle;
	}
 }