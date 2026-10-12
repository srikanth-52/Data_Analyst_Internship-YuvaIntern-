# Data Analyst Internship Project
A six-task educational portfolio using the real scikit-learn diabetes dataset.

## Quick start on Windows
```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python run_all.py
jupyter notebook
```
On macOS/Linux, activate with `source .venv/bin/activate` instead.
Use Python 3.10 or newer. Run commands from this extracted project folder.
No dataset download or account is needed after dependencies are installed.

## Deliverables
- reports/: six separate Word reports for the six portal tasks.
- notebooks/: six runnable Jupyter notebooks; saved outputs demonstrate the verified run.
- src/: fundamentals and complete data analysis implementation.
- data/: source CSV, clean CSV, deliberately dirty lab copy, source description.
- sql/: SQL exercises; outputs/analysis.sqlite contains the ready-to-query database.
- outputs/: computed statistics, model evaluation, prediction errors, charts, versions.
- submission/: six descriptions of at least 200 words and upload checklist.
- presentation/: final capstone presentation in HTML; open in a browser.

## Task mapping
1. Fundamentals: src/fundamentals.py and notebook 01.
2. Data lab: notebook 02, setup and deliberately dirty sample.
3. EDA: notebook 03, audited full dataset and plots.
4. Tools: notebook 04, NumPy/Pandas/Matplotlib/SQLite/scikit-learn.
5. Reporting: notebook 05 and stakeholder report.
6. Capstone: notebook 06, training-only cross-validation and held-out evaluation.

## Validation and limitations
Results are produced by executed code; see outputs/results.json for environment versions.
A fixed 80/20 split and five training folds avoid model selection using the final test set.
The cohort is small; correlations are associations, not proof of causation.
No time-series, financial impact or intervention outcomes are invented.
This portfolio does not establish clinical validity or independent completion by its recipient.
Read, run, understand and personalize the reports before submission.

## GitHub and submission
Create your own repository named Data-Analyst-Internship-Project.
Upload the extracted folder contents, including notebooks, code, reports and source notes.
Do not upload .venv or __pycache__.
Copy the actual repository URL from GitHub; no repository has been published by this package.
Upload each task's matching DOCX and paste its corresponding description.
The internship portal requires a real GitHub URL for technical submissions.
