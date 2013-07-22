/*
 * Exercise 27-6
 *
 * Suppose that a parent process has established a handler for SIGCHLD and
 * also blocked this signal. Subsequently, one of its children exits, and
 * the parent then does a wait() to collect the child’s status. What happens
 * when the parent unblocks SIGCHLD? Write a program to verify your answer.
 *
 */

#include "tlpi_hdr.h"
#include <signal.h>
#include <errno.h>

void sigchldHandler(int sig) {
    int childPid;
    printf("Handler: Caught SIGCHLD\n");
    childPid = wait(NULL);
    if (childPid > 0)
        printf("Handler: Reaped child %ld\n", (long)childPid);
    else if (childPid == -1 && errno == ECHILD)
        printf("Handler: No children to reap.\n");
    else
        errMsg("waitpid");
}

int
main() {
    pid_t childPid;
    sigset_t blockMask, origMask;
    struct sigaction sa;

    sigemptyset(&blockMask);
    sigaddset(&blockMask, SIGCHLD);
    if(sigprocmask(SIG_BLOCK, &blockMask, &origMask) == -1)
        errExit("sigprocmask - SIG_BLOCK");

    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sa.sa_handler = sigchldHandler;
    sigaction(SIGCHLD, &sa, NULL);

    switch(childPid = fork()) {
        case -1:
            errExit("fork");
        case 0:
            printf("Child [pid=%ld]: exiting...\n", (long)getpid());
            _exit(EXIT_SUCCESS);
        default:
            childPid = wait(NULL);
            if (childPid == -1)
                errExit("waitpid");
            else
                printf("Parent [pid=%ld]: Reaped child %ld.\n",
                    (long)getpid(), (long)childPid);
    }

    if(sigprocmask(SIG_SETMASK, &origMask, NULL) == -1)
        errExit("sigprocmask - SIG_SETMASK");

    /* Waits for sigchldHandler to execute */
    sleep(2);
}
