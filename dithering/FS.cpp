#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <cmath>
using namespace std;
int main(int argc, char *argv[])
{
	// Define file pointer and variables

  FILE *file;
  int BytesPerPixel;
  int Size1 = 400;
  int Size2= 600;

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
cout<<"test";
int op[Size1][Size2];
cout<<"test3";
int i,j,e;
for(i=0;i<Size1;i++){
  for(j=0;j<Size2;j++){
    op[i][j]=Imagedata[i][j][0];
  }
}
cout<<"test1";
for(i=0;i<Size1;i++){
  for(j=0;j<Size2;j++){
    if(i%2 == 0){               //Even row
      if(op[i][j] >= 128){
        e=op[i][j]-255;
        op[i][j]=255;
        op[i][j+1]+=trunc((float)7/16*e);
        op[i+1][j+1]+=trunc((float)1/16*e);
        op[i+1][j]+=trunc((float)5/16*e);
        op[i+1][j-1]+=trunc((float)3/16*e);
      }
      else if(op[i][j] < 128){
        e=op[i][j];
        op[i][j]=0;
        op[i][j+1]+=trunc((float)7/16*e);
        op[i+1][j+1]+=trunc((float)1/16*e);
        op[i+1][j]+=trunc((float)5/16*e);
        op[i+1][j-1]+=trunc((float)3/16*e);
      }
    }
    else if(i%2 != 0){           //odd row
      if(op[i][Size2-1-j] >= 128){
        e=op[i][Size2-1-j]-255;
        op[i][Size2-1-j]=255;
        op[i][Size2-1-j-1]+=trunc((float)7/16*e);
        op[i+1][Size2-1-j+1]+=trunc((float)3/16*e);
        op[i+1][Size2-1-j]+=trunc((float)5/16*e);
        op[i+1][Size2-1-j-1]+=trunc((float)5/16*e);
      }
      else if(op[i][Size2-1-j] < 128){
        e=op[i][Size2-1-j];
        op[i][Size2-1-j]=0;
        op[i][Size2-1-j-1]+=trunc((float)7/16*e);
        op[i+1][Size2-1-j+1]+=trunc((float)3/16*e);
        op[i+1][Size2-1-j]+=trunc((float)5/16*e);
        op[i+1][Size2-1-j-1]+=trunc((float)1/16*e);
      }
    }
  }
}

unsigned char op1[Size1][Size2];
for(i=0;i<Size1;i++){
  for(j=0;j<Size2;j++){
    op1[i][j]=(unsigned char)op[i][j];
  }
}

	// Write image data (filename specified by second argument) from image data matrix


            if (!(file=fopen(argv[2],"wb"))) {

              cout << "Cannot open file: " << argv[2] << endl;
		exit(1);
	}

              fwrite(op1, sizeof(unsigned char), Size1*Size2*BytesPerPixel, file);

              fclose(file);


              	return 0;
}
