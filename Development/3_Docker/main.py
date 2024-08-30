from groq import Groq
import json
import time
import os

def read_prompts(file_path):
    # Read prompts from a text file.
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def call_llm_api(prompt):
    # Make an API call to the LLM and record timestamps.
    time_sent = int(time.time())  # Time the prompt was sent as a UNIX timestamp
    client = Groq(
        # This is the default and can be omitted
        api_key= os.environ.get("GROQ_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    time_recvd = int(time.time())  # Time the response was received as a UNIX timestamp

    return {
            "Prompt": prompt,
            "Message": completion.choices[0].message.content,  # Extract the response message
            "TimeSent": time_sent,
            "TimeRecvd": time_recvd,
            "Source": "Llama3-8b"
        }

def save_responses(responses, output_file):
    # Save the responses to a JSON file.
    with open(output_file, "w") as file:
        json.dump(responses, file, indent=4)
