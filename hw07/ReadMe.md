# Homework 7

## Requirements:
### Project
By now your project should be well underway.  It’s time to start documenting it.  Copy (don’t edit) the Project Template. The title for the wiki page should be ECE497 Project - Your Title, where Your Title is the title of your project.  Notice the first line in the template is [[Category:ECE497 |Px]].  Change the x to the first letter of your project title. There is no space between the | and the P or the P and the x.
Fill in what you can about your project.  Fill in the Executive Summary with what your project is about and what’s done so far.
### GPIO Speed
In this class we have learned a number of ways to read and write GPIO pins.  The purpose of this homework is to compare the speeds and CPU loads of the various methods. You are to write (or adapt) several programs (noted below) that will read the value of GP1_3 and copy it to GP1_4. For each program attach a function generator to GP1_3 and input a square wave and measure the time for the output on GP1_4 to respond with an oscilloscope. Estimate the min, max and average times.  Also note the percent CPU usage while the program is running. (Hint:  Use htop). Capture a screenshot from the oscilloscope for at least one of your tests. Write a small (one page) report presenting your results.  Use a table to compare each.
### JavaScript, Python, Java or C
Write a script the uses interrupts to detect when GP1_3 changes and writes the new value to GP1_4.
### mmap via C
Write a C program that uses mmap to copy GP1_3 to GP1_4.
### Kernel
Modify the kernel driver presented [here](http://derekmolloy.ie/kernel-gpio-programming-buttons-and-leds) to copy GP1_3 to GP1_4.

## Work

### GPIO Speed
I developed a report from the result of my efforts. It is in [homework7report.pdf](homework7report.pdf)

### JavaScript, Python, Java or C
Here I wrote a Python script using interrupts to detect a pin change. It is [here](python_interrupts.py).
### mmap via C
Here I wrote a program that uses mmap and polls for changes on the GPIO [here](gpioThru.c).
### Kernel
Here I modified the kernel driver presented in the link above and made it utilize the functionality of copying different pins. It is [here](gpio_kernel.c).

### Requirements:
- A beaglebone
- Kernel Headers

### Usage:
#### Python
	- `sudo python python_interrupts.py`
#### mmap via C
	- `gcc -O3 -Wall gpioThru.c -o gpioThru`
	- `sudo ./gpioThru`
#### Kernel
	- `make`
	- `sudo insmod ./gpio_kernel.ko`
	- `sudo rmmod GPIO_kernel`