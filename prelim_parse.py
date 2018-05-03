from lxml import html
import requests

"""
stores a single date entry of the prelim time for a given courseID
precondition: courseID is a properly formatted courseID in the form 'XXX ####'.
Arguments to pass: the courseID to find (raw input), and the url to parse.
Note: also works for final exam parsing.
"""


def prelim_and_exam_parse(course_id, url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # creates a list of courses of length 1 from the Cornell website
    prelim_info = tree.xpath('//pre/text()') # finds the <pre> tag and grabs the text
    courses = prelim_info[0]
    relevant_courses = []

    index = 0
    prelim = 1

    # assuming that there are at most 3 prelims
    while prelim <= 3:
        index = courses.find(course_id, index)
        last = courses.find('\n', index)

        if index != -1:
            relevant_courses.append(courses[index: last])
            index += len(courses[index: last])
            last += len(courses[index: last])

        prelim += 1

    return relevant_courses


exam = [raw_input("enter 1nd class, all caps in form LLLL ####: "),
        raw_input("enter 2nd class, all caps in form LLLL ####: "),
        raw_input("enter 3rd class, all caps in form LLLL ####: ")]


for clss in exam:
    to_print = prelim_parser(clss, 'https://registrar.cornell.edu/exams/spring-prelim-schedule')
    print to_print

for clss in exam:
    to_print = prelim_parser(clss, 'https://registrar.cornell.edu/exams/spring-final-exam-schedule')
    print to_print

