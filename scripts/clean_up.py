
# Script for resource cleanup.

import argparse
from human_alignment import HumanAlignment


def main(project_id, location, bucket_name, delete_bucket):
    """
    Clean up resources created for the human alignment project.

    Parameters:
        project_id (str): Google Cloud Project ID.
        location (str): Google Cloud region.
        bucket_name (str): Cloud Storage bucket name to clean up.
        delete_bucket (bool): Whether to delete the Cloud Storage bucket.
    """
    # Initialize HumanAlignment instance
    alignment = HumanAlignment(project_id=project_id, location=location, bucket_name=bucket_name)

    # Clean up resources
    alignment.clean_up(delete_bucket=delete_bucket)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Clean up resources for the human alignment project.")
    parser.add_argument("--project_id", type=str, required=True, help="Google Cloud Project ID")
    parser.add_argument("--location", type=str, default="us-central1", help="Google Cloud Region")
    parser.add_argument("--bucket_name", type=str, required=True, help="Cloud Storage bucket name to clean up")
    parser.add_argument(
        "--delete_bucket", action="store_true", help="If set, deletes the Cloud Storage bucket"
    )

    args = parser.parse_args()

    # Execute the main clean-up function
    main(
        project_id=args.project_id,
        location=args.location,
        bucket_name=args.bucket_name,
        delete_bucket=args.delete_bucket,
    )

    print("Clean-up process completed.")
