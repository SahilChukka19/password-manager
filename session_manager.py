
class SessionManager:
    def __init__(self):
        self.user_id = None

    def set_user(self, user_id):
        self.user_id = user_id

    def get_user(self):
        return self.user_id

    def clear(self):
        self.user_id = None
