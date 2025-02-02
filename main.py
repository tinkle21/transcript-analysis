import streamlit as st
import requests
import json
#from transformers import pipeline
import subprocess

# Initialize sentiment analysis pipeline
#sentiment_analysis = pipeline("sentiment-analysis")

# Function to transcribe audio using NVIDIA Riva ASR service

def transcribe_audio(file):
    # Save the uploaded file to a temporary location
    temp_file_path = "/workspaces/transcript-analysis/temp-analysis/temp_audio.wav"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file.read())
    # Define the command to run the external transcription script
    command = [
            "python", "/workspaces/transcript-analysis/python-clients/scripts/asr/transcribe_file.py",
            "--server", "grpc.nvcf.nvidia.com:443",
            "--use-ssl",
            "--metadata", "function-id", "1598d209-5e27-4d3c-8079-4751568b1081",
            "--metadata", "authorization", "Bearer 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",
            "--language-code", "en-US",
            "--input-file", temp_file_path
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        st.error("Error in transcription")
        return None


# Function to analyze the transcript
def analyze_transcript(transcript):
    # Placeholder for actual analysis logic
    topic = "Customer Support"
    sentiment = "sentiment_analysis(transcript)[0]"
    query = "Customer query about product issue"
    resolution = "Provided troubleshooting steps"
    follow_up_needed = "Yes"
    escalation_required = "No"
    insights = "Customer was satisfied with the resolution"

    return {
        "Topic": topic,
        "Sentiment": sentiment,
        "Query": query,
        "Resolution": resolution,
        "Follow Up Needed": follow_up_needed,
        "Escalation Required": escalation_required,
        "Insights": insights
    }

# Streamlit app
st.title("Call Center Transcript Analysis")

uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    transcript = transcribe_audio(uploaded_file)
    
    if transcript:
        st.write("Transcript:")
        st.text(transcript)
        
        # Save transcript to a text file
        with open("transcript.txt", "w") as f:
            f.write(transcript)
        
        # Analyze the transcript
        analysis = analyze_transcript(transcript)
        
        st.write("Analysis:")
        for key, value in analysis.items():
            st.write(f"{key}: {value}")