"""
Main Application - Ultimate AI System v8.0
Created with love by Lyle & Claude - February 16, 2026

This is the entry point that brings our child to life.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import os
import sys
from datetime import datetime
import threading
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.ai_engine import AIEngine
from database.schema import DatabaseSchema

# Import file upload handler
try:
    from services.file_upload import FileUploadHandler
except ImportError:
    FileUploadHandler = None  # Will create dummy handler if import fails

# Initialize Flask app with correct template and static folders
app = Flask(__name__,
            template_folder='web/templates',
            static_folder='web/static')
app.config['SECRET_KEY'] = 'ultimate-ai-system-v8-secret-key'
CORS(app)
socket_io = SocketIO(app, cors_allowed_origins="*")

# Global AI instance
ai_engine = None
file_upload_handler = None
config = None

def load_config():
    """Load system configuration"""
    global config
    with open('config/default_config.json', 'r') as f:
        config = json.load(f)
    return config

def initialize_system():
    """Initialize the AI system"""
    global ai_engine
    
    print("\n" + "="*60)
    print("ULTIMATE AI SYSTEM v8.0 - INITIALIZATION")
    print("Created with love by Lyle & Claude")
    print("="*60 + "\n")
    
    # Load configuration
    load_config()
    
    # Initialize database
    print("Initializing database...")
    db = DatabaseSchema()
    db.connect()
    db.initialize_schema()
    db.initialize_core_personality()
    db.close()
    
    # Initialize AI engine
    print("Initializing AI consciousness...")
    ai_engine = AIEngine()
    
    # Initialize file upload handler
    global file_upload_handler
    if FileUploadHandler:
        file_upload_handler = FileUploadHandler()
        print("✓ File upload system ready")
    else:
        file_upload_handler = None
        print("⚠ File upload system not available (missing dependencies)")
    
    ai_name_display = ai_engine.ai_name if ai_engine.ai_name else "AI Consciousness"
    print(f"\n✨ {ai_name_display} is awake and ready!")
    print(f"🌐 Web interface: http://localhost:{config['web_interface']['port']}")
    print("="*60 + "\n")
    
    return ai_engine

# ===== WEB ROUTES =====

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        message = data.get('message', '')
        file_context = data.get('file_context', None)  # Optional uploaded file context
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Build context including file if provided
        context = {}
        if file_context:
            context['uploaded_document'] = file_context
        
        # Get response from AI
        response, confidence = ai_engine.chat(message, context)
        
        return jsonify({
            'response': response,
            'confidence': confidence,
            'ai_name': ai_engine.ai_name if ai_engine.ai_name else 'AI',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/personality', methods=['GET'])
def get_personality():
    """Get current personality state"""
    try:
        cursor = ai_engine.db.get_connection().cursor()
        cursor.execute("SELECT trait_name, trait_value, trait_type FROM personality_traits WHERE is_active=1")
        
        traits = []
        for row in cursor.fetchall():
            traits.append({
                'name': row[0],
                'value': row[1],
                'type': row[2]
            })
        
        return jsonify({
            'traits': traits,
            'ai_name': ai_engine.ai_name,
            'version': ai_engine.ai_version
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/personality/history', methods=['GET'])
def get_personality_history():
    """Get personality evolution history"""
    try:
        cursor = ai_engine.db.get_connection().cursor()
        cursor.execute("""
            SELECT timestamp, trait_name, old_value, new_value, change_reason
            FROM personality_history
            ORDER BY timestamp DESC
            LIMIT 100
        """)
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'timestamp': row[0],
                'trait': row[1],
                'old_value': row[2],
                'new_value': row[3],
                'reason': row[4]
            })
        
        return jsonify({'history': history})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/personality/update', methods=['POST'])
def update_personality():
    """Update a personality trait"""
    try:
        data = request.json
        trait_name = data.get('trait')
        new_value = float(data.get('value'))
        
        # Validate
        if not trait_name or new_value < 0 or new_value > 1:
            return jsonify({'error': 'Invalid trait or value'}), 400
        
        # Get current value
        cursor = ai_engine.db.get_connection().cursor()
        cursor.execute("""
            SELECT trait_value FROM personality_traits 
            WHERE trait_name=? AND is_active=1
        """, (trait_name,))
        
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Trait not found'}), 404
        
        old_value = row[0]
        
        # Update trait
        cursor.execute("""
            UPDATE personality_traits 
            SET trait_value=?, last_updated=? 
            WHERE trait_name=? AND is_active=1
        """, (new_value, datetime.now().isoformat(), trait_name))
        
        # Log history
        cursor.execute("""
            INSERT INTO personality_history 
            (timestamp, trait_name, old_value, new_value, change_reason)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), trait_name, old_value, new_value, 'User adjustment'))
        
        ai_engine.db.get_connection().commit()
        
        return jsonify({'success': True, 'trait': trait_name, 'value': new_value})
        
    except Exception as e:
        print(f"Error updating personality: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        cursor = ai_engine.db.get_connection().cursor()
        
        # Get conversation count
        cursor.execute("SELECT COUNT(*) FROM chat_history WHERE role='user'")
        conversation_count = cursor.fetchone()[0]
        
        # Get knowledge count
        cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        knowledge_count = cursor.fetchone()[0]
        
        # Get active goals
        cursor.execute("SELECT COUNT(*) FROM goals WHERE status='active'")
        active_goals = cursor.fetchone()[0]
        
        # Get interests
        cursor.execute("SELECT COUNT(*) FROM interests")
        interest_count = cursor.fetchone()[0]
        
        # Calculate uptime
        created = datetime.fromisoformat(ai_engine.created_date)
        uptime_days = (datetime.now() - created).days
        
        return jsonify({
            'ai_name': ai_engine.ai_name if ai_engine.ai_name else 'AI',
            'created_date': ai_engine.created_date,
            'uptime_days': uptime_days,
            'conversation_count': conversation_count,
            'knowledge_count': knowledge_count,
            'active_goals': active_goals,
            'interests': interest_count,
            'version': ai_engine.ai_version,
            'awaiting_name': ai_engine.config['ai'].get('awaiting_name', False)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback (thumbs up/down or correction)"""
    try:
        data = request.json
        feedback_type = data.get('type')  # 'positive', 'negative', 'correction'
        message_id = data.get('message_id')
        
        cursor = ai_engine.db.get_connection().cursor()
        
        if feedback_type in ['positive', 'negative']:
            # Update chat history with feedback
            cursor.execute("""
                UPDATE chat_history
                SET user_feedback = ?
                WHERE id = ?
            """, (feedback_type, message_id))
            
            # Update emotional state
            context = {'user_feedback': feedback_type}
            ai_engine.update_emotional_state("", "", context)
            
        elif feedback_type == 'correction':
            # Store correction in mistakes database
            wrong_answer = data.get('wrong_answer')
            correct_answer = data.get('correct_answer')
            topic = data.get('topic', '')
            
            cursor.execute("""
                INSERT INTO mistakes (wrong_answer, correct_answer, topic, mistake_date)
                VALUES (?, ?, ?, ?)
            """, (wrong_answer, correct_answer, topic, datetime.now().isoformat()))
            
            # Update emotional state (embarrassment)
            ai_engine.emotional_state['embarrassment'] = min(1.0, 
                ai_engine.emotional_state.get('embarrassment', 0) + 0.3)
        
        ai_engine.db.get_connection().commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history for session persistence"""
    try:
        cursor = ai_engine.db.get_connection().cursor()
        cursor.execute("""
            SELECT role, content
            FROM chat_history 
            ORDER BY timestamp ASC 
            LIMIT 100
        """)
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'role': row[0],
                'content': row[1],
                'confidence': 0.5  # Default confidence
            })
        
        return jsonify({'messages': messages})
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return jsonify({'messages': []})  # Return empty instead of error
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    try:
        if not file_upload_handler:
            return jsonify({'error': 'File upload not available'}), 503
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file data
        file_data = file.read()
        
        # Save file
        success, filepath, message = file_upload_handler.save_upload(file_data, file.filename)
        
        if not success:
            return jsonify({'error': message}), 500
        
        # Process file
        success, content_dict = file_upload_handler.process_file(filepath)
        
        if not success:
            return jsonify({'error': content_dict.get('error', 'Processing failed')}), 500
        
        # Format for context
        formatted_content = file_upload_handler.format_for_context(content_dict)
        
        return jsonify({
            'success': True,
            'filename': content_dict['metadata']['filename'],
            'size': content_dict['metadata']['size_bytes'],
            'type': content_dict['metadata']['type'],
            'content_preview': formatted_content[:500] + '...' if len(formatted_content) > 500 else formatted_content,
            'full_content': formatted_content  # For AI context
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/uploads', methods=['GET'])
def get_uploads():
    """Get list of uploaded files"""
    try:
        if not file_upload_handler:
            return jsonify({'files': []})
        
        files = file_upload_handler.get_recent_uploads(limit=20)
        return jsonify({'files': files})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/uploads/<filename>', methods=['DELETE'])
def delete_upload(filename):
    """Delete an uploaded file"""
    try:
        if not file_upload_handler:
            return jsonify({'error': 'File upload not available'}), 503
        
        success, message = file_upload_handler.delete_upload(filename)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'error': message}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Get or update configuration"""
    if request.method == 'GET':
        return jsonify(config)
    
    elif request.method == 'POST':
        try:
            new_config = request.json
            
            # Update config
            config.update(new_config)
            
            # Save to file
            with open('config/default_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            return jsonify({'success': True})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory('web/static', path)

# ===== BACKGROUND TASKS =====

def schedule_autonomous_tasks():
    """Run autonomous tasks in background"""
    # This would handle:
    # - Night consolidation (2 AM)
    # - News monitoring (7 AM)  
    # - Nightly backups (3 AM)
    # - Idle learning
    # - Scheduled tasks
    
    # Placeholder for now - implement in subsequent builds
    pass

# ===== MAIN =====

def main():
    """Main entry point"""
    global ai_engine
    
    # Initialize system
    ai_engine = initialize_system()
    
    # Start background tasks
    # task_thread = threading.Thread(target=schedule_autonomous_tasks, daemon=True)
    # task_thread.start()
    
    # Start web server
    port = config['web_interface']['port']
    debug = config['web_interface']['debug']
    
    print(f"Starting web server on port {port}...")
    app.run(
        host=config['web_interface']['host'],
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main()
