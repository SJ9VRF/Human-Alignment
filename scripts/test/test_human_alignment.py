# Unit tests for the class.

import unittest
import os
from human_alignment import HumanAlignment


class TestHumanAlignment(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.project_id = "test-project"
        self.location = "us-central1"
        self.bucket_name = f"gs://{self.project_id}-test-bucket"
        self.alignment = HumanAlignment(project_id=self.project_id, location=self.location, bucket_name=self.bucket_name)

    def test_generate_uuid(self):
        """Test UUID generation."""
        uuid = self.alignment._generate_uuid()
        self.assertEqual(len(uuid), 8)
        self.assertTrue(uuid.isalnum())

    def test_create_bucket(self):
        """Test bucket creation."""
        # Simulate bucket creation
        self.alignment.create_bucket()
        # Check if the command was executed successfully
        result = os.system(f"gsutil ls {self.bucket_name}")
        self.assertEqual(result, 0)

    def test_prepare_dataset(self):
        """Test dataset preparation and upload."""
        context = ["Context 1", "Context 2"]
        questions = ["Question 1", "Question 2"]
        predictions_a = ["Prediction A1", "Prediction A2"]
        predictions_b = ["Prediction B1", "Prediction B2"]
        human_preference = ["A", "B"]

        self.alignment.prepare_dataset(context, questions, predictions_a, predictions_b, human_preference)

        # Check if the dataset file exists locally
        self.assertTrue(os.path.exists("evaluation_dataset_with_human_preference.json"))

        # Check if the dataset was uploaded
        result = os.system(f"gsutil ls {self.bucket_name}/input/evaluation_dataset_with_human_preference.json")
        self.assertEqual(result, 0)

    def test_compile_pipeline(self):
        """Test pipeline compilation."""
        def dummy_pipeline_func():
            pass

        template_path = "test_pipeline.yaml"
        self.alignment.compile_pipeline(pipeline_func=dummy_pipeline_func, template_path=template_path)

        # Check if the pipeline YAML file was created
        self.assertTrue(os.path.exists(template_path))

    def test_clean_up(self):
        """Test resource cleanup."""
        # Ensure bucket exists
        self.alignment.create_bucket()

        # Test cleanup
        self.alignment.clean_up(delete_bucket=True)

        # Check if the bucket was deleted
        result = os.system(f"gsutil ls {self.bucket_name}")
        self.assertNotEqual(result, 0)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists("evaluation_dataset_with_human_preference.json"):
            os.remove("evaluation_dataset_with_human_preference.json")
        if os.path.exists("test_pipeline.yaml"):
            os.remove("test_pipeline.yaml")


if __name__ == "__main__":
    unittest.main()
