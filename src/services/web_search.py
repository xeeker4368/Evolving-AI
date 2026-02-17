"""
Web Search Service - Internet Search Integration
Created with love by Xeeker & Claude - February 2026

Provides internet search capability using DuckDuckGo.
"""

from duckduckgo_search import DDGS
from typing import List, Dict
import json


class WebSearchService:
    """Handle web searches using DuckDuckGo with stability fixes for 2026"""
    
    def __init__(self):
        # Adding a real browser header helps avoid the 'Ratelimit' error
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        try:
            results = []
            # Use backend="lite" to bypass the main API rate limits
            with DDGS(headers=self.headers) as ddgs:
                search_results = ddgs.text(query, max_results=max_results, backend="lite")
                
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'link': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'source': 'DuckDuckGo'
                    })
            return results
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def search_news(self, query: str, max_results: int = 5) -> List[Dict]:
        try:
            results = []
            with DDGS(headers=self.headers) as ddgs:
                news_results = ddgs.news(query, max_results=max_results)
                
                for result in news_results:
                    results.append({
                        'title': result.get('title', ''),
                        'link': result.get('url', ''), # Changed from 'link' to 'url'
                        'snippet': result.get('body', ''),
                        'date': result.get('date', ''),
                        'source': result.get('source', 'Unknown')
                    })
            return results
        except Exception as e:
            print(f"News search error: {e}")
            return []

    def format_results_for_context(self, results: List[Dict]) -> str:
        if not results:
            return "No search results found."
        
        context = "WEB SEARCH RESULTS:\n\n"
        for i, result in enumerate(results, 1):
            context += f"{i}. {result['title']}\n"
            context += f"   {result['snippet']}\n"
            context += f"   Source: {result['link']}\n\n"
        return context
