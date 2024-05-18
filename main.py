import pytesseract
from googletrans import Translator
from PIL import ImageGrab
import tkinter as tk
import time
from mouse_select import ScreenBoxSelector
import keyboard
import threading as th

translator = Translator()

# Function to get the bounding box of the selected area
def get_bbox():
    print("Drag the mouse to select the area to capture.")
    selector = ScreenBoxSelector()
    bbox = selector.start_selection()
    print(f"Final bounding box: {bbox}")
    return bbox

# Function to perform OCR and translation
def ocr_and_translate(bbox):
    x1, y1, x2, y2 = bbox
    screen = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    text = pytesseract.image_to_string(screen, lang='eng')  # Adjust lang as needed
    print('ori:', text)
    translated = translator.translate(text, src='auto', dest='zh-cn')
    print('trans:', translated.text)
    return translated.text

# Function to display translation
def display_translation(text, x, y):
    root = tk.Tk()
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)

    root.geometry(f"+{x}+{y}")
    label = tk.Label(root, text=text, bg='white', font=('Helvetica', 12))
    label.pack()
    root.after(3000, root.destroy)  # Auto-close after 5 seconds
    root.mainloop()

# Main function
def main():
    bbox = get_bbox()
    trans = False
    hold = False
    ww = None
    while True:
        if keyboard.is_pressed('f8'):
            if not hold: trans = not trans
            hold = True
        else:
            hold = False
        if keyboard.is_pressed('f9'):
            break
        if keyboard.is_pressed('f10'):
            bbox = get_bbox()

        if trans and (ww is None or not ww.is_alive()):
            succ = False
            while not succ:
                try:
                    translation = ocr_and_translate(bbox)
                    succ = True
                except:
                    pass
            x1, y1, x2, y2 = bbox
            ww = th.Thread(target=display_translation, args=(translation, x1, y2 + 20))
            ww.start()
            # display_translation(translation, x1, y2 + 20)
        
        time.sleep(0.1)  # Adjust the interval as needed

if __name__ == "__main__":
    main()
