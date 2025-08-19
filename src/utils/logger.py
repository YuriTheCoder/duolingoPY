#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Logging do LinguaMaster Pro
Gerencia logs da aplicação com diferentes níveis
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    """Sistema de logging personalizado para LinguaMaster Pro"""
    
    def __init__(self, name="LinguaMaster", log_file="linguamaster.log"):
        self.name = name
        self.log_file = log_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configura o sistema de logging"""
        # Criar diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configurar logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        
        # Evitar duplicação de handlers
        if logger.handlers:
            return logger
        
        # Formatter para logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para arquivo
        file_handler = logging.FileHandler(
            log_dir / self.log_file, 
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Adicionar handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def debug(self, message):
        """Log de debug"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log de informação"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de erro"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log crítico"""
        self.logger.critical(message)
    
    def log_user_action(self, user_id, action, details=None):
        """Log específico para ações do usuário"""
        message = f"User {user_id}: {action}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_game_event(self, user_id, game_type, score, details=None):
        """Log específico para eventos de jogos"""
        message = f"Game Event - User {user_id}: {game_type} - Score: {score}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_translation_request(self, source_lang, target_lang, text_length):
        """Log específico para requisições de tradução"""
        message = f"Translation: {source_lang} -> {target_lang} ({text_length} chars)"
        self.info(message)
    
    def log_error_with_context(self, error, context=None):
        """Log de erro com contexto adicional"""
        message = f"Error: {str(error)}"
        if context:
            message += f" - Context: {context}"
        self.error(message)
    
    def clear_old_logs(self, days=30):
        """Remove logs antigos"""
        try:
            log_dir = Path("logs")
            if not log_dir.exists():
                return
            
            cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)
            
            for log_file in log_dir.glob("*.log"):
                if log_file.stat().st_mtime < cutoff_date:
                    log_file.unlink()
                    self.info(f"Removed old log file: {log_file}")
        
        except Exception as e:
            self.error(f"Error clearing old logs: {e}")