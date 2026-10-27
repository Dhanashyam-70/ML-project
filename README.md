# Inbox Guardian: SMS Spam Detector

A simple machine-learning lab project that classifies SMS messages as **spam** or **ham** (normal). The model is trained in Google Colab and used by a small local website.

## Run the website

Install Python 3.10 or newer, then open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
python run_site.py
```

Open [http://localhost:8501](http://localhost:8501). Type or paste a message and select **Check message**. The local website uses a normal HTML text box and binds only to your own computer.

An optional Streamlit version is also included:

```bash
streamlit run app.py
```

## Model and data

- Dataset: [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms%2Bspam%2Bcollection)
- Text features: TF-IDF, with single words and two-word phrases
- Classifier: Linear Support Vector Classifier (`LinearSVC`)
- The Colab notebook adds 20 hand-written spam examples to the **training split only**. The original held-out test split remains separate for evaluation.
- The website includes a small extra check for common prize-scam wording.

To retrain, upload `SMS_Spam_Detector_Colab.ipynb` to Google Colab and run its cells. Download the new `spam_model.joblib` and replace the copy in this folder.

## Project files

- `SMS_Spam_Detector_Colab.ipynb` — data loading, training, evaluation, and model download
- `spam_model.joblib` — trained model used by the website
- `local_web.py` and `run_site.py` — local website and prediction endpoint
- `app.py` — optional Streamlit version
- `requirements.txt` — Python dependencies

This is an educational demo. Its predictions can be wrong and should not be treated as a security guarantee.
