# app.py
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

st.set_page_config(page_title="YouTube Full Content Extractor", page_icon="📝", layout="centered")

st.title("YouTube Full Content Extractor")
st.write("Paste any YouTube video link below to instantly extract and download its entire transcript in text format.")

youtube_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

if st.button("Extract Full Text", type="primary"):
    if not youtube_url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            st.error("Could not parse the Video ID. Please check the URL.")
        else:
            with st.spinner("Fetching full video content..."):
                try:
                    # Updated syntax using YouTubeTranscriptApi instance and fetch()
                    ytt_api = YouTubeTranscriptApi()
                    transcript_list = ytt_api.fetch(video_id)
                    
                    # Extract text from the new object structure
                    full_text = " ".join([item.text for item in transcript_list])
                    
                    st.success("Content extracted successfully!")
                    st.text_area("Full Content (Text Format)", full_text, height=350)
                    
                    st.download_button(
                        label="Download Full Text as .txt",
                        data=full_text,
                        file_name=f"youtube_content_{video_id}.txt",
                        mime="text/plain"
                    )
                    
                except TranscriptsDisabled:
                    st.error("Subtitles and transcripts are disabled for this video.")
                except NoTranscriptFound:
                    st.error("No transcripts were found for this video.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    
