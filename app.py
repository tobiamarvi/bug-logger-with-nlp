from flask import Flask, render_template, request
import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv
load_dotenv()
num_test_cases = 10

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Store bugs and test cases
bugs = []

@app.route("/", methods=["GET"])
def index():
    # Render the front end with all logged bugs and test cases
    return render_template("index.html", bugs=bugs)

@app.route("/submit_bug", methods=["POST"])
def submit_bug():
    # Get bug name and description from form
    bug_name = request.form.get("name")
    bug_description = request.form.get("description")

    # Generate test cases using placeholder logic
    test_cases = generate_test_cases(bug_description)

    # Append the bug with its test cases to the list
    bugs.append({"name": bug_name, "description": bug_description, "test_cases": test_cases})

    # Redirect back to the index page to display updated bugs
    return render_template("index.html", bugs=bugs)

@app.route("/delete_bug/<bug_name>", methods=["POST"])
def delete_bug(bug_name):
    # Find and remove the bug from the list
    global bugs
    bugs = [bug for bug in bugs if bug["name"] != bug_name]

    # Redirect back to the index page after deletion
    return render_template("index.html", bugs=bugs)

def generate_test_cases(description):
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        #inital prompt/system instructions
        system_instruction="Generate a list of " + str(num_test_cases) + " test cases from the given bug description (the test cases shouldn't be too long and must be separate by line) Try to fit it on one line.",
    )

    chat_session = model.start_chat(
    history=[
        ]
    )

    prompt = {description}
    response = chat_session.send_message(prompt)
    print(response)
    # Extract the text response and split into individual test cases
    test_cases = response.text.split("\n")  # Assuming test cases are separated by newlines
    return [case for case in test_cases if case.strip()]  # Filter out empty cases

if __name__ == "__main__":
    app.run(debug=True)
