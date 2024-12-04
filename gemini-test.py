import google.generativeai as genai
#print(dir(genai))

# Configure Gemini AI
genai.configure(api_key="AIzaSyAc2_LSq3Vfn27DGlSdpgpG3vR9DbgSrzQ")

import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("make a list of 5 test cases based on a crashing logging in system")

print(response.text)