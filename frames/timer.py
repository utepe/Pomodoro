import tkinter as tk
from tkinter import ttk
from collections import deque
import winsound as sound
from notification import notification
from windows import setDpiAwareness

setDpiAwareness()
        
class Timer(ttk.Frame):
    def __init__(self, parent, controller, showSettings):
        super().__init__(parent)
        
        self["style"] = "Background.TFrame"
        
        self.controller = controller
        pomodoroTime = int(controller.pomodoro.get())
        
        self.currentTime = tk.StringVar(value = f"{pomodoroTime:02d}:00")
        
        self.currentTimerLabel = tk.StringVar(value = controller.timerSchedule[0])
        self.timerRunning = False
        self._timerDecrementJob = None
        
        self.skipButton = ttk.Button(
            self,
            text = "Skip",
            command = self.skipSession,
            style = "PomodoroButton.TButton",
            cursor = "hand2"
        )
        self.skipButton.grid(row = 0, column = 1, sticky = "E", padx = 10, pady = (10, 0))
        
        timerDescription = ttk.Label(self, textvariable = self.currentTimerLabel, style = "LightText.TLabel")
        timerDescription.grid(row = 0, column = 0, sticky = "W", padx = (10, 0), pady = (10, 0))
        
        timerFrame = ttk.Frame(self, height = "100", style = "Timer.TFrame")
        timerFrame.grid(row = 1, column = 0, columnspan = 2, pady = (10, 0), sticky = "NESW")
        
        timerCounter = ttk.Label(timerFrame, textvariable = self.currentTime, style = "TimerText.TLabel")
        timerCounter.place(relx = 0.5, rely = 0.5, anchor = "center")
        
        buttonContainer = ttk.Frame(self, padding = 10, style = "Background.TFrame")
        buttonContainer.grid(row = 2, column = 0, columnspan = 2, sticky = "EW")
        buttonContainer.columnconfigure((0, 1, 2), weight = 1)
        
        self.startButton = ttk.Button(buttonContainer,
                                      text = "Start",
                                      command = self.startTimer,
                                      style = "PomodoroButton.TButton",
                                      cursor = "hand2")
        self.startButton.grid(row = 0, column = 0, sticky = "EW")
        
        self.stopButton = ttk.Button(buttonContainer,
                                      text = "Stop",
                                      state = "disabled",
                                      command = self.stopTimer,
                                      style = "PomodoroButton.TButton",
                                      cursor = "hand2")
        self.stopButton.grid(row = 0, column = 1, sticky = "EW", padx = 5)
        
        resetButton = ttk.Button(buttonContainer,
                                 text = "Reset",
                                 command = self.resetTimer,
                                 style = "PomodoroButton.TButton",
                                 cursor = "hand2")
        resetButton.grid(row = 0, column = 2, sticky = "EW")
    
    def startTimer(self):
        self.timerRunning = True
        self.startButton["state"] = "disabled"
        self.stopButton["state"] = "enabled"
        self.skipButton["state"] = "disabled"
        self.decrementTime()
        
    def stopTimer(self):
        self.timerRunning = False
        self.startButton["state"] = "enabled"
        self.stopButton["state"] = "disabled"
        self.skipButton["state"] = "enabled"
        
        if self._timerDecrementJob:
            self.after_cancel(self._timerDecrementJob)    
            self._timerDecrementJob = None
    
    def skipSession(self):
        self.controller.timerSchedule.rotate(-1)
        nextUp = self.controller.timerSchedule[0]
        self.currentTimerLabel.set(nextUp)

        if nextUp == "Pomodoro":
            pomodoroTime = int(self.controller.pomodoro.get())
            self.currentTime.set(f"{pomodoroTime:02d}:00")
        elif nextUp == "Short Break":
            shortBreakTime = int(self.controller.shortBreak.get())
            self.currentTime.set(f"{shortBreakTime:02d}:00")
        elif nextUp == "Long Break":
            longBreakTime = int(self.controller.longBreak.get())
            self.currentTime.set(f"{longBreakTime:02d}:00")
        
    def resetTimer(self):
        self.stopTimer()
        pomodoroTime = int(self.controller.pomodoro.get())
        self.currentTime.set(f"{pomodoroTime:02d}:00")
        self.timerSchedule = deque(self.controller.timerOrder)
        self.currentTimerLabel.set(self.controller.timerSchedule[0])
       
    def decrementTime(self):
        currentTime = self.currentTime.get()
        
        if self.timerRunning and currentTime != "00:00":
            minutes, seconds = currentTime.split(":")

            if int(seconds) > 0:
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else:
                seconds = 59
                minutes = int(minutes) - 1
                
            self.currentTime.set(f"{minutes:02d}:{seconds:02d}")
            self._timerDecrementJob = self.after(1000, self.decrementTime)
            
        elif self.timerRunning and currentTime == "00:00":
            self.controller.timerSchedule.rotate(-1)
            nextUp = self.controller.timerSchedule[0]
            self.currentTimerLabel.set(nextUp)
            
            if nextUp == "Pomodoro":
                notification("Break has ended. Get back to work!")
                pomodoroTime = int(self.controller.pomodoro.get())
                self.currentTime.set(f"{pomodoroTime:02d}:00")
            elif nextUp == "Short Break":
                notification("Focus session has ended. Let's take a Short Break!")
                shortBreakTime = int(self.controller.shortBreak.get())
                self.currentTime.set(f"{shortBreakTime:02d}:00")
            elif nextUp == "Long Break":
                notification("4th Focus session has ended. Time for a Long Break")
                longBreakTime = int(self.controller.longBreak.get())
                self.currentTime.set(f"{longBreakTime:02d}:00")

            sound.Beep(500, 1000)
            self._timerDecrementJob = self.after(1000, self.decrementTime)
