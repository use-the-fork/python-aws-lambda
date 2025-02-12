from .job import Job

class SpecificJob(Job):
    def handle(self):
        # Implement specific job logic here
        print(f"Processing specific job with data: {self.data}")
