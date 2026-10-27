# Inbox Guardian: SMS Spam Detector

A simple machine-learning lab project that classifies SMS messages as **spam** or **ham** (normal). The model is trained in Google Colab and used by a Streamlit website.

## Deploy on Streamlit Community Cloud

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with the GitHub account that can access this repository.
2. Select **Create app**.
3. Choose repository `Dhanashyam-70/ML-project`.
4. Set the branch to `main` and the app file to `app.py`.
5. In **Advanced settings**, choose Python **3.12**, then deploy.

The repository contains `requirements.txt` and `spam_model.joblib` at its root, so Community Cloud can install the dependencies and load the model. Streamlit documents that the entrypoint and dependency file can be placed at the repository root, and its current default Python version is 3.12.

## Run locally

Install Python 3.10 or newer, then run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address shown by Streamlit. You can also use `python run_site.py` for the standalone HTML version.

## Model and data

- Dataset: [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms%2Bspam%2Bcollection)
- Text features: TF-IDF, with single words and two-word phrases
- Classifier: Linear Support Vector Classifier (`LinearSVC`)
- The Colab notebook adds 20 hand-written spam examples to the **training split only**. The original held-out test split remains separate for evaluation.
- The website includes a small extra check for common prize-scam wording.

To retrain, upload `SMS_Spam_Detector_Colab.ipynb` to Google Colab and run its cells. Download the new `spam_model.joblib` and replace the copy in this repository.

## Project files

- `SMS_Spam_Detector_Colab.ipynb` — data loading, training, evaluation, and model download
- `spam_model.joblib` — trained model used by the website
- `app.py` — Streamlit website entrypoint
- `local_web.py` and `run_site.py` — standalone local website option
- `requirements.txt` — pinned Python dependencies

This is an educational demo. Its predictions can be wrong and should not be treated as a security guarantee.
