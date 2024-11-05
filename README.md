# Video Q&A Web Application

A web application that allows users to upload a video file or provide a YouTube URL and ask questions related to the video's content. The application utilizes **OpenAI's Whisper** model to generate transcripts and **Google Gemini API** to create a question-answering system. The project is developed using Flask and deployed using **Render**.

## Features

- Users can **upload a video** (MP4 format) or provide a **YouTube URL**.
- Extracts **captions/transcripts** from the video using OpenAI's **Whisper** model.
- Provides a **Q&A feature** allowing users to ask questions about the video content using **Google Gemini API**.
- Deployed to **Render** for easy online access.

## Screenshots

*Figure 1: Home Page of the Video Q&A Web Application*
<img width="1345" alt="image" src="https://github.com/user-attachments/assets/a893fd69-9186-4e7a-857e-ef626c633215">
<br>

*Figure 2: Ask a question based on the video content*
<img width="1183" alt="image" src="https://github.com/user-attachments/assets/b7144a1b-a7f8-4dd1-9a71-9a45e47e73b3">

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Transcription**: OpenAI Whisper Model
- **Q&A System**: Google Gemini API
- **Deployment**: Render

## Prerequisites

- **Python** (>= 3.8)
- **pip**
- **Git**
- **Render Account** (for deployment)
- **OpenAI API Key**
- **Google Gemini API Key**

## Installation

Follow these instructions to set up and run the project locally.

### 1. Clone the Repository

```sh
$ git clone https://github.com/Hem2021/Chat_with_video_text_only.git
$ cd Chat_with_video_text_only
```

### 2. Create a Virtual Environment

It's recommended to create a virtual environment to manage dependencies.

```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using `pip`.

```sh
$ pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project to store sensitive information such as API keys.

```
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_google_gemini_api_key
UPLOAD_FOLDER=./uploads
```

### 5. Run the Application

To run the application locally, use the following command:

```sh
$ python app.py
```

By default, the application will be accessible at `http://127.0.0.1:5000`.

### 6. Uploading Videos and Testing

- Navigate to `http://127.0.0.1:5000`.
- Use the "Upload Video" or "YouTube URL" tabs to upload a video or enter a YouTube link.
- Once the video is processed, ask questions related to the video content.

## Deployment

The application can be deployed using **Render** or any other hosting platform.

### Deploying to Render

1. **Create a Render Account**: Sign up at [Render](https://render.com/).
2. **Connect GitHub Repository**: Link your GitHub repository to Render.
3. **Create a New Web Service**:
   - Choose the repository and branch.
   - Specify the `build command` as:
     ```sh
     pip install -r requirements.txt
     ```
   - Set the `start command` as:
     ```sh
     gunicorn app:app
     ```
4. **Environment Variables**: Add the necessary environment variables such as API keys via the Render dashboard.
5. **Deploy**: Render will automatically deploy the application, and you will get a public URL.

## Directory Structure

```
Chat_with_video_text_only/
│
├── app.py                     # Main Flask application
├── requirements.txt           # List of dependencies
├── templates/
│   └── index.html             # Main HTML file
├── uploads/                   # Temporary folder for uploaded videos (ephemeral)
├── .env                       # Environment variables (not included in Git)
└── README.md                  # Project README file
```

## Usage

- **Upload a video**: Choose a local MP4 file or provide a YouTube URL.
- **Generate transcript**: The app will generate a transcript using Whisper.
- **Ask questions**: Use the Q&A feature to interact with the video content.
- **Q&A History**: The app maintains a history of questions and answers for easy reference.

## Important Considerations

- **Storage**: Uploaded files are stored temporarily during runtime. For persistent storage, use **AWS S3**.
- **API Rate Limits**: Ensure that you stay within the rate limits of **OpenAI** and **Google Gemini** APIs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


## Future Improvements

- **Add Authentication**: Implement user authentication to personalize the user experience.
- **Persistent Q&A History**: Store questions and answers in a database for returning users.
- **Multi-Language Support**: Add support for multiple languages in transcripts and Q&A.
- **Add Multi modal support**
