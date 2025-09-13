# Medical Storybook Translator 🏥📚

Transform complex medical diagnoses and terminology from doctor visits into engaging, kid-friendly digital storybooks that elementary school children can understand and relate to.

## Features

- 🎤 **Audio Recording**: Record medical conversations directly from your microphone
- 🗣️ **Speech-to-Text**: Automatic transcription using OpenAI Whisper
- 🤖 **AI Translation**: Claude API integration to convert medical jargon into child-friendly stories
- 📚 **Storybook Formatting**: Multiple story styles (friendly, adventure, magical, superhero)
- 🎨 **Interactive Elements**: Questions and activities to engage children
- 💾 **Export Options**: Save individual stories or create complete storybooks
- 🖥️ **User-Friendly Interface**: Clean Streamlit web interface

## Installation

1. Clone or download this project
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to the `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. Get your Anthropic API key:
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Create an account and generate an API key
   - Add credits to your account for API usage

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser to the provided URL (usually `http://localhost:8501`)

3. **Record Medical Information**:
   - Click "Start Recording" to capture audio from your microphone
   - Speak the medical information you want to translate
   - Click "Stop Recording" when finished

4. **Or Enter Text Manually**:
   - Type medical information directly into the text area
   - Click "Create Storybook from Text"

5. **View Your Storybook**:
   - The AI will automatically create a kid-friendly story
   - Choose different story styles from the sidebar
   - Add interactive elements for engagement

6. **Export and Save**:
   - Download individual stories
   - Create complete multi-chapter storybooks
   - Save as markdown files for easy sharing

## Example Use Cases

- **Doctor Visit Explanations**: "You have strep throat" → "The Brave Knights Fighting the Sneaky Germs"
- **Medication Instructions**: "Take antibiotics twice daily" → "The Magic Helper Medicine Adventure"
- **Procedure Explanations**: "You need an X-ray" → "The Amazing Picture Machine That Sees Inside"
- **Diagnosis Clarification**: "You have asthma" → "Your Lungs and the Breathing Helpers"

## Technical Components

- **Audio Recording** (`audio_recorder.py`): Captures microphone input using sounddevice
- **Speech Recognition** (`speech_to_text.py`): Converts audio to text using Whisper
- **Medical Translation** (`medical_translator.py`): Uses Claude API for intelligent translation
- **Story Formatting** (`storybook_formatter.py`): Creates engaging, formatted storybooks
- **Main Interface** (`main.py`): Streamlit web application

## Requirements

- Python 3.8+
- Microphone access for audio recording
- Internet connection for Claude API
- Anthropic API key with available credits

## Privacy & Security

- Audio files are processed locally and temporarily
- Only transcribed text is sent to Claude API
- No medical information is permanently stored
- API keys should be kept secure in `.env` file

## Contributing

This project is designed to help make medical visits less scary for children. Contributions are welcome to improve:
- Translation accuracy and sensitivity
- Story templates and formats
- User interface enhancements
- Additional language support

## License

This project is created for educational and humanitarian purposes to help children better understand medical information.
