#include <stdio.h>
#include <string.h>

int flag = 0;

int main(int argc, char **argv) {
	char buf[1024];
    if (argc < 2) return 1;
	strncpy(buf, argv[1], sizeof(buf) - 1);
	printf(buf);
	printf("\n");

    if (flag == 0x13371337) {
        printf("You Win!\n");
    }
	
	return 0;
}
