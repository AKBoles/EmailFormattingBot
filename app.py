import os
from flask import Flask, render_template, request
import openai

# Load environment variables for local development
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    formatted_email = ""
    raw_email = ""
    action = ""
    
    if request.method == "POST":
        raw_email = request.form.get("raw_email", "")
        action = request.form.get("action", "cleanup")
        
        if raw_email.strip():
            if action == "cleanup":
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
            elif action == "compose":
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are an email composing assistant. "
                            "Based on the user's instructions, write a well-formatted, professional email. "
                            "Return only the final email content as it should be sent."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Compose an email based on the following instructions:\n'''{raw_email}'''"
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
    
    return render_template("index.html", raw_email=raw_email, formatted_email=formatted_email, action=action)

if __name__ == "__main__":
    # Bind to 0.0.0.0 and use the PORT env variable if present (for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
