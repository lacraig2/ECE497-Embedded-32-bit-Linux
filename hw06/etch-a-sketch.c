/*
To test that the Linux framebuffer is set up correctly, and that the device permissions
are correct, use the program below which opens the frame buffer and draws a gradient-
filled red square:

retrieved from:
Testing the Linux Framebuffer for Qtopia Core (qt4-x11-4.2.2)

http://cep.xor.aps.anl.gov/software/qt4-x11-4.2.2/qtopiacore-testingframebuffer.html
*/

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <string.h> 
#include <sys/ioctl.h>

#include "/opt/source/Robotics_Cape_Installer/libraries/rc_usefulincludes.h"
#include "/opt/source/Robotics_Cape_Installer/libraries/roboticscape.h"

int main(int argc, char **argv, char *envp[]){
    int fbfd = 0;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    long int screensize = 0;
    char *fbp = 0;
    int x = 0, y = 1;       // Make it so the it runs before the encoder is moved
    int xold = 0, yold = 0;
    long int location = 0;

    // Open the file for reading and writing
    fbfd = open("/dev/fb0", O_RDWR);
    if (fbfd == -1) {
        perror("Error: cannot open framebuffer device");
        exit(1);
    }
    printf("The framebuffer device was opened successfully.\n");

    // Get fixed screen information
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo) == -1) {
        perror("Error reading fixed information");
        exit(2);
    }

    // Get variable screen information
    if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo) == -1) {
        perror("Error reading variable information");
        exit(3);
    }

    printf("%dx%d, %dbpp\n", vinfo.xres, vinfo.yres, vinfo.bits_per_pixel);
    printf("Offset: %dx%d, line_length: %d\n", vinfo.xoffset, vinfo.yoffset, finfo.line_length);
    
    if (vinfo.bits_per_pixel != 16) {
        printf("Can't handle %d bpp, can only do 16.\n", vinfo.bits_per_pixel);
        exit(5);
    }

    // Figure out the size of the screen in bytes
    screensize = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8;

    // Map the device to memory
    fbp = (char *)mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);
    if ((int)fbp == -1) {
        perror("Error: failed to map framebuffer device to memory");
        exit(4);
    }
    printf("The framebuffer device was mapped to memory successfully.\n");

    // initialize hardware first
    if(rc_initialize()){
        fprintf(stderr,"ERROR: failed to run rc_initialize(), are you root?\n");
        return -1;
    }

    printf("\nRaw encoder positions\n");
    printf("   E1   |");
    printf("   E2   |");
    printf("   E3   |");
    printf("   E4   |");
    printf(" \n");
    
    // Black out the screen
    short color = (0<<11) | (0 << 5) | 8;  // RGB
    for(int i=0; i<screensize; i+=2) {
        fbp[i  ] = color;      // Lower 8 bits
        fbp[i+1] = color>>8;   // Upper 8 bits
    }

    int q = 0;
    for (q=0; q<argc; q++){
        printf("%d %s", q, argv[q]);
    }

    while(rc_get_state() != EXITING) {
        printf("\r");
        for(int i=1; i<=4; i++){
            printf("%6d  |", rc_get_encoder_pos(i));
        }
        fflush(stdout);
        // Update framebuffer
        // Figure out where in memory to put the pixel
        x = (rc_get_encoder_pos(1)/2 + vinfo.xres) % vinfo.xres;
        y = (rc_get_encoder_pos(3)/2 + vinfo.yres) % vinfo.yres;
        // printf("xpos: %d, xres: %d\n", rc_get_encoder_pos(1), vinfo.xres);
        int z = 0;
        if (argc > 1){
            z = atoi(argv[1])/2;
            if (z < 0 || z > 240){
                z = 0;
            }
        }
        int r = 0;     // 5 bits
        int g = 17;      // 6 bits
        int b = 0;      // 5 bits
        unsigned short int t = r<<11 | g << 5 | b;
        if (argc > 2){
            if (strcmp(argc[2], "red")==0){
                r = 255;
                b = 0;
                g = 0;
                t = r<<11 | g << 5 | b;
            }else if (strcmp(argc[2], "green")==0){
                r = 0;
                b = 0;
                g = 255;
                t = r<<11 | g << 5 | b;
            }else if (strcmp(argc[2],"blue")==0){
                r = 0;
                b = 255;
                g = 255;
                t = r<<11 | g << 5 | b;
            }
        }


        if((x != xold) || (y != yold)) {
            int i = 0, j= 0;
            // printf("\n");
            for (i=-z; i<=z; i++){
                for (j=-z; j<=z; j++){
                    location = (xold+i+vinfo.xoffset) * (vinfo.bits_per_pixel/8) +
                               (yold+j+vinfo.yoffset) * finfo.line_length;    
                    *((unsigned short int*)(fbp + location)) = t;
                }
            }

            for (i=-z; i <= z; i++){
                for (j=-z; j<=z; j++){
                    // printf("position: %d %d\n", i, j);
                    // printf("Updating location to %d, %d\n", x+i, y+j);
                    // // Set old location to green
                    // Set new location to white
                    location = (x+i+vinfo.xoffset) * (vinfo.bits_per_pixel/8) +
                               (y+j+vinfo.yoffset) * finfo.line_length;
                    *((unsigned short int*)(fbp + location)) = 0xff;
                }
            }
            xold = x;
            yold = y;
        }
        
        rc_usleep(5000);
    }
    
    rc_cleanup();
    
    munmap(fbp, screensize);
    close(fbfd);
    return 0;
}