import boto3

class AWS:
    def __init__(self):
        self.session = None

    def get_session(self):
        if self.session is not None:
            return self.session
        try:
            self.session = boto3.Session()
            return self.session
        except (Exception) as error:
            print("오류 발생:", error)