// FROM DR.YODER's GITHUB:

// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

#define GPIO_17  (1<<17)
#define GPIO3_START_ADDR 0x481AE000
/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr;
    volatile unsigned int *gpio_oe_addr;
    volatile unsigned int *gpio_setdataout_addr;
    volatile unsigned int *gpio_cleardataout_addr;
    volatile void *gpio1_addr;
    volatile unsigned int *gpio1_oe_addr;
    volatile unsigned int *gpio1_setdataout_addr;
    volatile unsigned int *gpio1_cleardataout_addr;
    volatile unsigned int *gpio1_datain;
    volatile void *gpio3_addr;
    volatile unsigned int *gpio3_oe_addr;
    volatile unsigned int *gpio3_setdataout_addr;
    volatile unsigned int *gpio3_cleardataout_addr;
    volatile unsigned int *gpio3_datain;
    unsigned int reg;
    
    // Set the signal callback for Ctrl-C
	signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, GPIO1_SIZE);

    gpio_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);

    gpio_oe_addr           = gpio_addr + GPIO_OE;
    gpio_setdataout_addr   = gpio_addr + GPIO_SETDATAOUT;
    gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;

    gpio1_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO1_START_ADDR);

    gpio1_oe_addr           = gpio1_addr + GPIO_OE;
    gpio1_datain            = gpio1_addr + GPIO_DATAIN;
    gpio1_setdataout_addr   = gpio1_addr + GPIO_SETDATAOUT;
    gpio1_cleardataout_addr = gpio1_addr + GPIO_CLEARDATAOUT;


    gpio3_addr = mmap(0, GPIO3_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO3_START_ADDR);

    gpio3_oe_addr           = gpio3_addr + GPIO_OE;
    gpio3_datain            = gpio3_addr + GPIO_DATAIN;
    gpio3_setdataout_addr   = gpio3_addr + GPIO_SETDATAOUT;
    gpio3_cleardataout_addr = gpio3_addr + GPIO_CLEARDATAOUT;

    if(gpio_addr == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }
    printf("GPIO mapped to %p\n", gpio_addr);
    printf("GPIO OE mapped to %p\n", gpio_oe_addr);
    printf("GPIO SETDATAOUTADDR mapped to %p\n", gpio_setdataout_addr);
    printf("GPIO CLEARDATAOUT mapped to %p\n", gpio_cleardataout_addr);

    // Set USR2 to be an output pin
    reg = *gpio_oe_addr;
    printf("GPIO1 configuration: %X\n", reg);
    reg &= ~USR2;       // Set USR2 bit to 0
    *gpio_oe_addr = reg;
    printf("GPIO1 configuration: %X\n", reg);

    // Set USR3 to be an output pin
    reg = *gpio_oe_addr;
    printf("GPIO1 configuration: %X\n", reg);
    reg &= ~USR3;       // Set USR3 bit to 0
    *gpio_oe_addr = reg;
    printf("GPIO1 configuration: %X\n", reg);

    printf("Start blinking LED USR3\n");
    while(keepgoing) {
        if(*gpio3_datain & GPIO_17) {
            printf("GPIO3_17 on\n");
            *gpio_setdataout_addr = USR2;
            usleep(100);
        } else {
            printf("GPIO3_17 off\n");
            *gpio_cleardataout_addr = USR2;
            usleep(100);
        }
        usleep(10000);
    }

    munmap((void *)gpio_addr, GPIO1_SIZE);
    munmap((void *)gpio3_addr, GPIO0_SIZE);
    close(fd);
    return 0;
}
