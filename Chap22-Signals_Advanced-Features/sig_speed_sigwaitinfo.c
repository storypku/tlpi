/*
   Usage: $ time ./sig_speed_sigwaitinfo num-sigs

   The 'num-sigs' argument specifies how many times the parent and
   child send signals to each other.

   Child                                  Parent

   for (s = 0; s < numSigs; s++) {        for (s = 0; s < numSigs; s++) {
       send signal to parent                  wait for signal from child
       wait for a signal from parent          send a signal to child
   }                                      }
*/
#include <signal.h>
#include "tlpi_hdr.h"

#define TESTSIG SIGUSR1

int
main(int argc, char *argv[])
{
    int numSigs, scnt;
    pid_t childPid;
    sigset_t blockedMask;
#ifdef _USE_SIGINFO
    siginfo_t si;
#endif

    if (argc != 2 || strcmp(argv[1], "--help") == 0)
        usageErr("%s num-sigs\n", argv[0]);

    numSigs = getInt(argv[1], GN_GT_0, "num-sigs");

    /* Block the signal before fork(), so that the child doesn't manage
       to send it to the parent before the parent is ready to catch it */

    sigemptyset(&blockedMask);
    sigaddset(&blockedMask, TESTSIG);
    if (sigprocmask(SIG_SETMASK, &blockedMask, NULL) == -1)
        errExit("sigprocmask");

    switch (childPid = fork()) {
    case -1: errExit("fork");

    case 0:     /* child */
        for (scnt = 0; scnt < numSigs; scnt++) {
            if (kill(getppid(), TESTSIG) == -1)
                errExit("kill");
            #ifdef _USE_SIGINFO
                if(sigwaitinfo(&blockedMask, &si) == -1)
            #else
                if(sigwaitinfo(&blockedMask, NULL) == -1)
            #endif
                errExit("sigwaitinfo");
            //if (sigsuspend(&emptyMask) == -1 && errno != EINTR)
            //        errExit("sigsuspend");
        }
        exit(EXIT_SUCCESS);

    default: /* parent */
        for (scnt = 0; scnt < numSigs; scnt++) {
            #ifdef _USE_SIGINFO
                if(sigwaitinfo(&blockedMask, &si) == -1)
            #else
                if(sigwaitinfo(&blockedMask, NULL) == -1)
            #endif
                errExit("sigwaitinfo");
            if (kill(childPid, TESTSIG) == -1)
                errExit("kill");
        }
        exit(EXIT_SUCCESS);
    }
}
