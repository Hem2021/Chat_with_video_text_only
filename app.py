import os
import glob
import yt_dlp as youtube_dl
import openai
import whisper
import google.generativeai as genai
from pytube import YouTube, exceptions
from tqdm import tqdm
from flask import Flask, request, render_template, jsonify
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import textwrap
import numpy as np
import google.generativeai as genai
from IPython.display import Markdown

# from yt_dlp import YoutubeDL
from pytubefix import YouTube
from pytubefix.cli import on_progress

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load Whisper model
whisper_model = whisper.load_model("small")

# Google Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Route for home page
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    # print("request.files", request.files)

    file = request.files["file"]
    print("FILE : ", file)
    print("FILE.fileName : ", file.filename)
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    print("Secure File Name : ", filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Return file path for later transcript generation
    return jsonify({"filePath": file_path}), 200


# Route to generate transcript
@app.route("/generate-transcript", methods=["POST"])
def generate_transcript():
    try:
        # Extract the file path from the request
        file_path = request.form.get("filePath")
        print("file_path", file_path)

        if not file_path or not os.path.exists(file_path):
            return (
                jsonify({"error": "File path is invalid or file does not exist."}),
                400,
            )

        # Extract audio and generate transcript using Whisper
        audio_path = extract_audio(file_path)
        trasnscript = transcribe_audio(audio_path)

        return jsonify({"transcript": trasnscript}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to handle YouTube video link
@app.route("/youtube", methods=["POST"])
def youtube_video():
    video_url = request.form.get("url")
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    # Download video using yt_dlp
    file_path = download_video(video_url, UPLOAD_FOLDER)
    if not file_path:
        return jsonify({"error": "Failed to download video"}), 500

    return jsonify({"filePath": file_path}), 200


# Route to handle question answering
@app.route("/ask", methods=["POST"])
def ask_question():
    transcript = request.form.get("transcript")
    question = request.form.get("question")
    if not transcript or not question:
        return jsonify({"error": "Missing transcript or question"}), 400

    # Create prompt and generate answer using Google Gemini
    prompt = make_prompt(question, transcript)
    model = genai.GenerativeModel("gemini-1.5-flash-8b-latest")
    answer = model.generate_content(prompt)

    return jsonify({"answer": answer.text}), 200


# Helper function to extract audio from video
def extract_audio(video_path):
    audio_path = video_path.replace(".mp4", ".mp3")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    return audio_path


# Helper function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    options = dict(task="translate", best_of=1, language="en")
    results = model.transcribe(audio_path, **options)
    # result = whisper_model.transcribe(audio_path)
    # Save the transcript to a file for future use
    transcripts_folder = "./uploads"
    if not os.path.exists(transcripts_folder):
        os.makedirs(transcripts_folder)

    transcript_filename = os.path.join(
        transcripts_folder, os.path.basename(audio_path).replace(".mp3", ".txt")
    )
    with open(transcript_filename, "w") as f:
        f.write(results["text"])

    return results["text"]


# Helper function to create a prompt for Gemini
def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = textwrap.dedent(
        f"""You are a helpful and informative bot that answers questions using text from the reference passage included below.
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and strike a friendly and conversational tone.
    If the passage is irrelevant to the answer, you may ignore it.
    QUESTION: '{query}'
    PASSAGE: '{escaped}'
    """
    )
    return prompt


def download_video(video_url, path="./tmp/"):
    print(f"Downloading video from {video_url}...")

    def progress_callback(stream, data_chunk, bytes_remaining):
        pbar.update(len(data_chunk))

    try:
        yt = YouTube(video_url, on_progress_callback=progress_callback)
        stream = (
            yt.streams.filter(progressive=True, file_extension="mp4", res="720p")
            .desc()
            .first()
        )
        if stream is None:
            stream = (
                yt.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
                .first()
            )
        if stream is None:
            print("No suitable stream found.")
            return None
        if not os.path.exists(path):
            os.makedirs(path)
        filename = secure_filename(stream.default_filename)
        filepath = os.path.join(path, filename)
        if not os.path.exists(filepath):
            print("Downloading video from YouTube...")
            pbar = tqdm(
                desc="Downloading video from YouTube",
                total=stream.filesize,
                unit="bytes",
            )
            stream.download(output_path=path, filename=filename)
            pbar.close()
        return filepath
    except exceptions.VideoUnavailable:
        print(f"The video {video_url} is unavailable.")
    except exceptions.PytubeError as e:
        print(f"An error occurred: {e}")


# Run the app locally
if __name__ == "__main__":
    # vid1_url = "https://www.youtube.com/watch?v=aqzxYofJ_ck"
    # download_video(vid1_url, UPLOAD_FOLDER)
    app.run(host="0.0.0.0", port=4000, debug=True)
