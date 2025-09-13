import streamlit as st
import os
from medical_translator import MedicalTranslator
from storybook_formatter import StorybookFormatter

# Page configuration with kid-friendly theme
st.set_page_config(
    page_title="🌈 My Medical Story Maker 🌈",
    page_icon="🏥📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for kid-friendly design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #FFE5F1 0%, #E5F3FF 50%, #F0FFE5 100%);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6B9D, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .big-title {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF6B9D, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        animation: rainbow 3s ease-in-out infinite;
    }
    
    @keyframes rainbow {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(180deg); }
    }
    
    .fun-box {
        background: linear-gradient(135deg, #FFE5F1, #E5F3FF);
        border: 3px solid #FF6B9D;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .parent-section {
        background: linear-gradient(135deg, #F0F8FF, #E6E6FA);
        border: 2px solid #4682B4;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .story-display {
        background: linear-gradient(135deg, #FFF8DC, #F0F8FF);
        border: 3px solid #32CD32;
        border-radius: 20px;
        padding: 25px;
        font-size: 18px;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'translator' not in st.session_state:
    st.session_state.translator = MedicalTranslator()
if 'formatter' not in st.session_state:
    st.session_state.formatter = StorybookFormatter()
if 'stories' not in st.session_state:
    st.session_state.stories = []
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'show_review' not in st.session_state:
    st.session_state.show_review = False

def main():
    # Fun animated title
    st.markdown('<h1 class="big-title">🌈 My Medical Story Maker 🌈</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #FF6B9D;">✨ Turn doctor visits into magical stories! ✨</p>', unsafe_allow_html=True)
    
    # Check API Key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ Please set your ANTHROPIC_API_KEY in Streamlit secrets")
        st.info("Go to your app settings and add ANTHROPIC_API_KEY to secrets")
        st.stop()
    
    # Sidebar for parent controls
    with st.sidebar:
        st.markdown('<div class="parent-section">', unsafe_allow_html=True)
        st.header("👨‍👩‍👧‍👦 Parent Controls")
        
        # API Key status
        st.success("✅ Story Magic Ready!")
        
        # Story style selection
        st.subheader("📖 Story Theme")
        story_style = st.selectbox(
            "Choose Adventure Type",
            ["friendly", "adventure", "magical", "superhero"],
            format_func=lambda x: {
                "friendly": "🐻 Friendly Friends",
                "adventure": "🗺️ Epic Adventure", 
                "magical": "✨ Magical Kingdom",
                "superhero": "🦸 Superhero Squad"
            }[x]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions for parents
        st.markdown('<div class="parent-section">', unsafe_allow_html=True)
        st.subheader("📋 Parent Guide")
        st.markdown("""
        **How it works:**
        1. 📝 Type medical information
        2. 👀 Review the text together
        3. ✨ Generate kid-friendly story
        4. 📚 Read and enjoy together!
        
        **Tips:**
        - Use simple, clear language
        - Review text before generating
        - Choose age-appropriate themes
        - Read stories together
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main interface with kid-friendly design
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="fun-box">', unsafe_allow_html=True)
        st.markdown("## 📝 Tell Me About Your Doctor Visit!")
        
        # Text input
        manual_text = st.text_area(
            "Parents: Enter medical information here:",
            height=200,
            placeholder="Example: The doctor said you have a sore throat and need to take medicine twice a day for 10 days to feel better..."
        )
        
        if st.button("📋 Review This Text", type="primary") and manual_text:
            st.session_state.transcribed_text = manual_text
            st.session_state.show_review = True
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Review section for parents
        if st.session_state.show_review and st.session_state.transcribed_text:
            st.markdown('<div class="parent-section">', unsafe_allow_html=True)
            st.markdown("## 👨‍👩‍👧‍👦 Parent Review")
            st.markdown("**Please review the text before creating the story:**")
            
            # Editable text area for review
            reviewed_text = st.text_area(
                "Edit if needed:",
                value=st.session_state.transcribed_text,
                height=120,
                key="review_text"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✨ Create Magic Story!", type="primary"):
                    with st.spinner("🪄 Creating your magical story..."):
                        try:
                            story = st.session_state.translator.translate_to_storybook(reviewed_text)
                            
                            if story:
                                formatted_story = st.session_state.formatter.format_storybook(story, story_style)
                                st.session_state.stories.append({
                                    'original': reviewed_text,
                                    'story': formatted_story,
                                    'timestamp': "Now",
                                    'style': story_style
                                })
                                st.session_state.show_review = False
                                st.session_state.transcribed_text = ""
                                st.success("📚 Your story is ready!")
                                st.rerun()
                            else:
                                st.error("❌ Story magic failed. Check your API key!")
                        except Exception as e:
                            st.error(f"❌ Oops! Something went wrong: {str(e)}")
            
            with col_b:
                if st.button("🔄 Start Over"):
                    st.session_state.show_review = False
                    st.session_state.transcribed_text = ""
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick examples section
        if not st.session_state.show_review:
            st.markdown('<div class="fun-box">', unsafe_allow_html=True)
            st.markdown("## 🚀 Try These Fun Examples!")
            
            col_ex1, col_ex2 = st.columns(2)
            
            with col_ex1:
                if st.button("🦠 Sore Throat Story"):
                    sample_text = "The doctor said you have a sore throat caused by germs. You need to take special medicine called antibiotics twice every day for 10 days. Drink lots of water and get plenty of rest to feel better!"
                    st.session_state.transcribed_text = sample_text
                    st.session_state.show_review = True
                    st.rerun()
                    
            with col_ex2:
                if st.button("🩻 X-ray Adventure"):
                    sample_text = "We need to take a special picture called an X-ray of your arm to make sure the bone is okay after you fell. The X-ray machine is like a camera that can see inside your body. It doesn't hurt at all!"
                    st.session_state.transcribed_text = sample_text
                    st.session_state.show_review = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="fun-box">', unsafe_allow_html=True)
        st.markdown("## 📚 Your Magical Stories!")
        
        if st.session_state.stories:
            # Show latest story with fun styling
            latest_story = st.session_state.stories[-1]
            st.markdown('<div class="story-display">', unsafe_allow_html=True)
            st.markdown(latest_story['story'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Interactive elements
            if st.checkbox("🎨 Add Fun Activities!", value=True):
                interactive_story = st.session_state.formatter.add_interactive_elements(latest_story['story'])
                st.markdown('<div class="story-display">', unsafe_allow_html=True)
                st.markdown(interactive_story)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Story history
            if len(st.session_state.stories) > 1:
                st.markdown("### 📖 Your Story Collection")
                for i, story_data in enumerate(reversed(st.session_state.stories[:-1])):
                    theme_emoji = {
                        "friendly": "🐻", "adventure": "🗺️", 
                        "magical": "✨", "superhero": "🦸"
                    }.get(story_data.get('style', 'friendly'), '📚')
                    
                    with st.expander(f"{theme_emoji} Story {len(st.session_state.stories) - i - 1}"):
                        st.markdown('<div class="story-display">', unsafe_allow_html=True)
                        st.markdown(story_data['story'])
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options with kid-friendly design
            st.markdown("### 💾 Save Your Stories!")
            
            col_save1, col_save2 = st.columns(2)
            
            with col_save1:
                if st.button("📄 Make Story Book"):
                    all_stories = [story['story'] for story in st.session_state.stories]
                    complete_book = st.session_state.formatter.create_chapter_format(all_stories)
                    
                    st.download_button(
                        label="📥 Download Story Book",
                        data=complete_book,
                        file_name=f"my_medical_storybook.md",
                        mime="text/markdown"
                    )
            
            with col_save2:
                if st.button("🗑️ Clear All Stories"):
                    st.session_state.stories = []
                    st.rerun()
        else:
            # Welcome message with animations
            st.markdown("""
            <div class="story-display">
            <h3 style="text-align: center;">🌟 Welcome to Your Story Maker! 🌟</h3>
            
            <p style="font-size: 1.2rem; text-align: center;">
            👈 Type what the doctor told you, and I'll turn it into a fun story!
            </p>
            
            <div style="text-align: center; margin: 20px 0;">
            📝 ➡️ 👀 ➡️ ✨ ➡️ 📚
            </div>
            
            <p style="text-align: center; color: #FF6B9D;">
            <strong>Try the example buttons to see the magic! ✨</strong>
            </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show example output
            st.markdown("### 📖 Example Story")
            st.markdown("""
            <div class="story-display">
            <h4>🌟 The Brave Throat Defenders 🌟</h4>
            
            <p>🌈 Once upon a time, in the magical kingdom of your throat, some sneaky germs called "strep bacteria" decided to cause trouble. These tiny troublemakers were making your throat feel scratchy and sore, like having a bunch of prickly thorns in a beautiful garden.</p>
            
            <p>📖 But don't worry! The wise doctor discovered these sneaky germs and called upon the superhero medicine called "Amoxicillin" to help. This amazing medicine is like a team of brave knights who march into your throat twice every day to chase away the bad germs.</p>
            
            <p>💝 For 10 whole days, these medicine knights will work hard to make your throat feel better. While they're working, you can help them by drinking lots of water (like giving them magical energy) and getting plenty of rest (so they can focus on their important mission). Soon, your throat will be happy and healthy again!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fun footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
    <h3 style="color: #FF6B9D;">✨ Made with ❤️ to make doctor visits fun! ✨</h3>
    <p style="font-size: 1.1rem;">🌈 Every visit is a new adventure! 🌈</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
