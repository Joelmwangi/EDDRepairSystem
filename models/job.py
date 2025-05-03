class Job:
    STATUS_CREATED = "Job Created"
    STATUS_ASSESSED = "Job Assessed"
    STATUS_COMPLETED = "Job Completed"

    def __init__(self, job_id, technician, equipment):
        self.job_id = job_id
        self.technician = technician
        self.equipment = equipment
        self.status = self.STATUS_CREATED
        self.tasks = []
        self.cost = 0.0

    def update_status(self, status):
        self.status = status

    def set_cost(self, cost):
        self.cost = cost

    def set_tasks(self, tasks):
        self.tasks = tasks

