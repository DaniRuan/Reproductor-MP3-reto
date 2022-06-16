#include <Arduino_FreeRTOS.h>
//uso de semáforos y la interrupción externa
#include "semphr.h"

//macros para la configuración y manejo de pines
#define MakeInputPin(REG, PIN)       (REG &= (~(1 << PIN)))
#define MakeOutputPin(REG, PIN)      (REG |= (1 << PIN))
#define EnablePullUp(REG, PIN)       (REG |= (1 << PIN))
#define ReadInputPin(REG, PIN)       (REG & (1 << PIN))
#define WriteOutputPinLow(REG, PIN)  (REG &= ~(1 << PIN))
#define WriteOutputPinHigh(REG, PIN) (REG |= (1 << PIN))
#define ToggleOutputPin(REG, PIN)    (REG ^= (1 << PIN))

//declaraciones de la tasa de comunicación serial
#define F_CPU 16000000UL
#define USART_BAUDRATE 19200
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

//semaphore handle
SemaphoreHandle_t interruptSemaphore1;

//semaphore handle
SemaphoreHandle_t interruptSemaphore2;

//semaphore handle
SemaphoreHandle_t interruptSemaphore3;

//semaphore handle
SemaphoreHandle_t interruptSemaphore4;

//int num_fila=0;
//int *ptrnum_fila= &num_fila;

uint8_t num_fila = 0;
char tecla; 

//retardo en ms
const unsigned int period = 24;

//buffer para el UART
unsigned char mybuffer[25];

void setup()
{
  //creación de tareas
  xTaskCreate(vTaskSendzeros,"Send zeros task",100,NULL,1,NULL);
  xTaskCreate(vHandler_line1,"Handler columna 1",100,NULL,1,NULL);
  xTaskCreate(vHandler_line2,"Handler columna 2",100,NULL,1,NULL);
  xTaskCreate(vHandler_line3,"Handler columna 3",100,NULL,1,NULL);
  xTaskCreate(vHandler_line4,"Handler columna 4",100,NULL,1,NULL);
  
  //configuración del puerto serial
  UBRR0H = (uint8_t)(UBRR_VALUE >> 8);
  UBRR0L = (uint8_t)UBRR_VALUE;
  UCSR0C = 0x06;       // Set frame format: 8data, 1stop bit 
  UCSR0B |= (1 << RXEN0) | (1 << TXEN0);   // TX y RX habilitados

  // Renglones en alta impedancia
  MakeInputPin(DDRB, PB3); WriteOutputPinHigh(PORTB, PB3); //RENGLON 1
  MakeInputPin(DDRB, PB2); WriteOutputPinHigh(PORTB, PB2); //RENGLON 2
  MakeInputPin(DDRB, PB1); WriteOutputPinHigh(PORTB, PB1); //RENGLON 3
  MakeInputPin(DDRB, PB0); WriteOutputPinHigh(PORTB, PB0); //RENGLON 4
  
  // Columnas en pullup
  MakeInputPin(DDRD, PD2); EnablePullUp(PORTD, PD2); //COLUMNA 1
  MakeInputPin(DDRD, PD3); EnablePullUp(PORTD, PD3); //COLUMNA 2
  MakeInputPin(DDRD, PD7); EnablePullUp(PORTD, PD7); //COLUMNA 3
  MakeInputPin(DDRB, PB4); EnablePullUp(PORTB, PB4); //COLUMNA 4

  //creación del semáforo binario
  interruptSemaphore1 = xSemaphoreCreateBinary();

  //creación del semáforo binario
  interruptSemaphore2 = xSemaphoreCreateBinary();

  //creación del semáforo binario
  interruptSemaphore3 = xSemaphoreCreateBinary();

  //creación del semáforo binario
  interruptSemaphore4 = xSemaphoreCreateBinary();
  
  //si el semáforo es creado, inicializa interrupción INT0 (PD2)
  if(interruptSemaphore1 != NULL)
  {
    //se hace PD2 (pin 2) entrada
    DDRD &= ~(1 << PD2);
    //se habilta resistencia pull-up en PD2 (opcional)
    PORTD |= (1 << PD2);
    //se configura interrupción INT0 para disparos positivos
    EICRA |= (1 << ISC00);
    EICRA |= (1 << ISC01);
    //se habilita interrupción INT0
    EIMSK |= (1 << INT0);
    //se habilitan las interrupciones
    sei();
  }

  //si el semáforo es creado, inicializa interrupción INT1 (PD3)
  if(interruptSemaphore2 != NULL)
  {
    //se hace PD3 (pin 3) entrada
    DDRD &= ~(1 << PD3);
    //se habilita resistencia pull-up en PD3 (opcional)
    PORTD |= (1 << PD3);
    //se configura interrupción INT1 para disparos positivos
    EICRA |= (1 << ISC10);
    EICRA |= (1 << ISC11);
    //se habilita interrupción INT1
    EIMSK |= (1 << INT1);
    //se habilitan las interrupciones
    sei();
  }

  //si el semáforo es creado, inicializa interrupción PCINT2 (PD7)
  if(interruptSemaphore3 != NULL)
  {
    //se hace PD7 (pin 7) entrada
    DDRD &= ~(1 << PD7);
    //se habilita interrupción por cambio de estado en PORTC
    PCICR |= (1 << PCIE2);
    //se habilita interrupción PCINT23
    PCMSK2 |= (1 << PCINT23);
    //se habilitan las interrupciones
    sei();
  }

  //si el semáforo es creado, inicializa interrupción PCINT0 (PB4)
  if(interruptSemaphore4 != NULL)
  {
    //se hace PB4 (pin 12) entrada
    DDRB &= ~(1 << PB4);  
    //se habilita interrupción por cambio de estado en PORTB
    PCICR |= (1 << PCIE0);
    //se habilita interrupción PCINT4
    PCMSK0 |= (1 << PCINT4);
    //se habilitan las interrupciones
    sei();
  }
}

void vTaskSendzeros(void * pvParameters)
{
  // Barrido de renglones

  num_fila=1;
  //renglón 1
  MakeOutputPin(DDRB, PB3); 
  WriteOutputPinLow(PORTB, PB3);
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB3); 
  MakeInputPin(DDRB, PB3);

  
  _delay_ms(period);
  num_fila=2;
  //renglón 2
  MakeOutputPin(DDRB, PB2); 
  WriteOutputPinLow(PORTB, PB2);
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB2); 
  MakeInputPin(DDRB, PB2); 

  _delay_ms(period);
  num_fila=3;
  //renglón 3
  MakeOutputPin(DDRB, PB1);  
  WriteOutputPinLow(PORTB, PB1);
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB1); 
  MakeInputPin(DDRB, PB1);

  _delay_ms(period);
  _delay_ms(period);
  num_fila=4;
  //renglón 4
  MakeOutputPin(DDRB, PB0); 
  WriteOutputPinLow(PORTB, PB0);
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB0); 
  MakeInputPin(DDRB, PB0);
  _delay_ms(period);
  
}

void vHandler_line1(void *pvParameters)
{ 
  while(1)
  {
    //espera por siempre al semáforo
    if (xSemaphoreTakeFromISR(interruptSemaphore1, NULL) == pdPASS) 
    {
    switch(num_fila){
      case 1:
        _delay_ms(period);
        tecla = '1';
        break;
      case 2:
        _delay_ms(period);
        tecla = '4';
        break;
      case 3:
        _delay_ms(period);
        tecla = '7';
        break;
      case 4:
        _delay_ms(period);
        tecla = '*';
        break;
    }
    sprintf(mybuffer, "%c\n", tecla);
    USART_Transmit_String((unsigned char *)mybuffer);
    }
  }
}


void vHandler_line2(void *pvParameters)
{
  while(1)
  {
    //espera por siempre al semáforo
    if (xSemaphoreTakeFromISR(interruptSemaphore2, NULL) == pdPASS) 
    {
      switch(num_fila)
      {
        case 1:
          _delay_ms(period);
          tecla = '2';
          break;
        case 2:
          _delay_ms(period);
          tecla = '5';
          break;
        case 3:
          _delay_ms(period);
          tecla = '8';
          break;
        case 4:
          _delay_ms(period);
          tecla = '0';
          break;
      }
      sprintf(mybuffer, "%c\n", tecla);
      USART_Transmit_String((unsigned char *)mybuffer);
    }
    
  }
}

void vHandler_line3(void *pvParameters)
{ 
  while(1)
  {
    //espera por siempre al semáforo
    if (xSemaphoreTakeFromISR(interruptSemaphore3, NULL) == pdPASS) 
    {
      switch(num_fila)
      {
        case 1:
          _delay_ms(period);
          tecla = '3';
          break;
        case 2:
          _delay_ms(period);
          tecla = '6';
          break;
        case 3:
          _delay_ms(period);
          tecla = '9';
          break;
        case 4:
          _delay_ms(period);
          tecla = '#';
          break;
      }
      sprintf(mybuffer, "%c\n", tecla);
      USART_Transmit_String((unsigned char *)mybuffer);
    }
    
  }
}

void vHandler_line4(void *pvParameters)
{ 
  while(1)
  {
    //espera por siempre al semáforo
    if (xSemaphoreTakeFromISR(interruptSemaphore4, NULL) == pdPASS) 
    {
      switch(num_fila)
      {
        case 1:
        _delay_ms(period);
        tecla = 'A';
          break;
        case 2:
        _delay_ms(period);
        tecla = 'B';
          break;
        case 3:
        _delay_ms(period);
        tecla = 'C';
          break;
        case 4:
        _delay_ms(period);
        tecla = 'D';
          break;
      }
      sprintf(mybuffer, "%c\n", tecla);
      USART_Transmit_String((unsigned char *)mybuffer);
    }
    
  }
}

ISR(INT0_vect){ //columna 1 pin 2 PORT D

  //da el semáforo desde ISR
  xSemaphoreGiveFromISR(interruptSemaphore1, NULL);

//sprintf(mybuffer,"INT0\n");
//USART_Transmit_String((unsigned char *)mybuffer);
}

ISR(INT1_vect){ //columna 2 pin 3 PORTD

  //da el semáforo desde ISR
  xSemaphoreGiveFromISR(interruptSemaphore2, NULL);

//sprintf(mybuffer,"INT1\n");
//USART_Transmit_String((unsigned char *)mybuffer);
}

ISR(PCINT2_vect){ //columna 3 pin 7 PORTD

  //da el semáforo desde ISR
  xSemaphoreGiveFromISR(interruptSemaphore3, NULL);

//sprintf(mybuffer,"PCINT2_(PD7)\n");
//USART_Transmit_String((unsigned char *)mybuffer);
}


ISR(PCINT0_vect){ //columna 4 pin 12 PORTB

  //da el semáforo desde ISR
  xSemaphoreGiveFromISR(interruptSemaphore4, NULL);

//sprintf(mybuffer,"PCINT0_(PD12)\n");
//USART_Transmit_String((unsigned char *)mybuffer);
}

void loop()
{
  
  //modo power down
  SMCR |= (1<<SM1); 
  //desactiva interrupciones
  cli(); 
  //habilita sleep           
  SMCR |= (1<<SE);
  //habilita interrupciones  
  sei();
  //aplica sleep
  asm("SLEEP");
  //deshabilita sleep
  SMCR &= ~(1<<SE);
}

//////////funciones de transmisión del UART///////////////

void USART_Transmit(unsigned char data)
{
  //wait for empty transmit buffer
  while(!(UCSR0A & (1 << UDRE0)));
  
  //put data into buffer, send data
  UDR0 = data;  
}

void USART_Transmit_String(unsigned char * pdata)
{
  unsigned char i;
  //calculate string length
  unsigned char len = strlen(pdata);

  //transmit byte for byte
  for(i=0; i < len; i++)
  {
    //wait for empty transmit buffer
    while(!(UCSR0A & (1 << UDRE0)));
    //put data into buffer, send data
    UDR0 = pdata[i];
  }
}
//////////////////////////////////////////////////////////////
