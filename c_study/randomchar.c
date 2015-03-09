#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int s_len;
int s_len_1;
int s_len_2;
char *result;
char string[]="0123456789#";

int main(){
    s_len = strlen(string);
    s_len_1 = s_len - 1;
    s_len_2 = s_len - 2;
    result = malloc(strlen(string)-1);

    randomChar(0);

    return 0;
}
 
int randomChar(int l_s_len){
    int i = l_s_len + 1;
    char c;
 
    if(l_s_len==s_len_1){
        printf("%s\n", result);
        return 0;
    }
 
    while(i < s_len){
        result[l_s_len] = string[l_s_len];
        randomChar(l_s_len + 1);
        c = string[l_s_len];
        string[l_s_len] = string[i];
        string[i] = c;
        i++;
    }
 
    for(l_s_len;l_s_len<s_len_2;l_s_len++){
            string[l_s_len]=string[l_s_len+1];
    }
 
    string[l_s_len] = c;
 
    return 0;
}
