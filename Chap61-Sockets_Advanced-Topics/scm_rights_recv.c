/*************************************************************************\
*                  Copyright (C) Michael Kerrisk, 2010.                   *
*                                                                         *
* This program is free software. You may use, modify, and redistribute it *
* under the terms of the GNU Affero General Public License as published   *
* by the Free Software Foundation, either version 3 or (at your option)   *
* any later version. This program is distributed without any warranty.    *
* See the file COPYING.agpl-v3 for details.                               *
\*************************************************************************/

/* Supplementary program for Chapter 61 */

/* scm_rights_recv.c

   Used in conjunction with scm_rights_send.c to demonstrate passing of
   file descriptors via a UNIX domain socket.

   This program receives N_FDS file descriptors sent to a UNIX domain socket.

   Usage is as shown in the usageErr() call below.

   File descriptors can exchanged over stream or datagram sockets. This
   program uses stream sockets by default; the "-d" command-line option
   specifies that datagram sockets should be used instead.

   This program is Linux-specific.
*/
#include "scm_rights.h"

#define BUF_SIZE 100

int
main(int argc, char *argv[])
{
    struct msghdr msgh;
    struct iovec iov;
    int data, lfd, sfd, fds[N_FDS], opt;
    int *fdptr, i;
    ssize_t nr;
    Boolean useDatagramSocket;
    union {
        struct cmsghdr cmh;
        char   control[CMSG_SPACE(sizeof(fds))];
                        /* Space large enough to hold N_FDS 'int's */
    } control_un;
    struct cmsghdr *cmhp;

    /* Parse command-line arguments */

    useDatagramSocket = FALSE;

    while ((opt = getopt(argc, argv, "d")) != -1) {
        switch (opt) {
        case 'd':
            useDatagramSocket = TRUE;
            break;

        default:
            usageErr("%s [-d]\n"
                     "        -d    use datagram socket\n", argv[0]);
        }
    }

    /* Create socket bound to well-known address */

    if (remove(SOCK_PATH) == -1 && errno != ENOENT)
        errExit("remove-%s", SOCK_PATH);

    if (useDatagramSocket) {
        fprintf(stderr, "Receiving via datagram socket\n");
        sfd = unixBind(SOCK_PATH, SOCK_DGRAM);
        if (sfd == -1)
            errExit("unixBind");

    } else {
        fprintf(stderr, "Receiving via stream socket\n");
        lfd = unixListen(SOCK_PATH, 5);
        if (lfd == -1)
            errExit("unixListen");

        sfd = accept(lfd, NULL, NULL);
        if (sfd == -1)
            errExit("accept");
    }

    /* Set 'control_un' to describe ancillary data that we want to receive */

    control_un.cmh.cmsg_len = CMSG_LEN(N_FDS * sizeof(int));
    control_un.cmh.cmsg_level = SOL_SOCKET;
    control_un.cmh.cmsg_type = SCM_RIGHTS;

    /* Set 'msgh' fields to describe 'control_un' */

    msgh.msg_control = control_un.control;
    msgh.msg_controllen = sizeof(control_un.control);
    fprintf(stderr, "Before recvmsg, msgh.msg_controllen: %ld\n", (long)msgh.msg_controllen);

    /* Set fields of 'msgh' to point to buffer used to receive (real)
       data read by recvmsg() */

    msgh.msg_iov = &iov;
    msgh.msg_iovlen = 1;
    iov.iov_base = &data;
    iov.iov_len = sizeof(int);

    msgh.msg_name = NULL;               /* We don't need address of peer */
    msgh.msg_namelen = 0;

    /* Receive real plus ancillary data */

    nr = recvmsg(sfd, &msgh, 0);
    if (nr == -1)
        errExit("recvmsg");
    fprintf(stderr, "recvmsg() returned %ld\n", (long) nr);
    
    if (nr > 0)
        fprintf(stderr, "Received data = %d\n", data);
    fprintf(stderr, "After recvmsg, msgh.msg_controllen: %ld\n", (long)msgh.msg_controllen);

    /* Get the received file descriptors (which are typically different
       file descriptor numbers than were used in the sending process) */

    cmhp = CMSG_FIRSTHDR(&msgh);
    if (cmhp == NULL || cmhp->cmsg_len != CMSG_LEN(N_FDS * sizeof(int)))
        fatal("bad cmsg header / message length");
    if (cmhp->cmsg_level != SOL_SOCKET)
        fatal("cmsg_level != SOL_SOCKET");
    if (cmhp->cmsg_type != SCM_RIGHTS)
        fatal("cmsg_type != SCM_RIGHTS");

    fdptr = (int *) CMSG_DATA(cmhp);
    memcpy(fds, fdptr, N_FDS * sizeof(int));
    fprintf(stderr, "Received fds:\n    ");
    for (i = 0; i < N_FDS; i++)
        fprintf(stderr, "%d ", fds[i]);
    fprintf(stderr, "\n");

    /* Having obtained the file descriptors, read the files' contents and
       print them on standard output */
    for (i = 0; i < N_FDS; i++) {
        for (;;) {
            char buf[BUF_SIZE];
            ssize_t numRead;

            numRead = read(fds[i], buf, BUF_SIZE);
            if (numRead == -1)
                errExit("read");

            if (numRead == 0)
                break;

            write(STDOUT_FILENO, buf, numRead);
        }
    }

    exit(EXIT_SUCCESS);
}
