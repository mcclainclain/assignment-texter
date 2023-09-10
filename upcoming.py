import datetime
import pytz
import apicanvas as can

# Get all upcoming events
events = can.load_json("/users/self/upcoming_events")
assignments = [event for event in events if event['type']
               == 'assignment']  # Get all upcoming assignments
details = []
cdt = pytz.timezone('America/Chicago')  # Get the timezone of the user

for assignment in assignments:
    a = {}
    a['name'] = assignment['title']  # Get the assignment name
    a['course'] = assignment['context_name']  # Get the course name
    a['Due Date'] = datetime.datetime.strptime(
        assignment['assignment']['due_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)  # Get the due date and time
    # Convert the due date and time to the user's timezone
    a['Due Date'] = a['Due Date'].astimezone(
        cdt).strftime("%m/%d/%y, %I:%M %p")
    details.append(a)

# Change name to shortened name (course code)
can.shorten_assign_names(details)


# Create the message to be sent
msg = "You have the following assignments due soon!\n\n"
msg += "Run at: " + datetime.datetime.now().strftime("%m/%d/%y, %I:%M:%S %p") + "\n\n"
for d in details:
    msg += d['name'] + " in " + d['course'] + \
        " is due on " + d['Due Date'] + "\n\n"

can.send_message(msg)
