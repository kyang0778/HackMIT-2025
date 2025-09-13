import streamlit as st
import os
import tempfile
import time
from audio_recorder import AudioRecorder
from speech_to_text import SpeechToText
from medical_translator import MedicalTranslator
from storybook_formatter import StorybookFormatter

# Page configuration
st.set_page_config(
    page_title="Medical Storybook Translator",
    page_icon="🏥📚",
    layout="wide"
)

# Initialize session state
if 'recorder' not in st.session_state:
    st.session_state.recorder = AudioRecorder()
if 'stt' not in st.session_state:
    st.session_state.stt = SpeechToText()
if 'translator' not in st.session_state:
    st.session_state.translator = MedicalTranslator()
if 'formatter' not in st.session_state:
    st.session_state.formatter = StorybookFormatter()
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'stories' not in st.session_state:
    st.session_state.stories = []

def main():
    st.title("🏥📚 Medical Storybook Translator")
    st.markdown("*Transform medical visits into kid-friendly storybooks!*")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key check
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            st.error("⚠️ Please set your ANTHROPIC_API_KEY in the .env file")
            st.stop()
        else:
            st.success("✅ Claude API connected")
        
        # Audio device selection
        devices = st.session_state.recorder.get_available_devices()
        input_devices = [f"{i}: {device['name']}" for i, device in enumerate(devices) 
                        if device['max_input_channels'] > 0]
        
        if input_devices:
            selected_device = st.selectbox("🎤 Select Microphone", input_devices)
            device_id = int(selected_device.split(':')[0])
            st.session_state.recorder.set_device(device_id)
        
        # Story style selection
        story_style = st.selectbox(
            "📖 Story Style",
            ["friendly", "adventure", "magical", "superhero"]
        )
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🎤 Record Medical Information")
        
        # Recording controls
        if not st.session_state.recording:
            if st.button("🔴 Start Recording", type="primary"):
                st.session_state.recording = True
                st.session_state.recorder.start_recording()
                st.rerun()
        else:
            if st.button("⏹️ Stop Recording", type="secondary"):
                st.session_state.recording = False
                audio_file = st.session_state.recorder.stop_recording()
                
                if audio_file:
                    with st.spinner("🔄 Converting speech to text..."):
                        transcribed_text = st.session_state.stt.transcribe_audio(audio_file)
                    
                    if transcribed_text:
                        st.success("✅ Audio transcribed successfully!")
                        st.text_area("📝 Transcribed Text:", transcribed_text, height=100)
                        
                        with st.spinner("🪄 Creating your storybook..."):
                            story = st.session_state.translator.translate_to_storybook(transcribed_text)
                            
                        if story:
                            formatted_story = st.session_state.formatter.format_storybook(story, story_style)
                            st.session_state.stories.append({
                                'original': transcribed_text,
                                'story': formatted_story,
                                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.success("📚 Storybook created!")
                        else:
                            st.error("❌ Failed to create storybook")
                    else:
                        st.error("❌ Failed to transcribe audio")
                    
                    # Clean up temp file
                    try:
                        os.unlink(audio_file)
                    except:
                        pass
                
                st.rerun()
        
        # Recording status
        if st.session_state.recording:
            st.warning("🎙️ Recording in progress... Click 'Stop Recording' when finished.")
            # Record audio chunks in real-time
            st.session_state.recorder.record_chunk(0.1)
        
        # Manual text input option
        st.subheader("📝 Or Enter Text Manually")
        manual_text = st.text_area("Enter medical information:", height=150)
        
        if st.button("🪄 Create Storybook from Text") and manual_text:
            with st.spinner("🪄 Creating your storybook..."):
                story = st.session_state.translator.translate_to_storybook(manual_text)
                
            if story:
                formatted_story = st.session_state.formatter.format_storybook(story, story_style)
                st.session_state.stories.append({
                    'original': manual_text,
                    'story': formatted_story,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("📚 Storybook created!")
                st.rerun()
            else:
                st.error("❌ Failed to create storybook")
    
    with col2:
        st.header("📚 Your Storybooks")
        
        if st.session_state.stories:
            # Show latest story
            latest_story = st.session_state.stories[-1]
            st.markdown(latest_story['story'])
            
            # Add interactive elements
            if st.checkbox("🎨 Add Interactive Elements"):
                interactive_story = st.session_state.formatter.add_interactive_elements(latest_story['story'])
                st.markdown(interactive_story)
            
            # Story history
            if len(st.session_state.stories) > 1:
                st.subheader("📖 Previous Stories")
                for i, story_data in enumerate(reversed(st.session_state.stories[:-1])):
                    with st.expander(f"Story {len(st.session_state.stories) - i - 1} - {story_data['timestamp']}"):
                        st.markdown(story_data['story'])
            
            # Export options
            st.subheader("💾 Export Options")
            
            if st.button("📄 Create Complete Storybook"):
                all_stories = [story['story'] for story in st.session_state.stories]
                complete_book = st.session_state.formatter.create_chapter_format(all_stories)
                
                st.download_button(
                    label="📥 Download Complete Storybook",
                    data=complete_book,
                    file_name=f"medical_storybook_{time.strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
            
            # Clear stories
            if st.button("🗑️ Clear All Stories"):
                st.session_state.stories = []
                st.rerun()
        else:
            st.info("👆 Record or enter medical information to create your first storybook!")
    
    # Footer
    st.markdown("---")
    st.markdown("*Made with ❤️ to help make medical visits less scary for kids*")

if __name__ == "__main__":
    main()
