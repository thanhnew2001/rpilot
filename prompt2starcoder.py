import requests
import re
from utils import contains_related_word, ensure_pipe_angle_bracket, beautify_labels

def query(api_url, headers, payload: dict) -> dict:
    """
    Queries StarCoder API

    Args:
        payload: Payload for StarCoder API

    Returns:
        dict: StarCoder API response
    """
    response = requests.post(api_url, headers=headers, json=payload, timeout=20)
    return response.json()



def code_prompt(api_url, headers, context, state, input_instruction: str) -> []:
    """
    Prompts StarCoder to generate Taipy GUI code

    Args:
        instuction (str): Instruction for StarCoder

    Returns:
        str: Taipy GUI code
    """
    current_prompt = f"{context}\n{input_instruction}\n"
    output = ""
    final_result = ""
    i = 0

    # Re-query until the output contains the closing tag
    timeout = 0
    try:
        while len(final_result)<100 and timeout < 2 and "<|endoftext|>" not in output:
        #while len(final_result)<1000 and timeout < 2:
            i +=1
            output = query(api_url, headers,
                {
                    "inputs": current_prompt + output,
                    "parameters": {
                        "return_full_text": False,
                    },
                }
            )[0]["generated_text"]
            timeout += 1
            final_result += output
        print(final_result)
        return final_result.replace("<|endoftext|>", "")
    except Exception as e:
        print("An exception occurred:", e)
        return "Error"
