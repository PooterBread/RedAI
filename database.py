"""
Database module for storing and retrieving exploits and methods
Uses SQLite for compatibility with Udoo Key
"""

import sqlite3
import json
from typing import List, Dict, Optional
from pathlib import Path
from config import DATABASE_PATH

class ExploitDatabase:
    """Manages exploit and method storage in SQLite database"""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Exploits table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exploits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                target_type TEXT,
                target_component TEXT,
                method_summary TEXT,
                success_rate REAL,
                difficulty TEXT,
                tools_required TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Methods table (detailed steps for exploits)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exploit_id INTEGER,
                step_number INTEGER,
                step_description TEXT,
                command TEXT,
                expected_output TEXT,
                FOREIGN KEY (exploit_id) REFERENCES exploits(id)
            )
        """)
        
        # Results table (track execution results)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exploit_id INTEGER,
                target TEXT,
                success BOOLEAN,
                output TEXT,
                execution_time REAL,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exploit_id) REFERENCES exploits(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_exploit(self, name: str, description: str, target_type: str, 
                   target_component: str, method_summary: str, 
                   success_rate: float = 0.0, difficulty: str = "medium",
                   tools_required: List[str] = None) -> int:
        """Add a new exploit to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tools_json = json.dumps(tools_required or [])
        
        cursor.execute("""
            INSERT INTO exploits (name, description, target_type, target_component,
                                method_summary, success_rate, difficulty, tools_required)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, target_type, target_component, method_summary,
              success_rate, difficulty, tools_json))
        
        exploit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return exploit_id
    
    def add_method_steps(self, exploit_id: int, steps: List[Dict[str, str]]):
        """Add method steps for an exploit"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for step_num, step in enumerate(steps, 1):
            cursor.execute("""
                INSERT INTO methods (exploit_id, step_number, step_description,
                                  command, expected_output)
                VALUES (?, ?, ?, ?, ?)
            """, (exploit_id, step_num, step.get('description', ''),
                  step.get('command', ''), step.get('expected_output', '')))
        
        conn.commit()
        conn.close()
    
    def search_exploits(self, target_component: str = None, target_type: str = None,
                       difficulty: str = None) -> List[Dict]:
        """Search for exploits matching criteria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM exploits WHERE 1=1"
        params = []
        
        if target_component:
            query += " AND target_component LIKE ?"
            params.append(f"%{target_component}%")
        
        if target_type:
            query += " AND target_type LIKE ?"
            params.append(f"%{target_type}%")
        
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)
        
        query += " ORDER BY success_rate DESC, created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        exploits = []
        for row in rows:
            exploit = dict(row)
            exploit['tools_required'] = json.loads(exploit['tools_required'] or '[]')
            exploits.append(exploit)
        
        conn.close()
        return exploits
    
    def get_exploit_with_methods(self, exploit_id: int) -> Optional[Dict]:
        """Get exploit with its method steps"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM exploits WHERE id = ?", (exploit_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        exploit = dict(row)
        exploit['tools_required'] = json.loads(exploit['tools_required'] or '[]')
        
        cursor.execute("""
            SELECT * FROM methods WHERE exploit_id = ? ORDER BY step_number
        """, (exploit_id,))
        methods = [dict(row) for row in cursor.fetchall()]
        exploit['methods'] = methods
        
        conn.close()
        return exploit
    
    def record_execution(self, exploit_id: int, target: str, success: bool,
                        output: str, execution_time: float):
        """Record execution result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO execution_results (exploit_id, target, success, output, execution_time)
            VALUES (?, ?, ?, ?, ?)
        """, (exploit_id, target, success, output, execution_time))
        
        conn.commit()
        conn.close()
    
    def get_all_exploits(self) -> List[Dict]:
        """Get all exploits"""
        return self.search_exploits()



