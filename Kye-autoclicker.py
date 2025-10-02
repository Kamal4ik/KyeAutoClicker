import customtkinter
import threading
import time
import random
import ctypes
from pynput import keyboard, mouse
from tkinter import messagebox
import tkinter as tk

# Constants for Windows API mouse events
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

# Localization dictionaries
LOCALIZATION = {
    'en': {
        'title': 'Advanced Auto-Clicker with Waiting Mode',
        'status_title': 'Auto-Clicker Status',
        'waiting_mode': 'Waiting Mode',
        'waiting_on': 'Waiting Mode: ON (press G to disable)',
        'waiting_off': 'Waiting Mode: OFF (press G)',
        'lmb': 'LMB',
        'rmb': 'RMB',
        'lmb_full': 'Left Mouse Button (LMB)',
        'rmb_full': 'Right Mouse Button (RMB)',
        'min_cps': 'Min CPS:',
        'max_cps': 'Max CPS:',
        'disable_click': 'Disable click activation',
        'start': 'Start',
        'stop': 'Stop',
        'stopped': 'Stopped. Click {button} to activate.',
        'running': 'Running... Click {button} to stop.',
        'status_control': 'Status Window Control:',
        'show_status': 'Show Status',
        'hide_status': 'Hide Status',
        'instructions': (
            "Instructions:\n"
            "1. Press G to enable/disable waiting mode\n"
            "2. In waiting mode, click LMB or RMB to start auto-clicker\n"
            "3. Click again or disable waiting mode to stop auto-clicker\n"
            "4. Check 'Disable click activation' to prevent starting/stopping\n"
            "   auto-clicker with corresponding button in waiting mode.\n"
            "5. The program distinguishes your clicks from automatic ones\n"
            "6. Status window is displayed on top of all applications"
        ),
        'language': 'Language:',
        'error_cps': 'CPS Error',
        'error_cps_msg': '{button}: Min CPS must be greater than 0 and less than or equal to Max CPS.',
        'error_value': 'Value Error',
        'error_value_msg': '{button}: CPS values must be numbers.',
        'waiting_mode_warning': 'Waiting Mode',
        'waiting_mode_msg': 'Enable waiting mode (press G) before starting {button}',
        'error_cps_thread': '{button}: CPS Error! Min > 0 and Min <= Max.',
        'error_value_thread': '{button}: CPS value error!',
        'enabled': 'ENABLED',
        'disabled': 'DISABLED',
        'active': 'Active',
        'off': 'Off'
    },
    'ru': {
        'title': 'Продвинутый Автокликер с режимом ожидания',
        'status_title': 'Статус автокликера',
        'waiting_mode': 'Режим ожидания',
        'waiting_on': 'Режим ожидания: ВКЛЮЧЕН (нажмите G для выключения)',
        'waiting_off': 'Режим ожидания: ВЫКЛЮЧЕН (нажмите G)',
        'lmb': 'ЛКМ',
        'rmb': 'ПКМ',
        'lmb_full': 'Левая кнопка мыши (ЛКМ)',
        'rmb_full': 'Правая кнопка мыши (ПКМ)',
        'min_cps': 'Min CPS:',
        'max_cps': 'Max CPS:',
        'disable_click': 'Отключить активацию по клику',
        'start': 'Старт',
        'stop': 'Стоп',
        'stopped': 'Остановлен. Кликните {button} для активации.',
        'running': 'Работает... Кликните {button} для остановки.',
        'status_control': 'Управление окном статуса:',
        'show_status': 'Показать статус',
        'hide_status': 'Скрыть статус',
        'instructions': (
            "Инструкция:\n"
            "1. Нажмите G для включения/выключения режима ожидания\n"
            "2. В режиме ожидания кликните ЛКМ или ПКМ для запуска автокликера\n"
            "3. Повторный клик или выключение режима ожидания остановит автокликер\n"
            "4. Отметьте чекбокс 'Отключить активацию по клику', чтобы предотвратить запуск/остановку\n"
            "   автокликера соответствующей кнопкой в режиме ожидания.\n"
            "5. Программа отличает ваши клики от автоматических\n"
            "6. Окно статуса отображается поверх всех приложений"
        ),
        'language': 'Язык:',
        'error_cps': 'Ошибка CPS',
        'error_cps_msg': '{button}: Min CPS должен быть больше 0 и меньше или равен Max CPS.',
        'error_value': 'Ошибка значения',
        'error_value_msg': '{button}: Значения CPS должны быть числами.',
        'waiting_mode_warning': 'Режим ожидания',
        'waiting_mode_msg': 'Включите режим ожидания (нажмите G) перед запуском {button}',
        'error_cps_thread': '{button}: Ошибка CPS! Min > 0 и Min <= Max.',
        'error_value_thread': '{button}: Ошибка значения CPS!',
        'enabled': 'ВКЛЮЧЕН',
        'disabled': 'ВЫКЛЮЧЕН',
        'active': 'Активен',
        'off': 'Выключен'
    }
}

class StatusWindow:
    """
    Separate window to display program status on top of all windows.
    """
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = tk.Toplevel()
        self.window.geometry("250x130")
        self.window.resizable(False, False)
        
        self.window.attributes("-topmost", True)
        self.window.attributes("-toolwindow", True)
        self.window.geometry("+{}+{}".format(
            self.window.winfo_screenwidth() - 270, 
            20
        ))
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_status()
    
    def setup_ui(self):
        """Creates the status window UI."""
        main_frame = tk.Frame(self.window, bg="#212121")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.title_label = tk.Label(
            main_frame, 
            font=("Arial", 12, "bold"),
            bg="#212121",
            fg="white"
        )
        self.title_label.pack(pady=(0, 10))
        
        self.waiting_status_label = tk.Label(
            main_frame,
            font=("Arial", 10),
            bg="#212121",
            fg="red"
        )
        self.waiting_status_label.pack(pady=2)
        
        self.lmb_status_label = tk.Label(
            main_frame,
            font=("Arial", 9),
            bg="#212121",
            fg="gray"
        )
        self.lmb_status_label.pack(pady=1)
        
        self.rmb_status_label = tk.Label(
            main_frame,
            font=("Arial", 9),
            bg="#212121",
            fg="gray"
        )
        self.rmb_status_label.pack(pady=1)
        
        self.update_texts()
    
    def update_texts(self):
        """Updates texts in the status window."""
        lang = self.parent_app.current_language
        loc = LOCALIZATION[lang]
        
        self.window.title(loc['status_title'])
        self.title_label.config(text=loc['status_title'])
    
    def update_status(self):
        """Updates the status in the window."""
        try:
            lang = self.parent_app.current_language
            loc = LOCALIZATION[lang]
            
            if self.parent_app.waiting_mode:
                self.waiting_status_label.config(
                    text=f"{loc['waiting_mode']}: {loc['enabled']}",
                    fg="lightgreen"
                )
            else:
                self.waiting_status_label.config(
                    text=f"{loc['waiting_mode']}: {loc['disabled']}",
                    fg="red"
                )
            
            if self.parent_app.lmb_active:
                self.lmb_status_label.config(
                    text=f"{loc['lmb']}: {loc['active']}",
                    fg="lightgreen"
                )
            else:
                self.lmb_status_label.config(
                    text=f"{loc['lmb']}: {loc['off']}",
                    fg="gray"
                )
            
            if self.parent_app.rmb_active:
                self.rmb_status_label.config(
                    text=f"{loc['rmb']}: {loc['active']}",
                    fg="lightgreen"
                )
            else:
                self.rmb_status_label.config(
                    text=f"{loc['rmb']}: {loc['off']}",
                    fg="gray"
                )
            
            self.window.after(200, self.update_status)
            
        except tk.TclError:
            pass
    
    def on_closing(self):
        """Handler for closing the status window."""
        self.window.withdraw()
    
    def show(self):
        """Shows the status window."""
        self.window.deiconify()
        self.window.attributes("-topmost", True)
    
    def hide(self):
        """Hides the status window."""
        self.window.withdraw()
    
    def destroy(self):
        """Destroys the status window."""
        try:
            self.window.destroy()
        except:
            pass

class ClickerThread(threading.Thread):
    """
    Thread for performing mouse clicks.
    """
    def __init__(self, button_type, min_cps_var, max_cps_var, status_var, app_ref, is_active_flag_getter):
        super().__init__()
        self.button_type = button_type
        self.min_cps_var = min_cps_var
        self.max_cps_var = max_cps_var
        self.status_var = status_var
        self.app_ref = app_ref
        self.is_active_flag_getter = is_active_flag_getter
        self.daemon = True

    def _click_mouse(self):
        """Performs a mouse click using Windows API."""
        self.app_ref.program_click_flag = True
        
        if self.button_type == 'left':
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif self.button_type == 'right':
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        
        time.sleep(0.005)
        self.app_ref.program_click_flag = False

    def run(self):
        """Main loop of the clicker thread."""
        lang = self.app_ref.current_language
        loc = LOCALIZATION[lang]
        button_name = loc['lmb'] if self.button_type == 'left' else loc['rmb']
        
        try:
            min_cps = float(self.min_cps_var.get())
            max_cps = float(self.max_cps_var.get())

            if not (0 < min_cps and min_cps <= max_cps):
                self.app_ref.after(0, lambda: self.status_var.set(loc['error_cps_thread'].format(button=button_name)))
                self.app_ref.after(0, self.app_ref.stop_clicker_by_type, self.button_type)
                return
        except ValueError:
            self.app_ref.after(0, lambda: self.status_var.set(loc['error_value_thread'].format(button=button_name)))
            self.app_ref.after(0, self.app_ref.stop_clicker_by_type, self.button_type)
            return
        except Exception as e:
            print(f"Ошибка инициализации в потоке кликера ({self.button_type}): {e}")
            self.app_ref.after(0, lambda: self.status_var.set(f"{button_name}: Error {e}"))
            self.app_ref.after(0, self.app_ref.stop_clicker_by_type, self.button_type)
            return

        while self.is_active_flag_getter():
            if not self.app_ref.waiting_mode:
                self.app_ref.after(0, self.app_ref.stop_clicker_by_type, self.button_type)
                return
                
            current_cps = random.uniform(min_cps, max_cps)
            delay = 1.0 / current_cps
            
            self._click_mouse()
            time.sleep(delay)
        
        print(f"Поток кликера ({self.button_type}) штатно завершается.")


class AutoClickerApp(customtkinter.CTk):
    """
    Main class of the auto-clicker application.
    """
    def __init__(self):
        super().__init__()

        self.current_language = 'en'
        
        self.geometry("650x650")
        self.resizable(False, False)

        self.lmb_active = False
        self.rmb_active = False
        self.waiting_mode = False
        self.program_click_flag = False

        self.lmb_clicker_thread = None
        self.rmb_clicker_thread = None
        self.waiting_mode_listener = None
        self.mouse_listener = None
        
        self.status_window = None

        self.lmb_min_cps_var = customtkinter.StringVar(value="8")
        self.lmb_max_cps_var = customtkinter.StringVar(value="12")
        self.lmb_status_var = customtkinter.StringVar()
        self.lmb_disable_on_click_var = customtkinter.BooleanVar(value=False)
        
        self.rmb_min_cps_var = customtkinter.StringVar(value="7")
        self.rmb_max_cps_var = customtkinter.StringVar(value="11")
        self.rmb_status_var = customtkinter.StringVar()
        self.rmb_disable_on_click_var = customtkinter.BooleanVar(value=False)

        self.waiting_mode_var = customtkinter.StringVar()

        self._setup_ui()
        self._setup_waiting_mode_listener()
        self._setup_mouse_listener()
        self._create_status_window()
        
        self.update_all_texts()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_status_window(self):
        """Creates the status window."""
        self.status_window = StatusWindow(self)

    def change_language(self, lang_code):
        """Changes the interface language."""
        self.current_language = lang_code
        self.update_all_texts()
        if self.status_window:
            self.status_window.update_texts()

    def update_all_texts(self):
        """Updates all texts in the interface."""
        loc = LOCALIZATION[self.current_language]
        
        self.title(loc['title'])
        
        if self.waiting_mode:
            self.waiting_mode_var.set(loc['waiting_on'])
        else:
            self.waiting_mode_var.set(loc['waiting_off'])
        
        self.lmb_title_label.configure(text=loc['lmb_full'])
        self.lmb_min_label.configure(text=loc['min_cps'])
        self.lmb_max_label.configure(text=loc['max_cps'])
        self.lmb_disable_checkbox.configure(text=loc['disable_click'])
        
        if self.lmb_active:
            self.lmb_toggle_button.configure(text=f"{loc['stop']} {loc['lmb']}")
            self.lmb_status_var.set(loc['running'].format(button=loc['lmb']))
        else:
            self.lmb_toggle_button.configure(text=f"{loc['start']} {loc['lmb']}")
            self.lmb_status_var.set(loc['stopped'].format(button=loc['lmb']))
        
        self.rmb_title_label.configure(text=loc['rmb_full'])
        self.rmb_min_label.configure(text=loc['min_cps'])
        self.rmb_max_label.configure(text=loc['max_cps'])
        self.rmb_disable_checkbox.configure(text=loc['disable_click'])
        
        if self.rmb_active:
            self.rmb_toggle_button.configure(text=f"{loc['stop']} {loc['rmb']}")
            self.rmb_status_var.set(loc['running'].format(button=loc['rmb']))
        else:
            self.rmb_toggle_button.configure(text=f"{loc['start']} {loc['rmb']}")
            self.rmb_status_var.set(loc['stopped'].format(button=loc['rmb']))
        
        self.status_control_label.configure(text=loc['status_control'])
        self.show_status_button.configure(text=loc['show_status'])
        self.hide_status_button.configure(text=loc['hide_status'])
        
        self.info_label.configure(text=loc['instructions'])
        
        self.language_label.configure(text=loc['language'])

    def _setup_ui(self):
        """Creates and places UI elements."""
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        lang_frame = customtkinter.CTkFrame(main_frame)
        lang_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        self.language_label = customtkinter.CTkLabel(lang_frame, font=("Arial", 11))
        self.language_label.pack(side="left", padx=(10, 5))
        
        self.lang_en_button = customtkinter.CTkButton(
            lang_frame, 
            text="English", 
            command=lambda: self.change_language('en'),
            width=80,
            height=25
        )
        self.lang_en_button.pack(side="left", padx=2)
        
        self.lang_ru_button = customtkinter.CTkButton(
            lang_frame, 
            text="Русский", 
            command=lambda: self.change_language('ru'),
            width=80,
            height=25
        )
        self.lang_ru_button.pack(side="left", padx=2)

        waiting_frame = customtkinter.CTkFrame(main_frame)
        waiting_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.waiting_status_label = customtkinter.CTkLabel(
            waiting_frame, 
            textvariable=self.waiting_mode_var, 
            font=("Arial", 14, "bold"),
            text_color=("red", "red")
        )
        self.waiting_status_label.pack(pady=15)

        lmb_frame = customtkinter.CTkFrame(main_frame)
        lmb_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.lmb_title_label = customtkinter.CTkLabel(lmb_frame, font=("Arial", 16, "bold"))
        self.lmb_title_label.grid(row=0, column=0, columnspan=3, pady=(0,10))
        
        self.lmb_min_label = customtkinter.CTkLabel(lmb_frame)
        self.lmb_min_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.lmb_min_cps_entry = customtkinter.CTkEntry(lmb_frame, textvariable=self.lmb_min_cps_var, width=60)
        self.lmb_min_cps_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.lmb_max_label = customtkinter.CTkLabel(lmb_frame)
        self.lmb_max_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.lmb_max_cps_entry = customtkinter.CTkEntry(lmb_frame, textvariable=self.lmb_max_cps_var, width=60)
        self.lmb_max_cps_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.lmb_disable_checkbox = customtkinter.CTkCheckBox(
            lmb_frame,
            variable=self.lmb_disable_on_click_var,
            font=("Arial", 10)
        )
        self.lmb_disable_checkbox.grid(row=3, column=0, columnspan=3, pady=(5, 10), sticky="w")

        self.lmb_toggle_button = customtkinter.CTkButton(lmb_frame, command=lambda: self.toggle_clicker('left'), width=150)
        self.lmb_toggle_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.lmb_status_label = customtkinter.CTkLabel(lmb_frame, textvariable=self.lmb_status_var, wraplength=250)
        self.lmb_status_label.grid(row=5, column=0, columnspan=3, pady=5)

        rmb_frame = customtkinter.CTkFrame(main_frame)
        rmb_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.rmb_title_label = customtkinter.CTkLabel(rmb_frame, font=("Arial", 16, "bold"))
        self.rmb_title_label.grid(row=0, column=0, columnspan=3, pady=(0,10))
        
        self.rmb_min_label = customtkinter.CTkLabel(rmb_frame)
        self.rmb_min_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.rmb_min_cps_entry = customtkinter.CTkEntry(rmb_frame, textvariable=self.rmb_min_cps_var, width=60)
        self.rmb_min_cps_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.rmb_max_label = customtkinter.CTkLabel(rmb_frame)
        self.rmb_max_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.rmb_max_cps_entry = customtkinter.CTkEntry(rmb_frame, textvariable=self.rmb_max_cps_var, width=60)
        self.rmb_max_cps_entry.grid(row=2, column=1, padx=5, pady=5)

        self.rmb_disable_checkbox = customtkinter.CTkCheckBox(
            rmb_frame,
            variable=self.rmb_disable_on_click_var,
            font=("Arial", 10)
        )
        self.rmb_disable_checkbox.grid(row=3, column=0, columnspan=3, pady=(5, 10), sticky="w")

        self.rmb_toggle_button = customtkinter.CTkButton(rmb_frame, command=lambda: self.toggle_clicker('right'), width=150)
        self.rmb_toggle_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.rmb_status_label = customtkinter.CTkLabel(rmb_frame, textvariable=self.rmb_status_var, wraplength=250)
        self.rmb_status_label.grid(row=5, column=0, columnspan=3, pady=5)

        status_control_frame = customtkinter.CTkFrame(main_frame)
        status_control_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.status_control_label = customtkinter.CTkLabel(status_control_frame, font=("Arial", 12, "bold"))
        self.status_control_label.pack(pady=(10,5))
        
        buttons_frame = customtkinter.CTkFrame(status_control_frame)
        buttons_frame.pack(pady=5)
        
        self.show_status_button = customtkinter.CTkButton(
            buttons_frame, 
            command=self.show_status_window,
            width=120
        )
        self.show_status_button.pack(side="left", padx=5)
        
        self.hide_status_button = customtkinter.CTkButton(
            buttons_frame, 
            command=self.hide_status_window,
            width=120
        )
        self.hide_status_button.pack(side="left", padx=5)

        self.info_label = customtkinter.CTkLabel(main_frame, justify="left", font=("Arial", 11))
        self.info_label.grid(row=4, column=0, columnspan=2, pady=(15,0), padx=10, sticky="w")

    def show_status_window(self):
        """Shows the status window."""
        if self.status_window:
            self.status_window.show()

    def hide_status_window(self):
        """Hides the status window."""
        if self.status_window:
            self.status_window.hide()

    def _setup_waiting_mode_listener(self):
        """Sets up listener for G key (waiting mode)."""
        try:
            self.waiting_mode_listener = keyboard.GlobalHotKeys({
                'g': self.toggle_waiting_mode
            })
            self.waiting_mode_listener.start()
        except Exception as e:
            print(f"Ошибка установки слушателя режима ожидания: {e}")

    def _setup_mouse_listener(self):
        """Sets up mouse listener."""
        try:
            self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
            self.mouse_listener.start()
        except Exception as e:
            print(f"Ошибка установки слушателя мыши: {e}")

    def on_mouse_click(self, x, y, button, pressed):
        """Mouse click handler."""
        if not pressed:
            return
            
        if self.program_click_flag:
            return
            
        if self.waiting_mode:
            if button == mouse.Button.left:
                if not self.lmb_disable_on_click_var.get():
                    self.after(0, self.toggle_clicker, 'left')
                else:
                    print("LMB auto-clicker not activated, 'Disable click activation' is enabled.")
            elif button == mouse.Button.right:
                if not self.rmb_disable_on_click_var.get():
                    self.after(0, self.toggle_clicker, 'right')
                else:
                    print("RMB auto-clicker not activated, 'Disable click activation' is enabled.")

    def toggle_waiting_mode(self):
        """Toggles waiting mode."""
        self.waiting_mode = not self.waiting_mode
        
        loc = LOCALIZATION[self.current_language]
        
        if self.waiting_mode:
            self.waiting_mode_var.set(loc['waiting_on'])
            self.waiting_status_label.configure(text_color=("green", "lightgreen"))
        else:
            self.waiting_mode_var.set(loc['waiting_off'])
            self.waiting_status_label.configure(text_color=("red", "red"))
            
            if self.lmb_active:
                self.after(0, self.stop_clicker, 'left')
            if self.rmb_active:
                self.after(0, self.stop_clicker, 'right')

    def toggle_clicker(self, button_type):
        prefix = "l" if button_type == 'left' else "r"
        is_active_attr = f"{prefix}mb_active"
        
        if getattr(self, is_active_attr):
            self.stop_clicker(button_type)
        else:
            # Check waiting mode before starting
            if not self.waiting_mode:
                button_name_rus = "ЛКМ" if button_type == 'left' else "ПКМ"
                messagebox.showwarning("Режим ожидания", f"Включите режим ожидания (нажмите G) перед запуском {button_name_rus}")
                return
            self.start_clicker(button_type)

    def start_clicker(self, button_type):
        prefix = "l" if button_type == 'left' else "r"
        is_active_attr = f"{prefix}mb_active"

        if getattr(self, is_active_attr): 
            return

        min_cps_var_attr = f"{prefix}mb_min_cps_var"
        max_cps_var_attr = f"{prefix}mb_max_cps_var"
        status_var_attr = f"{prefix}mb_status_var"
        clicker_thread_attr = f"{prefix}mb_clicker_thread"
        
        button_name_rus = "ЛКМ" if button_type == 'left' else "ПКМ"
        toggle_button_widget = self.lmb_toggle_button if button_type == 'left' else self.rmb_toggle_button

        try:
            min_cps = float(getattr(self, min_cps_var_attr).get())
            max_cps = float(getattr(self, max_cps_var_attr).get())
            if not (0 < min_cps and min_cps <= max_cps):
                self.show_error("Ошибка CPS", f"{button_name_rus}: Min CPS должен быть больше 0 и меньше или равен Max CPS.")
                return
        except ValueError:
            self.show_error("Ошибка CPS", f"{button_name_rus}: Значения CPS должны быть числами.")
            return

        setattr(self, is_active_attr, True)
        getattr(self, status_var_attr).set(f"{button_name_rus}: Работает... Кликните {button_name_rus} для остановки.")
        toggle_button_widget.configure(text=f"Стоп {button_name_rus}")
        
        thread = ClickerThread(
            button_type=button_type,
            min_cps_var=getattr(self, min_cps_var_attr),
            max_cps_var=getattr(self, max_cps_var_attr),
            status_var=getattr(self, status_var_attr),
            app_ref=self,
            is_active_flag_getter=lambda p=prefix: getattr(self, f"{p}mb_active") 
        )
        setattr(self, clicker_thread_attr, thread)
        thread.start()

    def stop_clicker(self, button_type):
        prefix = "l" if button_type == 'left' else "r"
        is_active_attr = f"{prefix}mb_active"

        if not getattr(self, is_active_attr): 
            return

        status_var_attr = f"{prefix}mb_status_var"
        
        button_name_rus = "ЛКМ" if button_type == 'left' else "ПКМ"
        toggle_button_widget = self.lmb_toggle_button if button_type == 'left' else self.rmb_toggle_button

        setattr(self, is_active_attr, False) 
        
        getattr(self, status_var_attr).set(f"{button_name_rus}: Остановлен. Кликните {button_name_rus} для активации.")
        toggle_button_widget.configure(text=f"Старт {button_name_rus}")

    def stop_clicker_by_type(self, button_type):
        self.stop_clicker(button_type)

    def show_error(self, title, message):
        messagebox.showerror(title, message, parent=self)

    def on_closing(self):
        print("Closing application...")
        self.lmb_active = False
        self.rmb_active = False

        if self.waiting_mode_listener:
            print("Stopping waiting mode listener...")
            self.waiting_mode_listener.stop()
        if self.mouse_listener:
            print("Stopping mouse listener...")
            self.mouse_listener.stop()
        
        if self.status_window:
            print("Closing status window...")
            self.status_window.destroy()
            
        print("Application closed.")
        self.destroy()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System") 
    customtkinter.set_default_color_theme("blue") 
    
    app = AutoClickerApp()
    app.mainloop()