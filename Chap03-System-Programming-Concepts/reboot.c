/* *
 * Demo program for Linux-specific reboot(2)
 * Note that only the superuser may call reboot()
 * */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/reboot.h>
int main() {
    sync();
    int rc = reboot(RB_AUTOBOOT);
    if(rc == -1) 
        perror("reboot");
    exit(EXIT_FAILURE);
}
