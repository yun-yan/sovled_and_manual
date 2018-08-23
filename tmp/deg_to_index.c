#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define PI 3.14159265358979323846

void  deg_to_index(float x,float y);      //call function deg_to_index


//elimate the repeat number
int delete_elem(int arr[])              
{   
    //To create a new array flag is [0,0,0...] and if the position has the number fron arr it will be 1
    int i=0,arr_len=4,new_arr_len=0;
    int flag[20]={0};
    for ( i =0; i < arr_len; i++)
    {
        if (flag[arr[i]]==0)
        {
            //just let 0 into arr if it has become 1, and then it will skip.
            arr[new_arr_len++] = arr[i];
            flag[arr[i]]=1;
        }
    }
    return new_arr_len;
}


//main funcion
int main(int argc, char *argv[]) 
{   
    //if the user doesn't use 3 argument
    if( argc!= 3 )
    {   
        printf("%s:\n","use two arugement here and they must be number");
        return 1;
    } 
    //Let str to float
    float RA,DEC;
    RA=atof(argv[1]);
    DEC=atof(argv[2]);
    deg_to_index(RA,DEC);
    return 0;
}


//deg to the position of healpix
void  deg_to_index(float x,float y)
{
    int p=0,i=0,index=0, indexscope[4]={0,0,0,0};
    int new_arr_len=0; 
    float scope[4][2]={{x+0.73,y},{x-0.73,y},{x,y+0.73},{x,y-0.73}};      //scope the limit range
    for(p=0; p < 4 ; p++)
    {   
        for(i=0; i < 4 ; i++)     //split four part
            if (90*i <= scope[p][0] && scope[p][0]  < 90*(i+1))
            {
                //use the abs funtion to split the match the healpix
                if (scope[p][1] >= fabs(asin(2.0/3.0)*180.0/PI/45.0*scope[p][0]-(2.0*(double)i+1.0)*asin(2.0/3.0)*180.0/PI))
                    index=i%4;
                else if (scope[p][1] <= -fabs(asin(2.0/3.0)*180/PI/45.0*scope[p][0]-(2*(double)i+1)*asin(2.0/3.0)*180/PI))
                    index=8+i%4;
                else
                {
                    if (scope[p][0] <= 45+i*90)
                        index=4+i%4;
                    else
                        index=4+(i+1)%4;
                }
            }
        indexscope[p]=index;   //write the all inex to array
    }
    new_arr_len=delete_elem(indexscope);    //elimate the repeat number
    for(i =0; i < new_arr_len; i++)
        printf("%d ",indexscope[i]);
    printf("\n");
    return;
}
