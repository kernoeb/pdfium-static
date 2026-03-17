#include <stdio.h>

extern void FPDF_InitLibrary(void);
extern void FPDF_DestroyLibrary(void);

int main(void) {
    printf("Initializing PDFium... ");
    FPDF_InitLibrary();
    printf("OK\n");
    FPDF_DestroyLibrary();
    printf("PDFium static library is valid.\n");
    return 0;
}
