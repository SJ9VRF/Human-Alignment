# Human Alignment: Evaluating AI Models with AutoSxS

This repository contains the implementation of a **Human Alignment Project**, which evaluates and aligns AI model outputs with human preferences. By leveraging **Google Cloud's Vertex AI AutoSxS (Automatic Side-by-Side)**, the project facilitates the evaluation of predictions from two competing models against a dataset annotated with human-preference data. This process ensures that AI systems are not only performant but also aligned with human values and expectations.


![Screenshot_2025-01-21_at_5 49 04_AM-removebg-preview](https://github.com/user-attachments/assets/d4b42393-98d9-4f47-a6fc-79ee9a11f2ad)



## Overview

AI models, especially **Large Language Models (LLMs)**, demonstrate remarkable capabilities in diverse domains. However, the effectiveness of these models in real-world scenarios often depends on their alignment with human preferences. Misalignment can lead to suboptimal or even harmful outcomes. This project addresses the critical need for a structured methodology to compare and evaluate such models.

The repository provides tools to:
- Prepare evaluation datasets.
- Compare model outputs for tasks like **question answering**.
- Measure alignment between an automatic rating system (AutoRater) and human-preference data.
- Generate judgments and metrics to guide further model improvement.

## Key Features

1. **Automated Evaluation Workflow**:
   - Utilize Vertex AI's **AutoSxS** to automate the side-by-side evaluation of two model predictions.
   - Support for tasks like **summarization** and **question answering**.

2. **Human Alignment Metrics**:
   - Compare model predictions to ground-truth human-preference annotations.
   - Evaluate alignment using metrics like win rates and preference agreement.

3. **Scalable Infrastructure**:
   - Integration with **Google Cloud Storage** for dataset storage.
   - Pipelines executed on **Vertex AI**, enabling scalability for large datasets.

4. **Flexible Dataset Preparation**:
   - Easily upload JSONL datasets with context, questions, model predictions, and human preferences.

## Technical Aspects

### Pipeline Definition
A Vertex AI pipeline is defined in `pipeline.yaml` to preprocess datasets, execute model comparisons, and compute metrics.

### Evaluation Dataset
The input dataset must follow the JSONL format, containing:
- `context`: The passage or background information.
- `questions`: A question requiring an answer.
- `pred_a`: Prediction from Model A.
- `pred_b`: Prediction from Model B.
- `actuals`: Human-preference labels (e.g., "A" or "B").

### Core Functionality
The `HumanAlignment` class abstracts interactions with Vertex AI and includes methods for:
- **Dataset Preparation**
- **Pipeline Execution**
- **Resource Cleanup**

### AutoSxS Workflow
The AutoSxS evaluation generates judgments by comparing predictions and calculates alignment metrics, such as:
- **Preference Win Rate** for each model.
- **Agreement** between AutoRater and human preferences.

## Scientific Aspects

### Importance of Human Alignment
AI models that fail to align with human expectations risk:
- Producing irrelevant or incorrect outputs.
- Misinterpreting nuanced tasks, especially in sensitive domains (e.g., healthcare, law).
- Losing user trust due to unpredictable behavior.

By quantitatively comparing model outputs with human preferences, this project contributes to:
- **Ethical AI Development**: Ensuring AI systems behave as intended.
- **Better User Experience**: Refining model outputs for real-world applicability.
- **Robustness and Reliability**: Identifying strengths and weaknesses in model behavior.

## Applications
This project is applicable across various domains:
- **Natural Language Processing (NLP)**: Question answering, summarization, sentiment analysis.
- **AI Ethics**: Quantifying how well AI respects human preferences.
- **Product Design**: Evaluating competing model versions for deployment.





## Getting Started

### Prerequisites

Python 3.8+
Google Cloud account with Vertex AI and Cloud Storage enabled.

### Installation
1. Clone the repository:
``` bash
git clone https://github.com/your-repo/human-alignment-project.git
cd human-alignment-project
```

3. Install dependencies:
``` bash
pip install -r requirements.txt
```

### Running the Pipeline
1. Prepare your dataset (evaluation_dataset.json) and upload it to Cloud Storage.
2. Use the run_pipeline.py script to start the pipeline:
``` bash
python scripts/run_pipeline.py \
    --project_id your-project-id \
    --location us-central1 \
    --context "Context 1" "Context 2" \
    --questions "Question 1" "Question 2" \
    --predictions_a "Prediction A1" "Prediction A2" \
    --predictions_b "Prediction B1" "Prediction B2" \
    --human_preference "A" "B"
```
3. Monitor the pipeline's progress in the Vertex AI console.
4. Fetch results and analyze metrics for human alignment.
### Cleaning Up Resources
Use the clean_up.py script to remove Cloud Storage buckets and other resources:
``` bash
python scripts/clean_up.py --project_id your-project-id --bucket_name your-bucket-name --delete_bucket
```
