#include <stdio.h>

// PDFium public API
extern void FPDF_InitLibrary(void);
extern void FPDF_DestroyLibrary(void);
extern int FPDF_GetLastError(void);

int main(void) {
    printf("Initializing PDFium... ");
    FPDF_InitLibrary();
    printf("OK\n");

    printf("FPDF_GetLastError() = %d\n", FPDF_GetLastError());

    printf("Destroying PDFium... ");
    FPDF_DestroyLibrary();
    printf("OK\n");

    printf("PDFium static library is valid.\n");
    return 0;
}
