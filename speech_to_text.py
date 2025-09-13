import whisper
import os
from typing import Optional

class SpeechToText:
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model for speech-to-text conversion
        Model sizes: tiny, base, small, medium, large
        """
        self.model = whisper.load_model(model_size)
        
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text or None if error
        """
        try:
            if not os.path.exists(audio_file_path):
                print(f"Audio file not found: {audio_file_path}")
                return None
                
            result = self.model.transcribe(audio_file_path)
            return result["text"].strip()
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
            
    def transcribe_with_timestamps(self, audio_file_path: str) -> Optional[dict]:
        """
        Transcribe audio with word-level timestamps
        
        Returns:
            Dictionary with segments and timestamps
        """
        try:
            if not os.path.exists(audio_file_path):
                print(f"Audio file not found: {audio_file_path}")
                return None
                
            result = self.model.transcribe(audio_file_path, word_timestamps=True)
            return result
            
        except Exception as e:
            print(f"Error transcribing audio with timestamps: {e}")
            return None
