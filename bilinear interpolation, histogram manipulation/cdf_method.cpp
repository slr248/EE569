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
	
	int i,j,l;
	int k;
//	int inp[Size][Size][1];
	
	/*for(i=0;i<Size;i++){
		for(j=0;j<Size;j++){
			inp[Size][Size][0]=(int)Imagedata[i][j][0];
		}
	}*/
	
	int row_val[160000]={0};
	int col_val[160000]={0};
	unsigned char output_img[Size][Size][1];
	int m=0,n=0;
	for(k=0;k<256;k++){
		for(i=0;i<400;i++){
			for(j=0;j<400;j++){
				if(Imagedata[i][j][0]==((int)k)){
					row_val[m]=i;
					col_val[n]=j;
					
					m=m+1;
					n=n+1;
				}
			}
		}
	}
	
	int x=0;
	for(k=0;k<256;k++){
	
	    for(j=x;j<625+x;j++){
			    output_img[row_val[j]][col_val[j]][0]=k;
		     }
		x=x+625;     
	}
//	for(i=0;i<;i++){
		cout<<(double)Imagedata[55][88][0]<<' ';
//	}
    

	// Write image data (filename specified by second argument) from image data matrix

	
            if (!(file=fopen(argv[2],"wb"))) {

              cout << "Cannot open file: " << argv[2] << endl;
		exit(1);
	}
              cout<<"test1";
              fwrite(output_img, sizeof(unsigned char), Size*Size*BytesPerPixel, file);
              cout<<"text2";
              fclose(file);


              	return 0;
}

