/*************************************************************************\
*                  Copyright (C) Michael Kerrisk, 2010.                   *
*                                                                         *
* This program is free software. You may use, modify, and redistribute it *
* under the terms of the GNU Affero General Public License as published   *
* by the Free Software Foundation, either version 3 or (at your option)   *
* any later version. This program is distributed without any warranty.    *
* See the file COPYING.agpl-v3 for details.                               *
\*************************************************************************/

/* Solution for Exercise 64-2 */
/* script.c
   
   Revised by Liu Jiaming based on the simple version of script(1) in List-
   ing 64-3 

   1) Features newly added 1: Add lines to the beginning and the end of the
      output file showing the time the script started and finished
   2) Add code to handle changes to the terminal window size, and restart
      the select() call if interrupted by SIGWINCH
*/

#include <sys/stat.h>
#include <fcntl.h>
#include <libgen.h>
#include <termios.h>
#include <signal.h>
#if ! defined(__hpux)
/* HP-UX 11 doesn't have this header file */
#include <sys/select.h>
#endif
#include "pty_fork.h"           /* Declaration of ptyFork() */
#include "tty_functions.h"      /* Declaration of ttySetRaw() */
#include "curr_time.h"
#include "tlpi_hdr.h"

#define BUF_SIZE 256
#define MAX_SNAME 1000

struct termios ttyOrig;
struct winsize wsOrig;
int masterFd;

static void             /* Reset terminal mode on program exit */
ttyReset(void)
{
    if (tcsetattr(STDIN_FILENO, TCSANOW, &ttyOrig) == -1)
        errExit("tcsetattr");
}

static void sigwinchHandler(int sig) {
    struct winsize ws;
    if(ioctl(STDIN_FILENO, TIOCGWINSZ, &ws) == -1)
        errExit("ioctl-TIOCGWINSZ");
    if(!(ws.ws_row == wsOrig.ws_row && ws.ws_col == wsOrig.ws_col)) {
        if(ioctl(masterFd, TIOCSWINSZ, &ws) == -1)
            errExit("ioctl-TIOCSWINSZ");
        wsOrig.ws_row = ws.ws_row;
        wsOrig.ws_row = ws.ws_row;
    }
}

int
main(int argc, char *argv[])
{
    char slaveName[MAX_SNAME];
    char *shell;
    int scriptFd;
    fd_set inFds;
    char buf[BUF_SIZE];
    ssize_t numRead;
    pid_t childPid;
    struct sigaction sa;

    /* Retrieve the attributes of terminal on which we are started */

    if (tcgetattr(STDIN_FILENO, &ttyOrig) == -1)
        errExit("tcgetattr");
    if (ioctl(STDIN_FILENO, TIOCGWINSZ, &wsOrig) < 0)
        errExit("ioctl-TIOCGWINSZ");

    /* Add SIGWINCH handler to handle changes to the terminal window size */

    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sa.sa_handler = sigwinchHandler;

    if(sigaction(SIGWINCH, &sa, NULL) == -1)
        errExit("sigaction");

    /* Create a child process, with parent and child connected via a
       pty pair. The child is connected to the pty slave and its terminal
       attributes are set to be the same as those retrieved above. */

    childPid = ptyFork(&masterFd, slaveName, MAX_SNAME, &ttyOrig, &wsOrig);
    if (childPid == -1)
        errExit("ptyFork");

    if (childPid == 0) {        /* Child: execute a shell on pty slave */

        /* If the SHELL variable is set, use its value to determine
           the shell execed in child. Otherwise use /bin/sh. */

        shell = getenv("SHELL");
        if (shell == NULL || *shell == '\0')
            shell = "/bin/sh";

        execlp(shell, shell, (char *) NULL);
        errExit("execlp");      /* If we get here, something went wrong */
    }

    /* Parent: relay data between terminal and pty master */

    scriptFd = open((argc > 1) ? argv[1] : "typescript",
                        O_WRONLY | O_CREAT | O_TRUNC,
                        S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP |
                                S_IROTH | S_IWOTH);
    if (scriptFd == -1)
        errExit("open typescript");
    snprintf(buf, BUF_SIZE, "Script started on %s\n", currTime("%T"));
    if(write(scriptFd, buf, strlen(buf)) != strlen(buf))
        errExit("write (script start)");

    /* Place terminal in raw mode so that we can pass all terminal
     input to the pseudoterminal master untouched */

    ttySetRaw(STDIN_FILENO, &ttyOrig);

    if (atexit(ttyReset) != 0)
        errExit("atexit");

    /* Loop monitoring terminal and pty master for input. If the
       terminal is ready for input, then read some bytes and write
       them to the pty master. If the pty master is ready for input,
       then read some bytes and write them to the terminal. */

    for (;;) {
        FD_ZERO(&inFds);
        FD_SET(STDIN_FILENO, &inFds);
        FD_SET(masterFd, &inFds);

        if (select(masterFd + 1, &inFds, NULL, NULL, NULL) == -1) {
            if(errno == EINTR)
                continue;
            else
                errExit("select");
        }

        if (FD_ISSET(STDIN_FILENO, &inFds)) {   /* stdin --> pty */
            numRead = read(STDIN_FILENO, buf, BUF_SIZE);
            if (numRead <= 0)
                break;
            if (write(masterFd, buf, numRead) != numRead)
                fatal("partial/failed write (masterFd)");
        }

        if (FD_ISSET(masterFd, &inFds)) {      /* pty --> stdout+file */
            numRead = read(masterFd, buf, BUF_SIZE);
            if (numRead <= 0)
                break;
            if (write(STDOUT_FILENO, buf, numRead) != numRead)
                fatal("partial/failed write (STDOUT_FILENO)");
            if (write(scriptFd, buf, numRead) != numRead)
                fatal("partial/failed write (scriptFd)");
        }
    }

    snprintf(buf, BUF_SIZE, "Script done on %s\n", currTime("%T"));
    if(write(scriptFd, buf, strlen(buf)) != strlen(buf))
        errExit("write() (script done)");
    close(scriptFd);

    exit(EXIT_SUCCESS);
}
