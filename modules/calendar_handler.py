import datetime

class CalendarHandler:
    def __init__(self):
        self.events = []

    def add_event(self, date_str, time_str, description):
        """Adds a new event to the calendar."""
        try:
            event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            event_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            self.events.append({
                "date": date_str,
                "time": time_str,
                "description": description
            })
            return f"Event '{description}' added for {date_str} at {time_str}."
        except ValueError:
            return "Invalid date or time format. Please use YYYY-MM-DD and HH:MM."
        except Exception as e:
            return f"Error adding event: {e}"

    def get_events_for_day(self, date_str):
        """Retrieves events for a specific day."""
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            daily_events = [
                event for event in self.events
                if datetime.datetime.strptime(event["date"], "%Y-%m-%d").date() == target_date
            ]
            if daily_events:
                return f"Events for {date_str}:\n" + "\n".join([f"- {e['time']}: {e['description']}" for e in daily_events])
            else:
                return f"No events found for {date_str}."
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."
        except Exception as e:
            return f"Error retrieving events: {e}"

    def get_upcoming_events(self, days=7):
        """Retrieves upcoming events within a specified number of days."""
        today = datetime.date.today()
        upcoming = []
        for event in self.events:
            event_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= today + datetime.timedelta(days=days):
                upcoming.append(event)
        
        if upcoming:
            upcoming.sort(key=lambda x: (x['date'], x['time']))
            return "Upcoming Events:\n" + "\n".join([f"- {e['date']} {e['time']}: {e['description']}" for e in upcoming])
        else:
            return "No upcoming events found."