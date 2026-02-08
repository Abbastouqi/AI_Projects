from datetime import datetime, timedelta
from typing import List, Dict
import random

class InterviewScheduler:
    """Handle interview scheduling logic."""
    
    def suggest_time_slots(self, num_slots: int = 5) -> List[Dict[str, str]]:
        """Generate available time slots for the next week."""
        slots = []
        start_date = datetime.now() + timedelta(days=1)
        
        for i in range(num_slots):
            # Randomly pick a day within next 7 days
            day_offset = random.randint(0, 6)
            current_date = start_date + timedelta(days=day_offset)
            
            # Randomly pick a time between 9 AM and 4 PM
            hour = random.randint(9, 16)
            
            slots.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "time": f"{hour:02d}:00"
            })
            
        # Sort slots
        slots.sort(key=lambda x: (x['date'], x['time']))
        return slots

    def schedule_interview(self, candidate_id: int, date: str, time: str, 
                         interviewer_email: str, candidate_email: str) -> Dict:
        """Schedule an interview."""
        # In a real app, this would integrate with Google Calendar/Outlook
        meeting_link = f"https://meet.google.com/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))}"
        
        return {
            "success": True,
            "message": "Interview scheduled successfully",
            "meeting_link": meeting_link
        }