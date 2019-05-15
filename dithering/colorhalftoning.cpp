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

  int Size1 = 375;
  int Size2=500;
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

            unsigned char Imagedata[Size1][Size2][3];

	// Read image (filename specified by first argument) into image data matrix

            if (!(file=fopen(argv[1],"rb"))) {

              cout << "Cannot open file: " << argv[1] <<endl;

              exit(1);
	}

              fread(Imagedata, sizeof(unsigned char), Size1*Size2*3, file);

              fclose(file);


	///////////////////////// INSERT YOUR PROCESSING CODE HERE /////////////////////////

short cmy_channel[Size1][Size2][3];

for(int k=0;k<3;k++){     //changing to CMY space
  for(int i=0;i<Size1;i++){
    for(int j=0;j<Size2;j++){
      cmy_channel[i][j][k]=255-(short)Imagedata[i][j][k];      
    }
  }
}


int e;
for(int k=0;k<3;k++){   //applying FS for all 3 channels
  for(int i=0;i<Size1;i++){
    for(int j=0;j<Size2;j++){
      if(i%2 == 0){               //Even row
        if(cmy_channel[i][j][k] >= 128){
          e=cmy_channel[i][j][k]-255;
          cmy_channel[i][j][k]=255;
          cmy_channel[i][j+1][k]+=trunc((float)7/16*e);
          cmy_channel[i+1][j+1][k]+=trunc((float)1/16*e);
          cmy_channel[i+1][j][k]+=trunc((float)5/16*e);
          cmy_channel[i+1][j-1][k]+=trunc((float)3/16*e);
        }
        else if(cmy_channel[i][j][k] < 128){
          e=cmy_channel[i][j][k];
          cmy_channel[i][j][k]=0;
          cmy_channel[i][j+1][k]+=trunc((float)7/16*e);
          cmy_channel[i+1][j+1][k]+=trunc((float)1/16*e);
          cmy_channel[i+1][j][k]+=trunc((float)5/16*e);
          cmy_channel[i+1][j-1][k]+=trunc((float)3/16*e);
        }
      }
      else if(i%2 != 0){           //odd row
        if(cmy_channel[i][Size2-1-j][k] >= 128){
          e=cmy_channel[i][Size2-1-j][k]-255;
          cmy_channel[i][Size2-1-j][k]=255;
          cmy_channel[i][Size2-1-j-1][k]+=trunc((float)7/16*e);
          cmy_channel[i+1][Size2-1-j+1][k]+=trunc((float)3/16*e);
          cmy_channel[i+1][Size2-1-j][k]+=trunc((float)5/16*e);
          cmy_channel[i+1][Size2-1-j-1][k]+=trunc((float)5/16*e);
        }
        else if(cmy_channel[i][Size2-1-j][k] < 128){
          e=cmy_channel[i][Size2-1-j][k];
          cmy_channel[i][Size2-1-j][k]=0;
          cmy_channel[i][Size2-1-j-1][k]+=trunc((float)7/16*e);
          cmy_channel[i+1][Size2-1-j+1][k]+=trunc((float)3/16*e);
          cmy_channel[i+1][Size2-1-j][k]+=trunc((float)5/16*e);
          cmy_channel[i+1][Size2-1-j-1][k]+=trunc((float)1/16*e);
        }
      }
    }
  }
}
//cout<<sizeof(unsigned char);
cout<<"test2";
//unsigned char rgb_op[Size1][Size2][3];         //converting cmy back to rgb
//cout<<"test";
for(int i=0;i<Size1;i++){
  for(int j=0;j<Size2;j++){
    Imagedata[i][j][0]=255-cmy_channel[i][j][0];
    Imagedata[i][j][1]=255-cmy_channel[i][j][1];
    Imagedata[i][j][2]=255-cmy_channel[i][j][2];
  }
}
// Write image data (filename specified by second argument) from image data matrix


          if (!(file=fopen(argv[2],"wb"))) {

            cout << "Cannot open file: " << argv[2] << endl;
  exit(1);
}

            fwrite(Imagedata, sizeof(unsigned char), Size1*Size2*3, file);

            fclose(file);


              return 0;
}
