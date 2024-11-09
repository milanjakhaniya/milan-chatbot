from celery import shared_task
import requests

@shared_task
def process_message(user_message):
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',  
            headers={
                'Authorization': 'Bearer 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',
                'Content-Type': 'application/json'
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [{
                    "role": "user",
                    "content": user_message
                }]
            }
        )
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
            
        else:
            return f"Error: Received status code {response.status_code} from the API."

    except requests.exceptions.RequestException as e:
        return f"Error communicating with the Groq API: {e}"
