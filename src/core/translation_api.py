#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Tradução do LinguaMaster Pro
Gerencia APIs de tradução gratuitas com cache offline
"""

import requests
import json
import time
from typing import Dict, Optional, List
from urllib.parse import quote
import sqlite3
from pathlib import Path

class TranslationCache:
    """Cache local para traduções"""
    
    def __init__(self, cache_file="translation_cache.db"):
        self.cache_file = cache_file
        self.connection = None
        self._init_cache()
    
    def _init_cache(self):
        """Inicializa cache SQLite"""
        try:
            self.connection = sqlite3.connect(self.cache_file)
            cursor = self.connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translation_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    api_used TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(source_text, source_lang, target_lang)
                )
            ''')
            
            self.connection.commit()
        except Exception as e:
            print(f"Erro ao inicializar cache: {e}")
    
    def get_cached_translation(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Busca tradução no cache"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT translated_text FROM translation_cache 
                WHERE source_text = ? AND source_lang = ? AND target_lang = ?
            ''', (text, source_lang, target_lang))
            
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception:
            return None
    
    def cache_translation(self, text: str, source_lang: str, target_lang: str, 
                         translation: str, api_used: str):
        """Armazena tradução no cache"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO translation_cache 
                (source_text, source_lang, target_lang, translated_text, api_used)
                VALUES (?, ?, ?, ?, ?)
            ''', (text, source_lang, target_lang, translation, api_used))
            
            self.connection.commit()
        except Exception as e:
            print(f"Erro ao cachear tradução: {e}")
    
    def close(self):
        """Fecha conexão do cache"""
        if self.connection:
            self.connection.close()

class GoogleTranslateFree:
    """API gratuita do Google Translate (não oficial)"""
    
    def __init__(self):
        self.base_url = "https://translate.googleapis.com/translate_a/single"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Traduz texto usando Google Translate gratuito"""
        try:
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and len(result[0]) > 0:
                    return result[0][0][0]
            
            return None
            
        except Exception as e:
            print(f"Erro no Google Translate: {e}")
            return None

class MyMemoryAPI:
    """API gratuita do MyMemory"""
    
    def __init__(self):
        self.base_url = "https://api.mymemory.translated.net/get"
        self.session = requests.Session()
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Traduz texto usando MyMemory API"""
        try:
            params = {
                'q': text,
                'langpair': f"{source_lang}|{target_lang}"
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('responseStatus') == 200:
                    return result['responseData']['translatedText']
            
            return None
            
        except Exception as e:
            print(f"Erro no MyMemory: {e}")
            return None

class LibreTranslateAPI:
    """API do LibreTranslate (instância pública)"""
    
    def __init__(self):
        self.base_url = "https://libretranslate.de/translate"
        self.session = requests.Session()
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Traduz texto usando LibreTranslate"""
        try:
            data = {
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            response = self.session.post(self.base_url, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('translatedText')
            
            return None
            
        except Exception as e:
            print(f"Erro no LibreTranslate: {e}")
            return None

class TranslationManager:
    """Gerenciador principal de traduções"""
    
    def __init__(self):
        self.cache = TranslationCache()
        self.apis = {
            'google': GoogleTranslateFree(),
            'mymemory': MyMemoryAPI(),
            'libretranslate': LibreTranslateAPI()
        }
        self.api_priority = ['google', 'mymemory', 'libretranslate']
        self.language_codes = {
            'pt': 'pt',
            'en': 'en', 
            'es': 'es',
            'de': 'de'
        }
    
    def translate(self, text: str, source_lang: str, target_lang: str, 
                 use_cache: bool = True) -> Dict[str, any]:
        """
        Traduz texto usando APIs disponíveis
        
        Returns:
            Dict com 'translation', 'api_used', 'cached', 'success'
        """
        # Normalizar códigos de idioma
        source_lang = self.language_codes.get(source_lang, source_lang)
        target_lang = self.language_codes.get(target_lang, target_lang)
        
        # Verificar cache primeiro
        if use_cache:
            cached_result = self.cache.get_cached_translation(text, source_lang, target_lang)
            if cached_result:
                return {
                    'translation': cached_result,
                    'api_used': 'cache',
                    'cached': True,
                    'success': True
                }
        
        # Tentar APIs em ordem de prioridade
        for api_name in self.api_priority:
            try:
                api = self.apis[api_name]
                translation = api.translate(text, source_lang, target_lang)
                
                if translation and translation.strip():
                    # Cachear resultado
                    if use_cache:
                        self.cache.cache_translation(
                            text, source_lang, target_lang, translation, api_name
                        )
                    
                    return {
                        'translation': translation,
                        'api_used': api_name,
                        'cached': False,
                        'success': True
                    }
                
                # Aguardar entre tentativas para evitar rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Erro na API {api_name}: {e}")
                continue
        
        return {
            'translation': None,
            'api_used': None,
            'cached': False,
            'success': False,
            'error': 'Todas as APIs falharam'
        }
    
    def translate_batch(self, texts: List[str], source_lang: str, 
                       target_lang: str) -> List[Dict[str, any]]:
        """Traduz múltiplos textos"""
        results = []
        
        for text in texts:
            result = self.translate(text, source_lang, target_lang)
            results.append(result)
            
            # Pausa entre traduções para evitar rate limiting
            if not result.get('cached', False):
                time.sleep(1)
        
        return results
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Retorna idiomas suportados"""
        return {
            'pt': 'Português',
            'en': 'English',
            'es': 'Español', 
            'de': 'Deutsch'
        }
    
    def detect_language(self, text: str) -> Optional[str]:
        """Detecta idioma do texto (implementação básica)"""
        # Implementação simples baseada em palavras comuns
        portuguese_words = ['o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os']
        english_words = ['the', 'of', 'and', 'a', 'to', 'in', 'is', 'you', 'that', 'it', 'he', 'was', 'for', 'on', 'are']
        spanish_words = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da']
        german_words = ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für', 'ist', 'im']
        
        words = text.lower().split()
        
        scores = {'pt': 0, 'en': 0, 'es': 0, 'de': 0}
        
        for word in words[:20]:  # Analisa apenas as primeiras 20 palavras
            if word in portuguese_words:
                scores['pt'] += 1
            if word in english_words:
                scores['en'] += 1
            if word in spanish_words:
                scores['es'] += 1
            if word in german_words:
                scores['de'] += 1
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return None
    
    def get_translation_stats(self) -> Dict[str, int]:
        """Obtém estatísticas de tradução"""
        try:
            cursor = self.cache.connection.cursor()
            
            # Total de traduções em cache
            cursor.execute('SELECT COUNT(*) FROM translation_cache')
            total_cached = cursor.fetchone()[0]
            
            # Traduções por API
            cursor.execute('''
                SELECT api_used, COUNT(*) 
                FROM translation_cache 
                GROUP BY api_used
            ''')
            api_stats = dict(cursor.fetchall())
            
            return {
                'total_cached': total_cached,
                'api_usage': api_stats
            }
            
        except Exception:
            return {'total_cached': 0, 'api_usage': {}}
    
    def clear_cache(self, older_than_days: int = 30):
        """Limpa cache antigo"""
        try:
            cursor = self.cache.connection.cursor()
            cursor.execute('''
                DELETE FROM translation_cache 
                WHERE created_at < datetime('now', '-{} days')
            '''.format(older_than_days))
            
            self.cache.connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
            return False
    
    def close(self):
        """Fecha conexões"""
        if self.cache:
            self.cache.close()