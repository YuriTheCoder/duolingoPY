#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Principal do LinguaMaster Pro
Tela inicial com visão geral do progresso e atividades
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, List, Optional
import threading
from datetime import datetime, timedelta
import random

class DashboardScreen:
    """Tela principal do dashboard"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db_manager = main_window.get_db_manager()
        self.logger = main_window.get_logger()
        self.config = main_window.get_config()
        
        # Estado da tela
        self.current_user = None
        self.user_progress = {}
        self.daily_challenge = None
        
        # Criar interface
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets do dashboard"""
        # Container principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        
        # Cabeçalho de boas-vindas
        self.create_welcome_header()
        
        # Cards de estatísticas principais
        self.create_stats_cards()
        
        # Seção de progresso por idioma
        self.create_language_progress()
        
        # Desafio diário
        self.create_daily_challenge()
        
        # Atividades recentes
        self.create_recent_activities()
        
        # Conquistas recentes
        self.create_recent_achievements()
        
        # Ações rápidas
        self.create_quick_actions()
    
    def create_welcome_header(self):
        """Cria cabeçalho de boas-vindas"""
        self.header_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Container interno
        header_content = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Saudação personalizada
        self.welcome_label = ctk.CTkLabel(
            header_content,
            text="👋 Bem-vindo de volta!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.config.get_color('primary')
        )
        self.welcome_label.pack(anchor="w")
        
        # Motivação do dia
        motivational_quotes = [
            "🌟 Cada palavra aprendida é um passo em direção ao mundo!",
            "🚀 Sua jornada linguística está apenas começando!",
            "💪 Persistência é a chave para dominar qualquer idioma!",
            "🎯 Foque no progresso, não na perfeição!",
            "🌍 Você está construindo pontes entre culturas!"
        ]
        
        self.motivation_label = ctk.CTkLabel(
            header_content,
            text=random.choice(motivational_quotes),
            font=ctk.CTkFont(size=14),
            text_color=self.config.get_color('text_secondary')
        )
        self.motivation_label.pack(anchor="w", pady=(5, 0))
    
    def create_stats_cards(self):
        """Cria cards de estatísticas principais"""
        self.stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Grid de 4 colunas
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Card XP Total
        self.xp_card = self.create_stat_card(
            self.stats_frame, "💎 XP Total", "0", 
            self.config.get_color('primary'), 0, 0
        )
        
        # Card Streak
        self.streak_card = self.create_stat_card(
            self.stats_frame, "🔥 Streak", "0 dias",
            self.config.get_color('error'), 0, 1
        )
        
        # Card Nível
        self.level_card = self.create_stat_card(
            self.stats_frame, "⭐ Nível", "1",
            self.config.get_color('warning'), 0, 2
        )
        
        # Card Palavras Aprendidas
        self.words_card = self.create_stat_card(
            self.stats_frame, "📚 Palavras", "0",
            self.config.get_color('success'), 0, 3
        )
    
    def create_stat_card(self, parent, title: str, value: str, color: str, row: int, col: int):
        """Cria um card de estatística"""
        card = ctk.CTkFrame(parent, corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color
        )
        title_label.pack(pady=(15, 5))
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.config.get_color('text')
        )
        value_label.pack(pady=(0, 15))
        
        return {'card': card, 'title': title_label, 'value': value_label}
    
    def create_language_progress(self):
        """Cria seção de progresso por idioma"""
        # Título da seção
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="🌍 Progresso por Idioma",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        section_title.pack(fill="x", padx=30, pady=(20, 10))
        
        # Container dos idiomas
        self.languages_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.languages_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Será preenchido dinamicamente
        self.language_cards = {}
    
    def create_language_card(self, parent, lang_code: str, progress_data: Dict):
        """Cria card de progresso de idioma"""
        card_frame = ctk.CTkFrame(parent, corner_radius=12)
        card_frame.pack(fill="x", padx=20, pady=10)
        
        # Container interno
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header do idioma
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        # Nome e bandeira do idioma
        flag = self.config.get_language_flag(lang_code)
        name = self.config.get_language_name(lang_code)
        
        lang_label = ctk.CTkLabel(
            header_frame,
            text=f"{flag} {name}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lang_label.pack(side="left")
        
        # Nível do idioma
        level = progress_data.get('level', 1)
        level_label = ctk.CTkLabel(
            header_frame,
            text=f"Nível {level}",
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary')
        )
        level_label.pack(side="right")
        
        # Barra de progresso XP
        xp = progress_data.get('xp', 0)
        xp_needed = level * 100  # XP necessário para próximo nível
        progress_value = min((xp % 100) / 100, 1.0)
        
        progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(10, 5))
        
        progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=8,
            progress_color=self.config.get_color('primary')
        )
        progress_bar.pack(fill="x")
        progress_bar.set(progress_value)
        
        # Texto do progresso
        xp_text = ctk.CTkLabel(
            content_frame,
            text=f"{xp % 100}/100 XP para próximo nível",
            font=ctk.CTkFont(size=10),
            text_color=self.config.get_color('text_secondary')
        )
        xp_text.pack(anchor="w")
        
        # Estatísticas do idioma
        stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(10, 0))
        
        # Lições completadas
        lessons = progress_data.get('lessons_completed', 0)
        lessons_label = ctk.CTkLabel(
            stats_frame,
            text=f"📖 {lessons} lições",
            font=ctk.CTkFont(size=11)
        )
        lessons_label.pack(side="left")
        
        # Palavras aprendidas
        words = progress_data.get('words_learned', 0)
        words_label = ctk.CTkLabel(
            stats_frame,
            text=f"📚 {words} palavras",
            font=ctk.CTkFont(size=11)
        )
        words_label.pack(side="left", padx=(20, 0))
        
        # Precisão
        accuracy = progress_data.get('accuracy_rate', 0.0)
        accuracy_label = ctk.CTkLabel(
            stats_frame,
            text=f"🎯 {accuracy:.1f}%",
            font=ctk.CTkFont(size=11)
        )
        accuracy_label.pack(side="right")
        
        return card_frame
    
    def create_daily_challenge(self):
        """Cria seção do desafio diário"""
        # Título da seção
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="🏆 Desafio Diário",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        section_title.pack(fill="x", padx=30, pady=(20, 10))
        
        # Card do desafio
        self.challenge_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.challenge_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Será preenchido dinamicamente
        self.update_daily_challenge()
    
    def update_daily_challenge(self):
        """Atualiza desafio diário"""
        # Limpar conteúdo anterior
        for widget in self.challenge_frame.winfo_children():
            widget.destroy()
        
        # Container interno
        content_frame = ctk.CTkFrame(self.challenge_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Desafio exemplo (seria carregado do banco)
        challenge_data = {
            'title': 'Mestre das Traduções',
            'description': 'Traduza 20 palavras corretamente hoje',
            'progress': 5,
            'target': 20,
            'xp_reward': 50,
            'completed': False
        }
        
        # Header do desafio
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"🎯 {challenge_data['title']}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left")
        
        reward_label = ctk.CTkLabel(
            header_frame,
            text=f"+{challenge_data['xp_reward']} XP",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.config.get_color('accent')
        )
        reward_label.pack(side="right")
        
        # Descrição
        desc_label = ctk.CTkLabel(
            content_frame,
            text=challenge_data['description'],
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary')
        )
        desc_label.pack(anchor="w", pady=(5, 10))
        
        # Progresso
        progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        progress_frame.pack(fill="x")
        
        progress_value = challenge_data['progress'] / challenge_data['target']
        progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=10,
            progress_color=self.config.get_color('success')
        )
        progress_bar.pack(fill="x")
        progress_bar.set(progress_value)
        
        progress_text = ctk.CTkLabel(
            content_frame,
            text=f"{challenge_data['progress']}/{challenge_data['target']} concluído",
            font=ctk.CTkFont(size=11),
            text_color=self.config.get_color('text_secondary')
        )
        progress_text.pack(anchor="w", pady=(5, 0))
    
    def create_recent_activities(self):
        """Cria seção de atividades recentes"""
        # Título da seção
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="📊 Atividades Recentes",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        section_title.pack(fill="x", padx=30, pady=(20, 10))
        
        # Lista de atividades
        self.activities_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.activities_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Atividades exemplo
        activities = [
            {"type": "quiz", "language": "en", "score": 85, "xp": 25, "time": "2 horas atrás"},
            {"type": "flashcards", "language": "es", "score": 92, "xp": 30, "time": "1 dia atrás"},
            {"type": "lesson", "language": "de", "score": 78, "xp": 50, "time": "2 dias atrás"}
        ]
        
        for i, activity in enumerate(activities):
            self.create_activity_item(self.activities_frame, activity, i == 0)
    
    def create_activity_item(self, parent, activity: Dict, is_first: bool):
        """Cria item de atividade"""
        # Container do item
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", padx=20, pady=(15 if is_first else 5, 5))
        
        # Ícone da atividade
        icons = {
            "quiz": "🧠",
            "flashcards": "🃏", 
            "lesson": "📖",
            "battle": "⚔️"
        }
        
        icon_label = ctk.CTkLabel(
            item_frame,
            text=icons.get(activity['type'], '🎯'),
            font=ctk.CTkFont(size=16)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Informações da atividade
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Título e idioma
        flag = self.config.get_language_flag(activity['language'])
        title_text = f"{activity['type'].title()} {flag}"
        
        title_label = ctk.CTkLabel(
            info_frame,
            text=title_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Score e tempo
        details_text = f"Score: {activity['score']}% • +{activity['xp']} XP • {activity['time']}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=10),
            text_color=self.config.get_color('text_secondary'),
            anchor="w"
        )
        details_label.pack(fill="x")
    
    def create_recent_achievements(self):
        """Cria seção de conquistas recentes"""
        # Título da seção
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="🏅 Conquistas Recentes",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        section_title.pack(fill="x", padx=30, pady=(20, 10))
        
        # Container das conquistas
        self.achievements_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.achievements_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Conquistas exemplo
        achievements = [
            {"name": "Primeiro Passo", "icon": "🎯", "description": "Complete sua primeira lição", "date": "Hoje"},
            {"name": "Estudioso", "icon": "📚", "description": "Complete 10 lições", "date": "Ontem"}
        ]
        
        for i, achievement in enumerate(achievements):
            self.create_achievement_item(self.achievements_frame, achievement, i == 0)
    
    def create_achievement_item(self, parent, achievement: Dict, is_first: bool):
        """Cria item de conquista"""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", padx=20, pady=(15 if is_first else 5, 5))
        
        # Ícone da conquista
        icon_label = ctk.CTkLabel(
            item_frame,
            text=achievement['icon'],
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        # Informações da conquista
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Nome da conquista
        name_label = ctk.CTkLabel(
            info_frame,
            text=achievement['name'],
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        name_label.pack(fill="x")
        
        # Descrição e data
        desc_text = f"{achievement['description']} • {achievement['date']}"
        desc_label = ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=ctk.CTkFont(size=10),
            text_color=self.config.get_color('text_secondary'),
            anchor="w"
        )
        desc_label.pack(fill="x")
    
    def create_quick_actions(self):
        """Cria seção de ações rápidas"""
        # Título da seção
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="⚡ Ações Rápidas",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        section_title.pack(fill="x", padx=30, pady=(20, 10))
        
        # Container dos botões
        actions_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Grid de botões
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Botões de ação
        actions = [
            ("📖 Nova Lição", "lessons", self.config.get_color('primary')),
            ("🎮 Jogar Quiz", "games", self.config.get_color('secondary')),
            ("🌍 Tradutor", "translator", self.config.get_color('success')),
            ("👤 Perfil", "profile", self.config.get_color('accent'))
        ]
        
        for i, (text, screen, color) in enumerate(actions):
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                height=40,
                fg_color=color,
                hover_color=self._darken_color(color),
                corner_radius=10,
                command=lambda s=screen: self.main_window.show_screen(s)
            )
            btn.grid(row=0, column=i, padx=5, sticky="ew")
    
    def set_user(self, user_data: Dict):
        """Define dados do usuário"""
        self.current_user = user_data
        self.update_user_data()
    
    def update_user_data(self):
        """Atualiza dados do usuário na interface"""
        if not self.current_user:
            return
        
        # Atualizar saudação
        name = self.current_user.get('full_name', self.current_user['username'])
        self.welcome_label.configure(text=f"👋 Bem-vindo de volta, {name}!")
        
        # Atualizar cards de estatísticas
        self.xp_card['value'].configure(text=str(self.current_user.get('total_xp', 0)))
        self.streak_card['value'].configure(text=f"{self.current_user.get('current_streak', 0)} dias")
        self.level_card['value'].configure(text=str(self.current_user.get('level', 1)))
        
        # Carregar progresso por idioma
        self.load_user_progress()
    
    def load_user_progress(self):
        """Carrega progresso do usuário por idioma"""
        if not self.current_user or self.current_user['id'] == 0:  # Demo user
            # Dados demo
            demo_progress = {
                'en': {'level': 2, 'xp': 150, 'lessons_completed': 5, 'words_learned': 45, 'accuracy_rate': 85.5},
                'es': {'level': 1, 'xp': 75, 'lessons_completed': 2, 'words_learned': 20, 'accuracy_rate': 92.0}
            }
            self.update_language_progress(demo_progress)
            return
        
        # Carregar do banco de dados em thread separada
        threading.Thread(
            target=self._load_progress_from_db,
            daemon=True
        ).start()
    
    def _load_progress_from_db(self):
        """Carrega progresso do banco de dados"""
        try:
            progress_data = self.db_manager.get_user_progress(self.current_user['id'])
            
            # Converter para formato adequado
            progress_dict = {}
            for progress in progress_data:
                progress_dict[progress['language_code']] = dict(progress)
            
            # Atualizar UI na thread principal
            self.parent.after(0, self.update_language_progress, progress_dict)
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar progresso: {e}")
    
    def update_language_progress(self, progress_data: Dict):
        """Atualiza progresso por idioma na interface"""
        # Limpar cards existentes
        for card in self.language_cards.values():
            card.destroy()
        self.language_cards.clear()
        
        # Criar cards para cada idioma com progresso
        for lang_code, progress in progress_data.items():
            card = self.create_language_card(self.languages_frame, lang_code, progress)
            self.language_cards[lang_code] = card
        
        # Atualizar card de palavras totais
        total_words = sum(p.get('words_learned', 0) for p in progress_data.values())
        self.words_card['value'].configure(text=str(total_words))
    
    def _darken_color(self, color: str, factor: float = 0.8) -> str:
        """Escurece cor para efeito hover"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        
        return color
    
    def show(self):
        """Mostra a tela"""
        self.main_frame.pack(fill="both", expand=True)
        # Atualizar dados quando mostrar a tela
        if self.current_user:
            self.update_user_data()
    
    def hide(self):
        """Oculta a tela"""
        self.main_frame.pack_forget()
    
    def clear_user(self):
        """Limpa dados do usuário"""
        self.current_user = None
        self.user_progress = {}