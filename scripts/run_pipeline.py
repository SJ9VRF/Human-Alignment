# Script to execute the pipeline.

import argparse
from human_alignment import HumanAlignment
from google_cloud_pipeline_components.v1 import model_evaluation


def main(project_id, location, bucket_name, context, questions, predictions_a, predictions_b, human_preference):
    # Initialize HumanAlignment instance
    alignment = HumanAlignment(project_id=project_id, location=location, bucket_name=bucket_name)

    # Create bucket if it doesn't exist
    alignment.create_bucket()

    # Prepare dataset
    alignment.prepare_dataset(context, questions, predictions_a, predictions_b, human_preference)

    # Compile pipeline
    alignment.compile_pipeline(pipeline_func=model_evaluation.autosxs_pipeline)

    # Define pipeline parameters
    parameters = {
        "evaluation_dataset": alignment.dataset_path,
        "id_columns": ["questions"],
        "autorater_prompt_parameters": {
            "inference_context": {"column": "context"},
            "inference_instruction": {"column": "questions"},
        },
        "task": "question_answering",
        "response_column_a": "pred_a",
        "response_column_b": "pred_b",
        "human_preference_column": "actuals",
    }

    # Run the pipeline
    display_name = f"human-alignment-check"
    job = alignment.run_pipeline(parameters, display_name=display_name)

    # Print the pipeline status
    print(f"Pipeline {display_name} is running. Check Vertex AI console for progress.")
    return job


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run the AutoSxS pipeline for human alignment.")
    parser.add_argument("--project_id", type=str, required=True, help="Google Cloud Project ID")
    parser.add_argument("--location", type=str, default="us-central1", help="Google Cloud Region")
    parser.add_argument("--bucket_name", type=str, help="Optional: Cloud Storage bucket name")
    parser.add_argument("--context", nargs="+", required=True, help="List of contexts for evaluation")
    parser.add_argument("--questions", nargs="+", required=True, help="List of questions for evaluation")
    parser.add_argument("--predictions_a", nargs="+", required=True, help="Predictions from Model A")
    parser.add_argument("--predictions_b", nargs="+", required=True, help="Predictions from Model B")
    parser.add_argument("--human_preference", nargs="+", required=True, help="Human preference labels")

    args = parser.parse_args()

    # Convert human preference labels to the correct format (list of strings)
    human_preference = list(args.human_preference)

    # Execute the main pipeline function
    job = main(
        project_id=args.project_id,
        location=args.location,
        bucket_name=args.bucket_name,
        context=args.context,
        questions=args.questions,
        predictions_a=args.predictions_a,
        predictions_b=args.predictions_b,
        human_preference=human_preference,
    )

    # Output instructions for checking pipeline progress
    print("Pipeline initiated. You can monitor the job in the Vertex AI console.")
