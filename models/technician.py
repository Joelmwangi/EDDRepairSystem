from models.user import User

class Technician(User):
    def __init__(self, user_id, name, email, expertise):
        super().__init__(user_id, name, email)
        self.expertise = expertise
        self.assigned_jobs = []

    def assign_job(self, job):
        self.assigned_jobs.append(job)

