/*
To test that the Linux framebuffer is set up correctly, and that the device permissions
are correct, use the program below which opens the frame buffer and draws a gradient-
filled red square:

retrieved from:
Testing the Linux Framebuffer for Qtopia Core (qt4-x11-4.2.2)

http://cep.xor.aps.anl.gov/software/qt4-x11-4.2.2/qtopiacore-testingframebuffer.html
*/

#include <ctype.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include "/opt/source/Robotics_Cape_Installer/libraries/rc_usefulincludes.h"
#include "/opt/source/Robotics_Cape_Installer/libraries/roboticscape.h"

int get_color(char* cvalue){

    char* pch = strtok(cvalue, ",");
    int red = atoi(pch);
    red = (red > 0 && red <=255) ? red : 0; 
    int green = atoi(strtok(NULL, ","));
    green = (green > 0 && green <=255) ? green : 0; 
    int blue = atoi(strtok(NULL, ","));
    blue = (blue > 0 && blue <=255) ? blue : 0;
    unsigned short int t = red<<11 | green << 5 | blue;
    return t;
}

int get_color_from_rgb(int red, int green, int blue){
    unsigned short int t = red<<11 | green << 5 | blue;
    return t;
}

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

    short color = (0<<11) | (0 << 5) | 8;  // RGB background color
    int line_color = get_color_from_rgb(0,17,0);
    int cursor_color = 0xff;
    int z = 0;  //line width
    int c = 0;
    char* cvalue = NULL;
    while ((c = getopt (argc, argv, "abc:")) != -1){
    switch (c)
      {
      case 'b': //background color
        cvalue = optarg;
        color = get_color(cvalue);
        break;
      case 'l': //line width
        cvalue = optarg;
        line_color = get_color(cvalue);
        break;
      case 'c': //cursor color
        cvalue = optarg;
        cursor_color = get_color(cvalue);
        break;
      case 'w': //line width
        char* cvalue = optarg;
        z = atoi(argv[1])/2;
        if (z < 0 || z > 240)
            z = 0;
        break;
      case '?':
        if (optopt == 'bg_color' || optopt == 'line_color' || optopt == 'cursor_color' || optopt == 'line_width')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        abort ();
      }
    }
    // Black out the screen
    
    for(int i=0; i<screensize; i+=2) {
        fbp[i  ] = color;      // Lower 8 bits
        fbp[i+1] = color>>8;   // Upper 8 bits
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
        // printf("xpos: %d, xres: %d\n", rc_get_encoder_pos(1), vinfo.xres)

        if((x != xold) || (y != yold)) {
            int i = 0, j= 0;
            // printf("\n");
            for (i=-z; i<=z; i++){
                for (j=-z; j<=z; j++){
                    location = (xold+i+vinfo.xoffset) * (vinfo.bits_per_pixel/8) +
                               (yold+j+vinfo.yoffset) * finfo.line_length;
                    *((unsigned short int*)(fbp + location)) = line_color;
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
                    *((unsigned short int*)(fbp + location)) = cursor_color;
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