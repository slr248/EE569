#include <stdio.h>
#include <iostream>
#include <stdlib.h>
using namespace std;
int main(int argc, char *argv[])
{
	// Define file pointer and variables
  FILE *file;
  int BytesPerPixel;
  int Size1 = 400;
  int Size2=600;
	// Check for proper syntax
	  if (argc < 3){

  	cout << "Syntax Error - Incorrect Parameter Usage:" << endl;

       cout << "program_name input_image.raw output_image.raw [BytesPerPixel = 1] [Size = 256]" << endl;

       return 0;

     }

	// Check if image is grayscale or color

     if (argc < 4){

       BytesPerPixel = 1; // default is grey image
	}

       	else {
		BytesPerPixel = atoi(argv[3]);
		// Check if size is specified

          if (argc >= 5){

            Size1 = atoi(argv[4]);
		}
	}

	// Allocate image data array

            unsigned char Imagedata[Size1][Size2][BytesPerPixel];

	// Read image (filename specified by first argument) into image data matrix

            if (!(file=fopen(argv[1],"rb"))) {

              cout << "Cannot open file: " << argv[1] <<endl;

              exit(1);
	}

              fread(Imagedata, sizeof(unsigned char), Size1*Size2*BytesPerPixel, file);

              fclose(file);


	///////////////////////// INSERT YOUR PROCESSING CODE HERE /////////////////////////
  int i=0,j=0,x;
  unsigned char op[Size1][Size2];
  for(i=0;i<Size1;i++){
    for(j=0;j<Size2;j++){
      x=rand() % 256;
      if(Imagedata[i][j][0] >= (int)x){
      op[i][j]=255;
      }
      else if(Imagedata[i][j][0] < (int)x){
        op[i][j]=0;
      }
    }
  }

	// Write image data (filename specified by second argument) from image data matrix


            if (!(file=fopen(argv[2],"wb"))) {

              cout << "Cannot open file: " << argv[2] << endl;
		exit(1);
	}

              fwrite(op, sizeof(unsigned char), Size1*Size2*BytesPerPixel, file);

              fclose(file);


              	return 0;

}
