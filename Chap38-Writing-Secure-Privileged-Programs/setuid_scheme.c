/*
 * A set-user-ID program that demonstrates its typical working flow. 
 *
 * After compiling and linking, the executable should be chowned and
 * chmoded for use.
 * 
 * $ sudo chown root:root ./setuid_scheme
 * $ sudo chmod u+s ./setuid_scheme
 * 
 */
#include "tlpi_hdr.h"
void show_uids(char *msg) {
    uid_t ruid, euid, suid;
    if(getresuid(&ruid, &euid, &suid) == -1)
        errExit("getresuid");
    printf("%s:\n", msg);
    printf("real=%ld   effective=%ld  saved=%ld\n",
            (long)ruid, (long)euid, (long)suid);
}

int main(int argc, char *argv[]) {
    show_uids("Original UIDs");
    FILE * fp = fopen("./abc.txt", "w");
    if(fp == NULL)
        errExit("fopen");
    fputs("Hello\n", fp);
    fclose(fp);

    uid_t orig_euid;
    orig_euid = geteuid();

    if (seteuid(getuid()) == -1)
        errExit("seteuid");
    show_uids("After dropping privileges");

    if (seteuid(orig_euid) == -1)
        errExit("seteuid");
    show_uids("After reacquiring privileges");
    
    if (setuid(getuid()) == -1)
        errExit("setuid");
    show_uids("After permanently drop privileges");
    return 0;
}
