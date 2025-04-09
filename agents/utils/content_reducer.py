import re
from typing import Dict, List

def reduce_content(content: str, max_length: int) -> str:
    """
    Intelligently reduce content size while maintaining readability using regex patterns
    
    Args:
        content: The original content text
        max_length: Maximum allowed length
    
    Returns:
        Reduced content that fits within max_length
    """
    if len(content) <= max_length:
        return content
        
    # Define content importance patterns
    patterns = {
        'headers': r'^#+\s+.*$',                              # Markdown headers
        'bullets': r'^\s*[-*•]\s+.*$',                        # Bullet points
        'numbered': r'^\s*\d+\.\s+.*$',                       # Numbered lists
        'code_blocks': r'```[\s\S]*?```',                     # Code blocks
        'key_terms': r'(important|note|warning|essential|critical|key|remember|significant)',  # Key indicator words
        'definitions': r'^.{1,50}:\s+.+$'                     # Short definitions
    }
    
    # Reserve space for truncation notice
    remaining_chars = max_length - 100
    result_parts = []
    
    # Step 1: Split content into paragraphs
    paragraphs = re.split(r'\n\n+', content)
    
    # Step 2: First pass - keep high priority elements intact
    high_priority_paragraphs = []
    normal_paragraphs = []
    
    for para in paragraphs:
        # Skip empty paragraphs
        if not para.strip():
            continue
            
        # Check if paragraph is a header, code block, etc.
        if (re.search(patterns['headers'], para, re.MULTILINE) or 
            re.search(patterns['code_blocks'], para) or
            para.strip().startswith('>')):  # Blockquotes
            high_priority_paragraphs.append(para)
        else:
            normal_paragraphs.append(para)
    
    # Step 3: Add all high priority paragraphs first (if they fit)
    for para in high_priority_paragraphs:
        if len(para) <= remaining_chars:
            result_parts.append(para)
            remaining_chars -= len(para) + 2  # +2 for the '\n\n'
        else:
            # Even if it doesn't fit completely, try to include headers
            lines = para.split('\n')
            for line in lines:
                if re.match(patterns['headers'], line) and len(line) <= remaining_chars:
                    result_parts.append(line)
                    remaining_chars -= len(line) + 1
    
    # Step 4: Process normal paragraphs more aggressively
    for para in normal_paragraphs:
        if remaining_chars <= 0:
            break
            
        # Check for bullets or numbered lists to preserve structure
        if re.search(patterns['bullets'], para, re.MULTILINE) or re.search(patterns['numbered'], para, re.MULTILINE):
            # For lists, keep only first item or items that contain key terms
            lines = para.split('\n')
            important_lines = [
                line for line in lines if (
                    re.search(patterns['key_terms'], line, re.IGNORECASE) or 
                    line == lines[0]  # Keep first list item
                )
            ]
            
            shortened = '\n'.join(important_lines)
            if len(shortened) <= remaining_chars:
                result_parts.append(shortened)
                remaining_chars -= len(shortened) + 2
            else:
                # If it doesn't fit, just add the first item
                if lines and len(lines[0]) <= remaining_chars:
                    result_parts.append(lines[0])
                    remaining_chars -= len(lines[0]) + 2
        else:
            # For normal paragraphs, prioritize those with key terms
            has_key_terms = bool(re.search(patterns['key_terms'], para, re.IGNORECASE))
            
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', para)
            
            # Take at least first sentence, more if it's an important paragraph
            if has_key_terms and len(sentences) > 1:
                # For important paragraphs, try to include more sentences
                num_sentences = min(3, len(sentences))
                shortened = ' '.join(sentences[:num_sentences])
            else:
                # For regular paragraphs, take just the first sentence
                shortened = sentences[0] if sentences else ''
            
            if shortened and len(shortened) <= remaining_chars:
                result_parts.append(shortened)
                remaining_chars -= len(shortened) + 2
    
    result = '\n\n'.join(result_parts)
    return result + "\n\n[Content intelligently reduced to fit model context limits. Content prioritized by headers, key points, and important statements.]"
