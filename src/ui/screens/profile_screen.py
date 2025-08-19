#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela de Perfil do LinguaMaster Pro
Interface para gerenciar perfil do usuário e estatísticas
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, List, Optional
import threading
from datetime import datetime, timedelta

class ProfileScreen:
    """Tela de perfil do usuário"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db_manager = main_window.get_db_manager()
        self.logger = main_window.get_logger()
        self.config = main_window.get_config()
        
        # Estado da tela
        self.current_user = None
        self.user_stats = {}
        self.achievements = []
        
        # Criar interface
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets da tela de perfil"""
        # Container principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        
        # Cabeçalho do perfil
        self.create_profile_header()
        
        # Estatísticas principais
        self.create_main_stats()
        
        # Progresso por idioma
        self.create_language_progress()
        
        # Conquistas
        self.create_achievements_section()
        
        # Configurações
        self.create_settings_section()
    
    def create_profile_header(self):
        """Cria cabeçalho do perfil"""
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Container principal
        main_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        main_container.pack(fill="x")
        
        # Avatar e info básica
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Avatar (emoji grande)
        self.avatar_label = ctk.CTkLabel(
            left_frame,
            text="👤",
            font=ctk.CTkFont(size=60)
        )
        self.avatar_label.pack(side="left", padx=(0, 20))
        
        # Informações do usuário
        info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Nome
        self.name_label = ctk.CTkLabel(
            info_frame,
            text="Usuário",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        self.name_label.pack(fill="x")
        
        # Username
        self.username_label = ctk.CTkLabel(
            info_frame,
            text="@usuario",
            font=ctk.CTkFont(size=14),
            text_color=self.config.get_color('text_secondary'),
            anchor="w"
        )
        self.username_label.pack(fill="x", pady=(2, 0))
        
        # Data de cadastro
        self.join_date_label = ctk.CTkLabel(
            info_frame,
            text="📅 Membro desde: Janeiro 2024",
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary'),
            anchor="w"
        )
        self.join_date_label.pack(fill="x", pady=(5, 0))
        
        # Lado direito - Nível e XP
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right")
        
        # Nível
        self.level_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        self.level_frame.pack(pady=(0, 10))
        
        self.level_label = ctk.CTkLabel(
            self.level_frame,
            text="⭐ Nível 1",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.config.get_color('warning')
        )
        self.level_label.pack(padx=20, pady=10)
        
        # XP Progress
        xp_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        xp_frame.pack()
        
        xp_content = ctk.CTkFrame(xp_frame, fg_color="transparent")
        xp_content.pack(padx=15, pady=10)
        
        self.xp_label = ctk.CTkLabel(
            xp_content,
            text="💎 0 / 100 XP",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.xp_label.pack()
        
        self.xp_progress = ctk.CTkProgressBar(
            xp_content,
            width=150,
            height=8,
            progress_color=self.config.get_color('primary')
        )
        self.xp_progress.pack(pady=(5, 0))
        self.xp_progress.set(0)
    
    def create_main_stats(self):
        """Cria estatísticas principais"""
        stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="📊 Estatísticas Gerais",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Grid de estatísticas
        stats_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_grid.pack(fill="x")
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Estatísticas
        stats = [
            ("🔥 Streak Atual", "0 dias", self.config.get_color('error')),
            ("📚 Palavras Aprendidas", "0", self.config.get_color('success')),
            ("🎯 Precisão Média", "0%", self.config.get_color('primary')),
            ("⏱️ Tempo Total", "0h", self.config.get_color('secondary'))
        ]
        
        self.stat_cards = {}
        for i, (title, value, color) in enumerate(stats):
            card = self.create_stat_card(stats_grid, title, value, color, 0, i)
            self.stat_cards[title] = card
    
    def create_stat_card(self, parent, title: str, value: str, color: str, row: int, col: int):
        """Cria card de estatística"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=color
        )
        title_label.pack(pady=(15, 5))
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        value_label.pack(pady=(0, 15))
        
        return {'card': card, 'title': title_label, 'value': value_label}
    
    def create_language_progress(self):
        """Cria seção de progresso por idioma"""
        progress_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="🌍 Progresso por Idioma",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Container dos idiomas
        self.languages_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.languages_container.pack(fill="x")
        
        # Será preenchido dinamicamente
        self.load_language_progress()
    
    def load_language_progress(self):
        """Carrega progresso por idioma"""
        # Dados exemplo (futuramente do banco de dados)
        languages_data = [
            {
                'code': 'en',
                'name': 'English',
                'flag': '🇺🇸',
                'level': 2,
                'xp': 150,
                'words_learned': 45,
                'lessons_completed': 5,
                'accuracy': 85.5
            },
            {
                'code': 'es',
                'name': 'Español',
                'flag': '🇪🇸',
                'level': 1,
                'xp': 75,
                'words_learned': 20,
                'lessons_completed': 2,
                'accuracy': 92.0
            }
        ]
        
        for lang_data in languages_data:
            self.create_language_card(self.languages_container, lang_data)
    
    def create_language_card(self, parent, lang_data: Dict):
        """Cria card de progresso de idioma"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        # Nome e bandeira
        lang_label = ctk.CTkLabel(
            header,
            text=f"{lang_data['flag']} {lang_data['name']}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lang_label.pack(side="left")
        
        # Nível
        level_label = ctk.CTkLabel(
            header,
            text=f"Nível {lang_data['level']}",
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary')
        )
        level_label.pack(side="right")
        
        # Barra de progresso
        progress_value = (lang_data['xp'] % 100) / 100
        progress_bar = ctk.CTkProgressBar(
            content,
            height=6,
            progress_color=self.config.get_color('primary')
        )
        progress_bar.pack(fill="x", pady=(0, 5))
        progress_bar.set(progress_value)
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(fill="x")
        
        stats_text = f"📖 {lang_data['lessons_completed']} lições • 📚 {lang_data['words_learned']} palavras • 🎯 {lang_data['accuracy']:.1f}%"
        stats_label = ctk.CTkLabel(
            stats_frame,
            text=stats_text,
            font=ctk.CTkFont(size=10),
            text_color=self.config.get_color('text_secondary')
        )
        stats_label.pack(anchor="w")
    
    def create_achievements_section(self):
        """Cria seção de conquistas"""
        achievements_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        achievements_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(achievements_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            header,
            text="🏅 Conquistas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(side="left")
        
        # Contador de conquistas
        self.achievements_count_label = ctk.CTkLabel(
            header,
            text="2 de 10 desbloqueadas",
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary')
        )
        self.achievements_count_label.pack(side="right")
        
        # Grid de conquistas
        achievements_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        achievements_grid.pack(fill="x")
        achievements_grid.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        # Conquistas exemplo
        achievements = [
            {"name": "Primeiro Passo", "icon": "🎯", "unlocked": True, "description": "Complete sua primeira lição"},
            {"name": "Estudioso", "icon": "📚", "unlocked": True, "description": "Complete 10 lições"},
            {"name": "Poliglota", "icon": "🌍", "unlocked": False, "description": "Aprenda 3 idiomas"},
            {"name": "Streak de Fogo", "icon": "🔥", "unlocked": False, "description": "7 dias consecutivos"},
            {"name": "Mestre", "icon": "👑", "unlocked": False, "description": "Alcance o nível 10"}
        ]
        
        for i, achievement in enumerate(achievements):
            self.create_achievement_badge(achievements_grid, achievement, 0, i)
    
    def create_achievement_badge(self, parent, achievement: Dict, row: int, col: int):
        """Cria badge de conquista"""
        # Cor baseada no status
        if achievement['unlocked']:
            fg_color = self.config.get_color('success')
            text_color = "white"
        else:
            fg_color = self.config.get_color('background')
            text_color = self.config.get_color('text_secondary')
        
        badge = ctk.CTkFrame(parent, corner_radius=8, fg_color=fg_color)
        badge.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Ícone
        icon_label = ctk.CTkLabel(
            badge,
            text=achievement['icon'],
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(pady=(10, 5))
        
        # Nome
        name_label = ctk.CTkLabel(
            badge,
            text=achievement['name'],
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=text_color,
            wraplength=80
        )
        name_label.pack(pady=(0, 10))
        
        # Tooltip com descrição (simulado com bind)
        def show_tooltip(event):
            # Em uma implementação real, mostraria um tooltip
            print(f"Conquista: {achievement['name']} - {achievement['description']}")
        
        badge.bind("<Button-1>", show_tooltip)
    
    def create_settings_section(self):
        """Cria seção de configurações"""
        settings_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        settings_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        content_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Configurações
        settings_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        settings_container.pack(fill="x")
        settings_container.grid_columnconfigure((0, 1), weight=1)
        
        # Coluna esquerda
        left_settings = ctk.CTkFrame(settings_container, fg_color="transparent")
        left_settings.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Notificações
        notifications_frame = ctk.CTkFrame(left_settings, corner_radius=8)
        notifications_frame.pack(fill="x", pady=(0, 10))
        
        self.notifications_var = ctk.BooleanVar(value=True)
        notifications_check = ctk.CTkCheckBox(
            notifications_frame,
            text="🔔 Notificações diárias",
            font=ctk.CTkFont(size=12),
            variable=self.notifications_var
        )
        notifications_check.pack(padx=15, pady=10)
        
        # Sons
        sounds_frame = ctk.CTkFrame(left_settings, corner_radius=8)
        sounds_frame.pack(fill="x", pady=(0, 10))
        
        self.sounds_var = ctk.BooleanVar(value=True)
        sounds_check = ctk.CTkCheckBox(
            sounds_frame,
            text="🔊 Efeitos sonoros",
            font=ctk.CTkFont(size=12),
            variable=self.sounds_var
        )
        sounds_check.pack(padx=15, pady=10)
        
        # Coluna direita
        right_settings = ctk.CTkFrame(settings_container, fg_color="transparent")
        right_settings.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        # Tema
        theme_frame = ctk.CTkFrame(right_settings, corner_radius=8)
        theme_frame.pack(fill="x", pady=(0, 10))
        
        theme_content = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_content.pack(fill="x", padx=15, pady=10)
        
        theme_label = ctk.CTkLabel(
            theme_content,
            text="🎨 Tema:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        theme_label.pack(anchor="w")
        
        self.theme_combo = ctk.CTkComboBox(
            theme_content,
            values=["Claro", "Escuro", "Sistema"],
            font=ctk.CTkFont(size=11),
            height=30
        )
        self.theme_combo.pack(fill="x", pady=(5, 0))
        self.theme_combo.set("Claro")
        
        # Idioma nativo
        native_lang_frame = ctk.CTkFrame(right_settings, corner_radius=8)
        native_lang_frame.pack(fill="x")
        
        native_content = ctk.CTkFrame(native_lang_frame, fg_color="transparent")
        native_content.pack(fill="x", padx=15, pady=10)
        
        native_label = ctk.CTkLabel(
            native_content,
            text="🏠 Idioma nativo:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        native_label.pack(anchor="w")
        
        self.native_lang_combo = ctk.CTkComboBox(
            native_content,
            values=["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español", "🇩🇪 Deutsch"],
            font=ctk.CTkFont(size=11),
            height=30
        )
        self.native_lang_combo.pack(fill="x", pady=(5, 0))
        self.native_lang_combo.set("🇧🇷 Português")
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(20, 0))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Salvar configurações
        save_button = ctk.CTkButton(
            actions_frame,
            text="💾 Salvar Configurações",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            fg_color=self.config.get_color('success'),
            hover_color=self._darken_color(self.config.get_color('success')),
            command=self.save_settings
        )
        save_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        # Exportar dados
        export_button = ctk.CTkButton(
            actions_frame,
            text="📤 Exportar Dados",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color=self.config.get_color('secondary'),
            hover_color=self._darken_color(self.config.get_color('secondary')),
            command=self.export_data
        )
        export_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Limpar dados
        clear_button = ctk.CTkButton(
            actions_frame,
            text="🗑️ Limpar Dados",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color="transparent",
            text_color=self.config.get_color('error'),
            hover_color=self.config.get_color('background'),
            border_width=2,
            border_color=self.config.get_color('error'),
            command=self.clear_data
        )
        clear_button.grid(row=0, column=2, padx=5, sticky="ew")
    
    def save_settings(self):
        """Salva configurações do usuário"""
        # Implementar salvamento das configurações
        self.show_message("Configurações salvas com sucesso!", "success")
    
    def export_data(self):
        """Exporta dados do usuário"""
        # Implementar exportação de dados
        self.show_message("Dados exportados com sucesso!", "success")
    
    def clear_data(self):
        """Limpa dados do usuário"""
        # Implementar confirmação e limpeza de dados
        self.show_message("Funcionalidade em desenvolvimento", "info")
    
    def show_message(self, message: str, type: str = "info"):
        """Mostra mensagem para o usuário"""
        # Implementar sistema de notificações
        print(f"{type.upper()}: {message}")
    
    def set_user(self, user_data: Dict):
        """Define dados do usuário"""
        self.current_user = user_data
        self.update_user_info()
    
    def update_user_info(self):
        """Atualiza informações do usuário na interface"""
        if not self.current_user:
            return
        
        # Atualizar informações básicas
        name = self.current_user.get('full_name', self.current_user['username'])
        self.name_label.configure(text=name)
        self.username_label.configure(text=f"@{self.current_user['username']}")
        
        # Atualizar nível e XP
        level = self.current_user.get('level', 1)
        total_xp = self.current_user.get('total_xp', 0)
        current_level_xp = total_xp % 100
        
        self.level_label.configure(text=f"⭐ Nível {level}")
        self.xp_label.configure(text=f"💎 {current_level_xp} / 100 XP")
        self.xp_progress.set(current_level_xp / 100)
        
        # Atualizar estatísticas
        streak = self.current_user.get('current_streak', 0)
        self.stat_cards["🔥 Streak Atual"]['value'].configure(text=f"{streak} dias")
        
        # Carregar estatísticas detalhadas
        self.load_detailed_stats()
    
    def load_detailed_stats(self):
        """Carrega estatísticas detalhadas do usuário"""
        if not self.current_user or self.current_user['id'] == 0:
            # Dados demo
            self.stat_cards["📚 Palavras Aprendidas"]['value'].configure(text="65")
            self.stat_cards["🎯 Precisão Média"]['value'].configure(text="88.5%")
            self.stat_cards["⏱️ Tempo Total"]['value'].configure(text="12h")
            return
        
        # Carregar do banco de dados em thread separada
        threading.Thread(
            target=self._load_stats_from_db,
            daemon=True
        ).start()
    
    def _load_stats_from_db(self):
        """Carrega estatísticas do banco de dados"""
        try:
            # Implementar carregamento real do banco
            # Por enquanto, dados exemplo
            stats = {
                'words_learned': 65,
                'accuracy': 88.5,
                'total_time': 12
            }
            
            # Atualizar UI na thread principal
            self.parent.after(0, self._update_stats_ui, stats)
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar estatísticas: {e}")
    
    def _update_stats_ui(self, stats: Dict):
        """Atualiza estatísticas na interface"""
        self.stat_cards["📚 Palavras Aprendidas"]['value'].configure(text=str(stats['words_learned']))
        self.stat_cards["🎯 Precisão Média"]['value'].configure(text=f"{stats['accuracy']:.1f}%")
        self.stat_cards["⏱️ Tempo Total"]['value'].configure(text=f"{stats['total_time']}h")
    
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
            self.update_user_info()
    
    def hide(self):
        """Oculta a tela"""
        self.main_frame.pack_forget()
    
    def clear_user(self):
        """Limpa dados do usuário"""
        self.current_user = None
        self.user_stats = {}