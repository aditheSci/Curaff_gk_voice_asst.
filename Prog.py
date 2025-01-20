import speech_recognition as sr
import requests
from gtts import gTTS
import os
from googletrans import Translator

# Function to fetch news by category
def fetch_news(category):
    api_key = "YOUR_NEWS_API_KEY"  # Replace with your NewsAPI key
    categories = {
        "national": "general",
        "international": "world",
        "sports": "sports",
        "health": "health",
        "science": "science",
        "technology": "technology",
        "business": "business",
        "entertainment": "entertainment",
        "environment": "environment",
    }

    if category not in categories:
        return ["Invalid category. Please try again."]

    # Build the API request URL
    url = f"https://newsapi.org/v2/top-headlines?category={categories[category]}&country=in&apiKey={api_key}"
    if category == "international":
        url = f"https://newsapi.org/v2/top-headlines?category=general&apiKey={api_key}"  # For international, fetch without restricting to India

    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        if articles:
            return [article["title"] for article in articles[:5]]  # Top 5 news titles
        else:
            return ["No news found for this category."]
    else:
        return ["Failed to fetch news. Please check your API key or internet connection."]

# Function to speak in Hindi
def speak_in_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, src="en", dest="hi").text
    tts = gTTS(translated_text, lang="hi")
    tts.save("news.mp3")
    os.system("start news.mp3")  # For Windows; use "open" on macOS or "xdg-open" on Linux.

# Function to process voice command
def process_command(command):
    command = command.lower()
    categories = ["national", "international", "sports", "health", "science", "technology", "business", "entertainment", "environment"]

    for category in categories:
        if category in command:
            news_list = fetch_news(category)
            return news_list

    return ["Sorry, I couldn't understand the category. Please try again."]

# Main Function for Voice Recognition
def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your command (e.g., 'Tell me current affairs in sports' or 'international news'):")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="en-IN").lower()
            print(f"You said: {command}")
            
            # Process command and fetch news
            news_list = process_command(command)
            
            # Speak out news in Hindi
            for news in news_list:
                print(news)
                speak_in_hindi(news)
        
        except sr.UnknownValueError:
            print("Sorry, I could not understand your voice.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == "__main__":
    main()
