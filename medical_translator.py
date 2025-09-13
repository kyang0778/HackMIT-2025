import anthropic
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class MedicalTranslator:
    def __init__(self):
        """Initialize the Claude API client"""
        try:
            # Try new version first
            self.client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            self.use_messages_api = True
        except TypeError:
            # Fall back to older version
            self.client = anthropic.Client(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            self.use_messages_api = False
        
    def translate_to_storybook(self, medical_text: str) -> Optional[str]:
        """
        Translate medical diagnosis/terminology into kid-friendly storybook format
        
        Args:
            medical_text: The medical text to translate
            
        Returns:
            Kid-friendly storybook version or None if error
        """
        try:
            prompt = f"""
You are a medical translator who specializes in converting complex medical information into engaging, age-appropriate storybooks for elementary school children (ages 6-10). 

Your task is to take the following medical text and transform it into a friendly, reassuring story that:
1. Uses simple, elementary school vocabulary
2. Explains medical concepts through relatable analogies and metaphors
3. Creates a narrative structure with characters (like brave cells, helpful medicines, etc.)
4. Maintains medical accuracy while being reassuring and non-scary
5. Includes positive, hopeful messaging
6. Uses a warm, caring tone

Medical text to translate:
"{medical_text}"

Please create a short storybook passage (2-3 paragraphs) that explains this medical information in a way that would help a child understand what's happening with their health. Make it engaging and comforting.

Format your response as a story with a title.
"""

            if self.use_messages_api:
                message = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                return message.content[0].text
            else:
                message = self.client.completions.create(
                    model="claude-2",
                    max_tokens_to_sample=1000,
                    temperature=0.7,
                    prompt=f"\n\nHuman: {prompt}\n\nAssistant:"
                )
                return message.completion
            
        except Exception as e:
            print(f"Error translating medical text: {e}")
            return None
            
    def get_medical_explanation(self, medical_text: str) -> Optional[str]:
        """
        Get a simple medical explanation suitable for parents
        
        Args:
            medical_text: The medical text to explain
            
        Returns:
            Parent-friendly explanation or None if error
        """
        try:
            prompt = f"""
Please provide a clear, simple explanation of the following medical information that would be appropriate for parents to understand. Focus on:
1. What this means in plain language
2. What to expect
3. Any important next steps or considerations
4. Reassuring information where appropriate

Medical text:
"{medical_text}"

Please provide a concise, informative explanation.
"""

            if self.use_messages_api:
                message = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=800,
                    temperature=0.3,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                return message.content[0].text
            else:
                message = self.client.completions.create(
                    model="claude-2",
                    max_tokens_to_sample=800,
                    temperature=0.3,
                    prompt=f"\n\nHuman: {prompt}\n\nAssistant:"
                )
                return message.completion
            
        except Exception as e:
            print(f"Error getting medical explanation: {e}")
            return None
