@echo off
cd /d "g:\dumategithub\duan\antlrparser\runtime"
"E:\Program Files\LLVM\bin\clang.exe" -c duan_runtime.c -o duan_runtime.o
echo Compilation completed!