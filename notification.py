def notification(msg):
    try:
        from win10toast import ToastNotifier
        import time
        toast = ToastNotifier()
        toast.show_toast("Pomodoro",
                         msg,
                         icon_path = "pomodoro_Vfd_icon.ico",
                         duration = 5,
                         threaded = True)
    except:
        pass