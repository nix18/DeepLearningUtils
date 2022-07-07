@echo off
for /r %%i in (*.eps) do (
gswin64 -dBATCH -dNOPAUSE -q   -sOutputFile=%%i.jpg -sDEVICE=jpeg -dJPEGQ=60 -r300x300 -dEPSCrop %%i

magick %%i.jpg eps2:%%i
)
pause