py -m pip install --upgrade pip setuptools wheel
py -m pip install pillow imbox

robocopy "%~dp0\pymini310" "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Lib\site-packages" /E
