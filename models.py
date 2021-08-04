class User:
    def __init__(self, chat_id, bb_id = "", psw = ""):
        self.bb_id = bb_id
        self.psw = psw
        self.id = chat_id


class Course:
    def __init__(self, course_name, course_id = 12345):
        self.name = course_name
        self.id = course_id