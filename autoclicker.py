# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:11:32 2017

@author: Ant443
"""

def autoClicker():

    import pyHook, threading, time
    import tkinter as tk    
    import pyautogui
    
    def changeButtonAppearance(Appearance, button):
        button.config(relief=getattr(tk, Appearance))
        
    def changeButtonState(state, *buttons):
        for button in buttons:
            button.config(state=getattr(tk, state))
            
    def setButtonText(text, button):
        button.config(wraplength=50, text=text)     
        
    def twoButtonGui():            
        """functions run by callbacks in createButtons"""
        
        def displayCountDown(seconds, button):
            for i in range(seconds,0,-1):
                setButtonText("clicking in: " + str(i) + "s", button)
                root.update()
                time.sleep(1)
                
        def runautoClickInNewThread():
            nonlocal clicking
            clicking = 1
            threading.Thread(target=autoClick, 
                                  args=(startButton, quitButton), 
                                  name="clicks").start()
            
        def runStartButtonTasks():
            nonlocal clicking
            changeButtonAppearance("SUNKEN", startButton)
            changeButtonState("DISABLED", startButton, quitButton)
            displayCountDown(2, startButton)
            setButtonText("press z to stop clicks", startButton)
            hm.HookKeyboard() # "Begin watching for keyboard events."
            runautoClickInNewThread()
                          
        def createButtons():
            """Make two buttons and assign a callback for each"""
            startButton = tk.Button(root, text="Start", 
                                    command=runStartButtonTasks,
                                    height=10, width=20)
            startButton.grid(row=1, column=0)
            quitButton = tk.Button(root, text="Quit", 
                                   command=root.destroy, 
                                   height=10, width=20)
            quitButton.grid(row=1, column=1)
            return (startButton, quitButton)
        
        startButton, quitButton = createButtons()
    
    def autoClick(startButton, quitButton):
        
        def runStopClickingTasks():
            changeButtonAppearance("RAISED", startButton)
            changeButtonState("NORMAL", startButton, quitButton)
            setButtonText("Start", startButton)
            
        while clicking:
            pyautogui.click(clicks=17, interval=0.06, button='right')
        runStopClickingTasks()
        
    def OnKeyboardEvent(event):
        """A key was pressed"""
        nonlocal clicking
        if event.Key == "Z":
            hm.UnhookKeyboard()
            clicking = 0
            return False
        return True
    
    pyautogui.FAILSAFE = False
    clicking = 0
    root = tk.Tk() # create an ordinary window
    hm = pyHook.HookManager() # allows capture of events in windows hookchain
    hm.KeyDown = OnKeyboardEvent
    twoButtonGui()
    root.mainloop()
    
autoClicker()



