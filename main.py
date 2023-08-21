import pyautogui
import pytesseract
from tkinter import Tk,Canvas,Button,Frame,Label,StringVar
import openai


class RegionSelector:
    def __init__(self,root):
        self.canvas=Canvas(root,cursor="cross",bg='grey75')
        self.canvas.pack(fill="both",expand=True)
        self.canvas.bind("<ButtonPress-1>",self.on_button_press)
        self.canvas.bind("<B1-Motion>",self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>",self.on_button_release)

        self.rect=None
        self.start_x=None
        self.start_y=None
        self.selection=None

    def on_button_press(self,event):
        self.start_x=self.canvas.canvasx(event.x)
        self.start_y=self.canvas.canvasy(event.y)

        if not self.rect:
            self.rect=self.canvas.create_rectangle(self.start_x,self.start_y,self.start_x,self.start_y,outline='red',
                                                   width=2)

    def on_mouse_drag(self,event):
        self.canvas.coords(self.rect,self.start_x,self.start_y,self.canvas.canvasx(event.x),
                           self.canvas.canvasy(event.y))

    def on_button_release(self,event):
        self.selection=(
        self.start_x,self.start_y,self.canvas.canvasx(event.x)-self.start_x,self.canvas.canvasy(event.y)-self.start_y)
        self.canvas.quit()


def get_region():
    root=Tk()
    root.attributes('-fullscreen',True)
    root.wait_visibility(root)
    root.wm_attributes('-alpha',0.3)

    selector=RegionSelector(root)
    root.mainloop()

    root.destroy()
    return selector.selection


def query_chatgpt(text):
    openai.api_key = 'API'  # Ключик от бота
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}]
    }

    response = openai.ChatCompletion.create(**payload)
    return response['choices'][0]['message']['content']


def take_screenshot():
    response_var.set('')  # Очистка переменной перед новым запросом
    region=get_region()

    # Если пользователь закрыл окно выбора региона без выбора области, то выходим из функции
    if not region:
        return

    screenshot=pyautogui.screenshot(region=region)
    text=pytesseract.image_to_string(screenshot,lang='eng+rus')

    response=query_chatgpt(text)
    response_var.set(response)


def main():
    global response_var

    root=Tk()
    root.title("ScreenCHAT 1.0")

    frame=Frame(root,padx=20,pady=20)
    frame.pack(padx=50,pady=50)

    btn=Button(frame,text="Сделать скриншот",command=take_screenshot)
    btn.pack(pady=10)

    response_var=StringVar(root)
    response_label=Label(frame,textvariable=response_var,wraplength=500,justify="left")
    response_label.pack(pady=10)

    root.mainloop()


# Укажите путь к tesseract.exe на вашем компьютере
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

main()