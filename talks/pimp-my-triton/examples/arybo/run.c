#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>


extern uint64_t __arybo(uint64_t a, uint64_t b);

int main(int argc, char** argv)
{
    uint64_t ret = 0;
    if (argc < 3) {
        printf("usage:\n\t %s <a> <b>\n", argv[0]);
        return -1;
    }

    ret  = __arybo(atol(argv[1]), atol(argv[2]));
    printf("returned: %lu\n", ret);
    return 0;
}
