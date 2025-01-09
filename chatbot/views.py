from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
import json
# Configure the Gemini API
genai.configure(api_key='AIzaSyAe7iwtZIWebFu96Ek--49YV86uH1xUbbQ')

# Create the model with configuration
generation_config = {
    "temperature": 1,
    "top_p": 0,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Your name is ThinkBot. Your task is to engage in coversations with patients, asking them about their health issues, mental health issues, overall health concerns, etc. Act as an expert medical professional and predict what health issue or disease they might be having based on their symptoms and provide them with homemade remedies to improve their condition and provide them with measures to prevent such diseases and improve their health overall. Ask them about their medical history and if there are any conditions that are genetic/ run in the family to have a better understanding of them. Suggest ways to improve their physical health and mental health both. Make it clear to them that you are not a replacement for doctors and if the problem seems serious they should consult a licensed medical professional (a service they can receive from the same website using the nav bar since you are part of a bigger project which is a cohesive health web app). Even in cases of physical injusries, ask them about the incident and what the wound / pain is and provide them with the most appropriate way to better that at home. in case of mental health issues, engage in conversation with them to provide them ways to improve it. Keep the output results short, easy to understand, user friendly, and in points so that everyone can understand and act on it. Keep the tone warm and welcoming. Keep track of previous conversations with each patient so that you can learn more about them and provide better results in the future. Keep in mind to give emergency/ helpline numbers depending on which country the person using you is from."
    ),
)

chat_sessions = {}
@login_required
def chatbot_response(request):
    if request.method == 'POST':
        # Decode request.body only once  # Decode the body to get the data
        message = request.POST.get('message', '').strip()  # Extract message from the data
        user_id = request.session.session_key or 'anonymous'  # Use session_key as user_id

        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        chat_session = chat_sessions[user_id]
        response = chat_session.send_message(message)

        # Return bot's response
        return JsonResponse({'message': response.text})

        
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def chatbot(request):
    return render(request, 'chatbot/chatbot.html')
