set PIP=C:\Python27\pyinstaller\
python %PIP%Makespec.py --onefile --upx --tk -w --icon=gfxblackjack.ico gfxblackjack.py
python %PIP%Build.py gfxblackjack.spec