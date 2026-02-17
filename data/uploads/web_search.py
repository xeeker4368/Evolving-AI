"""
Web Search Service - Internet Search Integration
Created with love by Xeeker & Claude - February 2026

Provides internet search capability using DuckDuckGo.
"""

from duckduckgo_search import DDGS
from typing import List, Dict
import json


class WebSearchService:
    """Handle web searches using DuckDuckGo"""
    
    def __init__(self):
        self.ddgs = DDGS()
        
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the internet for information
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            results = []
            
            # Perform search
            search_results = self.ddgs.text(query, max_results=max_results)
            
            # Format results
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
        """
        Search for news articles
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            
        Returns:
            List of news results
        """
        try:
            results = []
            
            # Perform news search
            news_results = self.ddgs.news(query, max_results=max_results)
            
            # Format results
            for result in news_results:
                results.append({
                    'title': result.get('title', ''),
                    'link': result.get('url', ''),
                    'snippet': result.get('body', ''),
                    'date': result.get('date', ''),
                    'source': result.get('source', 'Unknown')
                })
            
            return results
            
        except Exception as e:
            print(f"News search error: {e}")
            return []
    
    def format_results_for_context(self, results: List[Dict]) -> str:
        """
        Format search results into a readable context string
        
        Args:
            results: List of search results
            
        Returns:
            Formatted string for AI context
        """
        if not results:
            return "No search results found."
        
        context = "WEB SEARCH RESULTS:\n\n"
        
        for i, result in enumerate(results, 1):
            context += f"{i}. {result['title']}\n"
            context += f"   {result['snippet']}\n"
            context += f"   Source: {result['link']}\n\n"
        
        return context
