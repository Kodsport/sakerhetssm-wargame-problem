#include <assert.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>

int MAX_LINE = 3e6;
int DEADLINE_US = 800e3;

char* OUTPUT;

void timeout() {
  if (OUTPUT != NULL) {
    write(STDOUT_FILENO, OUTPUT, strlen(OUTPUT) + 1);
  }
  exit(0);
}

void init() {
  setvbuf(stdout, NULL, _IONBF, 0); // Disable output buffering
  setvbuf(stdin, NULL, _IONBF, 0); // Disable input buffering
  signal(SIGALRM, timeout);
}

char* TIMEOUT_MSG = "TIMEOUT\n";

int main() {
  init();
  char* line;
  size_t len;
  puts("Welcome to envdb, the unbloated in-memory database\nCommands:\n\tGET <key>\n\tSET <key>=<var>\n"
      "Commands are separated by newline or semicolon");
  for (;;) {
    if (getline(&line, &len, stdin) == -1) break;
    {
      size_t llen = strlen(line);
      if (line[llen-1] == '\n') line[llen-1] = '\0';
    }
    if (len > MAX_LINE) {
      puts("Too large!");
      exit(0);
    }
    char* cmd = line;
    char* subcmd;
    OUTPUT = TIMEOUT_MSG;
    while ((subcmd = strtok(cmd, ";")) != NULL) {
      {
        struct itimerval deadline = {.it_value = {.tv_usec = DEADLINE_US}};
        setitimer(ITIMER_REAL, &deadline, NULL);
      }
      cmd = NULL;
      if (strncmp(subcmd, "GET ", 4) == 0) {
        OUTPUT = getenv(subcmd + 4);
      } else if (strncmp(subcmd, "SET ", 4) == 0) {
        putenv(subcmd + 4);
      }
    }
    {
        struct itimerval deadline = {0};
        setitimer(ITIMER_REAL, &deadline, NULL);
    }
    if (OUTPUT != NULL && strstr(OUTPUT, "SSM{")) {
      OUTPUT = "<censored>";
    }
    if (OUTPUT != NULL && OUTPUT != TIMEOUT_MSG) {
      puts(OUTPUT);
    }
  }
}
