import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy
from gtts import gTTS
import subprocess
import time
from art import text2art

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

speaking = False  # Flag to track if the assistant is currently speaking

def get_website_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all paragraphs on the webpage
        paragraphs = soup.find_all(['p', 'ul', 'ol'])

        # Concatenate the text content of all paragraphs
        website_data = ' '.join(element.get_text() for element in paragraphs)
        return website_data.lower()  # Convert to lowercase
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing the website: {e}")
        return None
    except Exception as ex:
        st.error(f"An unexpected error occurred: {ex}")
        return None

def process_question(question):
    # Use spaCy for NLP processing
    doc = nlp(question)
    
    # Extract keywords (non-stop words)
    keywords = [token.text.lower() for token in doc if not token.is_stop]
    
    return keywords

def generate_response(processed_question, website_data, url):
    global speaking

    if not website_data:
        return f"I couldn't retrieve information from the website."

    # Convert both processed_question and website_data to lowercase for case-insensitive comparison
    processed_question_lower = [keyword.lower() for keyword in processed_question]
    website_data_lower = website_data.lower()

    # Check if any keyword is present in the website data
    matched_keywords = [keyword for keyword in processed_question_lower if keyword in website_data_lower]

    if matched_keywords:
        # Provide context for the matched keywords by finding sentences containing them
        context_sentences = []
        for sentence in website_data.split('. '):
            if any(keyword in sentence.lower() for keyword in matched_keywords):
                context_sentences.append(sentence)

        if context_sentences:
            context = '. '.join(context_sentences)
            response = f"The website mentions the following keywords: {', '.join(matched_keywords)}. Here is some context: {context}."
        else:
            response = f"The website mentions the following keywords: {', '.join(matched_keywords)}. No additional context found."
    else:
        # Check for specific question patterns
        if any(word in processed_question_lower for word in ['admission', 'apply', 'enroll']):
            # Respond with admission information
            response = f"The admission information for {url} is available on the website. Here are the details:\n\n1. Application Process: [Details]\n2. Important Dates: [Details]\n3. Admission Requirements: [Details]"

        elif any(word in processed_question_lower for word in ['courses', 'programs', 'degrees']):
            # Respond with information about courses/programs
            response = f"The courses and programs offered by {url} are available on the website. Here are the details:\n\n1. Undergraduate Programs: [Details]\n2. Graduate Programs: [Details]\n3. Specialized Courses: [Details]"

        elif any(word in processed_question_lower for word in ['faculty', 'staff', 'professors']):
            # Respond with information about faculty/staff
            response = f"The faculty and staff information for {url} is available on the website. Here are the details:\n\n1. Faculty Members: [Details]\n2. Staff Members: [Details]\n3. Research Profiles: [Details]"

        elif any(word in processed_question_lower for word in ['departments', 'departmental information']):
            # Respond with information about departments
            response = f"The departmental information for {url} is available on the website. Here are the details:\n\n1. Computer Science Department: [Details]\n2. Mathematics Department: [Details]\n3. Engineering Department: [Details]"

        else:
            response = f"I couldn't find specific information based on your question about {url}."

    speaking = True  # Set speaking flag to True before speaking
    return response

def main():
    st.title("Nexus - Your Virtual Assistant")
    
    # Display art banner
    st.text(text2art("Nexus"))

    # User input
    user_query = st.text_input("Ask me anything:")

    if user_query:
        college_data = {
             "nri": [
                'https://www.nrigroupindia.com/'
            ],
            "courses": [
                'https://www.nrigroupindia.com/courses/'
            ],
            "inception":[
                'https://www.nrigroupindia.com/about-us/the-inception/'
                ],
            "vision":[
                'https://www.nrigroupindia.com/about-us/the-inception/'
                ],
            "mission":[
                'https://www.nrigroupindia.com/about-us/the-inception/'
                ],
            "admission":[
                'https://www.nrigroupindia.com/admission-procedure/'
                ],

            "computer science department":[
                'https://www.nrigroupindia.com/niist/computer-science-department/'
                ]
           # Add more keywords with their respective URLs
        }
        
        processed_question = process_question(user_query)
        found = False

        for keyword, urls in college_data.items():
            if keyword.lower() in processed_question:
                found = True
                for url in urls:
                    website_data = get_website_data(url)
                    if website_data:
                        response = generate_response(processed_question, website_data, url)
                        st.write(f"Response: {response}")
                        break  # Break after finding a match on any URL for the keyword

        if not found:
            st.write("I couldn't find information based on your query.")

if __name__ == "__main__":
    main()
