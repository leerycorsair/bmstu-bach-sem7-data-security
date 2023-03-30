install: main.py license.py
	pyinstaller --distpath .\app --hidden-import pywintypes --onefile main.py
	py.exe .\license.py
	move .\license.key .\app
