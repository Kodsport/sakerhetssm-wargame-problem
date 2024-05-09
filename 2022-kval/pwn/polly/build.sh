#!/bin/bash
echo '#define FLAG "SSM{polly_gillar_kakor}"' > flag.h
gcc -o container/papegoja papegoja.c flag.h
echo '#define FLAG "SSM{fake_flag}"' > flag.h
gcc -o papegoja papegoja.c flag.h
rm flag.h
