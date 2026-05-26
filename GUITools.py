def WindowSizer(window, windowWidth, windowHeight):
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth // 2) - (windowWidth // 2)
    y = (screenHeight // 2) - (windowHeight // 2)
    return f"{windowWidth}x{windowHeight}+{x}+{y}"