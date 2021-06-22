#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BufferedSerial uart(D1,D0); 
BufferedSerial xbee(D10, D9);
DigitalOut led1(LED1);
DigitalInOut pin10(D11);
BBCar car(pin5, pin6, servo_ticker);

Thread thread;

void stage1(Arguments *in, Reply *out);
void stage2(Arguments *in, Reply *out);
void stage3(Arguments *in, Reply *out);
RPCFunction rpcXBee1(&stage1, "stage1");
RPCFunction rpcXBee2(&stage2, "stage2");
RPCFunction rpcXBee3(&stage3, "stage3");

void stage1(Arguments *in, Reply *out){
   xbee.write("stage 1 completed \r\n", 20);
}

void stage2(Arguments *in, Reply *out){
   xbee.write("stage 2 completed \r\n", 20);
}

void stage3(Arguments *in, Reply *out){
   xbee.write("stage 3 completed \r\n", 20);
}

void ping_thread(){
   while(1) {
      parallax_ping  ping1(pin10);
      if((float)ping1>5){
         led1 = 1;
      }
      else {
         led1 = 0;
         car.stop();
      }
      ThisThread::sleep_for(10ms);
   }
}


int main() {
   thread.start(ping_thread);

   char buf[256], outbuf[256];
   FILE *devin = fdopen(&uart, "r");
   FILE *devout = fdopen(&uart, "w");
   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}
