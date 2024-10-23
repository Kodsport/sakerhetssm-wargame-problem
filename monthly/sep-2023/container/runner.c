#include <linux/version.h>
#include <linux/bpf.h>
#include <linux/unistd.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#define ptrtou64(ptr) ((__u64)(unsigned long)(ptr))

#define strfy(t) #t
#define SSM(flag) strfy(flag)

char *flag = SSM(FLAG);

char log_buf[1024] = { 0 };

/*
    Create a new BPF program, bytecode specified by prog.
    Return value is the filedescriptor to the program
*/
int load_prog(char *prog, size_t instruction_count) {
    union bpf_attr attr = {
        .kern_version   = LINUX_VERSION_CODE,
        .prog_flags     = BPF_F_SLEEPABLE,       // this is relevant
        .prog_type      = BPF_PROG_TYPE_SYSCALL, // and this is relevant
        .insns          = ptrtou64(prog),
        .insn_cnt       = instruction_count,
        .license        = ptrtou64("GPL"),
        .log_buf        = ptrtou64(log_buf),
        .log_size       = sizeof(log_buf),
        .log_level      = 1,
    };

    return syscall(__NR_bpf, BPF_PROG_LOAD, &attr, sizeof(attr));
}

/*
    Run the loaded program at fd once.
*/
int test_prog(int fd) {
    char data_in[0x1000];

    union bpf_attr attr = {
        .test = {
            .prog_fd = fd
        }
    };

    return syscall(__NR_bpf, BPF_PROG_RUN, &attr, sizeof(attr));
}

int main() {
    puts("[Secure eBPF Loader]");
    printf("Flag at: %p\n", flag);
    printf("Enter bytecode: ");
    fflush(stdout);

    char prog[0x1000] = {0};
    int nread = read(0, &prog, sizeof (prog));

    puts("");

    if (nread < 1 || nread % sizeof(struct bpf_insn))
        goto helpful_recommendation;

    int fd = load_prog(prog, nread / sizeof(struct bpf_insn));
    
    if (fd == -1)
        goto helpful_recommendation;

    int res = test_prog(fd);

    if (res) {
        printf("Error: %s\n", strerror(errno));
    }

    puts("Stats output:\n");
    puts(log_buf);
    
    return 0;

helpful_recommendation:
    puts("Please write better bytecode.");
 
    return 1;
}