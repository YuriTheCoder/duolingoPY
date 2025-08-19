#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela de Lições do LinguaMaster Pro
Interface para lições estruturadas de idiomas
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, List, Optional
import threading
import random

class LessonScreen:
    """Tela de lições"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db_manager = main_window.get_db_manager()
        self.translation_manager = main_window.get_translation_manager()
        self.logger = main_window.get_logger()
        self.config = main_window.get_config()
        
        # Estado da tela
        self.current_user = None
        self.available_lessons = []
        self.current_lesson = None
        
        # Criar interface
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets da tela de lições"""
        # Container principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        
        # Cabeçalho
        self.create_header()
        
        # Seleção de idioma
        self.create_language_selector()
        
        # Lista de lições
        self.create_lessons_list()
    
    def create_header(self):
        """Cria cabeçalho da tela"""
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="📚 Centro de Lições",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.config.get_color('secondary')
        )
        title_label.pack(anchor="w")
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Aprenda de forma estruturada com lições organizadas por nível!",
            font=ctk.CTkFont(size=14),
            text_color=self.config.get_color('text_secondary')
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
    
    def create_language_selector(self):
        """Cria seletor de idioma"""
        selector_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        selector_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(selector_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=25, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="🌍 Escolha o Idioma",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Botões de idiomas
        languages_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        languages_frame.pack(fill="x")
        languages_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Idiomas disponíveis (excluindo português)
        languages = [
            ('en', '🇺🇸', 'English', self.config.get_color('primary')),
            ('es', '🇪🇸', 'Español', self.config.get_color('success')),
            ('de', '🇩🇪', 'Deutsch', self.config.get_color('accent'))
        ]
        
        self.language_buttons = {}
        for i, (code, flag, name, color) in enumerate(languages):
            btn = ctk.CTkButton(
                languages_frame,
                text=f"{flag} {name}",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=45,
                fg_color=color,
                hover_color=self._darken_color(color),
                command=lambda c=code: self.select_language(c)
            )
            btn.grid(row=0, column=i, padx=10, sticky="ew")
            self.language_buttons[code] = btn
        
        # Idioma selecionado inicialmente
        self.selected_language = 'en'
    
    def create_lessons_list(self):
        """Cria lista de lições"""
        self.lessons_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.lessons_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Carregar lições iniciais
        self.load_lessons()
    
    def select_language(self, language_code: str):
        """Seleciona idioma e carrega lições"""
        self.selected_language = language_code
        
        # Atualizar visual dos botões
        for code, btn in self.language_buttons.items():
            if code == language_code:
                btn.configure(fg_color=self.config.get_color('primary'))
            else:
                # Restaurar cor original
                colors = {'en': self.config.get_color('primary'), 
                         'es': self.config.get_color('success'), 
                         'de': self.config.get_color('accent')}
                btn.configure(fg_color=colors.get(code, self.config.get_color('text')))
        
        # Recarregar lições
        self.load_lessons()
    
    def load_lessons(self):
        """Carrega lições do idioma selecionado"""
        # Limpar lições atuais
        for widget in self.lessons_frame.winfo_children():
            widget.destroy()
        
        content_frame = ctk.CTkFrame(self.lessons_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título da seção
        flag = self.config.get_language_flag(self.selected_language)
        name = self.config.get_language_name(self.selected_language)
        
        title_label = ctk.CTkLabel(
            content_frame,
            text=f"📖 Lições de {flag} {name}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Lições exemplo (futuramente do banco de dados)
        lessons = [
            {
                'id': 1,
                'title': 'Primeiras Palavras',
                'description': 'Aprenda vocabulário básico essencial',
                'difficulty': 'Iniciante',
                'words_count': 15,
                'xp_reward': 50,
                'completed': True,
                'locked': False,
                'progress': 100
            },
            {
                'id': 2,
                'title': 'Família e Relacionamentos',
                'description': 'Vocabulário sobre família e pessoas próximas',
                'difficulty': 'Iniciante',
                'words_count': 20,
                'xp_reward': 60,
                'completed': False,
                'locked': False,
                'progress': 65
            },
            {
                'id': 3,
                'title': 'Casa e Móveis',
                'description': 'Aprenda sobre objetos domésticos',
                'difficulty': 'Iniciante',
                'words_count': 25,
                'xp_reward': 70,
                'completed': False,
                'locked': False,
                'progress': 0
            },
            {
                'id': 4,
                'title': 'Comida e Bebidas',
                'description': 'Vocabulário culinário essencial',
                'difficulty': 'Intermediário',
                'words_count': 30,
                'xp_reward': 80,
                'completed': False,
                'locked': True,
                'progress': 0
            },
            {
                'id': 5,
                'title': 'Viagem e Transporte',
                'description': 'Palavras úteis para viagens',
                'difficulty': 'Intermediário',
                'words_count': 35,
                'xp_reward': 90,
                'completed': False,
                'locked': True,
                'progress': 0
            }
        ]
        
        # Criar cards das lições
        for lesson in lessons:
            self.create_lesson_card(content_frame, lesson)
    
    def create_lesson_card(self, parent, lesson: Dict):
        """Cria card de lição"""
        # Card principal
        card = ctk.CTkFrame(parent, corner_radius=12)
        card.pack(fill="x", pady=10)
        
        # Aplicar opacidade se bloqueado
        if lesson['locked']:
            card.configure(fg_color=self.config.get_color('background'))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header da lição
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        # Lado esquerdo - Info da lição
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Título e status
        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=lesson['title'],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Status icons
        if lesson['completed']:
            status_label = ctk.CTkLabel(
                title_frame,
                text="✅",
                font=ctk.CTkFont(size=14)
            )
            status_label.pack(side="left", padx=(10, 0))
        elif lesson['locked']:
            status_label = ctk.CTkLabel(
                title_frame,
                text="🔒",
                font=ctk.CTkFont(size=14)
            )
            status_label.pack(side="left", padx=(10, 0))
        elif lesson['progress'] > 0:
            status_label = ctk.CTkLabel(
                title_frame,
                text="📖",
                font=ctk.CTkFont(size=14)
            )
            status_label.pack(side="left", padx=(10, 0))
        
        # Descrição
        desc_label = ctk.CTkLabel(
            left_frame,
            text=lesson['description'],
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary'),
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(2, 0))
        
        # Lado direito - Dificuldade e XP
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right")
        
        # Dificuldade
        diff_colors = {
            'Iniciante': self.config.get_color('success'),
            'Intermediário': self.config.get_color('warning'),
            'Avançado': self.config.get_color('error')
        }
        
        diff_label = ctk.CTkLabel(
            right_frame,
            text=lesson['difficulty'],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=diff_colors.get(lesson['difficulty'], self.config.get_color('text'))
        )
        diff_label.pack(anchor="e")
        
        # XP
        xp_label = ctk.CTkLabel(
            right_frame,
            text=f"💎 {lesson['xp_reward']} XP",
            font=ctk.CTkFont(size=11),
            text_color=self.config.get_color('accent')
        )
        xp_label.pack(anchor="e", pady=(2, 0))
        
        # Progresso (se iniciado)
        if lesson['progress'] > 0 and not lesson['completed']:
            progress_frame = ctk.CTkFrame(content, fg_color="transparent")
            progress_frame.pack(fill="x", pady=(5, 10))
            
            progress_bar = ctk.CTkProgressBar(
                progress_frame,
                height=6,
                progress_color=self.config.get_color('primary')
            )
            progress_bar.pack(fill="x")
            progress_bar.set(lesson['progress'] / 100)
            
            progress_label = ctk.CTkLabel(
                progress_frame,
                text=f"{lesson['progress']}% concluído",
                font=ctk.CTkFont(size=10),
                text_color=self.config.get_color('text_secondary')
            )
            progress_label.pack(anchor="w", pady=(2, 0))
        
        # Footer com detalhes e botão
        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(fill="x")
        
        # Detalhes
        details_label = ctk.CTkLabel(
            footer,
            text=f"📝 {lesson['words_count']} palavras",
            font=ctk.CTkFont(size=11),
            text_color=self.config.get_color('text_secondary')
        )
        details_label.pack(side="left")
        
        # Botão de ação
        if lesson['locked']:
            action_button = ctk.CTkButton(
                footer,
                text="🔒 Bloqueado",
                font=ctk.CTkFont(size=12),
                height=35,
                width=100,
                fg_color="transparent",
                text_color=self.config.get_color('text_secondary'),
                state="disabled"
            )
        elif lesson['completed']:
            action_button = ctk.CTkButton(
                footer,
                text="🔄 Revisar",
                font=ctk.CTkFont(size=12),
                height=35,
                width=100,
                fg_color=self.config.get_color('secondary'),
                hover_color=self._darken_color(self.config.get_color('secondary')),
                command=lambda l=lesson: self.start_lesson(l)
            )
        elif lesson['progress'] > 0:
            action_button = ctk.CTkButton(
                footer,
                text="▶️ Continuar",
                font=ctk.CTkFont(size=12),
                height=35,
                width=100,
                fg_color=self.config.get_color('primary'),
                hover_color=self._darken_color(self.config.get_color('primary')),
                command=lambda l=lesson: self.start_lesson(l)
            )
        else:
            action_button = ctk.CTkButton(
                footer,
                text="🚀 Iniciar",
                font=ctk.CTkFont(size=12),
                height=35,
                width=100,
                fg_color=self.config.get_color('success'),
                hover_color=self._darken_color(self.config.get_color('success')),
                command=lambda l=lesson: self.start_lesson(l)
            )
        
        action_button.pack(side="right")
    
    def start_lesson(self, lesson: Dict):
        """Inicia uma lição"""
        self.current_lesson = lesson
        
        # Limpar frame principal
        for widget in self.lessons_frame.winfo_children():
            widget.destroy()
        
        # Criar interface da lição
        self.create_lesson_interface()
    
    def create_lesson_interface(self):
        """Cria interface da lição em andamento"""
        content_frame = ctk.CTkFrame(self.lessons_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header da lição
        header = ctk.CTkFrame(content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        # Título da lição
        title_label = ctk.CTkLabel(
            header,
            text=f"📖 {self.current_lesson['title']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.config.get_color('primary')
        )
        title_label.pack(side="left")
        
        # Botão voltar
        back_button = ctk.CTkButton(
            header,
            text="← Voltar",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color="transparent",
            text_color=self.config.get_color('text_secondary'),
            hover_color=self.config.get_color('background'),
            command=self.back_to_lessons
        )
        back_button.pack(side="right")
        
        # Progresso da lição
        progress_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        progress_content = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_content.pack(fill="x", padx=20, pady=15)
        
        progress_label = ctk.CTkLabel(
            progress_content,
            text="Progresso da Lição",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        progress_label.pack(anchor="w")
        
        progress_bar = ctk.CTkProgressBar(
            progress_content,
            height=8,
            progress_color=self.config.get_color('success')
        )
        progress_bar.pack(fill="x", pady=(5, 0))
        progress_bar.set(0.3)  # Exemplo: 30% concluído
        
        # Conteúdo da lição
        lesson_content = ctk.CTkFrame(content_frame, corner_radius=12)
        lesson_content.pack(fill="x", pady=(0, 20))
        
        # Placeholder para conteúdo da lição
        placeholder_content = ctk.CTkFrame(lesson_content, fg_color="transparent")
        placeholder_content.pack(fill="both", expand=True, padx=30, pady=40)
        
        placeholder_label = ctk.CTkLabel(
            placeholder_content,
            text=f"🚧 Lição '{self.current_lesson['title']}' em desenvolvimento...\n\nEm breve você terá acesso a:\n• Vocabulário interativo\n• Exercícios práticos\n• Áudio de pronúncia\n• Testes de compreensão",
            font=ctk.CTkFont(size=16),
            text_color=self.config.get_color('text_secondary'),
            justify="center"
        )
        placeholder_label.pack(expand=True)
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x")
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Botão anterior
        prev_button = ctk.CTkButton(
            actions_frame,
            text="⬅️ Anterior",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="transparent",
            text_color=self.config.get_color('text'),
            hover_color=self.config.get_color('background'),
            border_width=2,
            border_color=self.config.get_color('text_secondary'),
            state="disabled"  # Desabilitado no primeiro item
        )
        prev_button.grid(row=0, column=0, padx=10, sticky="ew")
        
        # Botão praticar
        practice_button = ctk.CTkButton(
            actions_frame,
            text="🎯 Praticar Vocabulário",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color=self.config.get_color('primary'),
            hover_color=self._darken_color(self.config.get_color('primary')),
            command=self.practice_vocabulary
        )
        practice_button.grid(row=0, column=1, padx=10, sticky="ew")
        
        # Botão próximo
        next_button = ctk.CTkButton(
            actions_frame,
            text="Próximo ➡️",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color=self.config.get_color('success'),
            hover_color=self._darken_color(self.config.get_color('success'))
        )
        next_button.grid(row=0, column=2, padx=10, sticky="ew")
    
    def practice_vocabulary(self):
        """Inicia prática de vocabulário da lição"""
        # Redirecionar para jogos com contexto da lição
        self.main_window.show_screen('games')
    
    def back_to_lessons(self):
        """Volta para lista de lições"""
        self.current_lesson = None
        self.load_lessons()
    
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
    
    def set_user(self, user_data: Dict):
        """Define dados do usuário"""
        self.current_user = user_data
    
    def show(self):
        """Mostra a tela"""
        self.main_frame.pack(fill="both", expand=True)
    
    def hide(self):
        """Oculta a tela"""
        self.main_frame.pack_forget()
    
    def clear_user(self):
        """Limpa dados do usuário"""
        self.current_user = None
        self.current_lesson = None
        self.load_lessons()