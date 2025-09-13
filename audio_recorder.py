import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
from typing import Optional

class AudioRecorder:
    def __init__(self, sample_rate: int = 44100, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        
    def start_recording(self):
        """Start recording audio from the microphone"""
        self.recording = True
        self.audio_data = []
        
    def stop_recording(self) -> Optional[str]:
        """Stop recording and save to temporary file"""
        self.recording = False
        
        if not self.audio_data:
            return None
            
        # Convert list to numpy array
        audio_array = np.concatenate(self.audio_data, axis=0)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_filename = temp_file.name
        temp_file.close()
        
        # Save audio to file
        sf.write(temp_filename, audio_array, self.sample_rate)
        
        return temp_filename
        
    def record_chunk(self, duration: float = 0.1):
        """Record a small chunk of audio"""
        if self.recording:
            try:
                chunk = sd.rec(
                    int(duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype=np.float32
                )
                sd.wait()
                self.audio_data.append(chunk)
            except Exception as e:
                print(f"Error recording audio chunk: {e}")
                
    def get_available_devices(self):
        """Get list of available audio input devices"""
        return sd.query_devices()
        
    def set_device(self, device_id: int):
        """Set the input device"""
        sd.default.device[0] = device_id
