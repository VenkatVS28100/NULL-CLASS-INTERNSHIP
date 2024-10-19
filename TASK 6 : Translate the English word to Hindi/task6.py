# -*- coding: utf-8 -*-
"""Task6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a-kqGIPToDE4i1EJ9vz91Uxjl8jkcnPc
"""

!pip install gradio
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import gradio as gr

import gradio as gr
from transformers import MarianMTModel, MarianTokenizer
from datetime import datetime
import pytz

model_name = 'Helsinki-NLP/opus-mt-en-hi'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def starts_with_vowel(word):
    vowels = 'AEIOUaeiou'
    return word[0] in vowels


def is_within_time_window():
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist)
    return current_time_ist.hour == 21

# Function to translate text
def translate_to_hindi(english_text):
    if starts_with_vowel(english_text):
        if is_within_time_window():

            tokenized_text = tokenizer([english_text], return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**tokenized_text)
            hindi_translation = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
            return f"Translated to Hindi: {hindi_translation[0]}"
        else:

            return "Error: This word starts with a vowel. Please provide a word that does not start with a vowel."
    else:

        tokenized_text = tokenizer([english_text], return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**tokenized_text)
        hindi_translation = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        return f"{hindi_translation[0]}"


def gradio_interface(english_word):
    return translate_to_hindi(english_word)


interface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    title="English to Hindi Translator",
    description="Translate English words to Hindi. Note: Words starting with vowels are only allowed to translate between 9 PM and 10 PM IST."
)


interface.launch()

