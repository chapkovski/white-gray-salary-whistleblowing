from shutil import copyfile
from creed.pages import page_sequence
import os.path

for i in page_sequence:
    filetocreate = f'./creed/templates/creed/{i.__name__}.html'
    if not os.path.exists(filetocreate):
        copyfile('./creed/templates/creed/MyPage.html', filetocreate)
    else:
        print(f'File {i.__name__} exist')
