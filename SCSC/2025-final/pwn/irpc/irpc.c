#include <signal.h>
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define SHMEM_ADDR 0x1337000

struct irpc_broadcast{
    long uid;
    long len;
    char broadcast_buf[0xff0];
};

struct irpc_msg{
    int parent;
    int uid;
    size_t msglen;
    char uname[0x70];
    char msg_buf[0xf80];
};

struct sigaction parent_sa;
struct sigaction user_sa;

int pids[0x1c] = {0};
int pid_idx = 0;

struct irpc_msg* parent_msg;
struct irpc_msg* user_msg;

struct irpc_msg* irpc_messages[0x1c];
struct irpc_broadcast* broadcast;


void irpc_broadcast(){
    for(int i = 0; i < sizeof(pids)/4; i++){
        if(pids[i] != 0){
            struct irpc_msg* curr = irpc_messages[i];
            kill(pids[i],curr->uid);
            sleep(0.1);
        }
    }
    return;
}

void irpc_reset(){
    for(int i = 0; i < sizeof(pids)/4; i++){
        if(pids[i] != 0){
            kill(pids[i],SIGKILL);
            sleep(0.1);
        }
    }
    return;
}

void parent_msg_recv(int sig){
    char tmp_buf[0x100];
    printf("sig?    %d\n",sig);
    int uid = (int)broadcast->uid;
    struct irpc_msg* user = irpc_messages[uid];

    printf("Got message from uid %d\n",user->uid);

    if(strcmp(user->msg_buf,"reset")==0){
        irpc_reset();
        exit(0);
    }

    //int tmplen = snprintf(tmp_buf,sizeof(tmp_buf),"\n[%s]: ",user->uname);

    //if((tmplen < user->msglen) && (tmplen + user->msglen) < 0x70){
    if((user->msglen + strlen(user->uname) + strlen("[]: ")) < sizeof(tmp_buf)){
        puts("Short message optimization!");
        // look into this
        int tmplen = snprintf(tmp_buf,sizeof(tmp_buf),"\n[%s]: ",user->uname);
        memcpy(tmp_buf+tmplen,user->msg_buf,user->msglen);
        strcpy(broadcast->broadcast_buf,tmp_buf);
        strcat(broadcast->broadcast_buf,"\n");
    }else{
        memset(broadcast->broadcast_buf,0,sizeof(broadcast));
        snprintf(broadcast->broadcast_buf,sizeof(broadcast->broadcast_buf),"\n[%s]: ",user->uname);
        strncat(broadcast->broadcast_buf,user->msg_buf,sizeof(broadcast->broadcast_buf)-strlen(broadcast->broadcast_buf));
        strcat(broadcast->broadcast_buf,"\n");
    }
    broadcast->len = strlen(broadcast->broadcast_buf);
    irpc_broadcast();

    return;
}

void user_msg_recv(int sig){
    write(1,broadcast->broadcast_buf,broadcast->len);

    return;
}

void set_username(struct irpc_msg* curr){
    printf("%s","Input a username\n> ");
    fgets(curr->uname,sizeof(curr->uname),stdin);
    char* newline = strstr(curr->uname,"\n");
    if(newline != 0){
        *newline = 0;
    }

    return;

}

void send_msg(struct irpc_msg* curr){
    broadcast->uid = (long)(curr->uid-SIGRTMIN-1);
    kill(curr->parent,SIGRTMIN);
    sleep(0.1);

    return;
}


void do_chat(struct irpc_msg* curr){
    int res = 0;
    set_username(curr);
    sigaction(user_msg->uid, &user_sa, NULL);
    
    while(1){
        printf("%s","> ");
        res = read(0,curr->msg_buf,sizeof(curr->msg_buf));

        if(res <= 0){
            continue;
        }
        curr->msglen = res;

        char* newline = strstr(curr->msg_buf,"\n");
        if(newline != 0){
            *newline = 0;
        }

        if(strcmp(curr->msg_buf,"quit") == 0){
            return;
        }

        send_msg(curr);
    }
    return;
}

void irpc_client(int parent_pid, int sockfd, int count){
    int uid = SIGRTMIN + count;
    user_msg = irpc_messages[count-1];
    user_msg->parent = parent_pid;
    user_msg->uid = uid;
    //memset(user_msg->uname,0,sizeof(user_msg->uname));
    //memset(user_msg->msg_buf,0,sizeof(user_msg->msg_buf));

    user_sa.sa_handler = user_msg_recv;

    dup2(sockfd,0);
    dup2(sockfd,1);
    close(sockfd);

    do_chat(user_msg);

    exit(0);
}

void init(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    parent_sa.sa_handler = parent_msg_recv;
    sigaction(SIGRTMIN, &parent_sa, NULL);

    broadcast = mmap((void*)SHMEM_ADDR,sizeof(struct irpc_msg)*0x1d,PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS | MAP_FIXED | MAP_POPULATE,0,0);
    
    return;
}

int main(int argc, char** argv){
    struct sockaddr_in myaddr ,clientaddr;
    int sockid,newsockid;

    if(argc < 2){
        puts("Usage:    ./irpc  <port>");
        exit(1);
    }

    int port = atoi(argv[1]);
    if(port < 0 || port > 0xffff){
        puts("Invalid port number");
        exit(1);
    }

    init();

    sockid=socket(AF_INET,SOCK_STREAM,0);
    memset(&myaddr,'0',sizeof(myaddr));
    myaddr.sin_family=AF_INET;
    myaddr.sin_port=htons(port);
    myaddr.sin_addr.s_addr=inet_addr("0.0.0.0");
    
    if(sockid==-1)
    {
        puts("socket");
        exit(1);
    }

    int len=sizeof(myaddr);
    if(bind(sockid,( struct sockaddr*)&myaddr,len)==-1)
    {
        puts("bind");
        exit(1);
    }

    if(listen(sockid,10)==-1)
    {
        puts("listen");
        exit(1);
    }

    int parent_pid,child_pid,new;
    int counter = 0;

    parent_pid = getpid();

    while(counter < 0x1d){
        new = accept(sockid,(struct sockaddr *)&clientaddr,&len);
        if(new < 0){
            continue;
        }
        counter++;
        irpc_messages[counter-1] = (struct irpc_msg*)&broadcast[counter];

        child_pid = fork();

        if(child_pid == 0){
            irpc_client(parent_pid,new,counter);
        }   
        else{
            printf("New client connected!\nuid: %d\npid:    %d\n",counter,child_pid);
            pids[pid_idx] = child_pid;
            pid_idx++;
            close(new);
        }
    }

    puts("Too many clients connected!");
    close(sockid);
    return 0;
}