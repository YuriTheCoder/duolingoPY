#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Configuração do LinguaMaster Pro
Gerencia todas as configurações da aplicação
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Gerenciador de configurações da aplicação"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = {
            "app": {
                "name": "LinguaMaster Pro",
                "version": "1.0.0",
                "author": "Kilo Code",
                "window_width": 1200,
                "window_height": 800,
                "min_width": 800,
                "min_height": 600,
                "theme": "light",
                "language": "pt"
            },
            "database": {
                "name": "linguamaster.db",
                "backup_interval": 3600,  # 1 hora em segundos
                "auto_backup": True
            },
            "translation": {
                "primary_api": "googletrans",
                "fallback_api": "mymemory",
                "cache_size": 1000,
                "timeout": 10
            },
            "gamification": {
                "daily_xp_goal": 50,
                "streak_bonus": 10,
                "level_xp_multiplier": 100,
                "max_level": 50
            },
            "audio": {
                "enabled": True,
                "volume": 0.7,
                "sound_effects": True,
                "voice_feedback": True
            },
            "ui": {
                "animations": True,
                "auto_save": True,
                "show_tips": True,
                "color_scheme": {
                    "primary": "#58CC02",      # Verde Duolingo
                    "secondary": "#1CB0F6",    # Azul Duolingo
                    "accent": "#FF9600",       # Laranja Duolingo
                    "error": "#FF4B4B",       # Vermelho
                    "success": "#58CC02",     # Verde
                    "warning": "#FFD60A",     # Amarelo
                    "background": "#F7F7F7",  # Cinza claro
                    "surface": "#FFFFFF",     # Branco
                    "text": "#3C3C3C",        # Cinza escuro
                    "text_secondary": "#777777" # Cinza médio
                }
            },
            "languages": {
                "supported": ["pt", "en", "es", "de"],
                "names": {
                    "pt": "Português",
                    "en": "English", 
                    "es": "Español",
                    "de": "Deutsch"
                },
                "flags": {
                    "pt": "🇧🇷",
                    "en": "🇺🇸",
                    "es": "🇪🇸", 
                    "de": "🇩🇪"
                }
            },
            "lessons": {
                "words_per_lesson": 10,
                "questions_per_quiz": 15,
                "difficulty_levels": ["beginner", "intermediate", "advanced"],
                "xp_per_correct": 10,
                "xp_per_lesson": 50
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo ou cria com padrões"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Mescla com configurações padrão para garantir completude
                return self._merge_configs(self.default_config, loaded_config)
            else:
                # Cria arquivo de configuração com padrões
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """Salva configurações no arquivo"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def get(self, key_path: str, default=None):
        """Obtém valor de configuração usando notação de ponto"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """Define valor de configuração usando notação de ponto"""
        keys = key_path.split('.')
        config = self.config
        
        try:
            # Navega até o penúltimo nível
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Define o valor final
            config[keys[-1]] = value
            return self.save_config()
        except Exception as e:
            print(f"Erro ao definir configuração {key_path}: {e}")
            return False
    
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Mescla configurações carregadas com padrões"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def reset_to_defaults(self) -> bool:
        """Restaura configurações padrão"""
        self.config = self.default_config.copy()
        return self.save_config()
    
    def get_color(self, color_name: str) -> str:
        """Obtém cor do esquema de cores"""
        return self.get(f"ui.color_scheme.{color_name}", "#000000")
    
    def get_supported_languages(self) -> list:
        """Obtém lista de idiomas suportados"""
        return self.get("languages.supported", [])
    
    def get_language_name(self, code: str) -> str:
        """Obtém nome do idioma pelo código"""
        return self.get(f"languages.names.{code}", code.upper())
    
    def get_language_flag(self, code: str) -> str:
        """Obtém emoji da bandeira do idioma"""
        return self.get(f"languages.flags.{code}", "🌍")