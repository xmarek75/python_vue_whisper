# backend/faster_whisper.py
from faster_whisper import WhisperModel
from utils import *

class FasterWhisper:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        # Load the model during initialization
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def simple_hours(self, seconds):
        """Helper function to convert seconds into minutes and seconds."""
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return minutes, remaining_seconds

    def transcribe(self, audio_path):
        """Transcribe the audio file and format the result with timestamps."""
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        text_result = ""

        for segment in segments:
            start_time = segment.start  # Start time in seconds
            end_time = segment.end      # End time in seconds
            text = segment.text         # Transcription text

            # Convert times to minutes and seconds
            start_minutes, start_seconds = self.simple_hours(start_time)
            end_minutes, end_seconds = self.simple_hours(end_time)

            # Format the output string
            new_string = f"[{start_minutes:.0f}:{start_seconds:.0f} - {end_minutes:.0f}:{end_seconds:.0f}] {text}"
            text_result += new_string #+ "\n"
            
        text_to_json(text_result)
        #test_text_processing()

        return text_result
