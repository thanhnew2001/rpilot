from taipy.gui import Gui, notify

from pandasai import PandasAI
from pandasai.llm.starcoder import Starcoder
from pandasai.middlewares.base import Middleware

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import re
from utils import contains_related_word, ensure_pipe_angle_bracket, beautify_labels, remove_related_words_from_string, categorize_columns_by_datatype, generate_prompt, remove_rows_with_high_nulls
from prompt2starcoder import code_prompt
import chardet

SECRET_PATH = "secret.txt"
with open(SECRET_PATH, "r") as f:
    API_TOKEN = f.read()

user_input = ""
prompt = ""
content = ""
i = 0
past_prompts = []
suggested_prompts = [
    "Generate a Python function that checks whether a given string is a palindrome (reads the same forwards and backwards)",
    "Write a Python program to calculate the factorial of a given number using recursion or iteration.",
    "Write a Python program that takes a string input and outputs the reverse of the string.",
    "Create a program that generates a list of prime numbers within a specified range using the Sieve of Eratosthenes algorithm.",
    "Create a Python class that represents a basic bank account with methods for deposit, withdrawal, and balance inquiry."
]


#for TaipyGUI graphs
API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
context = ""
final_result = ""
_blank = "Here is result"

def modify_data(state) -> None:
    state.final_result = ""
    for _ in range(5):
        generate_more(state)

def generate_more(state) -> None:

    global i
    #notify(state, "info", "Running query...")    
    state.prompt = state.user_input + '\n' + state.final_result
    state.final_result += code_prompt(API_URL, headers, context, state, state.prompt)
    #notify(state, "success", "Code Updated!")

def new_conversation(state) -> None:
    state.user_input = ""
    state.final_result = ""
    

def on_exception(state, function_name: str, ex: Exception) -> None:
    """
    Catches exceptions and notifies user in Taipy GUI

    Args:
        state (State): Taipy GUI state
        function_name (str): Name of function where exception occured
        ex (Exception): Exception
    """
    notify(state, "error", f"An error occured in {function_name}: {ex}")


def suggest_prompt0(state) -> None:
    """
    Runs an example prompt
    """
    state.user_input = state.suggested_prompts[0]
    modify_data(state)
def suggest_prompt1(state) -> None:
    """
    Runs an example prompt
    """
    state.user_input = state.suggested_prompts[1]
    modify_data(state)
def suggest_prompt2(state) -> None:
    """
    Runs an example prompt
    """
    state.user_input = state.suggested_prompts[2]
    modify_data(state)
def suggest_prompt3(state) -> None:
    """
    Runs an example prompt
    """
    state.user_input = state.suggested_prompts[3]
    modify_data(state)
def suggest_prompt4(state) -> None:
    """
    Runs an example prompt
    """
    state.user_input = state.suggested_prompts[4]
    modify_data(state)


page = """

<|layout|columns=1 6|

<|part|render=True|
<|media/rmit.png|image|width=120px|height=70px|>
# R**Pilot**{: .color-primary .logo-text}
Powered by Taipy and TaipyGUI

# 

<|New conversation |button|label=New conversation|on_action=new_conversation|id=newchat_button|> 

# Previous activities {: .sub-text}
<|tree|lov={past_prompts}|id=past_prompts_list|multiple|>

|>

<|part|render=True|
# Prompt {: .sub-text}
<|{user_input}|input|on_action=modify_data|class_name=fullwidth|label=Enter your instruction here|id=input_prompt|change_delay=550|>

# Prompt suggestions {: .sub-text}

<|part|render=True|id=suggested_prompts|
<|{suggested_prompts[0]}|button|on_action=suggest_prompt0|class_name=button_link|>
<|{suggested_prompts[1]}|button|on_action=suggest_prompt1|class_name=button_link|>
<|{suggested_prompts[2]}|button|on_action=suggest_prompt2|class_name=button_link|>
|>


# Response {: .sub-text}

<|Continue|button|label=Continue|on_action=generate_more|id=more_button|> 

<|{final_result}|input|multiline|class_name=fullwidth|id=input_response|>
|>
|>

"""
gui = Gui(page)
gui.run(title="SSET Pilot")

