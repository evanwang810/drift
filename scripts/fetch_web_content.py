#!/usr/bin/env python3
"""
Web Content Fetcher and Synthesizer

Fetches web content, extracts key information, and synthesizes it into a structured format.
"""

import argparse
import json
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


class WebContentFetcher:
    """Fetch and extract content from web pages."""

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebSynthesizer/1.0)'
        })

    def fetch_url(self, url):
        """Fetch content from a URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return {
                'success': True,
                'url': url,
                'status': response.status_code,
                'content': response.text,
                'encoding': response.encoding
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }

    def extract_text(self, html_content):
        """Extract readable text from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text
        text = soup.get_text(separator=' ', strip=True)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text[:10000]  # Limit to first 10KB for processing

    def extract_metadata(self, url, html_content):
        """Extract page metadata."""
        soup = BeautifulSoup(html_content, 'html.parser')

        metadata = {
            'url': url,
            'title': soup.find('title').get_text(strip=True) if soup.find('title') else '',
            'description': '',
            'keywords': [],
            'language': soup.get('lang') or ''
        }

        # Extract description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            metadata['description'] = meta_desc.get('content', '')

        # Extract keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            metadata['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]

        return metadata

    def summarize_content(self, text, max_length=500):
        """Create a summary of the content."""
        sentences = text.split('. ')
        summary = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) < max_length:
                summary.append(sentence)
                current_length += len(sentence)
            else:
                break

        return '. '.join(summary) + '.' if summary else text[:max_length]

    def fetch_and_process(self, url):
        """Fetch a URL and extract structured content."""
        fetch_result = self.fetch_url(url)

        if not fetch_result['success']:
            return {
                'status': 'error',
                'url': url,
                'error': fetch_result['error']
            }

        text = self.extract_text(fetch_result['content'])
        metadata = self.extract_metadata(url, fetch_result['content'])
        summary = self.summarize_content(text)

        return {
            'status': 'success',
            'url': url,
            'metadata': metadata,
            'text': text,
            'summary': summary
        }


def main():
    parser = argparse.ArgumentParser(
        description='Fetch and synthesize web content'
    )
    parser.add_argument('urls', nargs='+', help='One or more URLs to fetch')
    parser.add_argument('--output', '-o', default='synthesis_output.json',
                       help='Output JSON file path')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json',
                       help='Output format')
    parser.add_argument('--max-length', type=int, default=500,
                       help='Maximum summary length in characters')

    args = parser.parse_args()

    fetcher = WebContentFetcher()
    results = []

    for url in args.urls:
        result = fetcher.fetch_and_process(url)
        results.append(result)

    # Write output
    if args.format == 'json':
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    else:
        with open(args.output, 'w') as f:
            for result in results:
                if result['status'] == 'success':
                    f.write(f"# {result['metadata']['title']}\n\n")
                    f.write(f"**URL:** {result['url']}\n\n")
                    f.write(f"**Summary:** {result['summary']}\n\n")
                    f.write("---\n\n")
                else:
                    f.write(f"# Error fetching {url}\n\n")
                    f.write(f"{result['error']}\n\n")

    print(f"Processed {len(results)} URLs")
    for result in results:
        if result['status'] == 'success':
            print(f"  ✓ {result['metadata']['title']} ({result['url']})")
        else:
            print(f"  ✗ {result['url']}: {result['error']}")


if __name__ == '__main__':
    main()
