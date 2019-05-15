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
  int N=4;                  //DO NOT CHANGE N
  int I2[2][2]={1,2,3,0};
  int I4[4][4];
  int I8[8][8];
  int I16[16][16];
  int I32[32][32];
  for(int i=0;i<N;i++){
  	for(int j=0;j<N;j++){
  		if(i<N/2 && j<N/2){
  			I4[i][j]=4*I2[i%(N/2)][j%(N/2)]+1;
		  }
		 if(i<N/2 && j>=N/2){
		 	I4[i][j]=4*I2[i%(N/2)][j%(N/2)]+2;
		 }
		 if(i>=N/2 && j<N/2){
		 	I4[i][j]=4*I2[i%(N/2)][j%(N/2)]+3;
		 }
		 if(i>=N/2 && j>=N/2){
		 	I4[i][j]=4*I2[i%(N/2)][j%(N/2)];
		 }
	  }
  }
  N=8;
   for(int i=0;i<N;i++){
  	for(int j=0;j<N;j++){
  		if(i<N/2 && j<N/2){
  			I8[i][j]=4*I4[i%(N/2)][j%(N/2)]+1;
		  }
		 if(i<N/2 && j>=N/2){
		 	I8[i][j]=4*I4[i%(N/2)][j%(N/2)]+2;
		 }
		 if(i>=N/2 && j<N/2){
		 	I8[i][j]=4*I4[i%(N/2)][j%(N/2)]+3;
		 }
		 if(i>=N/2 && j>=N/2){
		 	I8[i][j]=4*I4[i%(N/2)][j%(N/2)];
		 }
	  }
  }
  N=16;
   for(int i=0;i<N;i++){
  	for(int j=0;j<N;j++){
  		if(i<N/2 && j<N/2){
  			I16[i][j]=4*I8[i%(N/2)][j%(N/2)]+1;
		  }
		 if(i<N/2 && j>=N/2){
		 	I16[i][j]=4*I8[i%(N/2)][j%(N/2)]+2;
		 }
		 if(i>=N/2 && j<N/2){
		 	I16[i][j]=4*I8[i%(N/2)][j%(N/2)]+3;
		 }
		 if(i>=N/2 && j>=N/2){
		 	I16[i][j]=4*I8[i%(N/2)][j%(N/2)];
		 }
	  }
  }
  N=32;          
   for(int i=0;i<N;i++){
  	for(int j=0;j<N;j++){
  		if(i<N/2 && j<N/2){
  			I32[i][j]=4*I16[i%(N/2)][j%(N/2)]+1;
		  }
		 if(i<N/2 && j>=N/2){
		 	I32[i][j]=4*I16[i%(N/2)][j%(N/2)]+2;
		 }
		 if(i>=N/2 && j<N/2){
		 	I32[i][j]=4*I16[i%(N/2)][j%(N/2)]+3;
		 }
		 if(i>=N/2 && j>=N/2){
		 	I32[i][j]=4*I16[i%(N/2)][j%(N/2)];
		 }
	  }
  }
int n=32;                       //CHANGE n to 2,4,6,8,16,32......
int T[n][n];
unsigned char op[Size1][Size2];
for(int i=0;i<n;i++){
  for(int j=0;j<n;j++){
    T[i][j]=((float)I32[i][j]+0.5)/(n*n)*255;       //CHANGE I32 //// I2 for n=2 , I4 n=4 , I8 n=8 , I16 n=16
  }
}
for(int i=0;i<Size1;i++){
  for(int j=0;j<Size2;j++){
    if(Imagedata[i][j][0]>=T[i%n][j%n]){
      op[i][j]=255;
    }
    if(Imagedata[i][j][0]<T[i%n][j%n]){
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
