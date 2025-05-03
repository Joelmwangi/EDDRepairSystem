class JobNotFoundError(Exception):
    def __init__(self, job_id):
        super().__init__(f"Job with ID '{job_id}' not found.")

