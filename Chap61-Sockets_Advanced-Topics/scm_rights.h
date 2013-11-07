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

/* scm_rights.h

   Header file used by scm_rights_send.c and scm_rights_recv.c.
*/
#ifndef SCM_RIGHTS_H_
#define SCM_RIGHTS_H_

#include <sys/socket.h>
#include <sys/un.h>
#include <fcntl.h>
#include "unix_sockets.h"       /* Declares our unix*() socket functions */
#include "tlpi_hdr.h"

#define SOCK_PATH "scm_rights"
#define N_FDS 3

#endif
