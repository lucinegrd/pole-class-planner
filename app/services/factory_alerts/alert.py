from datetime import datetime


class Alert:
    def __init__(self, student=None, course=None):
        self.student = student
        self.course = course
        self.timestamp = datetime.now()

    def get_type(self):
        raise NotImplementedError()

    def get_message(self):
        raise NotImplementedError()
    def get_actions(self):
        raise NotImplementedError()

    def to_dict(self):
        return {
            "type": self.get_type(),
            "message": self.get_message(),
            "date": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.get_data(),
            "actions": self.get_actions()
        }

    def get_data(self):
        data = {}
        if self.student:
            data["student_id"] = self.student.id
        if self.course:
            data["course_id"] = self.course.id
        return data

