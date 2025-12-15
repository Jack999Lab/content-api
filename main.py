#!/usr/bin/env python3
"""
Command line interface for AI Content Generator
"""

import json
import sys
from app import SimpleContentGenerator

def main():
    if len(sys.argv) > 1:
        try:
            input_data = json.loads(sys.argv[1])
            
            generator = SimpleContentGenerator()
            
            result = generator.generate_content(
                topic=input_data.get('topic', ''),
                keywords=input_data.get('keywords', ''),
                tone=input_data.get('tone', 'professional'),
                length=int(input_data.get('length', 500))
            )
            
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }))
    else:
        print("Usage: python main.py '{\"topic\":\"Your Topic\"}'")

if __name__ == "__main__":
    main()
