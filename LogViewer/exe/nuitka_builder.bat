cd E:\modules\LogViewer\LogViewer\source
rem python -m nuitka --follow-imports --standalone -output-dir=E:\modules\LogViewer\exe --remove-output main.py
python -m nuitka --follow-imports --standalone --plugin-enable=numpy --plugin-enable=wx --remove-output main.py
cd E:\modules\LogViewer\LogViewer\exe