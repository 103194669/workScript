#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

int s_len;
int s_len_1;
int s_len_2;
char *result;
char string[]="0123456789";

int main(){
    int i;
    char c;
    s_len = strlen(string);
    s_len_1 = s_len - 1;
    s_len_2 = s_len - 2;
    result = malloc(s_len);
    for(i=0; i<s_len;i++){
        result[s_len_1] = string[s_len_1];
        if(fork()==0){
            randomChar(0);
            exit(0);
        }
        c = string[s_len_1];
        string[s_len_1] = string[i];
        string[i] = c;
    }

    for(i=0;i<s_len;i++){
        wait(0);
    }
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
