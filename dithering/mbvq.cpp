#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <cmath>

using namespace std;
int get_mbvq(int r,int g,int b){
int cmyw=1,mygc=2,rgmy=3,krgb=4,rgbm=5,cmgb=6;
  if((r+g)>255){
    if((g+b)>255){
      if((r+g+b)>510){
        return cmyw;
      }
      else{
        return mygc;
      }
    }
    else{
      return rgmy;
    }
  }
  else{
    if(!((g+b)>255)){
      if(!((r+g+b)>255)){
        return krgb;
      }
      else{
        return rgbm;
      }
    }
    else{
      return cmgb;
    }
}
}

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
//cout<<"test0";
//cout<<"test";
for(int k=0;k<3;k++){
  for(int i=0;i<Size1;i++){
    for(int j=0;j<Size2;j++){
      cmy_channel[i][j][k]=Imagedata[i][j][k];      
    }
  }
}

int vertex[3];
int e;
float R,G,B;
int R1, G1, B1;
////
for(int i=0;i<Size1;i++){
	for(int j=0;j<Size2;j++){
if(i%2==0){		
 R1=cmy_channel[i][j][0];
 G1=cmy_channel[i][j][1];
 B1=cmy_channel[i][j][2];
}
else{
 R1=cmy_channel[i][Size2-j-1][0];
 G1=cmy_channel[i][Size2-j-1][1];
 B1=cmy_channel[i][Size2-j-1][2];
}

int mbvq;
mbvq=get_mbvq(R1,G1,B1);          //get mbvq for rgb(i,j)+e(i,j)
R = (float)R1/255;
G = (float)G1/255;
B = (float)B1/255;
//////finding vertex///////
  if (mbvq == 1){         //cmyw 
        vertex[0]=255;   //white
        vertex[1]=255;
		vertex[2]=255;
        if (B < 0.5){
            if (B <= R){
                if (B <= G){
                    vertex[0]=255;   //yellow
                    vertex[1]=255;
					vertex[2]=0;	
				}
            }
        }
        
        if (G < 0.5){
            if (G <= B){
                if (G <= R){
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
               }
           } 
        }
        if (R < 0.5){
            if (R <= B){
                if (R <= G){
                    vertex[0]=0;   //cyan
                    vertex[1]=255;
					vertex[2]=255;
               }
           }
       }
   }


// No.2 for MYGC            //mygc
    if(mbvq == 2){
        vertex[0]=255;   //magenta
        vertex[1]=0;
		vertex[2]=255;
        if (G >= B){
            if (R >= B){
                if (R >= 0.5){
                    vertex[0]=255;   //yellow
                    vertex[1]=255;
					vertex[2]=0;
                }
                else{
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
            }
        }
        if(G >= R){
            if (B >= R){
                if (B >= 0.5){
                    vertex[0]=0;   //cyan
                    vertex[1]=255;
					vertex[2]=255;
                }
                else{
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
            }
        }
    }
    


// No.3 for RGMY                  //Looks right
    if (mbvq == 3){
        if (B > 0.5){
            if (R > 0.5){
                if (B >= G){
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
                }
                else{
                    vertex[0]=255;   //yellow
                    vertex[1]=255;
					vertex[2]=0;
                }
            }
        
            else{
                if (G > B + R){
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
                else{
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
                }
            }
        }
        else{
            if (R >= 0.5){
                if (G >= 0.5){
                    vertex[0]=255;   //yellow
                    vertex[1]=255;
					vertex[2]=0;
                }
                else{
                    vertex[0]=255;   //red
                    vertex[1]=0;
					vertex[2]=0;
                }
            }
            else{
                if (R >= G){
                    vertex[0]=255;   //red
                    vertex[1]=0;
					vertex[2]=0;
                }
                else{
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
            }
        }
   }


// No.4 for KRGB
    if (mbvq == 4){
        vertex[0]=0;   //black
        vertex[1]=0;
	    vertex[2]=0;
        if (B > 0.5){
            if (B >= R){
                if (B >= G){
                    vertex[0]=0;   //blue
                    vertex[1]=0;
					vertex[2]=255;
                } 
            }
        }
        if (G > 0.5){
            if (G >= B){
                if (G >= R){
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
            }
        }
        if (R > 0.5){
            if (R >= B){
                if (R >= G){
                    vertex[0]=255;   //red
                    vertex[1]=0;
					vertex[2]=0;
                }
            }
        }
    }


// No.5 for RGBM
    if (mbvq == 5){
        vertex[0]=0;   //green
        vertex[1]=255;
		vertex[2]=0;
        if (R > G){
            if (R >= B){
                if (B < 0.5){
                    vertex[0]=255;   //red
                    vertex[1]=0;
					vertex[2]=0;
                }
                else{
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
                }                
            }
        }
        if (B > G){
            if (B >= R){
                if (R < 0.5){
                    vertex[0]=0;   //blue
                    vertex[1]=0;
					vertex[2]=255;
                }
                else{
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
                }
            }
        }
    }


// No.6 for CMGB
    if (mbvq == 6){
        if (B > 0.5){
            if ( R > 0.5){
                if (G >= R){
                    vertex[0]=0;   //cyan
                    vertex[1]=255;
					vertex[2]=255;
                }
                else{
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
                }
            }
            else{
                if (G > 0.5){
                    vertex[0]=0;   //cyan
                    vertex[1]=255;
					vertex[2]=255;
                }
                else{
                    vertex[0]=0;   //blue
                    vertex[1]=0;
					vertex[2]=255;
                }
            }
        }
        else{
            if ( R > 0.5){
                if (R - G + B >= 0.5){
                    vertex[0]=255;   //magenta
                    vertex[1]=0;
					vertex[2]=255;
                }
                else{
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
            }
            else{
                if (G >= B){
                    vertex[0]=0;   //green
                    vertex[1]=255;
					vertex[2]=0;
                }
                else{
                    vertex[0]=0;   //blue
                    vertex[1]=0;
					vertex[2]=255;
                }
            }
        }
    }

if(i%2==0){		              ///saving vertex values in serpentine manner
    cmy_channel[i][j][0]=vertex[0];
    cmy_channel[i][j][1]=vertex[1];
    cmy_channel[i][j][2]=vertex[2];
}
else{
    cmy_channel[i][Size2-1-j][0]=vertex[0];
    cmy_channel[i][Size2-1-j][1]=vertex[1];
    cmy_channel[i][Size2-1-j][2]=vertex[2];
}

    for(int k=0;k<3;k++){                
    	if(i%2 == 0){               //Even row
       
          e=Imagedata[i][j][k]-cmy_channel[i][j][k];
          cmy_channel[i][j+1][k]+=trunc((float)7/16*e);
          cmy_channel[i+1][j+1][k]+=trunc((float)1/16*e);
          cmy_channel[i+1][j][k]+=trunc((float)5/16*e);
          cmy_channel[i+1][j-1][k]+=trunc((float)3/16*e);
        }
        else if(i%2 != 0){           //odd row
          e=Imagedata[i][Size2-1-j][k]-cmy_channel[i][Size2-1-j][k];
          cmy_channel[i][Size2-1-j-1][k]+=trunc((float)7/16*e);
          cmy_channel[i+1][Size2-1-j+1][k]+=trunc((float)3/16*e);
          cmy_channel[i+1][Size2-1-j][k]+=trunc((float)5/16*e);
          cmy_channel[i+1][Size2-1-j-1][k]+=trunc((float)5/16*e);
        
      }
	}
}
}
///converting to unsigned char///
for(int i=0;i<Size1;i++){                    
    for(int j=0;j<Size2;j++){
        Imagedata[i][j][0]=(unsigned char)cmy_channel[i][j][0];
        Imagedata[i][j][1]=(unsigned char)cmy_channel[i][j][1];
        Imagedata[i][j][2]=(unsigned char)cmy_channel[i][j][2];
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


