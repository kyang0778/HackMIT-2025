import re
from typing import Dict, List, Optional

class StorybookFormatter:
    def __init__(self):
        """Initialize the storybook formatter with styling options"""
        self.story_templates = {
            "adventure": "🌟 **{title}** 🌟\n\n{content}",
            "friendly": "📚 **{title}** 📚\n\n{content}",
            "magical": "✨ **{title}** ✨\n\n{content}",
            "superhero": "🦸 **{title}** 🦸\n\n{content}"
        }
        
    def format_storybook(self, story_text: str, style: str = "friendly") -> str:
        """
        Format the story text with appropriate styling and structure
        
        Args:
            story_text: The story content from Claude
            style: The visual style to apply
            
        Returns:
            Formatted storybook text
        """
        try:
            # Extract title if present
            lines = story_text.strip().split('\n')
            title = "Your Health Story"
            content = story_text
            
            # Look for a title in the first few lines
            for i, line in enumerate(lines[:3]):
                if line.strip() and (line.startswith('#') or line.isupper() or 'title' in line.lower()):
                    title = line.strip('#').strip()
                    content = '\n'.join(lines[i+1:]).strip()
                    break
            
            # Clean up the content
            content = self._format_paragraphs(content)
            
            # Apply template
            template = self.story_templates.get(style, self.story_templates["friendly"])
            formatted_story = template.format(title=title, content=content)
            
            return formatted_story
            
        except Exception as e:
            print(f"Error formatting storybook: {e}")
            return story_text
            
    def _format_paragraphs(self, text: str) -> str:
        """Format paragraphs with proper spacing and emoji"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        formatted_paragraphs = []
        for i, paragraph in enumerate(paragraphs):
            # Add some visual elements
            if i == 0:
                paragraph = f"🌈 {paragraph}"
            elif i == len(paragraphs) - 1:
                paragraph = f"💝 {paragraph}"
            else:
                paragraph = f"📖 {paragraph}"
                
            formatted_paragraphs.append(paragraph)
            
        return '\n\n'.join(formatted_paragraphs)
        
    def create_chapter_format(self, stories: List[str]) -> str:
        """
        Create a multi-chapter storybook format
        
        Args:
            stories: List of individual stories
            
        Returns:
            Combined storybook with chapters
        """
        if not stories:
            return ""
            
        chapter_book = "📚 **Your Complete Health Storybook** 📚\n\n"
        
        for i, story in enumerate(stories, 1):
            chapter_book += f"## Chapter {i}\n\n{story}\n\n---\n\n"
            
        return chapter_book
        
    def add_interactive_elements(self, story: str) -> str:
        """
        Add interactive elements like questions and activities
        
        Args:
            story: The formatted story
            
        Returns:
            Story with interactive elements
        """
        interactive_story = story + "\n\n"
        
        # Add reflection questions
        interactive_story += "🤔 **Think About It:**\n"
        interactive_story += "• How do you think the characters in this story felt?\n"
        interactive_story += "• What questions do you have about your visit?\n"
        interactive_story += "• What was your favorite part of this story?\n\n"
        
        # Add activity suggestion
        interactive_story += "🎨 **Fun Activity:**\n"
        interactive_story += "Draw a picture of the helpful characters from your story!\n\n"
        
        return interactive_story
