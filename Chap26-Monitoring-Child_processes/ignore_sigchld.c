/*
 * P.560, TLPI
 * 
 * SUSv3 specifies that if the disposition of SIGCHLD is set to SIG_IGN, and the parent has 
 * no terminated children that have been transformed into zombies and have not yet been
 * waited for, then a call to wait() (or watipid()) should block until all of the parent's
 * children have terminated, at which point the call should terminate with the error ECHILD.
 *
 */
#include "tlpi_hdr.h"
#include <signal.h>
int main(int argc, char *argv[]) {

    #ifndef _UNWAITED_ZOMBIE
    if(signal(SIGCHLD, SIG_IGN) == SIG_ERR)
        errExit("signal");
    #endif
    pid_t childPid;
    int status;
    switch(fork()) {
        case -1:
            errExit("fork");
        case 0:
            printf("[Child  pid=%ld] existing\n", (long)getpid());
            _exit(EXIT_SUCCESS);
        default:
            #ifdef _UNWAITED_ZOMBIE /* Parent process sleeps to wait for the child
                                       terminating and becoming a zombie */
            sleep(3);
            if(signal(SIGCHLD, SIG_IGN) == SIG_ERR)
                errExit("signal");
            #endif
            childPid = wait(&status);
            if(childPid > 0)
                printf("[Parent pid=%ld] reaped child %ld with status: %d\n",\
                        (long)getpid(), (long)childPid, status);
            else if(childPid == -1 && errno == ECHILD)
                printf("[Parent pid=%ld] blocked in wait() till ECHILD.\n", (long)getpid());
            else
                errExit("wait");
            exit(EXIT_SUCCESS);
    }
}
