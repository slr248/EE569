
#include <stdio.h>
#include <iostream>
#include <stdlib.h>


using namespace std;


int main(int argc, char *argv[])

{
	// Define file pointer and variables

  FILE *file;

  int BytesPerPixel;

  int Size = 400;

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

            Size = atoi(argv[4]);
		}
	}

	// Allocate image data array
	
            unsigned char Imagedata[Size][Size][BytesPerPixel];

	// Read image (filename specified by first argument) into image data matrix

            if (!(file=fopen(argv[1],"rb"))) {

              cout << "Cannot open file: " << argv[1] <<endl;

              exit(1);
	}

              fread(Imagedata, sizeof(unsigned char), Size*Size*BytesPerPixel, file);

              fclose(file);


	///////////////////////// INSERT YOUR PROCESSING CODE HERE /////////////////////////
	int hist[256];
	int i,j;
	for(i=0;i<256;i++){
		hist[i]=0;
	}
    for(i=0;i<Size;i++){
	    for(j=0;j<Size;j++){
		    hist[Imagedata[i][j][0]]=hist[Imagedata[i][j][0]]+1;      //Get histogram (frequency of pixels per intensity 0-255)
	}
}
	int  bin =625;
	double prob[256];
	for(i=0;i<256;i++){  //initalize prob to zero
		prob[i]=0;
	}
	for(i=0;i<256;i++){
		prob[i]=(double)hist[i]/160000;            //get the probability of a pixel to occur for a particular intensity ( pixel freq/Total pixels)
	}
	double sum=0;
	double cdf[256];
	for(i=0;i<256;i++){                   //initialize cdf to zero
		cdf[i]=0;
	}
	for(i=0;i<256;i++){
		sum=sum+prob[i];                //get the cdf 
		cdf[i]=sum;
		
	}
	double T=255;
	unsigned char output[Size][Size][1];
	for(i=0;i<400;i++){    
	    for(j=0;j<400;j++){            //distribute values uniformly
		     output[i][j][0]=cdf[Imagedata[i][j][0]];
	}
}
 
    for(i=0;i<256;i++){  //debug
    	cout<<cdf[i]<<',';
    	
	}

	// Write image data (filename specified by second argument) from image data matrix

	
            if (!(file=fopen(argv[2],"wb"))) {

              cout << "Cannot open file: " << argv[2] << endl;
		exit(1);
	}

              fwrite(output, sizeof(unsigned char), Size*Size*1, file);

              fclose(file);


              	return 0;
}

