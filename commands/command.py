from datetime import datetime, timedelta
import re

class ScheduledCommand:
    def __init__(self, command, start_time, interval_minutes) -> None:
        self.command = command
        self.start_time = start_time
        self.interval_minutes = interval_minutes
    
    def start(self):
        self.command()