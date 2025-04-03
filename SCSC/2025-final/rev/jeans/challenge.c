#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "elk.h"
#include "scripts.h"

jsval_t chr(struct js *js, jsval_t *args, int nargs)
{
    if (nargs != 1)
    {
        return js_mkerr(js, "1 arg expected");
    }
    double a = js_getnum(args[0]);
    result[result_idx++] = (char)a;
    return js_mknum(1);
}

jsval_t flag(struct js *js, jsval_t *args, int nargs)
{
    if (nargs != 0)
    {
        return js_mkerr(js, "0 arg expected");
    }
    printf("Flag: %s\n", result);
    return js_mknum(1);
}

int main()
{
    char mem[0x1000];
    struct js *js = js_create(mem, sizeof(mem));
    js_set(js, js_glob(js), "chr", js_mkfun(chr));
    js_set(js, js_glob(js), "flag", js_mkfun(flag));
    for (size_t i = 0; i < sizeof(functable) / sizeof(functable[0]); i++)
    {
#ifdef DEBUG
        printf("init %s()\n", functable[i].name);
#endif
        js_set(js, js_glob(js), functable[i].name, js_mkfun(functable[i].func));
    }

    jsval_t result;
    while (1)
    {
#ifdef DEBUG
        for (size_t i = 0; i < sizeof(scripts) / sizeof(scripts[0]); i++)
        {
            printf("scripts[%ld] = %s\n", i, scripts[i]);
        }
#endif

        printf("Choice: ");
        int choice = 0;
        if (scanf("%d", &choice) != 1)
        {
            printf("Goodbye!\n");
            break;
        }

        if (choice < 0 || choice >= sizeof(scripts) / sizeof(scripts[0]))
        {
#ifdef DEBUG
            printf("Invalid choice\n");
#endif
            printf("Goodbye!\n");
            break;
        }

        char temp[sizeof(scripts[0])];
        memcpy(temp, scripts[choice], sizeof(temp));
#ifdef DEBUG
        printf("Executing: \"%s\"\n", temp);
#endif
        result = js_eval(js, temp, ~0U); // Call sum
        if (js_type(result) == 6)
        {
#ifdef DEBUG
            printf("JS error\n");
            printf("result: %s\n", js_str(js, result));
#endif
            printf("Goodbye!\n");
            break;
        }
#ifdef DEBUG
        for (size_t i = 0; i < sizeof(scripts) / sizeof(scripts[0]); i++)
        {
            printf("scripts[%ld] = %s\n", i, scripts[i]);
        }
#endif
    }

    return 0;
}
