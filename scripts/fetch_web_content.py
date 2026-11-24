#!/usr/bin/env python3
"""
Web Information Retrieval and Synthesis System

Fetches web content, extracts key information, and synthesizes it into structured knowledge.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import re
import hashlib


class WebContentFetcher:
    """Fetches and extracts text content from web URLs."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebInfoRetriever/1.0)'
        })
    
    def fetch(self, url: str) -> Optional[str]:
        """Fetch text content from a URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Determine content type and extract text
            content_type = response.headers.get('content-type', '')
            
            if 'text/html' in content_type:
                return self._extract_text_from_html(response.text)
            elif 'text/plain' in content_type:
                return response.text
            elif 'application/json' in content_type:
                return self._extract_text_from_json(response.json())
            else:
                # For other content types, try to extract as text
                return response.text[:10000]  # Limit for non-text content
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _extract_text_from_html(self, html: str) -> str:
        """Extract main text content from HTML."""
        # Remove script and style elements
        soup = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert HTML entities
        soup = soup.replace('&nbsp;', ' ')
        soup = soup.replace('&lt;', '<')
        soup = soup.replace('&gt;', '>')
        soup = soup.replace('&amp;', '&')
        soup = soup.replace('&quot;', '"')
        soup = soup.replace('&apos;', "'")
        
        # Remove HTML tags, keep text
        text = re.sub(r'<[^>]+>', ' ', soup)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_text_from_json(self, data: Any) -> str:
        """Extract text from JSON data."""
        def _extract(obj: Any) -> str:
            if isinstance(obj, str):
                return obj
            elif isinstance(obj, (int, float, bool)):
                return str(obj)
            elif isinstance(obj, dict):
                parts = []
                for k, v in obj.items():
                    parts.append(f"{k}: {_extract(v)}")
                return " | ".join(parts)
            elif isinstance(obj, list):
                return " | ".join(_extract(item) for item in obj)
            else:
                return str(obj)
        
        return _extract(data)


class ContentSummarizer:
    """Extracts key information from fetched content."""
    
    @staticmethod
    def extract_headlines(text: str, max_headlines: int = 5) -> List[str]:
        """Extract headlines from text."""
        # Look for patterns like "# Heading" or "**Heading**"
        headlines = []
        
        # Markdown-style headlines
        markdown_headlines = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
        headlines.extend(markdown_headlines[:max_headlines])
        
        # Bold text that looks like headlines
        bold_headlines = re.findall(r'\*\*(.+?)\*\*', text)
        headlines.extend(bold_headlines[:max_headlines])
        
        # Sentence-based headlines (first few sentences)
        sentences = re.split(r'[.!?]+', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        headlines.extend(sentences[:max_headlines])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_headlines = []
        for h in headlines:
            h_normalized = h.lower().strip()
            if h_normalized and h_normalized not in seen:
                seen.add(h_normalized)
                unique_headlines.append(h)
        
        return unique_headlines[:max_headlines]
    
    @staticmethod
    def extract_key_facts(text: str, max_facts: int = 10) -> List[str]:
        """Extract key facts from text."""
        facts = []
        
        # Look for bullet points, numbered lists, and facts patterns
        bullet_patterns = [
            r'^\s*[-*]\s+(.+)$',
            r'^\s*\d+\.\s+(.+)$',
            r'^\s*•\s+(.+)$'
        ]
        
        for pattern in bullet_patterns:
            facts.extend(re.findall(pattern, text, re.MULTILINE))
        
        # Look for "key", "important", "critical", "note" patterns
        fact_patterns = [
            r'Key\s+(?:point|fact):\s*(.+)$',
            r'Important\s+(?:point|fact):\s*(.+)$',
            r'Critical\s+(?:point|fact):\s*(.+)$',
            r'Note:\s*(.+)$'
        ]
        
        for pattern in fact_patterns:
            facts.extend(re.findall(pattern, text, re.MULTILINE))
        
        # Extract first sentences that look like facts
        sentences = re.split(r'[.!?]+', text.strip())
        for sentence in sentences[:max_facts]:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                facts.append(sentence)
        
        # Remove duplicates
        seen = set()
        unique_facts = []
        for f in facts:
            f_normalized = f.lower().strip()
            if f_normalized and f_normalized not in seen:
                seen.add(f_normalized)
                unique_facts.append(f)
        
        return unique_facts[:max_facts]
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract dates from text."""
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # ISO format
            r'\b\d{2}/\d{2}/\d{4}\b',  # MM/DD/YYYY
            r'\b\d{4}/\d{2}/\d{2}\b',  # YYYY/MM/DD
            r'\b\d{2} \w+ \d{4}\b',   # DD Month YYYY
            r'\b\d{1,2}st|nd|rd|th \w+ \d{4}\b'  # 1st Jan 2024
        ]
        
        dates = set()
        for pattern in date_patterns:
            dates.update(re.findall(pattern, text))
        
        return sorted(list(dates))
    
    @staticmethod
    def extract_entities(text: str) -> List[str]:
        """Extract potential entities (capitalized words, organizations, etc.)."""
        entities = []
        
        # Capitalized words (potential proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(capitalized[:20])
        
        # Organizations (e.g., "Company ABC")
        org_pattern = r'\b[A-Z][a-zA-Z&\s]+\b'
        orgs = re.findall(org_pattern, text)
        entities.extend(orgs[:15])
        
        # Remove duplicates
        seen = set()
        unique_entities = []
        for e in entities:
            e_normalized = e.lower()
            if e_normalized and e_normalized not in seen:
                seen.add(e_normalized)
                unique_entities.append(e)
        
        return unique_entities


class KnowledgeBaseStorage:
    """Stores synthesized information in a structured format."""
    
    def __init__(self, storage_file: str = 'scripts/knowledge_base.json'):
        self.storage_file = storage_file
        self.data = self._load_storage()
    
    def _load_storage(self) -> Dict[str, Any]:
        """Load existing storage or create new structure."""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'metadata': {
                    'created_at': datetime.utcnow().isoformat(),
                    'version': '1.0'
                },
                'sources': {},
                'entries': []
            }
    
    def _save_storage(self) -> None:
        """Save storage to file."""
        self.data['metadata']['last_updated'] = datetime.utcnow().isoformat()
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_entry(self, source_url: str, title: str, content_summary: str,
                  headlines: List[str], key_facts: List[str],
                  entities: List[str], extracted_at: Optional[str] = None) -> str:
        """Add a new knowledge entry."""
        if extracted_at is None:
            extracted_at = datetime.utcnow().isoformat()
        
        # Create entry
        entry = {
            'id': hashlib.md5(f"{source_url}:{title}".encode()).hexdigest()[:12],
            'source_url': source_url,
            'title': title,
            'content_summary': content_summary,
            'headlines': headlines,
            'key_facts': key_facts,
            'entities': entities,
            'extracted_at': extracted_at
        }
        
        # Add to entries
        self.data['entries'].append(entry)
        
        # Add source reference
        if source_url not in self.data['sources']:
            self.data['sources'][source_url] = {
                'first_seen': extracted_at,
                'entry_count': 0
            }
        self.data['sources'][source_url]['entry_count'] += 1
        
        # Save
        self._save_storage()
        
        return entry['id']
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search entries by query."""
        query_lower = query.lower()
        results = []
        
        for entry in self.data['entries']:
            # Search in title, content, headlines, facts, entities
            text = f"{entry['title']} {entry['content_summary']} {' '.join(entry['headlines'])} {' '.join(entry['key_facts'])} {' '.join(entry['entities'])}"
            
            # Simple term matching
            score = 0
            for term in query_lower.split():
                if term in text.lower():
                    score += 1
            
            if score > 0:
                results.append({
                    'entry': entry,
                    'score': score
                })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return [r['entry'] for r in results[:limit]]
    
    def get_by_source(self, source_url: str) -> List[Dict[str, Any]]:
        """Get all entries from a specific source."""
        return [e for e in self.data['entries'] if e['source_url'] == source_url]
    
    def list_sources(self) -> List[str]:
        """List all unique sources."""
        return list(self.data['sources'].keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        return {
            'total_entries': len(self.data['entries']),
            'total_sources': len(self.data['sources']),
            'sources': list(self.data['sources'].keys()),
            'metadata': self.data['metadata']
        }


def main():
    """Demonstrate the system with a test run."""
    print("Web Information Retrieval and Synthesis System")
    print("=" * 50)
    
    # Test URLs
    test_urls = [
        'https://www.wikipedia.org',
        'https://www.python.org',
        'https://github.com',
        'https://example.com'
    ]
    
    # Initialize components
    fetcher = WebContentFetcher(timeout=15)
    summarizer = ContentSummarizer()
    storage = KnowledgeBaseStorage()
    
    # Fetch and process each URL
    for url in test_urls:
        print(f"\nFetching: {url}")
        content = fetcher.fetch(url)
        
        if content:
            print(f"  Fetched {len(content)} characters")
            
            # Extract information
            headlines = summarizer.extract_headlines(content)
            key_facts = summarizer.extract_key_facts(content)
            entities = summarizer.extract_entities(content)
            
            print(f"  Extracted {len(headlines)} headlines")
            print(f"  Extracted {len(key_facts)} key facts")
            print(f"  Extracted {len(entities)} entities")
            
            # Store in knowledge base
            entry_id = storage.add_entry(
                source_url=url,
                title=f"Web Page: {url}",
                content_summary=content[:500] + "...",
                headlines=headlines[:3],
                key_facts=key_facts[:5],
                entities=entities[:10]
            )
            print(f"  Stored as entry {entry_id}")
    
    # Show search functionality
    print("\n" + "=" * 50)
    print("Search Examples")
    print("=" * 50)
    
    queries = ['python', 'github', 'web', 'example']
    for query in queries:
        results = storage.search(query, limit=3)
        print(f"\nQuery: '{query}'")
        print(f"  Found {len(results)} entries")
        for result in results:
            print(f"    - {result['title'][:60]}...")
    
    # Show statistics
    print("\n" + "=" * 50)
    print("Knowledge Base Statistics")
    print("=" * 50)
    stats = storage.get_stats()
    print(f"Total entries: {stats['total_entries']}")
    print(f"Total sources: {stats['total_sources']}")
    print(f"Sources: {', '.join(stats['sources'])}")


if __name__ == '__main__':
    main()
