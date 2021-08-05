class User:
    def __init__(self, chat_id, bb_id = "", psw = ""):
        self.bb_id = bb_id
        self.psw = psw
        self.id = chat_id
        self.course_list = []

    def update_course_list(self, course_list):
        self.course_list = course_list


class Course:
    def __init__(self, course_name, course_id=12345):
        self.name = course_name
        self.course_id = course_id
