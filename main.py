import time
import kivy
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.textinput import TextInput

import plyer

import threading
from threading import current_thread, Condition
from kivy.config import Config

condition = Condition()

# from kivy.utils import platform
# if kivy.utils.platform == 'android':
#     import android


Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "1924")
Config.write()


class MyLabel(Label):
    pass


Builder.load_string(
    """
<MyLabel>:
    canvas.before:
        Color:
            rgba: 0,0,0,0
        Rectangle:
            pos: self.pos
            size: self.size
"""
)


class ButtonApp(App):
    def build(self):
        self.vibrate_status = False
        self.current_price = None
        self.thr_name = ""
        self.key = False
        self.window = Screen()
        self.label = MyLabel(
            text="-_-_-_-_-_-_-_-_-_-_-", size=(12, 8), pos=(-35, 175), color="yellow"
        )
        self.window.add_widget(self.label)

        # use a (r, g, b, a) tuple
        self.btn = Button(
            text="ON",
            font_size="25sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(2, 2),
            size_hint=(0.2, 0.2),
            pos=(50, 970),
        )
        self.window.add_widget(self.btn)
        # bind() use to bind the button to function callback
        self.btn.bind(on_release=self.callback)

        btnOff = Button(
            text="OFF",
            font_size="25sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(2, 2),
            size_hint=(0.2, 0.2),
            pos=(50, 500),
        )
        self.window.add_widget(btnOff)
        # bind() use to bind the button to function callback
        btnOff.bind(on_release=self.callback_off)

        btnText0 = Button(
            text="  Если карта\n       Ваша",
            font_size="6sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(3, 2),
            size_hint=(0.1, 0.1),
            pos=(315, 500),
        )
        self.window.add_widget(btnText0)
        # bind() use to bind the button to function callback
        btnText0.bind(on_release=self.TextCard0)

        btnText1 = Button(
            text="   Оплатил\nЖду токены",
            font_size="6sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(3, 2),
            size_hint=(0.1, 0.1),
            pos=(435, 500),
        )
        self.window.add_widget(btnText1)
        # bind() use to bind the button to function callback
        btnText1.bind(on_release=self.TextCard1)

        btnText2 = Button(
            text="        Карта\nРодственника",
            font_size="6sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(3, 2),
            size_hint=(0.1, 0.1),
            pos=(555, 500),
        )
        self.window.add_widget(btnText2)
        # bind() use to bind the button to function callback
        btnText2.bind(on_release=self.TextCard2)

        btnExit = Button(
            text="Exit",
            font_size="25sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(2, 2),
            size_hint=(0.2, 0.2),
            pos=(740, 500),
        )
        self.window.add_widget(btnExit)
        # bind() use to bind the button to function callback
        btnExit.bind(on_release=self.ExitCode)

        self.btnVibrate = Button(
            text="Alarm \n OFF",
            font_size="17sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(2, 2),
            size_hint=(0.2, 0.2),
            pos=(740, 970),
        )
        self.window.add_widget(self.btnVibrate)
        # bind() use to bind the button to function callback
        self.btnVibrate.bind(on_release=self.vibrate)

        return self.window

    def TextCard0(self, event):
        text = "Добрый день, если карта ваша (ФИО БИНАНС совпадает с картой) или карта родственника с одинаковой фамилией и дополнительно квитанцию в чат - жду оплату"
        Clipboard.copy(text)

    def TextCard1(self, event):
        text = "Добрый день, оплатил. Жду токены"
        Clipboard.copy(text)

    def TextCard2(self, event):
        text = "Добрый день, оплата с карты родственника(фамилия одинаковая), работаем?"
        Clipboard.copy(text)

    # callback function tells when button pressed
    def callback(self, event):

        if current_thread().name == self.thr_name:
            self.label.color = "yellow"
            self.label.text = f"Thread is running..."
            return False
        else:
            self.thr_name = current_thread().name
        self.key = False
        self.btn.background_color = "green"

        def thr():
            while 1:
                time.sleep(2.25)  # 1,346.01
                if self.key:
                    return False
                price, notify_price = Clipboard.paste(), Clipboard.paste()
                try:
                    if 12 > len(price) > 3:
                        if "," in price or "." in price:
                            price = price.replace(",", "")
                            notify_price = notify_price.replace(",", " ")
                            if price != self.current_price and float(price) >= 1:
                                self.label.color = "green"
                                self.label.text = f"STATUS: [ON]\n{price}"
                                self.current_price = price
                                # print(notify_price, price)
                                plyer.notification.notify(
                                    title="   New Value",
                                    message=f" 👉 {notify_price} $ ",
                                )
                                Clipboard.copy(price)
                                # if self.vibrate_status == True:
                                #     # print('SSSSFFDSF')
                                #     plyer.vibrator.vibrate(time=1)
                        elif price == self.current_price:
                            self.label.color = "yellow"
                            self.label.text = f"STATUS: [ON]\n{price} - same"
                            continue
                        else:
                            self.label.color = "yellow"
                            self.label.text = f"STATUS: [ON]\nPending..."
                            continue
                    else:
                        self.label.color = "red"
                        self.label.text = f"STATUS: [ON]\nWrongValue - Pending..."
                        continue
                except Exception as e:
                    self.label.color = "yellow"
                    self.label.text = f"STATUS: [Error]\n {e}"
                    pass

        threading.Thread(target=thr).start()

    def callback_off(self, event):
        def thr1():
            self.key = True
            self.label.text = "STATUS: [OFF]"
            self.label.color = "red"
            self.btn.background_color = "red"
            time.sleep(0.2)
            self.btn.background_color = (1, 1, 1, 1)
            self.thr_name = ""
            self.current_price = None
            return True

        threading.Thread(target=thr1).start()

    def ExitCode(self, event):
        if threading.active_count() > 1:
            self.callback_off(self)
        # time.sleep(0.1)
        # quit()
        App.get_running_app().stop()

    def vibrate(self, event):
        if self.vibrate_status == True:
            self.btnVibrate.background_color = (1, 1, 1, 1)
            self.btnVibrate.text = 'Alarm OFF'
            self.vibrate_status = False

        else: self.vibrate_status = True
        def vibrate_thr():
            while 1:
                if self.vibrate_status == True:
                    self.btnVibrate.background_color = 'green'
                    self.btnVibrate.text = 'Alarm \nON'
                elif self.vibrate_status == False:
                    return True
                time.sleep(600)
                plyer.notification.notify(
                                title="🔔 Alarm",
                                message=f"📢 Don't forget to check orders ⚠️\n \
                                and take some rest if possible 🙏🏼"
                            )
        vibrate_thr = threading.Thread(target=vibrate_thr, name="vibrate_thr", daemon=True)
        vibrate_thr.start()





if __name__ == "__main__":
    ButtonApp().run()
