import cv2 
import pytesseract
from PIL import ImageGrab
import pyperclip
import time
from pywinauto import application

pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = application.Application()
app.start("Notepad.exe")

recent_value = ''

update_notepad = False

while True:
    try:
        img_grab = ImageGrab.grabclipboard()

        img_grab_repr = repr(img_grab)
        size_index = img_grab_repr.find('size')
        size_index_end = img_grab_repr.find(' ', size_index)
        img_grab_repr = img_grab_repr[:size_index_end]

        if (not img_grab is None) and (img_grab_repr != recent_value):
            
            print('running from image')
            recent_value = img_grab_repr

            img_grab.save('somefile.png','PNG')
            img_grab = cv2.imread('somefile.png')

            # Adding custom options
            custom_config = r'--oem 3 --psm 6'
            result = pytesseract.image_to_string(img_grab, config=custom_config)
            
            update_notepad = True
            
        text_grab = pyperclip.paste()
        
        if (text_grab != '') and (text_grab != recent_value):
            
            print('running from text')
            result = pyperclip.paste()
            recent_value = result
            
            update_notepad = True
            
        if update_notepad == True:
            
            if not app['Notepad']['Edit'].exists():
            
                app.start("Notepad.exe")
            
            app['Notepad']['Edit'].set_edit_text(result)
            
            update_notepad = False
            
    except:
        pass
    time.sleep(0.1)
