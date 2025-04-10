import re
from typing import Dict, List, Protocol, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from constants import COMMON_WORDS

# Value Object Pattern - immutable content representation
@dataclass(frozen=True)
class ContentContext:
    """Immutable representation of content with context for reduction"""
    text: str
    max_length: int
    patterns: Dict[str, str]
    
    @property
    def length(self) -> int:
        return len(self.text)
    
    @property
    def is_within_limits(self) -> bool:
        return self.length <= self.max_length
    
    @property
    def remaining_chars(self) -> int:
        """Calculate remaining characters, reserving space for notice"""
        return self.max_length - 100  # Reserve 100 chars for notice
    
    def with_text(self, new_text: str) -> 'ContentContext':
        """Create new context with updated text"""
        return ContentContext(
            text=new_text,
            max_length=self.max_length,
            patterns=self.patterns
        )

# Strategy Pattern - define interface for reduction strategies
class ReductionStrategy(Protocol):
    """Interface for content reduction strategies"""
    def reduce(self, context: ContentContext) -> ContentContext:
        """Apply reduction strategy to content"""
        ...

# Chain of Responsibility Pattern
class ReductionPipeline:
    """Chain of responsibility for content reduction"""
    
    def __init__(self, strategies: List[ReductionStrategy] = None):
        self.strategies = strategies or []
    
    def add_strategy(self, strategy: ReductionStrategy) -> 'ReductionPipeline':
        """Add a reduction strategy to the pipeline"""
        self.strategies.append(strategy)
        return self
    
    def process(self, context: ContentContext) -> ContentContext:
        """Process content through strategies until it fits or all strategies applied"""
        current = context
        
        for strategy in self.strategies:
            if current.is_within_limits:
                break
            current = strategy.reduce(current)
            
        return current

# Concrete Reduction Strategies

class HeaderPreservationStrategy:
    """Preserves headers and other high-priority elements"""
    
    def reduce(self, context: ContentContext) -> ContentContext:
        if context.is_within_limits:
            return context
            
        paragraphs = re.split(r'\n\n+', context.text)
        high_priority = []
        normal_paragraphs = []
        remaining_chars = context.remaining_chars
        
        # Categorize paragraphs
        for para in paragraphs:
            if not para.strip():
                continue
                
            # Check if paragraph is a header, code block, etc.
            if (re.search(context.patterns['headers'], para, re.MULTILINE) or 
                re.search(context.patterns['code_blocks'], para) or
                para.strip().startswith('>')):
                high_priority.append(para)
            else:
                normal_paragraphs.append(para)
        
        # Add high priority paragraphs
        result_parts = []
        for para in high_priority:
            if len(para) <= remaining_chars:
                result_parts.append(para)
                remaining_chars -= len(para) + 2  # +2 for the '\n\n'
            else:
                # Try to include headers even if paragraph doesn't fit
                lines = para.split('\n')
                for line in lines:
                    if re.match(context.patterns['headers'], line) and len(line) <= remaining_chars:
                        result_parts.append(line)
                        remaining_chars -= len(line) + 1
        
        # Reconstruct preserved content and add remaining paragraphs back for further processing
        preserved_content = '\n\n'.join(result_parts)
        remaining_paragraphs = '\n\n'.join(normal_paragraphs)
        
        # Return both preserved content and pending content for further reduction
        if preserved_content:
            return context.with_text(preserved_content + "\n\n" + remaining_paragraphs)
        else:
            return context.with_text(remaining_paragraphs)

class ListReductionStrategy:
    """Reduces list content while preserving structure"""
    
    def reduce(self, context: ContentContext) -> ContentContext:
        if context.is_within_limits:
            return context
            
        paragraphs = re.split(r'\n\n+', context.text)
        result_parts = []
        remaining_chars = context.remaining_chars
        
        for para in paragraphs:
            if remaining_chars <= 0:
                break
                
            # Check if it's a list paragraph - more aggressive detection including multi-line lists
            is_list = (re.search(context.patterns['bullets'], para, re.MULTILINE) or 
                       re.search(context.patterns['numbered'], para, re.MULTILINE) or
                       len(re.findall(r'^\s*[-"\'*•]\s+.*$', para, re.MULTILINE)) > 3)  # Detect lists with quotes
            
            if is_list:
                # Process list paragraph
                lines = para.split('\n')
                
                # Extract list items with better pattern matching for quoted items
                list_items = []
                current_item = ""
                
                for line in lines:
                    # Check for various list item formats including quoted items
                    list_marker_match = re.match(r'^(\s*[-*•]\s+|"\s*|\'|^\s*\d+\.\s+)(.*)', line)
                    
                    if list_marker_match:
                        # If we have a previous item being built, add it
                        if current_item:
                            list_items.append(current_item.strip())
                            current_item = ""
                        
                        content = list_marker_match.group(2)
                        current_item = content
                    else:
                        # This might be a continuation of the previous item
                        if line.strip() and current_item:
                            current_item += " " + line.strip()
                        elif line.strip():
                            # New content but not a list marker - might be a non-formatted list
                            list_items.append(line.strip())
                
                # Add the last item if there is one
                if current_item:
                    list_items.append(current_item.strip())
                
                # Detect repetitive structures or patterns to compress further
                if list_items and len(list_items) > 3:
                    # Try to find common patterns
                    patterns = self._find_patterns(list_items)
                    if patterns:
                        sample_items = [list_items[0], list_items[1], list_items[2]]
                        formatted = f"List of {len(list_items)} similar items showing pattern: {patterns}. Examples: {' | '.join(sample_items)}..."
                        if len(formatted) <= remaining_chars:
                            result_parts.append(formatted)
                            remaining_chars -= len(formatted) + 2
                            continue
                
                # Normal list processing when no patterns found or pattern summary is too long
                # Filter to keep only important items plus examples
                if list_items:
                    # Always include some examples (first and last)
                    sample_size = min(3, len(list_items))
                    samples = []
                    
                    # Take beginning samples
                    samples.extend(list_items[:sample_size])
                    
                    # Take end samples if list is long
                    if len(list_items) > 6:
                        samples.append("...")
                        samples.extend(list_items[-1:])
                    
                    # Add count if many items
                    if len(list_items) > 4:
                        prefix = f"List ({len(list_items)} items): "
                    else:
                        prefix = "List: "
                    
                    combined = " | ".join(samples)
                    formatted = prefix + combined
                    
                    if len(formatted) <= remaining_chars:
                        result_parts.append(formatted)
                        remaining_chars -= len(formatted) + 2
                    elif list_items and len(prefix + list_items[0]) <= remaining_chars:
                        # If too long, just keep count and first item
                        result_parts.append(f"List ({len(list_items)} items): {list_items[0]}...")
                        remaining_chars -= len(prefix + list_items[0]) + 5  # +5 for "..."
            else:
                # Keep non-list paragraphs for further processing
                if len(para) <= remaining_chars:
                    result_parts.append(para)
                    remaining_chars -= len(para) + 2
        
        return context.with_text('\n\n'.join(result_parts))
    
    def _find_patterns(self, items: List[str]) -> str:
        """Identify common patterns in list items"""
        # Look for common prefixes/suffixes
        common_prefixes = []
        common_suffixes = []
        
        # Check for items in quotes
        quote_count = len([item for item in items if item.startswith('"') or item.startswith("'")])
        if quote_count > len(items) * 0.7:  # If more than 70% are quoted
            common_prefixes.append("quoted statements")
        
        # Check for common phrasing at beginning
        prefixes = {}
        for item in items:
            words = item.strip('"\'').split()
            if words:
                first_2_words = ' '.join(words[:2]) if len(words) >= 2 else words[0]
                prefixes[first_2_words] = prefixes.get(first_2_words, 0) + 1
        
        for prefix, count in prefixes.items():
            if count > len(items) * 0.3:  # If more than 30% share prefix
                common_prefixes.append(f"often starting with '{prefix}'")
                break
        
        # Check for common endings
        suffixes = {}
        for item in items:
            words = item.strip('"\'').split()
            if words:
                last_word = words[-1]
                suffixes[last_word] = suffixes.get(last_word, 0) + 1
        
        for suffix, count in suffixes.items():
            if count > len(items) * 0.3:  # If more than 30% share suffix
                common_suffixes.append(f"often ending with '{suffix}'")
                break
        
        # Combine findings
        patterns = []
        if common_prefixes:
            patterns.extend(common_prefixes)
        if common_suffixes:
            patterns.extend(common_suffixes)
        
        return ", ".join(patterns) if patterns else ""

class ParagraphReductionStrategy:
    """Reduces normal paragraphs by keeping initial sentences"""
    
    def reduce(self, context: ContentContext) -> ContentContext:
        if context.is_within_limits:
            return context
            
        paragraphs = re.split(r'\n\n+', context.text)
        result_parts = []
        remaining_chars = context.remaining_chars
        
        for para in paragraphs:
            if remaining_chars <= 0:
                break
                
            # For normal paragraphs, prioritize those with key terms
            has_key_terms = bool(re.search(context.patterns['key_terms'], para, re.IGNORECASE))
            
            # Skip lists, they should be processed by ListReductionStrategy
            is_list = re.search(context.patterns['bullets'], para, re.MULTILINE) or re.search(context.patterns['numbered'], para, re.MULTILINE)
            if is_list:
                # Pass through list items unchanged
                if len(para) <= remaining_chars:
                    result_parts.append(para)
                    remaining_chars -= len(para) + 2
                continue
                
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
        
        return context.with_text('\n\n'.join(result_parts))

class TextCompressionStrategy:
    """Applies aggressive text compression techniques while maintaining some readability"""
    
    def reduce(self, context: ContentContext) -> ContentContext:
        if context.is_within_limits:
            return context
        
        text = context.text
        
        # 0. Preserve <ReferenceMaterials> tags by temporarily replacing them
        reference_materials = []
        
        def save_reference_materials(match):
            reference_materials.append(match.group(0))
            return f"__REF_MATERIAL_{len(reference_materials) - 1}__"
        
        # Find and temporarily replace <ReferenceMaterials> tags and their content
        text = re.sub(r'<ReferenceMaterials>[\s\S]*?</ReferenceMaterials>', save_reference_materials, text)
        
        # 1. Replace common words with abbreviations using the centralized dictionary
        for word, abbr in COMMON_WORDS.items():
            # Use word boundaries to avoid partial word replacements
            text = re.sub(rf'\b{word}\b', abbr, text, flags=re.IGNORECASE)
        
        # 2. Remove articles and some prepositions in non-essential contexts
        # Be careful not to damage readability too much
        for phrase in [" a ", " an ", " the ", " that ", " which ", " who ", " whom "]:
            text = text.replace(phrase, " ")
        
        # 3. Remove redundant spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # 4. Ensure paragraphs are separated by single newlines, not double
        text = re.sub(r'\n\n+', '\n', text)
        
        # 5. Restore the <ReferenceMaterials> tags
        for i, ref in enumerate(reference_materials):
            text = text.replace(f"__REF_MATERIAL_{i}__", ref)
        
        # 6. Add notice about compression
        if not text.endswith("[Content compressed]"):
            text += "\n[Content compressed]"
        
        return context.with_text(text)

class FinalFormattingStrategy:
    """Apply final formatting and add reduction notice"""
    
    def reduce(self, context: ContentContext) -> ContentContext:
        text = context.text
        
        # Add the reduction notice
        text += "\n\n[Content intelligently reduced to fit model context limits. Content prioritized by headers, key points, and important statements.]"
        
        # If still too long, truncate to fit max_length
        if len(text) > context.max_length:
            text = text[:context.max_length - 60] + "\n\n[Content truncated to fit model context limits.]"
            
        return context.with_text(text)

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
    
    context = ContentContext(content, max_length, patterns)
    
    pipeline = ReductionPipeline([
        HeaderPreservationStrategy(),
        ListReductionStrategy(),
        ParagraphReductionStrategy(),
        TextCompressionStrategy(), 
        FinalFormattingStrategy()
    ])
    
    reduced_context = pipeline.process(context)
    return reduced_context.text
