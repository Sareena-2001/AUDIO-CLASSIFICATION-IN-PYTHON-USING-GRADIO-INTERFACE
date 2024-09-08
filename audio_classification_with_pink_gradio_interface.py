# -*- coding: utf-8 -*-
"""AUDIO CLASSIFICATION WITH PINK GRADIO INTERFACE

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V2w86us7IM2yeLbyy7lyDyJcCf3sbxOz
"""

from transformers import pipeline
import gradio as gr
import numpy as np
import soundfile as sf
import os

# Define the model pipeline for audio classification
model_id = "sanchit-gandhi/distilhubert-finetuned-gtzan"
pipe = pipeline("audio-classification", model=model_id)

def classify_audio(filepath):
    if filepath is None:
        return "No file provided"

    if not os.path.isfile(filepath):
        return f"File does not exist: {filepath}"

    try:
        print(f"Classifying file: {filepath}")

        # Read the audio file from the filepath
        audio, sample_rate = sf.read(filepath)

        # Convert to mono if the audio has multiple channels
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        # Ensure the audio is in the correct format
        audio = np.array(audio)

        # Classify the audio
        preds = pipe(audio)

        if preds:
            # Find the prediction with the highest confidence
            best_pred = max(preds, key=lambda x: x["score"])
            return best_pred["label"]
        else:
            return "No predictions"
    except Exception as e:
        print(f"Error during classification: {e}")
        return f"Error: {e}"

# Gradio interface with custom styling
demo = gr.Interface(
    fn=classify_audio,
    inputs=gr.Audio(type="filepath"),
    outputs=gr.Label(),
    css="""
    .gradio-container {
        background-color: #FADADD;  /* Baby pink color */
    }
    """
)

# Launch the app
demo.launch(debug=True)