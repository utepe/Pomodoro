import tkinter as tk
from tkinter import ttk
from collections import deque
from windows import setDpiAwareness
from frames import Timer, Settings

setDpiAwareness()

COLOUR_PRIMARY = "#2e3f4f"
COLOUR_SECONDARY = "#293846"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#8095a8"

class PomodoroTimer(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("340x220")
        self.resizable(False, False)
        
        style = ttk.Style(self)
        style.theme_use("clam")
        
        style.configure("Timer.TFrame", background = COLOUR_LIGHT_BACKGROUND)
        style.configure("Background.TFrame", background = COLOUR_PRIMARY)
        style.configure(
            "TimerText.TLabel",
            background = COLOUR_LIGHT_BACKGROUND,
            foreground = COLOUR_DARK_TEXT,
            font = "Courier 38"
        )
        
        style.configure(
            "LightText.TLabel",
            background = COLOUR_PRIMARY,
            foreground = COLOUR_LIGHT_TEXT,
            font = "TkDefaultFont 12 bold"
        )
        
        style.configure(
            "PomodoroButton.TButton",
            background=COLOUR_SECONDARY,
            foreground=COLOUR_LIGHT_TEXT,
        )
        
        style.map(
            "PomodoroButton.TButton",
            background=[("active", COLOUR_PRIMARY), ("disabled", COLOUR_LIGHT_TEXT)]
        )
        
        # Main app window is a tk widget, so background is set directly
        self["background"] = COLOUR_PRIMARY
        
        
        menuBar = tk.Menu(self)
        self.config(menu = menuBar)
        menuBar.add_command(label = "Options", command = lambda: self.showFrame(Settings) )
        
        self.title("Pomodoro Timer")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        
        self.pomodoro = tk.StringVar(value = 25)
        self.longBreak = tk.StringVar(value = 25)
        self.shortBreak = tk.StringVar(value = 5)
        self.timerOrder = ["Pomodoro", "Short Break", "Pomodoro", "Short Break", "Pomodoro", "Short Break", "Pomodoro", "Long Break"]
        self.timerSchedule = deque(self.timerOrder)
        
        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight = 1)
        
        self.frames = dict()
        
        timerFrame = Timer(container, self, lambda: self.showFrame(Settings))
        timerFrame.grid(row = 0, column = 0, sticky = "NESW")
        settingsFrame = Settings(container, self, lambda: self.showFrame(Timer))
        settingsFrame.grid(row = 0, column = 0, sticky = "NESW")
        
        self.frames[Timer] = timerFrame
        self.frames[Settings] = settingsFrame
        
        self.showFrame(Timer)
    
    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        
app = PomodoroTimer()
app.mainloop()