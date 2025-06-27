import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy
from gtts import gTTS
import base64
import io
import time
import re
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="Nexus - Virtual Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #A23B72;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .response-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 30px;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Load spaCy model with error handling
@st.cache_resource
def load_nlp_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("spaCy English model not found. Please install it using: python -m spacy download en_core_web_sm")
        return None

nlp = load_nlp_model()

def get_website_data(url: str) -> Optional[str]:
    """
    Fetch and extract text content from a website.
    
    Args:
        url (str): The URL to fetch data from
        
    Returns:
        Optional[str]: Extracted text content or None if failed
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        with st.spinner(f"Fetching data from {url}..."):
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text from paragraphs, headings, and list items
            elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div'])
            website_data = ' '.join(element.get_text(strip=True) for element in elements if element.get_text(strip=True))
            
            return website_data.lower()
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing the website: {e}")
        return None
    except Exception as ex:
        st.error(f"An unexpected error occurred: {ex}")
        return None

def process_question(question: str) -> str:
    """
    Process the user's question using NLP techniques.
    
    Args:
        question (str): The user's question
        
    Returns:
        str: Processed question
    """
    if not nlp:
        return question.lower()
    
    try:
        doc = nlp(question)
        
        # Extract important tokens (excluding stop words and punctuation)
        important_tokens = [token.lemma_.lower() for token in doc 
                          if not token.is_stop and not token.is_punct and token.is_alpha]
        
        return ' '.join(important_tokens) if important_tokens else question.lower()
    
    except Exception as e:
        st.warning(f"NLP processing failed: {e}. Using basic processing.")
        return question.lower()

def find_relevant_info(processed_question: str, website_data: str, url: str) -> str:
    """
    Find relevant information from website data based on the processed question.
    
    Args:
        processed_question (str): The processed user question
        website_data (str): The website content
        url (str): The source URL
        
    Returns:
        str: Relevant information or default message
    """
    try:
        # Split website data into sentences
        sentences = re.split(r'[.!?]+', website_data)
        relevant_sentences = []
        
        # Find sentences containing keywords from the question
        question_words = processed_question.split()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Filter out very short sentences
                # Check if sentence contains any question words
                sentence_words = sentence.lower().split()
                if any(word in sentence_words for word in question_words):
                    relevant_sentences.append(sentence)
        
        if relevant_sentences:
            # Return the most relevant sentences (up to 3)
            return '. '.join(relevant_sentences[:3]).capitalize() + '.'
        else:
            # Fallback: return first few sentences of the website
            first_sentences = sentences[:2]
            return '. '.join(s.strip() for s in first_sentences if s.strip()).capitalize() + '.'
            
    except Exception as e:
        st.warning(f"Error processing website data: {e}")
        return f"I found some information from {url}, but couldn't process it properly. Please visit the link for more details."

def generate_audio(text: str) -> bytes:
    """
    Generate audio from text using gTTS.
    
    Args:
        text (str): Text to convert to speech
        
    Returns:
        bytes: Audio data
    """
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.read()
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

def get_college_data() -> Dict[str, List[str]]:
    """
    Return the college data dictionary with keywords and URLs.
    
    Returns:
        Dict[str, List[str]]: Dictionary mapping keywords to URLs
    """
    return {
        "nri": [
            'https://www.nrigroupindia.com/'
        ],
        "courses": [
            'https://www.nrigroupindia.com/courses/'
        ],
        "inception": [
            'https://www.nrigroupindia.com/about-us/the-inception/'
        ],
        "vision": [
            'https://www.nrigroupindia.com/about-us/the-inception/'
        ],
        "mission": [
            'https://www.nrigroupindia.com/about-us/the-inception/'
        ],
        "admission": [
            'https://www.nrigroupindia.com/admission-procedure/'
        ],
        "computer science department": [
            'https://www.nrigroupindia.com/niist/computer-science-department/'
        ],
        "faculty": [
            'https://www.nrigroupindia.com/faculty/'
        ],
        "facilities": [
            'https://www.nrigroupindia.com/facilities/'
        ],
        "contact": [
            'https://www.nrigroupindia.com/contact-us/'
        ]
    }

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Intelligent Virtual Assistant for NRI Group</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Features")
        st.markdown("- **Smart Search**: Ask questions about NRI Group")
        st.markdown("- **Voice Output**: Get audio responses")
        st.markdown("- **Real-time Data**: Fetches live information")
        st.markdown("- **Conversation History**: Track your queries")
        
        st.markdown("### 📚 Available Topics")
        topics = [
            "About NRI Group", "Courses", "Admission Process", 
            "Computer Science Department", "Faculty", "Facilities", 
            "Vision & Mission", "Contact Information"
        ]
        for topic in topics:
            st.markdown(f"• {topic}")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.conversation_history = []
            st.success("History cleared!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User input
        user_query = st.text_input(
            "💬 Ask me anything about NRI Group:",
            placeholder="e.g., What courses are available? Tell me about admission process...",
            key="user_input"
        )
        
        # Search button
        search_clicked = st.button("🔍 Search", use_container_width=True)
        
        if user_query and search_clicked:
            with st.spinner("🔍 Searching for information..."):
                college_data = get_college_data()
                processed_question = process_question(user_query)
                found = False
                response_text = ""
                
                # Search through college data
                for keyword, urls in college_data.items():
                    if keyword.lower() in processed_question or any(word in keyword.lower() for word in processed_question.split()):
                        found = True
                        for url in urls:
                            website_data = get_website_data(url)
                            if website_data:
                                response_text = find_relevant_info(processed_question, website_data, url)
                                
                                # Display response
                                st.markdown(f'<div class="response-box"><h3>📝 Response:</h3><p>{response_text}</p><p><strong>Source:</strong> <a href="{url}" target="_blank">{url}</a></p></div>', unsafe_allow_html=True)
                                
                                # Add to conversation history
                                st.session_state.conversation_history.append({
                                    "question": user_query,
                                    "response": response_text,
                                    "source": url,
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                                })
                                
                                # Generate and play audio
                                audio_data = generate_audio(response_text)
                                if audio_data:
                                    st.audio(audio_data, format='audio/mp3')
                                
                                break
                        break
                
                if not found:
                    fallback_response = "I couldn't find specific information based on your query. Please try asking about courses, admission, faculty, facilities, or other aspects of NRI Group."
                    st.markdown(f'<div class="info-box"><p>{fallback_response}</p></div>', unsafe_allow_html=True)
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append({
                        "question": user_query,
                        "response": fallback_response,
                        "source": "System",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
    
    with col2:
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        quick_queries = [
            "What courses are available?",
            "Tell me about admission process",
            "Computer science department info",
            "Contact information"
        ]
        
        for query in quick_queries:
            if st.button(query, key=f"quick_{query}", use_container_width=True):
                st.session_state.user_input = query
                st.rerun()
    
    # Conversation History
    if st.session_state.conversation_history:
        st.markdown("### 📜 Conversation History")
        
        for i, conversation in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5
            with st.expander(f"💬 {conversation['question'][:50]}... - {conversation['timestamp']}"):
                st.markdown(f"**Question:** {conversation['question']}")
                st.markdown(f"**Response:** {conversation['response']}")
                st.markdown(f"**Source:** {conversation['source']}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666;">Powered by Nexus AI Assistant | Built with Streamlit</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
