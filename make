pipenv shell
pipenv install
pyinstaller semicircles.py
pyinstaller semicircles.py --onefile
chmod +x dist/semicircles
echo ''
echo 'Successfuly builded'