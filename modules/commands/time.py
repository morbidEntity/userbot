from datetime import datetime

def get_time():
    return f"The current date and time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
