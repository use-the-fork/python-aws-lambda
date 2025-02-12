import json
from python_aws_lambda.job.job import Job

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        job_name = body['job']
        data = body['data']
        
        # Dynamically import and execute the job
        job_class = globals().get(job_name)
        if job_class and issubclass(job_class, Job):
            job_instance = job_class(data)
            job_instance.handle()
        else:
            raise ValueError(f"Job class {job_name} not found or is not a subclass of Job")
