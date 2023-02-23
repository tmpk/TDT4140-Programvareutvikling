import requests

def get_courses_from_1024(calendarname):
    # TODO: 2017/spring shouldn't be hardcoded, at least it should be set in config
    ical_url = "https://ntnu.1024.no/2017/spring/" + calendarname + "/ical/lectures/"

    ical_content = requests.get(ical_url).text

    course_codes = extract_course_codes_from_ical(ical_content)

    return course_codes

def extract_course_codes_from_ical(ical_content):
    """
    Extracts the course codes from an ical file generated by 1024.ntnu.no

    :param ical_content: string with the complete content of a ical file retrieved from 1024.ntnu.no
    :returns: list with zero to n courses
    """

    # Splits the ical into individual lines
    ical_lines = ical_content.split('\r\n')

    # All coursecodes will be on a DESCRIPTION line
    description_lines = set(filter(lambda x: "DESCRIPTION" in x, ical_lines))

    course_codes = extract_course_code_from_description_lines(description_lines)

    list_of_courses = list(set(course_codes))

    return list_of_courses

def extract_course_code_from_description_lines(description_lines):
    """Returns a generator for the course codes in the description list"""
    for line in description_lines:
        yield extract_course_code_from_description_line(line)

def extract_course_code_from_description_line(description_line):
    """Returns the course code from a description string"""
    # All coursecodes are contained within parenteses (coursecode)
    # NB, if coursename is too long, the closing parenteses may be missing
    # 'DESCRIPTION:Forelesning - Teknologiledelse (TIØ4258)'
    return description_line.split('(')[-1].split(')')[0]
