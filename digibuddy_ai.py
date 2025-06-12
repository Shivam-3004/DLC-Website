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
cors(app, allow_origin="https://shivam-3004.github.io")  # Allow GitHub Pages frontend

# Set up Groq API client
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Handle CORS preflight requests
@app.route("/chat", methods=["OPTIONS"])
async def handle_options():
    response = jsonify({"message": "CORS preflight handled"})
    response.headers.add("Access-Control-Allow-Origin", "https://shivam-3004.github.io")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

# ✅ Fix route to match frontend requests
@app.route("/chat", methods=["POST"])
async def chat():
    try:
        data = await request.get_json()
        user_message = data.get("message", "")

        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama3-70b-8192"
        )

        # ✅ Add CORS headers to response
        api_response = jsonify({"response": response.choices[0].message.content})
        api_response.headers.add("Access-Control-Allow-Origin", "https://shivam-3004.github.io")
        return api_response

    except Exception as e:
        print(f"Error: {e}")  # Log error in terminal
        return jsonify({"error": str(e)}), 500

# ✅ Run Quart server with correct port binding
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))  # Use Render's PORT variable
    app.run(host="0.0.0.0", port=PORT, debug=True)