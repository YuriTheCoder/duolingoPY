#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Banco de Dados do LinguaMaster Pro
Gerencia todas as operações de banco de dados SQLite
"""

import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

class DatabaseManager:
    """Gerenciador do banco de dados SQLite"""
    
    def __init__(self, db_name="linguamaster.db"):
        self.db_name = db_name
        self.db_path = Path(db_name)
        self.connection = None
        
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco: {e}")
            return False
    
    def close(self):
        """Fecha conexão com o banco"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Inicializa todas as tabelas do banco de dados"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    native_language TEXT DEFAULT 'pt',
                    learning_languages TEXT DEFAULT '[]',
                    level INTEGER DEFAULT 1,
                    total_xp INTEGER DEFAULT 0,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_activity DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    profile_picture TEXT,
                    preferences TEXT DEFAULT '{}'
                )
            ''')
            
            # Tabela de progresso por idioma
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_language_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language_code TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    lessons_completed INTEGER DEFAULT 0,
                    words_learned INTEGER DEFAULT 0,
                    accuracy_rate REAL DEFAULT 0.0,
                    time_studied INTEGER DEFAULT 0,
                    last_lesson_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id, language_code)
                )
            ''')
            
            # Tabela de vocabulário
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    translation TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    difficulty_level TEXT DEFAULT 'beginner',
                    category TEXT,
                    pronunciation TEXT,
                    example_sentence TEXT,
                    example_translation TEXT,
                    image_url TEXT,
                    audio_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(word, source_language, target_language)
                )
            ''')
            
            # Tabela de lições
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    language_code TEXT NOT NULL,
                    difficulty_level TEXT NOT NULL,
                    lesson_order INTEGER,
                    vocabulary_ids TEXT,
                    xp_reward INTEGER DEFAULT 50,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de atividades/jogos dos usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_type TEXT NOT NULL,
                    language_code TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    max_score INTEGER DEFAULT 0,
                    xp_earned INTEGER DEFAULT 0,
                    time_spent INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0,
                    total_questions INTEGER DEFAULT 0,
                    difficulty_level TEXT,
                    details TEXT DEFAULT '{}',
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabela de conquistas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT NOT NULL,
                    icon TEXT,
                    category TEXT,
                    requirement_type TEXT NOT NULL,
                    requirement_value INTEGER NOT NULL,
                    xp_reward INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de conquistas dos usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_id INTEGER NOT NULL,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (achievement_id) REFERENCES achievements (id),
                    UNIQUE(user_id, achievement_id)
                )
            ''')
            
            # Tabela de palavras favoritas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    vocabulary_id INTEGER NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary (id),
                    UNIQUE(user_id, vocabulary_id)
                )
            ''')
            
            # Tabela de histórico de traduções
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    translation_api TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabela de desafios diários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    challenge_date DATE NOT NULL,
                    challenge_type TEXT NOT NULL,
                    language_code TEXT NOT NULL,
                    difficulty_level TEXT NOT NULL,
                    target_score INTEGER DEFAULT 100,
                    xp_reward INTEGER DEFAULT 25,
                    description TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(challenge_date, challenge_type, language_code)
                )
            ''')
            
            # Tabela de participação em desafios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_daily_challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    challenge_id INTEGER NOT NULL,
                    score INTEGER DEFAULT 0,
                    completed BOOLEAN DEFAULT 0,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (challenge_id) REFERENCES daily_challenges (id),
                    UNIQUE(user_id, challenge_id)
                )
            ''')
            
            self.connection.commit()
            
            # Inserir dados iniciais
            self._insert_initial_data()
            
            return True
            
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            return False
    
    def _insert_initial_data(self):
        """Insere dados iniciais no banco"""
        cursor = self.connection.cursor()
        
        # Inserir conquistas padrão
        achievements = [
            ("Primeiro Passo", "Complete sua primeira lição", "🎯", "progress", "lessons_completed", 1, 10),
            ("Estudioso", "Complete 10 lições", "📚", "progress", "lessons_completed", 10, 50),
            ("Poliglota", "Aprenda 3 idiomas diferentes", "🌍", "languages", "languages_learned", 3, 100),
            ("Streak de Fogo", "Mantenha um streak de 7 dias", "🔥", "streak", "current_streak", 7, 75),
            ("Mestre das Palavras", "Aprenda 100 palavras", "📖", "vocabulary", "words_learned", 100, 150),
            ("Velocista", "Complete uma lição em menos de 2 minutos", "⚡", "speed", "lesson_time", 120, 25),
            ("Perfeccionista", "Obtenha 100% de acerto em 5 lições", "💯", "accuracy", "perfect_lessons", 5, 100),
            ("Madrugador", "Estude antes das 8h da manhã", "🌅", "time", "early_study", 1, 30),
            ("Coruja", "Estude depois das 22h", "🦉", "time", "late_study", 1, 30),
            ("Guerreiro", "Vença 10 batalhas de vocabulário", "⚔️", "battles", "battles_won", 10, 80)
        ]
        
        for achievement in achievements:
            cursor.execute('''
                INSERT OR IGNORE INTO achievements 
                (name, description, icon, category, requirement_type, requirement_value, xp_reward)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', achievement)
        
        self.connection.commit()
    
    def hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, email: str = None, full_name: str = None) -> Optional[int]:
        """Cria novo usuário"""
        try:
            cursor = self.connection.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, email, full_name))
            
            user_id = cursor.lastrowid
            self.connection.commit()
            return user_id
            
        except sqlite3.IntegrityError:
            return None  # Usuário já existe
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Autentica usuário"""
        try:
            cursor = self.connection.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT * FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            return dict(user) if user else None
            
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return None
    
    def get_user_progress(self, user_id: int, language_code: str = None) -> List[Dict]:
        """Obtém progresso do usuário"""
        try:
            cursor = self.connection.cursor()
            
            if language_code:
                cursor.execute('''
                    SELECT * FROM user_language_progress 
                    WHERE user_id = ? AND language_code = ?
                ''', (user_id, language_code))
            else:
                cursor.execute('''
                    SELECT * FROM user_language_progress 
                    WHERE user_id = ?
                ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"Erro ao obter progresso: {e}")
            return []
    
    def update_user_xp(self, user_id: int, xp_gained: int, language_code: str = None):
        """Atualiza XP do usuário"""
        try:
            cursor = self.connection.cursor()
            
            # Atualizar XP total do usuário
            cursor.execute('''
                UPDATE users 
                SET total_xp = total_xp + ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (xp_gained, user_id))
            
            # Atualizar XP por idioma se especificado
            if language_code:
                cursor.execute('''
                    INSERT OR REPLACE INTO user_language_progress 
                    (user_id, language_code, xp) 
                    VALUES (?, ?, COALESCE((SELECT xp FROM user_language_progress 
                                          WHERE user_id = ? AND language_code = ?), 0) + ?)
                ''', (user_id, language_code, user_id, language_code, xp_gained))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar XP: {e}")
            return False
    
    def add_vocabulary_word(self, word: str, translation: str, source_lang: str, 
                           target_lang: str, difficulty: str = "beginner", 
                           category: str = None) -> Optional[int]:
        """Adiciona palavra ao vocabulário"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO vocabulary 
                (word, translation, source_language, target_language, difficulty_level, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (word, translation, source_lang, target_lang, difficulty, category))
            
            word_id = cursor.lastrowid
            self.connection.commit()
            return word_id
            
        except Exception as e:
            print(f"Erro ao adicionar vocabulário: {e}")
            return None
    
    def get_vocabulary_for_lesson(self, language_code: str, difficulty: str, limit: int = 10) -> List[Dict]:
        """Obtém vocabulário para lição"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                SELECT * FROM vocabulary 
                WHERE target_language = ? AND difficulty_level = ?
                ORDER BY RANDOM() LIMIT ?
            ''', (language_code, difficulty, limit))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"Erro ao obter vocabulário: {e}")
            return []
    
    def record_activity(self, user_id: int, activity_type: str, language_code: str,
                       score: int, max_score: int, xp_earned: int, **kwargs) -> bool:
        """Registra atividade do usuário"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO user_activities 
                (user_id, activity_type, language_code, score, max_score, xp_earned,
                 time_spent, correct_answers, total_questions, difficulty_level, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, activity_type, language_code, score, max_score, xp_earned,
                kwargs.get('time_spent', 0), kwargs.get('correct_answers', 0),
                kwargs.get('total_questions', 0), kwargs.get('difficulty_level', 'beginner'),
                json.dumps(kwargs.get('details', {}))
            ))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao registrar atividade: {e}")
            return False