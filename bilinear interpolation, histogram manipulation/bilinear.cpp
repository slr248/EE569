#include <stdio.h>
#include <iostream>
#include <stdlib.h>


using namespace std;


int main(int argc, char *argv[])

{
	// Define file pointer and variables

  FILE *file;

  int BytesPerPixel;

  int Size1 = 300;
  int Size2= 390;

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
            Size2 = atoi(argv[5]);
		}
	}

	// Allocate image data array
	
            unsigned char Imagedata[Size1][Size2][BytesPerPixel];

	// Read image (filename specified by first argument) into image data matrix

            if (!(file=fopen(argv[1],"rb"))) {

              cout << "Cannot open file: " << argv[1] <<endl;

              exit(1);
	}

              fread(Imagedata, sizeof(unsigned char), Size2*Size1*BytesPerPixel, file);

              fclose(file);


	///////////////////////// INSERT YOUR PROCESSING CODE HERE /////////////////////////
	struct rgbpixel{
		unsigned char Red;
		unsigned char Green;
		unsigned char Blue;
		
		rgbpixel(){
		
			Red=0;
			Green=0;
			Blue=0;
	}
	};
	int i,j;
	rgbpixel output[Size1][Size2];
		for(i=0;i<Size1;i++)
		{
			for(j=0;j<Size2;j++)
			{
				if(i%2==0 and j%2!=0) //extract original red values from imagedata and save to new red location( Red values  at even rows odd columns)
				{
					output[i][j].Red=Imagedata[i][j][0];
					
				}
				else if(i%2!=0 && j%2==0) //interpolate red value at blue location
				{
					output[i][j].Red=(Imagedata[i-1][j-1][0]+Imagedata[i-1][j+1][0]+Imagedata[i+1][j-1][0]+Imagedata[i+1][j+1][0])/4;
				}
				else if(i%2!=0 && j%2!=0)//red at green location odd row , odd  column
				{
					output[i][j].Red=(Imagedata[i-1][j][0]+Imagedata[i+1][j][0])/2;
					
				}
				else if(i%2==0 && j%2==0 ) // red at green , even row , even column
				{
					output[i][j].Red=(Imagedata[i][j-1][0]+Imagedata[i][j+1][0])/2;
				}
			
				
			}
		}
		for(i=0;i<Size1;i++)
		{
			for(j=0;j<Size2;j++)
			{
				if(i%2!=0 && j%2!=0)//extract green , odd row, odd col
				{
					output[i][j].Green=(Imagedata[i][j][0]);
					
				}
				else if(i%2==0 && j%2==0 ) // green, even row , even column
				{
					output[i][j].Green=(Imagedata[i][j][0]);
				}
				if(i%2==0 and j%2!=0) //green at red locations ,even rows ,odd columns
				{
					output[i][j].Green=(Imagedata[i-1][j][0]+Imagedata[i][j-1][0]+Imagedata[i][j+1][0]+Imagedata[i+1][j][0])/4;
					
				}
				if(i%2!=0 and j%2==0) //green at blue locations ,odd rows ,even columns
				{
					output[i][j].Green=(Imagedata[i-1][j][0]+Imagedata[i][j-1][0]+Imagedata[i][j+1][0]+Imagedata[i+1][j][0])/4;
					
				}
		   }
	   }
	   	for(i=0;i<Size1;i++)
		{
			for(j=0;j<Size2;j++)
			{
			    if(i%2!=0 and j%2==0) //extract blue , odd row , even column
				{
					output[i][j].Blue=Imagedata[i][j][0];
			    }
			    if(i%2==0 and j%2!=0)
				{ //blue at red, even row ,odd column
					output[i][j].Blue=(Imagedata[i-1][j-1][0]+Imagedata[i-1][j+1][0]+Imagedata[i+1][j-1][0]+Imagedata[i+1][j+1][0])/4;
			    }
			    if(i%2!=0 && j%2!=0)//Blue at green , odd row, odd col
				{
					output[i][j].Blue=(Imagedata[i][j+1][0]+Imagedata[i][j-1][0])/2;
					
				}
				if(i%2==0 && j%2==0)//Blue at green , even row, even col
				{
					output[i][j].Blue=(Imagedata[i+1][j][0]+Imagedata[i-1][j][0])/2;
					
				}
		    }
		}
			    
				
	       
				
				
				
				
			
	
		

	// Write image data (filename specified by second argument) from image data matrix

	
            if (!(file=fopen(argv[2],"wb"))) {

              cout << "Cannot open file: " << argv[2] << endl;
		exit(1);
	}

              fwrite(output, sizeof(unsigned char), Size1*Size2*3, file);

              fclose(file);


              	return 0;
}

