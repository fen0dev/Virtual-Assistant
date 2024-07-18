import platform
import subprocess as sb
from zina import speak

# Open browser function
def open_browser(choice):
    try:
        if platform.system() == "Windows":
            if "chrome" in choice:
                sb.Popen("start chrome", shell=True)
            elif "firefox" in choice:
                sb.Popen("start firefox", shell=True)
            elif "edge" in choice:
                sb.Popen("start edge", shell=True)
            else:
                speak("Sorry, I can only open Chrome, Firefox, or Edge.")
        elif platform.system() == "Darwin":
            if "chrome" in choice:
                sb.Popen(
                    ["open", "-a", "chrome"]
                )
            elif "firefox" in choice:
                sb.Popen(
                    ["open", "-a", "firefox"]
                )
            elif "safari" in choice:
                sb.Popen(
                    ["open", "-a", "safari"]
                )
            else:
                speak("Sorry, I can only open Chrome, Firefox, or Safari.")
        elif platform.system() == "Linux":
            if "chrome" in choice:
                sb.Popen(["google-chrome"])
            elif "firefox" in choice:
                sb.Popen(["firefox"])
            else:
                speak("Sorry, I can only open Chrome or Firefox.")
    except Exception as e:
        speak(f"Failed to open {choice}. Error: {str(e)}")