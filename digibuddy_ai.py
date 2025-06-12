from quart import Quart, request, jsonify
from quart_cors import cors  # Import Quart-CORS
import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq

# Load API key from .env file
load_dotenv()

# Initialize Quart app
app = Quart(__name__)
cors(app, allow_origin="*")  # Enable CORS for all origins

# Set up Groq API client
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/chat", methods=["POST"])
async def chat():
    try:
        data = await request.get_json()
        user_message = data.get("message", "")

        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama3-70b-8192"
        )

        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        print(f"Error: {e}")  # Log error in terminal
        return jsonify({"error": str(e)}), 500

# Run Quart server
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))  # Use Render's PORT variable

    app.run(host="0.0.0.0", port=PORT, debug=True)
