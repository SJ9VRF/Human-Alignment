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

5. **Modular Design**:
   - Python classes and utility scripts for seamless interaction with Vertex AI components.
   - Jupyter notebooks for interactive experimentation.
