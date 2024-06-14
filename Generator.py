import json
from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import pipeline
import time

# Introduction:
# This script uses our trained BART model to generate summaries for a test dataset. It loads the test data,
# initializes the model and tokenizer from the saved model, and uses a summarization pipeline to produce summaries.
# The process is timed, and the generated summaries are saved to a JSON file, showcasing the model's application in
# generating concise representations of legal texts, part of the NLP challenge addressed by ALBOND Innovation at the Airbus hackathon.

# Path to the test dataset
test_set_path = "data/test_set.json"

# Load the JSON file
with open(test_set_path, "r") as file:
    test_set_data = json.load(file)

# Load the model and tokenizer
model = BartForConditionalGeneration.from_pretrained("./model_saved")
tokenizer = BartTokenizer.from_pretrained("./model_saved")

# Create a text generation pipeline without specifying a device
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Select original texts for summary generation
test_texts = [item["original_text"] for item in test_set_data.values()]

# Measure the time taken to generate summaries
start_time = time.time()

# Generate summaries
generated_summaries = summarizer(
    test_texts,
    max_length=80,
    min_length=5,
    length_penalty=5.0,
    num_beams=100,
    early_stopping=True,
)

# Calculate elapsed time for summary generation
elapsed_time = time.time() - start_time
print(f"Elapsed time for summary generation: {elapsed_time} seconds")

# Initialize a dictionary for the generated summaries
generated_summaries_dict = {}

# Iterate over the generated summaries, using existing IDs from the dictionary
for i, summary in enumerate(generated_summaries):
    uid = list(test_set_data.values())[i][
        "uid"
    ]  # Modified to use the list generated from dictionary values
    original_text = test_texts[i]
    generated_summary = summary["summary_text"]
    generated_summaries_dict[uid] = {"generated_summary": generated_summary, "uid": uid}

# Save the dictionary of generated summaries to a JSON file
output_file_path = "data/generated-summaries.json"
with open(output_file_path, "w") as json_file:
    json.dump(generated_summaries_dict, json_file, indent=4)

print(f"Generated summaries have been saved to the JSON file: {output_file_path}")
