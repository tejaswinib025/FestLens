# Festival Log 🪔

Festival Log is a Streamlit web application for collecting, browsing, and exporting festival-related media (audio, video, image, and text) contributed by users. It features user authentication, AI-powered media processing, and a leaderboard for contributors.

## Features
- **User Login/Sign Up:** Secure authentication using phone and password.
- **Upload Media:** Add new festival items (audio, video, image, or text) with metadata.
- **AI Processing:** Optional transcription for audio and captioning for images.
- **Browse:** Filter and search uploaded items by festival, language, media type, or text.
- **Export:** Download the dataset as CSV or JSON.
- **Leaderboard:** View top contributors by number of uploads.

## Installation
1. Clone this repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## File Structure
- `app.py` — Main Streamlit app
- `db.py` — Database functions (SQLite)
- `utils.py` — Utility functions (AI, file handling)
- `requirements.txt` — Python dependencies
- `uploads/` — Uploaded media files
- `exports/` — Exported datasets

## Usage
- Open the app in your browser after running the Streamlit command.
- Sign up or log in with your phone number.
- Use the sidebar to upload, browse, export, or view the leaderboard.

## Requirements
- Python 3.7+
- See `requirements.txt` for Python packages

## License
MIT License
