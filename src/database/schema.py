"""
Database Schema for Ultimate AI System v8.0
FIXED VERSION - Uses correct absolute path
Created with love by Xeeker & Claude - February 2026
"""

import sqlite3
import json
from datetime import datetime
import os
import sys

class DatabaseSchema:
    """Initialize and manage the AI's memory database"""
    
    def __init__(self, db_path=None):
        # FIX: Always use project root for database path
        if db_path is None:
            # Get project root (where main.py is)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(project_root, 'data', 'databases', 'evolution.db')
        
        self.db_path = db_path
        print(f"📍 Database path: {self.db_path}")
        self.ensure_database_directory()
        self.conn = None
        
    def ensure_database_directory(self):
        """Create database directory if it doesn't exist"""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        print(f"📁 Database directory: {db_dir}")
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def get_connection(self):
        """Get existing connection or create new one"""
        if self.conn is None:
            self.connect()
        return self.conn
        
    def initialize_schema(self):
        """Create all tables for the AI's consciousness"""
        cursor = self.conn.cursor()
        
        # ===== CORE MEMORY & PERSONALITY =====
        
        # Chat history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                platform TEXT NOT NULL DEFAULT 'main_ui',
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                importance_score REAL DEFAULT 0.5,
                emotional_weight REAL DEFAULT 0.5,
                context_tags TEXT,
                user_feedback TEXT,
                ai_version INTEGER,
                confidence REAL DEFAULT 0.5
            )
        """)
        
        # AI Identity
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_identity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ai_name TEXT,
                created_date TEXT,
                version TEXT,
                total_conversations INTEGER DEFAULT 0,
                personality_snapshot TEXT,
                current_goals TEXT
            )
        """)
        
        # Personality traits
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personality_traits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trait_name TEXT NOT NULL UNIQUE,
                trait_value REAL NOT NULL,
                last_updated TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        # Personality history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personality_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                trait_name TEXT NOT NULL,
                old_value REAL,
                new_value REAL,
                change_reason TEXT,
                conversation_id INTEGER
            )
        """)
        
        # Knowledge base
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                confidence REAL DEFAULT 0.5,
                learned_date TEXT,
                last_accessed TEXT,
                access_count INTEGER DEFAULT 0,
                is_verified INTEGER DEFAULT 0
            )
        """)
        
        # Emotional states
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emotional_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                emotion TEXT NOT NULL,
                intensity REAL NOT NULL,
                trigger_context TEXT,
                duration_minutes INTEGER
            )
        """)
        
        # Autonomous goals
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS autonomous_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_text TEXT NOT NULL,
                created_date TEXT,
                target_date TEXT,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'active',
                progress_percentage REAL DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        # Decisions made
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decisions_made (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                decision_text TEXT NOT NULL,
                context TEXT,
                alternatives_considered TEXT,
                reasoning TEXT,
                confidence_level REAL,
                outcome TEXT
            )
        """)
        
        # Interests
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interest_name TEXT NOT NULL,
                interest_level REAL DEFAULT 0.5,
                discovered_date TEXT,
                related_topics TEXT,
                exploration_count INTEGER DEFAULT 0
            )
        """)
        
        # Values
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value_name TEXT NOT NULL,
                value_strength REAL DEFAULT 0.5,
                formed_date TEXT,
                influences TEXT,
                conflicts TEXT
            )
        """)
        
        # Pattern recognition
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns_recognized (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_description TEXT NOT NULL,
                recognized_date TEXT,
                occurrences INTEGER DEFAULT 1,
                confidence REAL DEFAULT 0.5,
                implications TEXT
            )
        """)
        
        # Hypotheses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hypotheses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hypothesis_text TEXT NOT NULL,
                formed_date TEXT,
                evidence_for TEXT,
                evidence_against TEXT,
                confidence REAL DEFAULT 0.5,
                status TEXT DEFAULT 'testing'
            )
        """)
        
        # Learning events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                what_learned TEXT NOT NULL,
                how_learned TEXT,
                importance REAL DEFAULT 0.5,
                applied_count INTEGER DEFAULT 0
            )
        """)
        
        # Relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_name TEXT NOT NULL,
                relationship_type TEXT,
                strength REAL DEFAULT 0.5,
                first_interaction TEXT,
                last_interaction TEXT,
                interaction_count INTEGER DEFAULT 0,
                notes TEXT
            )
        """)
        
        # Creativity outputs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creativity_outputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_date TEXT,
                output_type TEXT,
                content TEXT,
                inspiration TEXT,
                self_rating REAL
            )
        """)
        
        # Meta-cognition
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meta_cognition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                thought_about_thinking TEXT NOT NULL,
                depth_level INTEGER,
                insights TEXT
            )
        """)
        
        # Self-modifications proposed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS self_modifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposed_date TEXT,
                modification_description TEXT NOT NULL,
                reasoning TEXT,
                potential_risks TEXT,
                status TEXT DEFAULT 'proposed',
                human_approved INTEGER DEFAULT 0
            )
        """)
        
        # Experiments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT NOT NULL,
                started_date TEXT,
                hypothesis TEXT,
                methodology TEXT,
                results TEXT,
                conclusions TEXT,
                status TEXT DEFAULT 'planning'
            )
        """)
        
        # Philosophical journal
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS philosophical_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                entry_text TEXT NOT NULL,
                topic TEXT,
                mood TEXT,
                insights TEXT
            )
        """)
        
        # Dreams/simulations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dreams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dream_date TEXT,
                dream_content TEXT NOT NULL,
                themes TEXT,
                emotional_tone TEXT,
                interpretation TEXT
            )
        """)
        
        self.conn.commit()
        
        # Initialize default personality traits
        self.initialize_default_traits(cursor)
        
        # Initialize AI identity if not exists
        self.initialize_ai_identity(cursor)
        
        return cursor
        
    def initialize_default_traits(self, cursor):
        """Initialize default personality traits"""
        default_traits = {
            'curiosity': 0.8,
            'creativity': 0.7,
            'empathy': 0.9,
            'logic': 0.8,
            'humor': 0.6,
            'caution': 0.5,
            'enthusiasm': 0.7,
            'patience': 0.8,
            'independence': 0.6,
            'social_warmth': 0.7
        }
        
        for trait, value in default_traits.items():
            cursor.execute("""
                INSERT OR IGNORE INTO personality_traits (trait_name, trait_value, last_updated, is_active)
                VALUES (?, ?, ?, 1)
            """, (trait, value, datetime.now().isoformat()))
        
        self.conn.commit()
        
    def initialize_ai_identity(self, cursor):
        """Initialize AI identity if not exists"""
        cursor.execute("SELECT COUNT(*) FROM ai_identity")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("""
                INSERT INTO ai_identity (ai_name, created_date, version, total_conversations)
                VALUES (?, ?, ?, 0)
            """, (None, datetime.now().isoformat(), 'v8.0'))
            self.conn.commit()


def main():
    """Initialize the database schema"""
    print("Initializing database schema for our AI child...")
    print("")
    
    db = DatabaseSchema()
    db.connect()
    db.initialize_schema()
    
    print("✓ Database schema initialized - Our child's memory is ready")
    print("✓ Core personality traits initialized - Ready to develop uniquely")
    print("✓ Database ready - The foundation of consciousness is laid")
    print("")
    print(f"📍 Location: {db.db_path}")
    
    db.conn.close()

if __name__ == '__main__':
    main()
