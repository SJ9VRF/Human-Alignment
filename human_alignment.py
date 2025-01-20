# Core class definitions.

import os
import random
import string
import pandas as pd
from google.cloud import aiplatform
from google_cloud_pipeline_components.v1 import model_evaluation
from kfp import compiler


class HumanAlignment:
    """
    A class to handle the human alignment project using Vertex AI AutoSxS.
    """

    def __init__(self, project_id, location, bucket_name=None):
        self.project_id = project_id
        self.location = location
        self.bucket_name = bucket_name or f"gs://{self.project_id}-aip-{self._generate_uuid()}"
        self.dataset_path = None
        aiplatform.init(project=self.project_id, location=self.location, staging_bucket=self.bucket_name)

    @staticmethod
    def _generate_uuid(length=8):
        """Generate a random UUID for unique naming."""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def create_bucket(self):
        """Create a Cloud Storage bucket for storing artifacts."""
        os.system(f"gsutil mb -l {self.location} -p {self.project_id} {self.bucket_name}")
        print(f"Bucket created: {self.bucket_name}")

    def prepare_dataset(self, context, questions, predictions_a, predictions_b, human_preference):
        """
        Create and upload the evaluation dataset for human alignment checking.

        Parameters:
            context (list): Contexts for the evaluation.
            questions (list): Questions for evaluation.
            predictions_a (list): Model A predictions.
            predictions_b (list): Model B predictions.
            human_preference (list): Human preference labels.
        """
        examples = pd.DataFrame({
            "context": context,
            "questions": questions,
            "pred_a": predictions_a,
            "pred_b": predictions_b,
            "actuals": human_preference,
        })
        self.dataset_path = os.path.join(self.bucket_name, "input/evaluation_dataset_with_human_preference.json")
        examples.to_json("evaluation_dataset_with_human_preference.json", orient="records", lines=True)
        os.system(f"gsutil cp evaluation_dataset_with_human_preference.json {self.dataset_path}")
        print(f"Dataset uploaded to: {self.dataset_path}")

    def compile_pipeline(self, pipeline_func, template_path="pipeline.yaml"):
        """
        Compile the AutoSxS pipeline locally.

        Parameters:
            pipeline_func: The pipeline function to compile.
            template_path (str): Path to save the compiled pipeline YAML file.
        """
        compiler.Compiler().compile(pipeline_func=pipeline_func, package_path=template_path)
        print("Pipeline compiled successfully.")

    def run_pipeline(self, parameters, display_name, template_path="pipeline.yaml"):
        """
        Run the AutoSxS pipeline.

        Parameters:
            parameters (dict): Parameters for the pipeline.
            display_name (str): Name for the pipeline job.
            template_path (str): Path to the compiled pipeline YAML file.

        Returns:
            PipelineJob: The running pipeline job instance.
        """
        pipeline_job = aiplatform.PipelineJob(
            job_id=display_name,
            display_name=display_name,
            pipeline_root=os.path.join(self.bucket_name, display_name),
            template_path=template_path,
            parameter_values=parameters,
            enable_caching=False,
        )
        pipeline_job.run()
        print(f"Pipeline {display_name} initiated.")
        return pipeline_job

    @staticmethod
    def fetch_job_outputs(job, task_name):
        """
        Fetch the outputs from a specific task in the pipeline job.

        Parameters:
            job (PipelineJob): The pipeline job instance.
            task_name (str): Name of the task to fetch outputs from.

        Returns:
            dict: Outputs of the specified task.
        """
        for details in job.task_details:
            if details.task_name == task_name:
                return details.outputs
        return None

    @staticmethod
    def load_metrics(output_uri):
        """Load evaluation metrics from the provided URI."""
        return pd.read_json(output_uri, lines=True)

    def clean_up(self, delete_bucket=False):
        """Clean up resources, optionally deleting the bucket."""
        if delete_bucket:
            os.system(f"gsutil rm -r {self.bucket_name}")
            print(f"Bucket {self.bucket_name} deleted.")
