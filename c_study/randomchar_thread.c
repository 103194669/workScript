#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

int s_len;
int s_len_1;
int s_len_2;

void *createthread(void *string){
    char s[s_len];
    char *result;
    printf(" create  %s\n", string);
    strcpy(s, string);
    result = malloc(s_len_1);
    randomChar(s, result, s_len);
}


int main(){
    char *result;
    char string[]="0123456789a";
    char c;
    int i;
    s_len = strlen(string);
    s_len_1 = s_len - 1;
    s_len_2 = s_len - 2;

    pthread_t t[s_len];
    memset(&t, 0, sizeof(t));
    for(i=0;i<s_len;i++){
        printf("main %s\n", string);
        pthread_create(&t[i], NULL, createthread, string);
        c = string[s_len-1];
        string[s_len-1] = string[i];
        string[i] = c;
        printf("main after: %s\n", string);
    }

    for(i=0;i<s_len;i++){
        pthread_join(t[i], NULL);
    }
    return 0;
}

int randomChar(char *s, char *r, int l_s_len){
    int i = 1;
    char c;
    if(l_s_len==1){
        printf("%s\n", r);
        return 0;
    }
    while(i < l_s_len){
        r[s_len - l_s_len] = s[0];
        randomChar(&s[1], r, l_s_len-1);
        c = s[0];
        s[0] = s[i];
        s[i] = c;
        i++;
    }
    for(i=0;i<l_s_len-2;i++){
            s[i]=s[i+1];
    }
    s[i] = c;
    return 0;
}
