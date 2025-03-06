import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Load your API key from the environment (use python-dotenv locally if needed)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    formatted_email = ""
    raw_email = ""
    if request.method == "POST":
        raw_email = request.form.get("raw_email", "")
        
        if raw_email.strip():
            # Prepare the conversation for ChatGPT with a more explicit system prompt.
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that formats email content. "
                        "When given text that may include extra commentary or instructions, extract only the pure email body. "
                        "Do not include any introductions, greetings, or meta commentary. "
                        "Return only the final email content exactly as it should appear when sent."
                    )
                },
                {
                    "role": "user",
                    "content": f"Format the following email text by removing any extraneous text:\n'''{raw_email}'''"
                }
            ]
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=500
                )
                formatted_email = response["choices"][0]["message"]["content"].strip()
            except Exception as e:
                formatted_email = f"Error formatting email: {str(e)}"
    
    return render_template("index.html", raw_email=raw_email, formatted_email=formatted_email)

if __name__ == "__main__":
    app.run(debug=True)
