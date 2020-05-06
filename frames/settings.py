import tkinter as tk
from tkinter import ttk

class Settings(ttk.Frame):
    def __init__(self, parent, controller, showTimer):
        super().__init__(parent)
        
        self["style"] = "Background.TFrame"
        
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)
        
        settingsContainer = ttk.Frame(
            self,
            padding = "30 15 30 15",
            style = "Background.TFrame"
        )
        
        settingsContainer.grid(row = 0, column = 0, sticky = "EW", padx = 10, pady = 10)
        
        settingsContainer.columnconfigure(0, weight = 1)
        settingsContainer.rowconfigure(1, weight = 1)
        
        # settings for Pomodoro Session
        pomodoroLabel = ttk.Label(
            settingsContainer,
            text = "Pomodoro Length: ",
            style = "LightText.TLabel"
        )
        pomodoroLabel.grid(column = 0, row = 0, sticky = "W")
        
        pomodoroInput = tk.Spinbox(
            settingsContainer,
            from_= 0,
            to = 60,
            increment = 1,
            justify = "center",
            textvariable = controller.pomodoro,
            width = 10
        )
        pomodoroInput.grid(column = 1, row = 0, sticky = "EW")
        pomodoroInput.focus()
        
        # settings for Short Break
        shortBreakLabel = ttk.Label(
            settingsContainer,
            text = "Short Break Length: ",
            style = "LightText.TLabel"
        )
        shortBreakLabel.grid(column = 0, row = 1, sticky = "W")
        
        shortBreakInput = tk.Spinbox(
            settingsContainer,
            from_= 0,
            to = 15,
            increment = 1,
            justify = "center",
            textvariable = controller.shortBreak,
            width = 10
        )
        shortBreakInput.grid(column = 1, row = 1, sticky = "EW")
        
        # settings for Long Break
        longBreakLabel = ttk.Label(
            settingsContainer,
            text = "Long Break Length: ",
            style = "LightText.TLabel"
        )
        longBreakLabel.grid(column = 0, row = 2, sticky = "W")
        
        longBreakInput = tk.Spinbox(
            settingsContainer,
            from_= 0,
            to = 60,
            increment = 1,
            justify = "center",
            textvariable = controller.longBreak,
            width = 10
        )
        longBreakInput.grid(column = 1, row = 2, sticky = "EW")
        
        for child in settingsContainer.winfo_children():
           child.grid_configure(padx = 5, pady  = 5)
        
        buttonContainer = ttk.Frame(self, style = "Background.TFrame")
        buttonContainer.grid(sticky = "EW", padx = 10)
        buttonContainer.columnconfigure(0, weight = 1)
        
        timerButton = ttk.Button(
            buttonContainer,
            text = "⮜ Back",
            command = showTimer,
            style = "PomodoroButton.TButton",
            cursor = "hand2")
        timerButton.grid(row = 0, column = 0, sticky = "EW", padx = 2)