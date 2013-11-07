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

/* scm_rights_send.c

   Used in conjunction with scm_rights_recv.c to demonstrate passing of
   file descriptors via a UNIX domain socket.

   This program sends at most 10 file descriptors to a UNIX domain socket.

   Usage is as shown in the usageErr() call below.

   File descriptors can exchanged over stream or datagram sockets. This
   program uses stream sockets by default; the "-d" command-line option
   specifies that datagram sockets should be used instead.

   This program is Linux-specific.
*/
#include "scm_rights.h"
int
main(int argc, char *argv[])
{
    struct msghdr msgh;
    struct iovec iov;
    int data, sfd, opt, fds[N_FDS];
    int *fdhdr;
    int  i;
    ssize_t ns;
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
            usageErr("%s [-d] file1 file2 file3\n"
                     "        -d    use datagram socket\n", argv[0]);
        }
    }

    if (argc != optind + N_FDS)
        usageErr("%s [-d] file1 file2 file3\n"
                 "        -d    use datagram socket\n", argv[0]);
    for(i=0; i < N_FDS; i++) {
    /* Open the files named on the command line */
        fds[i] = open(argv[optind+i], O_RDONLY);
        if (fds[i] == -1)
            errExit("open");
    }
    /* On Linux, we must transmit at least 1 byte of real data in
       order to send ancillary data */

    msgh.msg_iov = &iov;
    msgh.msg_iovlen = 1;
    iov.iov_base = &data;
    iov.iov_len = sizeof(int);
    data = 12345;

    /* We don't need to specify destination address, because we use
       connect() below */

    msgh.msg_name = NULL;
    msgh.msg_namelen = 0;

    msgh.msg_control = control_un.control;
    msgh.msg_controllen = sizeof(control_un.control);
    printf("msgh.msg_controllen: %ld\n", msgh.msg_controllen);
    fprintf(stderr, "Sending fds:\n"
                    "   ");
    for(i=0; i < N_FDS; i++)
        fprintf(stderr, "%d ", fds[i]);
    fprintf(stderr, "\n");


    /* Set message header to describe ancillary data that we want to send */

    cmhp = CMSG_FIRSTHDR(&msgh);
    cmhp->cmsg_len = CMSG_LEN(N_FDS * sizeof(int));
    printf("cmhp->cmsg_len: %ld\n", (long) cmhp->cmsg_len);
    cmhp->cmsg_level = SOL_SOCKET;
    cmhp->cmsg_type = SCM_RIGHTS;
    fdhdr = (int *) CMSG_DATA(cmhp);
    memcpy(fdhdr, fds, N_FDS * sizeof(int));


    /*
    We could rewrite the preceding lines as:

    control_un.cmh.cmsg_len = CMSG_LEN(N_FDS * sizeof(int));
    control_un.cmh.cmsg_level = SOL_SOCKET;
    control_un.cmh.cmsg_type = SCM_RIGHTS;
    memcpy((int *) CMSG_DATA(CMSG_FIRSTHDR(&msgh)), fds, N_FDS * sizeof(int));
    */

    msgh.msg_controllen = cmhp->cmsg_len;

    /* Do the actual send */

    sfd = unixConnect(SOCK_PATH, useDatagramSocket ? SOCK_DGRAM : SOCK_STREAM);
    if (sfd == -1)
        errExit("unixConnect");

    ns = sendmsg(sfd, &msgh, 0);
    if (ns == -1)
        errExit("sendmsg");

    fprintf(stderr, "sendmsg() returned %ld\n", (long) ns);
    exit(EXIT_SUCCESS);
}
