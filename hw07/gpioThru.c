// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Read one gpio pin and write it out to another using mmap.
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
//C file using MMAP to read two buttons and toggle two leds
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

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
    volatile void *gpio_addr_led;
    volatile unsigned int *gpio_oe_addr_l;
    volatile unsigned int *gpio_datain_l;
    volatile unsigned int *gpio_setdataout_addr_l;
    volatile unsigned int *gpio_cleardataout_addr_l;
    unsigned int reg;

    // Set the signal callback for Ctrl-C
    signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    //printf("Mapping %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, 
    //                                       GPIO0_SIZE);

    gpio_addr_led    = mmap(0, GPIO3_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO3_START_ADDR);
    
    gpio_oe_addr_l           = gpio_addr_led + GPIO_OE;
    gpio_datain_l            = gpio_addr_led + GPIO_DATAIN;
    gpio_setdataout_addr_l   = gpio_addr_led + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_l = gpio_addr_led + GPIO_CLEARDATAOUT;

    if(gpio_addr_led == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }
    printf("led GPIO mapped to %p\n", gpio_addr_led);
    printf("led GPIO OE mapped to %p\n", gpio_oe_addr_l);
    printf("led GPIO SETDATAOUTADDR mapped to %p\n", gpio_setdataout_addr_l);
    printf("led GPIO CLEARDATAOUT mapped to %p\n", gpio_cleardataout_addr_l);

    printf("Start copying GPIO3[2] to GPIO3[1]\n");
    while(keepgoing) {
        if((*gpio_datain_l & GPIO_2)) {
            *gpio_setdataout_addr_l= GPIO_1;
        }else {
            *gpio_cleardataout_addr_l = GPIO_1;
        }
        //usleep(1);
    }

    //munmap((void *)gpio_addr, GPIO0_SIZE);
    close(fd);
    return 0;
}