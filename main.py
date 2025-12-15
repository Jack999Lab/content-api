#!/usr/bin/env python3
"""
Simple AI Content Generator API for GitHub
Run: python main.py '{"topic":"AI in Healthcare","keywords":"ai,healthcare"}'
"""

import sys
import json
import random
import re
from typing import Dict, List, Tuple
import requests
from bs4 import BeautifulSoup

class SimpleAIGenerator:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
    
    def get_random_user_agent(self):
        return random.choice(self.user_agents)
    
    def fetch_web_data(self, query: str) -> str:
        """Google থেকে ডেটা ফেচ করুন"""
        try:
            url = f"https://www.google.com/search?q={query}&num=5"
            headers = {'User-Agent': self.get_random_user_agent()}
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract snippets
            snippets = []
            for g in soup.find_all('div', {'class': 'VwiC3b'}):
                text = g.get_text()
                if text and len(text) > 20:
                    snippets.append(text)
            
            return ' '.join(snippets[:3]) if snippets else ""
        except:
            return ""
    
    def generate_content(self, topic: str, keywords: str = "", tone: str = "professional", length: int = 500) -> Dict:
        """মেইন কন্টেন্ট জেনারেশন ফাংশন"""
        
        # 1. Research
        research = self.fetch_web_data(topic)
        
        # 2. Generate structure
        content = self.create_structure(topic, keywords, research, tone)
        
        # 3. Adjust length
        content = self.adjust_length(content, length)
        
        # 4. Humanize
        content = self.humanize_content(content, tone)
        
        # 5. Calculate metrics
        word_count = len(content.split())
        seo_score = self.calculate_seo_score(content, keywords)
        plagiarism_score = self.check_plagiarism(content)
        
        return {
            "content": content,
            "word_count": word_count,
            "seo_score": seo_score,
            "plagiarism_score": plagiarism_score,
            "topic": topic,
            "keywords": keywords
        }
    
    def create_structure(self, topic: str, keywords: str, research: str, tone: str) -> str:
        """কন্টেন্ট স্ট্রাকচার তৈরি করুন"""
        
        sections = []
        
        # Introduction
        intro_templates = [
            f"# {topic}\n\nIn today's rapidly evolving world, {topic.lower()} has become increasingly important. ",
            f"# Understanding {topic}\n\n{topic} represents a significant development in modern technology. ",
            f"# {topic}: A Comprehensive Guide\n\nThe field of {topic.lower()} is transforming industries worldwide. "
        ]
        
        intro = random.choice(intro_templates)
        
        if research:
            sentences = research.split('. ')
            if sentences:
                intro += sentences[0] + ". "
        
        sections.append(intro)
        
        # Key points
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(',')]
            sections.append("\n## Key Features\n")
            for i, keyword in enumerate(keyword_list[:5], 1):
                sections.append(f"{i}. **{keyword.title()}**: This aspect of {topic.lower()} is particularly important. ")
        
        # Body content
        body_templates = [
            "\n## Main Benefits\n\nThe primary advantages of {topic} include improved efficiency and better results. ",
            "\n## Implementation Strategies\n\nSuccessful implementation of {topic} requires careful planning. ",
            "\n## Future Outlook\n\nLooking ahead, {topic} is expected to continue its growth trajectory. "
        ]
        
        for template in random.sample(body_templates, min(2, len(body_templates))):
            sections.append(template.format(topic=topic))
        
        # Conclusion
        conclusion = f"\n## Conclusion\n\nIn summary, {topic} offers substantial benefits for organizations and individuals alike. "
        conclusion += f"By understanding and implementing {topic.lower()}, you can achieve better outcomes. "
        
        sections.append(conclusion)
        
        return ''.join(sections)
    
    def adjust_length(self, content: str, target_words: int) -> str:
        """কন্টেন্টের length adjust করুন"""
        words = content.split()
        
        if len(words) >= target_words:
            return ' '.join(words[:target_words])
        
        # If content is too short, add more
        while len(words) < target_words:
            additional = [
                "This demonstrates the practical applications. ",
                "Many experts agree with this perspective. ",
                "The evidence supports these conclusions. ",
                "Further research continues in this area. "
            ]
            words.extend(random.choice(additional).split())
        
        return ' '.join(words[:target_words])
    
    def humanize_content(self, content: str, tone: str) -> str:
        """কন্টেন্টকে মানবিক করুন"""
        
        # Replace robotic phrases
        replacements = {
            'is important': 'plays a crucial role',
            'very good': 'exceptionally beneficial',
            'many people': 'numerous individuals',
            'in order to': 'to',
            'due to the fact that': 'because'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Adjust tone
        if tone == "casual":
            content = content.replace('therefore', 'so')
            content = content.replace('however', 'but')
            content = content.replace('individuals', 'people')
        elif tone == "academic":
            content = content.replace('so', 'therefore')
            content = content.replace('but', 'however')
            content = content.replace('get', 'obtain')
        
        # Add some natural variations
        sentences = content.split('. ')
        if len(sentences) > 3:
            # Occasionally add transitional words
            transitions = ['Moreover,', 'Additionally,', 'Furthermore,']
            for i in range(1, len(sentences) - 1):
                if random.random() > 0.7:
                    sentences[i] = random.choice(transitions) + ' ' + sentences[i]
        
        return '. '.join(sentences)
    
    def calculate_seo_score(self, content: str, keywords: str) -> int:
        """এসইও স্কোর ক্যালকুলেট করুন"""
        score = 50
        
        # Word count
        words = content.split()
        if len(words) > 300:
            score += 20
        elif len(words) > 150:
            score += 10
        
        # Headings
        headings = content.count('#')
        if headings >= 2:
            score += 10
        
        # Keywords
        if keywords:
            keyword_list = [k.strip().lower() for k in keywords.split(',')]
            for keyword in keyword_list:
                if keyword in content.lower():
                    score += 5
        
        # Paragraphs
        paragraphs = content.count('\n\n')
        if paragraphs >= 3:
            score += 10
        
        return min(score, 100)
    
    def check_plagiarism(self, content: str) -> float:
        """বেসিক প্লেগরিজম চেক"""
        sentences = content.split('. ')
        unique_sentences = set(sentences)
        
        if len(sentences) == 0:
            return 100.0
        
        uniqueness = len(unique_sentences) / len(sentences) * 100
        return round(uniqueness, 2)

def main():
    """মেইন ফাংশন - কমান্ড লাইন থেকে কল করলে"""
    if len(sys.argv) > 1:
        try:
            # Parse input JSON
            input_data = json.loads(sys.argv[1])
            
            # Initialize generator
            generator = SimpleAIGenerator()
            
            # Generate content
            result = generator.generate_content(
                topic=input_data.get('topic', ''),
                keywords=input_data.get('keywords', ''),
                tone=input_data.get('tone', 'professional'),
                length=int(input_data.get('length', 500))
            )
            
            # Add success flag
            result['success'] = True
            
            # Output as JSON
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }))
    else:
        # Test mode
        generator = SimpleAIGenerator()
        result = generator.generate_content(
            topic="Artificial Intelligence",
            keywords="ai, machine learning, technology",
            tone="professional",
            length=300
        )
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()