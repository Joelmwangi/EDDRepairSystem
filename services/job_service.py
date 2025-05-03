import csv
from models.job import Job

class JobService:
    def __init__(self):
        self.jobs = {}

    def create_job(self, job_id, technician, equipment):
        job = Job(job_id, technician, equipment)
        self.jobs[job_id] = job
        technician.assign_job(job)
        return job

    def assess_job(self, job_id, tasks):
        job = self.jobs.get(job_id)
        if job:
            job.set_tasks(tasks)
            job.update_status(Job.STATUS_ASSESSED)
        return job

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def save_jobs_to_csv(self, filename="jobs.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Job ID", "Technician", "Equipment", "Status", "Tasks", "Cost"])
            for job in self.jobs.values():
                writer.writerow([
                    job.job_id,
                    job.technician.name,
                    job.equipment.name,
                    job.status,
                    ";".join(job.tasks),
                    job.cost
                ])

    def load_jobs_from_csv(self, filename="jobs.csv"):
        try:
            with open(filename, mode="r") as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

