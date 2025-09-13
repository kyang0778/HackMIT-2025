import streamlit as st
import os
from medical_translator import MedicalTranslator
from storybook_formatter import StorybookFormatter

# Page configuration
st.set_page_config(
    page_title="Medical Storybook Translator",
    page_icon="🏥📚",
    layout="wide"
)

# Initialize session state
if 'translator' not in st.session_state:
    st.session_state.translator = MedicalTranslator()
if 'formatter' not in st.session_state:
    st.session_state.formatter = StorybookFormatter()
if 'stories' not in st.session_state:
    st.session_state.stories = []

def main():
    st.title("🏥📚 Medical Storybook Translator")
    st.markdown("*Transform medical visits into kid-friendly storybooks!*")
    
    # Check API Key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ Please set your ANTHROPIC_API_KEY in the .env file")
        st.stop()
    else:
        st.success("✅ Claude API connected")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Story style selection
        story_style = st.selectbox(
            "📖 Story Style",
            ["friendly", "adventure", "magical", "superhero"]
        )
        
        st.markdown("---")
        st.markdown("### 💡 Example Medical Inputs:")
        st.markdown("- 'The patient has strep throat and needs antibiotics'")
        st.markdown("- 'Child needs an X-ray of their arm'")
        st.markdown("- 'Diagnosed with asthma, prescribed inhaler'")
        st.markdown("- 'Ear infection, antibiotic drops needed'")
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Enter Medical Information")
        
        # Text input
        medical_text = st.text_area(
            "Enter medical information from doctor visit:",
            height=200,
            placeholder="Example: The patient has strep throat and needs to take antibiotics twice daily for 10 days..."
        )
        
        if st.button("🪄 Create Storybook", type="primary") and medical_text:
            with st.spinner("🪄 Creating your storybook..."):
                try:
                    story = st.session_state.translator.translate_to_storybook(medical_text)
                    
                    if story:
                        formatted_story = st.session_state.formatter.format_storybook(story, story_style)
                        st.session_state.stories.append({
                            'original': medical_text,
                            'story': formatted_story,
                            'timestamp': st.session_state.get('timestamp', 'Now')
                        })
                        st.success("📚 Storybook created!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to create storybook. Please check your API key and try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Sample buttons for quick testing
        st.subheader("🚀 Quick Test Examples")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🦠 Strep Throat Example"):
                sample_text = "The patient has strep throat caused by bacterial infection. They need to take amoxicillin antibiotics twice daily for 10 days. Rest and plenty of fluids are recommended."
                st.session_state['sample_text'] = sample_text
                
        with col_b:
            if st.button("🩻 X-ray Example"):
                sample_text = "The child needs an X-ray of their left arm to check for a possible fracture after falling off their bike. The procedure is painless and takes only a few minutes."
                st.session_state['sample_text'] = sample_text
        
        # Display sample text if selected
        if 'sample_text' in st.session_state:
            st.text_area("Sample text loaded:", st.session_state['sample_text'], height=100)
            if st.button("🪄 Create Story from Sample"):
                with st.spinner("🪄 Creating your storybook..."):
                    try:
                        story = st.session_state.translator.translate_to_storybook(st.session_state['sample_text'])
                        if story:
                            formatted_story = st.session_state.formatter.format_storybook(story, story_style)
                            st.session_state.stories.append({
                                'original': st.session_state['sample_text'],
                                'story': formatted_story,
                                'timestamp': 'Sample'
                            })
                            del st.session_state['sample_text']
                            st.success("📚 Sample storybook created!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.header("📚 Your Storybooks")
        
        if st.session_state.stories:
            # Show latest story
            latest_story = st.session_state.stories[-1]
            st.markdown(latest_story['story'])
            
            # Add interactive elements
            if st.checkbox("🎨 Add Interactive Elements"):
                interactive_story = st.session_state.formatter.add_interactive_elements(latest_story['story'])
                st.markdown("---")
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
                    file_name=f"medical_storybook.md",
                    mime="text/markdown"
                )
            
            # Clear stories
            if st.button("🗑️ Clear All Stories"):
                st.session_state.stories = []
                st.rerun()
        else:
            st.info("👈 Enter medical information to create your first storybook!")
            
            # Show example output
            st.subheader("📖 Example Output")
            st.markdown("""
            **🌟 The Brave Throat Defenders 🌟**
            
            🌈 Once upon a time, in the magical kingdom of your throat, some sneaky germs called "strep bacteria" decided to cause trouble. These tiny troublemakers were making your throat feel scratchy and sore, like having a bunch of prickly thorns in a beautiful garden.
            
            📖 But don't worry! The wise doctor discovered these sneaky germs and called upon the superhero medicine called "Amoxicillin" to help. This amazing medicine is like a team of brave knights who march into your throat twice every day to chase away the bad germs.
            
            💝 For 10 whole days, these medicine knights will work hard to make your throat feel better. While they're working, you can help them by drinking lots of water (like giving them magical energy) and getting plenty of rest (so they can focus on their important mission). Soon, your throat will be happy and healthy again!
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Made with ❤️ to help make medical visits less scary for kids*")

if __name__ == "__main__":
    main()
