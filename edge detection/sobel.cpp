#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <math.h>

using namespace std;


int main(int argc, char *argv[])

{
	// Define file pointer and variables

  FILE *file;

  int BytesPerPixel;

  int Size1 = 321;
  int Size2= 481;
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
//converting to  grayscale
int i,j,k;
unsigned char grayscale[Size1][Size2];
for(i=0;i<Size1;i++){
  for(j=0;j<Size2;j++){
    grayscale[i][j]=((float)Imagedata[i][j][0]+(float)Imagedata[i][j][1]+(float)Imagedata[i][j][2])/3;
    //cout<<(double)grayscale[i][j]<<' ';
  }
}


//////////////////////////////////boundary extension//////////////////////////
int N=3;

unsigned char grayscale_ext[Size1+N-1][Size2+N-1];
for(k=0;k<1;k++){
    for(i=0;i<(N-1)/2;i++){
      for(j=0;j<Size2;j++){
        grayscale_ext[(N-1)/2-i-1][j+(N-1)/2]=grayscale[i][j];
      }
    }
    //cout<<k;
    //left
    for(i=0;i<Size1;i++){
      for(j=0;j<(N-1)/2;j++){
        grayscale_ext[i+(N-1)/2][(N-1)/2-j-1]=grayscale[i][j];
      }
    }
    //right
    for(i=0;i<Size1;i++){
      for(j=0;j<(N-1)/2;j++){
        grayscale_ext[i+(N-1)/2][Size2+(N-1)/2+j]=grayscale[i][Size2-1-j];
      }
    }
    //bottom
    for(i=0;i<(N-1)/2;i++){
      for(j=0;j<Size2;j++){
        grayscale_ext[Size1+(N-1)/2+i][j+(N-1)/2]=grayscale[Size1-1-i][j];
      }
    }
    //Everything else
    for(i=0;i<Size1;i++){
      for(j=0;j<Size2;j++){
        grayscale_ext[(N-1)/2+i][(N-1)/2+j]=grayscale[i][j];
      }
    }
  }
 ///////////////////////////////////////////////////////////////////////////////////////////// 
int x_grad=0;    //Calculating gradient
int y_grad=0;
float mag;
//float gradient[Size1][Size2];
short gradient[Size1][Size2];
for(i=1;i<Size1+1;i++){
  for(j=1;j<Size2+1;j++){
     x_grad=-1*grayscale_ext[i-1][j-1]-2*grayscale_ext[i][j-1]-1*grayscale_ext[i+1][j-1]+1*grayscale_ext[i-1][j+1]+2*grayscale_ext[i][j+1]+1*grayscale_ext[i+1][j+1];
     y_grad=1*grayscale_ext[i-1][j-1]+2*grayscale_ext[i-1][j]+1*grayscale_ext[i-1][j+1]-1*grayscale_ext[i+1][j-1]-2*grayscale_ext[i+1][j]-1*grayscale_ext[i+1][j+1];
     mag=sqrt(x_grad*x_grad+y_grad*y_grad);
     //gradient[i-1][j-1]=mag;
     gradient[i-1][j-1]=mag;
	 //cout<<mag<<" ";
	 if(y_grad > 1020){
	 	cout<<y_grad<<' ';
	 }
  }
}
//cout<<gradient[100][100]<<" ";
int hist_x[]={0};          // normalizing gradient values
int hist_y[]={0};
float range;
float min=gradient[0][0];
float max=gradient[0][0];
for(i=0;i<Size1;i++){
	for(j=0;j<Size2;j++){
		if(gradient[i][j]<min && gradient[i][j]<=1020){
			min=gradient[i][j];
		}
		if(gradient[i][j]>max && gradient[i][j]<=1020){
			max=gradient[i][j];
		}
	}
}
cout<<"||"<<max<<' ';
cout<<min<<' ';
range=max-min;
//cout<<range<<"aa";
unsigned char norm_grad[Size1][Size2];
for(i=0;i<Size1;i++){
	for(j=0;j<Size2;j++){
		float temp = float((gradient[i][j]-min)*(255/range));
		norm_grad[i][j]=(unsigned char)(temp);
		
	}
}

float hist[256]={0};        //creating histogram
for(i=0;i<Size1;i++){
	for(j=0;j<Size2;j++){
		hist[norm_grad[i][j]]+=1;
	}
}
float y=0;
for(i=0;i<256;i++){
	hist[i]=((float)hist[i]/(Size1*Size2));
	//cout<<hist[i]<<' ';
}
float sum=0;
float cdf[256]={0};
for(i=0;i<256;i++){  
    sum=sum+hist[i];            //initialize cdf to zero
	cdf[i]=sum;
	//cout<<cdf[i]<<' ';
}
//cout<<hist[0];
float T=0.95;               //ENTER PERCENTAGE
int thresh;
for(i=0;i<256;i++){
	if(cdf[i]<=T){
		thresh=i;                
	}
}
//cout<<thresh;
for(i=0;i<Size1;i++){                  //THRESHOLDING BASED ON PERCENTAGE
	for(j=0;j<Size2;j++){
		if(norm_grad[i][j]<thresh){
			norm_grad[i][j]=255;
		}
		else if(norm_grad[i][j]>=thresh){
			norm_grad[i][j]=0;
		}
	}
}



 	// Write image data (filename specified by second argument) from image data matrix


            if (!(file=fopen(argv[2],"wb"))) {

              cout << "Cannot open file: " << argv[2] << endl;
		exit(1);
	}

              fwrite(norm_grad, sizeof(unsigned char), Size1*Size2, file);

              fclose(file);


              	return 0;


 }
