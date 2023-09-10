import datetime
import apicanvas as can
student_id = can.load_json("/users/self")['id']  # 359085
curr = can.short_course_list()


def get_grades():
    enrollments = can.load_json("/users/self/enrollments/")
    toRet = []
    for e in enrollments:
        d = {}
        if e['course_id'] in curr.values():
            d['course'] = can.get_course_name(e['course_id'])
            d['course_id'] = e['course_id']
            try:
                d['grade'] = e['grades']['current_score']
            except KeyError:
                d['grade'] = None
            toRet.append(d)
    toRet = list(map(dict, set(tuple(sorted(sub.items())) for sub in toRet)))
    dig = [str(item) for item in range(0, 10)]
    for f in toRet:
        if f['course'][-1] not in dig:
            toRet.remove(f)

    return toRet


grades = get_grades()


message = "Here are your grades:\n\nRun at: " + \
    datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S %p") + "\n\n"

for grade in grades:
    percent = "%\n\n"
    if grade['grade'] == None:
        percent = percent.replace("%", "");
    message += grade['course'] + ": " + str(grade['grade']) + percent

can.send_message(message)
