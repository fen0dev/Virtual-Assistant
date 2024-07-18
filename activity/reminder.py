from zina import speak, listen

# Set a reminder
def set_reminder():
    speak("What is the reminder?")
    reminder_text = listen()
    if reminder_text:
        speak("When should I remind you? Please specify in minutes.")
        reminder_time = listen()
        if reminder_time.isdigit():
            time = time.sleep(int(reminder_time) * 60)
            speak(f"Reminder: {reminder_text} set for {time}.")
        else:
            speak("Invalid time specified. Please repeat")
            listen()