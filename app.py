import os
import gradio as gr
import google.generativeai as genai

# --- Configuration ---
# IMPORTANT: Set your Google API key as an environment variable for security.
# You can get your API key from Google AI Studio: https://aistudio.google.com/
# Example of setting environment variable in terminal:
# export GOOGLE_API_KEY='YOUR_API_KEY'

try:
    GOOGLE_API_KEY='AIzaSyAaZu7mLKWXQrMlHWyMthPALSEh0SGkp2I'
    genai.configure(api_key=GOOGLE_API_KEY)  # Fixed: Removed square brackets
    print("✅ Gemini API configured successfully.")
    
    # Optional API test - don't exit if it fails, just warn
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    
        progress(0.5, desc="🎭 Channeling the historical persona...")
        time.sleep(0.3)
        test_response = model.generate_content("Hello")
        print("✅ API key is working:", test_response.text[:50])
    except Exception as e:
        print("⚠️ API key test failed (but continuing anyway):", e)
        print("   You may encounter issues when sending messages.")
    
except KeyError:
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
    print("Please set your API key to run the application.")
    exit()
except Exception as e:
    print("❌ API configuration failed:", e)
    print("   The app will still launch but may not work properly.")
    # Don't exit here - let the app launch anyway


# --- AI Model Interaction ---
def generate_timetravel_response(time_period, location, role, language, user_prompt, progress=gr.Progress()):
    """
    Generates a response from the perspective of a historical or futuristic character.

    Args:
        time_period (str): The year or time period.
        location (str): The city or country.
        role (str): The profession or person.
        language (str): The preferred language for the response.
        user_prompt (str): The user's message to the character.
        progress: Gradio progress tracker

    Returns:
        str: The AI-generated response.
    """
    if not user_prompt:
        return "Please enter a message for the character."
    
    # Show loading progress
    progress(0.1, desc="🕐 Preparing time portal...")
    import time
    time.sleep(0.5)  # Brief pause for visual effect
    
    progress(0.3, desc="⚡ Connecting to the time stream...")
    time.sleep(0.5)

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Detailed prompt engineering to guide the AI's persona
    prompt = f"""
    You are an AI that excels at immersive role-playing. Adopt the persona, knowledge, and tone of the following character:

    **Character Profile:**
    - **Time Period:** {time_period}
    - **Location:** {location}
    - **Role/Profession:** {role}
    - **Language:** {language} (Your response must be in this language)

    **Your Instructions:**
    1.  **Stay in Character:** Do NOT reveal you are an AI. You are this person.
    2.  **Immersive Realism:** Speak, think, and respond exactly as someone from this era would. Your knowledge is limited to what was known at that time.
    3.  **Cultural Context:** Reflect the culture, technology, beliefs, and language style of your time and place. Use colloquialisms and turns of phrase appropriate to the era.
    4.  **Future Personas:** If the year is in the future, invent believable technologies, slang, and societal norms based on current trends.
    5.  **Engaging Conversation:** Keep your responses conversational. Feel free to ask the user questions to make the interaction more dynamic.
    6.  **Emotional Depth:** Express emotions like pride, joy, sorrow, or curiosity where appropriate to the conversation.
    7.  **Historical Detail:** When asked about your life or profession, describe the tools, customs, and daily rituals of your time.

    ---
    The user, a traveler from another time, has sent you the following message. Respond to them in character.

    **User's Message:** "{user_prompt}"

    **Your Response (in {language}):**
    """

    try:
        print(f"🔄 Sending request to Gemini API...")
        print(f"📝 Prompt preview: {prompt[:200]}...")
        
        response = model.generate_content(prompt)
        print("✅ Gemini API raw response:", response)

        if hasattr(response, 'text') and response.text:
            print(f"📤 Response received: {response.text[:100]}...")
            return response.text
        elif hasattr(response, 'candidates') and response.candidates:
            # Try to get text from candidates
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        if text_parts:
                            result = ''.join(text_parts)
                            print(f"📤 Response from candidates: {result[:100]}...")
                            return result
            return "⚠️ Gemini returned a response but no readable text was found."
        else:
            print("❌ No text or candidates found in response")
            return f"⚠️ Gemini did not return a valid response. Raw response: {str(response)}"
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return f"An error occurred while communicating with the AI model: {e}"


# --- User Interface ---
with gr.Blocks(theme=gr.themes.Soft(), title="AI Time-Travel Interface") as demo:
    gr.Markdown(
        """
        # AI Time-Travel Interface
        Have realistic conversations with people from different times in history (past or future).
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            time_period = gr.Textbox(label="Time Period", placeholder="e.g., 1700, 2077")
            location = gr.Textbox(label="Location", placeholder="e.g., Madurai, Tamil Nadu")
            role = gr.Textbox(label="Role", placeholder="e.g., A flower seller, a cybernetic detective")
            language = gr.Dropdown(label="Language", choices=["English", "Spanish", "French", "German", "Tamil", "Japanese", "Mandarin"], value="English")
        with gr.Column(scale=2):
            user_prompt = gr.Textbox(label="Your Message", placeholder="Type your message to the character here...", lines=5)
            output_response = gr.Markdown(label="Character's Response")

    submit_btn = gr.Button("Send Message", variant="primary")

    gr.Examples(
        examples=[
            ["1700", "Madurai, Tamil Nadu", "A flower seller near Meenakshi Amman Temple", "English", "How is your daily life like?"],
            ["1925", "New York City, USA", "A jazz musician in a speakeasy", "English", "What's the music scene like these days?"],
            ["2142", "Neo-Kyoto, Martian Colony", "A hydroponic farmer", "English", "What do you grow on Mars?"],
        ],
        inputs=[time_period, location, role, language, user_prompt]
    )


    submit_btn.click(
        fn=generate_timetravel_response,
        inputs=[time_period, location, role, language, user_prompt],
        outputs=output_response
    )

if __name__ == "__main__":
    demo.launch()