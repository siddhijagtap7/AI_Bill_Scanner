import os
import google.generativeai as genai
import pandas as pd
import json
from functools import lru_cache
import toml
import streamlit as st

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)


@lru_cache
def load_model():
    model = genai.GenerativeModel(
        'models/gemini-1.5-flash'
    )
    return model

def items_price(text):
    prompt = f"""
    You are an AI assistant. Here is a restaurant bill. Understand the bill and your task is to create a json string of item, quantity and price only from the below given data. For prices, only the price should be as the output, not any symbol preceeding or succeeding it.
    Data: {text}

    """
    prompt = prompt + """
    Expected Output Format: If the data contains three items,
        {
        "Items": ["Item1","Item2","Item3"],
        "Quantity": ["Quantity1","Quantity2","Quantity3"],
        "Prices": ["Price1","Price2","Price3"]
        }"""
    model = load_model()
    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(
                temperature=0.1,candidate_count=1)
                )
    
    # data = json.loads(response.text)
    response = response.text
    cleaned_string = response.strip("```json\n").strip("```")
    data = json.loads(cleaned_string)
    df = pd.DataFrame(data)
    df['Prices'] = df['Prices'].astype(float)
    return df

def total_gst(text):
    prompt2 = f"""
    You are an AI assistant. Here is a restaurant bill. Understand the bill and your task is to create a json string of final total amount, cgst percentage, sgst percentage only from the below given data. Extract percentage not the amount. If no SGST or CGST is present, consider 0. The response given would be directly loaded into json, so give it accordingly; no backticks
    Data: {text}

    """
    prompt2 = prompt2 + """
    Expected Output Format: 
        {
        "Total": "",
        "CGST": "",
        "SGST": ""
        }"""
    model = load_model()
    response = model.generate_content(prompt2, generation_config=genai.GenerationConfig(
                temperature=0.1,candidate_count=1)
                )
    # print(response.text)
    data = json.loads(response.text)
    # print(data)
    df = pd.DataFrame([data])
    # print(df)
    df = df.astype(float)
    return df