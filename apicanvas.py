import json
import smtplib
import subprocess
import datetime
from email.mime.text import MIMEText
import config as c

'''
Add relative url to https://canvas.wisc.edu/api/v1 to get a dictionary of the json response. For example, to get the user's information, use /users/self.
'''


def load_json(relative_path):
    command = "curl https://canvas.wisc.edu/api/v1" + relative_path + \
        "/?per_page=20000 -H \"Authorization: Bearer {}\"".format(c.API_KEY)
    response = subprocess.check_output(
        command, stderr=subprocess.DEVNULL, shell=True)
    r = json.loads(response.decode("utf-8"))
    return r


'''
Get's the current courses the user is enrolled in and returns a list of the courses.
'''


def get_curr_courses():
    courses = get_courses()
    current_courses = []  # Get the courses the user is currently enrolled in

    for course in courses:
        if course["id"] == 343528:
            continue
        if 'end_at' in course.keys() and course['end_at'] != None:
            end_at = course['end_at']
        else:
            continue
        # Convert the end date to a datetime object
        end_at = datetime.datetime.strptime(end_at, '%Y-%m-%dT%H:%M:%SZ')
        if end_at > datetime.datetime.now():
            current_courses.append(course)

    return current_courses


'''
Gets the user's courses.
'''


def get_courses():
    return load_json("/courses")


'''
Returns the names of the courses in the courses array.
'''


def get_course_names(courses):
    # Get the names of the courses in the courses list.
    return [course['name'] for course in courses]


'''
shortens current course names to the course code
'''


def shorten_assign_names(courses):
    for course in courses:
        course['course'] = course['course'].split()[0][:-1]
    return courses


def shorten_course_names(courses):
    for course in courses:
        course['name'] = course['name'].split()[0][:-1]
    return courses


'''
Returns a dictionary of the user's current courses, shortened to include only name and id.
'''


def short_course_list():
    courses = shorten_course_names(get_curr_courses())
    c = {}
    for course in courses:
        c[course['name']] = course['id']
    return c


def get_course_name(id):
    courses = short_course_list()
    keys = list(courses.keys())
    values = list(courses.values())
    return keys[values.index(id)]


def send_message(message):
    CARRIERS = {
        "att": "@mms.att.net",
        "tmobile": "@tmomail.net",
        "verizon": "@vtext.com",
        "sprint": "@messaging.sprintpcs.com"
    }

    phone_number = c.PHONE_NUM

    def send(phone_number, carrier, message):
        recipient = phone_number + CARRIERS[carrier]
        auth = (c.EMAIL, c.PASSWORD)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(auth[0], auth[1])

        server.sendmail(auth[0], recipient, message)

    message = MIMEText(message)
    message['Date'] = datetime.datetime.now().strftime("%m/%d/%y, %I%M %p")
    message['From'] = c.EMAIL
    send(phone_number, "att", message.as_string())
