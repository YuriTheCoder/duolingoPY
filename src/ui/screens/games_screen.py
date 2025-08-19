#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela de Jogos do LinguaMaster Pro
Interface com diferentes jogos educativos
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, List, Optional
import random
import threading
import time

class GamesScreen:
    """Tela principal de jogos"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db_manager = main_window.get_db_manager()
        self.translation_manager = main_window.get_translation_manager()
        self.logger = main_window.get_logger()
        self.config = main_window.get_config()
        
        # Estado da tela
        self.current_user = None
        self.current_game = None
        self.game_data = {}
        
        # Criar interface
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets da tela de jogos"""
        # Container principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        
        # Cabeçalho
        self.create_header()
        
        # Seleção de jogos
        self.create_game_selection()
        
        # Área do jogo atual
        self.create_game_area()
    
    def create_header(self):
        """Cria cabeçalho da tela"""
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="🎮 Centro de Jogos",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.config.get_color('secondary')
        )
        title_label.pack(anchor="w")
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Aprenda se divertindo com jogos educativos interativos!",
            font=ctk.CTkFont(size=14),
            text_color=self.config.get_color('text_secondary')
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
    
    def create_game_selection(self):
        """Cria seleção de jogos"""
        selection_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título da seção
        title_label = ctk.CTkLabel(
            content_frame,
            text="🎯 Escolha seu Jogo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Grid de jogos
        games_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        games_grid.pack(fill="x")
        games_grid.grid_columnconfigure((0, 1), weight=1)
        
        # Definir jogos disponíveis
        games = [
            {
                'name': 'Quiz Rápido',
                'icon': '🧠',
                'description': 'Teste seus conhecimentos com perguntas de múltipla escolha',
                'difficulty': 'Fácil',
                'xp': '10-25 XP',
                'color': self.config.get_color('primary'),
                'action': 'quiz'
            },
            {
                'name': 'Flashcards',
                'icon': '🃏',
                'description': 'Memorize palavras com cartões interativos',
                'difficulty': 'Médio',
                'xp': '15-30 XP',
                'color': self.config.get_color('secondary'),
                'action': 'flashcards'
            },
            {
                'name': 'Associação',
                'icon': '🔗',
                'description': 'Conecte palavras com suas traduções',
                'difficulty': 'Fácil',
                'xp': '10-20 XP',
                'color': self.config.get_color('success'),
                'action': 'association'
            },
            {
                'name': 'Completar Frases',
                'icon': '📝',
                'description': 'Preencha as lacunas nas frases',
                'difficulty': 'Médio',
                'xp': '15-35 XP',
                'color': self.config.get_color('accent'),
                'action': 'fill_blanks'
            }
        ]
        
        # Criar cards dos jogos
        for i, game in enumerate(games):
            row = i // 2
            col = i % 2
            self.create_game_card(games_grid, game, row, col)
    
    def create_game_card(self, parent, game: Dict, row: int, col: int):
        """Cria card de jogo"""
        card = ctk.CTkFrame(parent, corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Container interno
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header do card
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        # Ícone e nome
        icon_name_frame = ctk.CTkFrame(header, fg_color="transparent")
        icon_name_frame.pack(side="left", fill="x", expand=True)
        
        icon_label = ctk.CTkLabel(
            icon_name_frame,
            text=game['icon'],
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        name_label = ctk.CTkLabel(
            icon_name_frame,
            text=game['name'],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack(side="left")
        
        # Dificuldade
        difficulty_label = ctk.CTkLabel(
            header,
            text=game['difficulty'],
            font=ctk.CTkFont(size=11),
            text_color=game['color']
        )
        difficulty_label.pack(side="right")
        
        # Descrição
        desc_label = ctk.CTkLabel(
            content,
            text=game['description'],
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('text_secondary'),
            wraplength=250
        )
        desc_label.pack(anchor="w", pady=(0, 10))
        
        # Footer com XP e botão
        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(fill="x")
        
        xp_label = ctk.CTkLabel(
            footer,
            text=f"💎 {game['xp']}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.config.get_color('accent')
        )
        xp_label.pack(side="left")
        
        play_button = ctk.CTkButton(
            footer,
            text="▶️ Jogar",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=80,
            fg_color=game['color'],
            hover_color=self._darken_color(game['color']),
            command=lambda action=game['action']: self.start_game(action)
        )
        play_button.pack(side="right")
    
    def create_game_area(self):
        """Cria área do jogo atual"""
        self.game_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.game_frame.pack(fill="x", padx=20, pady=10)
        
        # Inicialmente vazio - será preenchido quando um jogo for selecionado
        welcome_label = ctk.CTkLabel(
            self.game_frame,
            text="🎯 Selecione um jogo acima para começar!",
            font=ctk.CTkFont(size=16),
            text_color=self.config.get_color('text_secondary')
        )
        welcome_label.pack(pady=50)
    
    def start_game(self, game_type: str):
        """Inicia um jogo específico"""
        self.current_game = game_type
        
        # Limpar área do jogo
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Carregar jogo específico
        if game_type == 'quiz':
            self.create_quiz_game()
        elif game_type == 'flashcards':
            self.create_flashcards_game()
        elif game_type == 'association':
            self.create_association_game()
        elif game_type == 'fill_blanks':
            self.create_fill_blanks_game()
    
    def create_quiz_game(self):
        """Cria jogo de quiz"""
        content = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header do quiz
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="🧠 Quiz Rápido",
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
            command=self.back_to_selection
        )
        back_button.pack(side="right")
        
        # Configuração do quiz
        config_frame = ctk.CTkFrame(content, corner_radius=10)
        config_frame.pack(fill="x", pady=(0, 20))
        
        config_content = ctk.CTkFrame(config_frame, fg_color="transparent")
        config_content.pack(fill="x", padx=20, pady=15)
        config_content.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Seleção de idioma
        lang_frame = ctk.CTkFrame(config_content, fg_color="transparent")
        lang_frame.grid(row=0, column=0, padx=10, sticky="ew")
        
        lang_label = ctk.CTkLabel(
            lang_frame,
            text="Idioma:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lang_label.pack()
        
        languages = []
        for lang_code in self.config.get_supported_languages():
            if lang_code != 'pt':  # Excluir português como opção de aprendizado
                flag = self.config.get_language_flag(lang_code)
                name = self.config.get_language_name(lang_code)
                languages.append(f"{flag} {name}")
        
        self.quiz_lang_combo = ctk.CTkComboBox(
            lang_frame,
            values=languages,
            font=ctk.CTkFont(size=11),
            height=30
        )
        self.quiz_lang_combo.pack(pady=(5, 0))
        self.quiz_lang_combo.set(languages[0] if languages else "")
        
        # Seleção de dificuldade
        diff_frame = ctk.CTkFrame(config_content, fg_color="transparent")
        diff_frame.grid(row=0, column=1, padx=10, sticky="ew")
        
        diff_label = ctk.CTkLabel(
            diff_frame,
            text="Dificuldade:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        diff_label.pack()
        
        self.quiz_diff_combo = ctk.CTkComboBox(
            diff_frame,
            values=["🟢 Iniciante", "🟡 Intermediário", "🔴 Avançado"],
            font=ctk.CTkFont(size=11),
            height=30
        )
        self.quiz_diff_combo.pack(pady=(5, 0))
        self.quiz_diff_combo.set("🟢 Iniciante")
        
        # Número de perguntas
        questions_frame = ctk.CTkFrame(config_content, fg_color="transparent")
        questions_frame.grid(row=0, column=2, padx=10, sticky="ew")
        
        questions_label = ctk.CTkLabel(
            questions_frame,
            text="Perguntas:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        questions_label.pack()
        
        self.quiz_questions_combo = ctk.CTkComboBox(
            questions_frame,
            values=["5", "10", "15", "20"],
            font=ctk.CTkFont(size=11),
            height=30
        )
        self.quiz_questions_combo.pack(pady=(5, 0))
        self.quiz_questions_combo.set("10")
        
        # Botão iniciar quiz
        start_quiz_button = ctk.CTkButton(
            content,
            text="🚀 Iniciar Quiz",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color=self.config.get_color('primary'),
            hover_color=self._darken_color(self.config.get_color('primary')),
            command=self.start_quiz_questions
        )
        start_quiz_button.pack(pady=20)
    
    def start_quiz_questions(self):
        """Inicia as perguntas do quiz"""
        # Obter configurações
        lang_text = self.quiz_lang_combo.get()
        diff_text = self.quiz_diff_combo.get()
        num_questions = int(self.quiz_questions_combo.get())
        
        # Extrair código do idioma
        lang_code = 'en'  # Default
        if '🇺🇸' in lang_text:
            lang_code = 'en'
        elif '🇪🇸' in lang_text:
            lang_code = 'es'
        elif '🇩🇪' in lang_text:
            lang_code = 'de'
        
        # Extrair dificuldade
        difficulty = 'beginner'
        if '🟡' in diff_text:
            difficulty = 'intermediate'
        elif '🔴' in diff_text:
            difficulty = 'advanced'
        
        # Inicializar dados do quiz
        self.game_data = {
            'type': 'quiz',
            'language': lang_code,
            'difficulty': difficulty,
            'total_questions': num_questions,
            'current_question': 0,
            'correct_answers': 0,
            'questions': [],
            'start_time': time.time()
        }
        
        # Gerar perguntas
        self.generate_quiz_questions()
    
    def generate_quiz_questions(self):
        """Gera perguntas do quiz"""
        # Por enquanto, perguntas exemplo
        # Futuramente, carregar do banco de dados
        sample_questions = [
            {
                'question': 'Como se diz "casa" em inglês?',
                'options': ['House', 'Car', 'Tree', 'Book'],
                'correct': 0,
                'word': 'casa'
            },
            {
                'question': 'Qual é a tradução de "water"?',
                'options': ['Fogo', 'Água', 'Terra', 'Ar'],
                'correct': 1,
                'word': 'water'
            },
            {
                'question': 'Como se diz "obrigado" em inglês?',
                'options': ['Please', 'Sorry', 'Thank you', 'Excuse me'],
                'correct': 2,
                'word': 'obrigado'
            }
        ]
        
        # Duplicar e embaralhar para ter mais perguntas
        all_questions = sample_questions * (self.game_data['total_questions'] // len(sample_questions) + 1)
        random.shuffle(all_questions)
        self.game_data['questions'] = all_questions[:self.game_data['total_questions']]
        
        # Mostrar primeira pergunta
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Mostra pergunta atual do quiz"""
        # Limpar área do jogo
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        content = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        current_q = self.game_data['current_question']
        total_q = self.game_data['total_questions']
        question_data = self.game_data['questions'][current_q]
        
        # Header com progresso
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        progress_label = ctk.CTkLabel(
            header,
            text=f"Pergunta {current_q + 1} de {total_q}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        progress_label.pack(side="left")
        
        score_label = ctk.CTkLabel(
            header,
            text=f"Acertos: {self.game_data['correct_answers']}/{current_q}",
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('success')
        )
        score_label.pack(side="right")
        
        # Barra de progresso
        progress_bar = ctk.CTkProgressBar(
            content,
            height=8,
            progress_color=self.config.get_color('primary')
        )
        progress_bar.pack(fill="x", pady=(0, 30))
        progress_bar.set((current_q + 1) / total_q)
        
        # Pergunta
        question_frame = ctk.CTkFrame(content, corner_radius=12)
        question_frame.pack(fill="x", pady=(0, 20))
        
        question_label = ctk.CTkLabel(
            question_frame,
            text=question_data['question'],
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=600
        )
        question_label.pack(pady=30)
        
        # Opções de resposta
        options_frame = ctk.CTkFrame(content, fg_color="transparent")
        options_frame.pack(fill="x")
        options_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.quiz_buttons = []
        for i, option in enumerate(question_data['options']):
            row = i // 2
            col = i % 2
            
            btn = ctk.CTkButton(
                options_frame,
                text=f"{chr(65 + i)}) {option}",
                font=ctk.CTkFont(size=14),
                height=50,
                fg_color=self.config.get_color('surface'),
                text_color=self.config.get_color('text'),
                hover_color=self.config.get_color('background'),
                border_width=2,
                border_color=self.config.get_color('text_secondary'),
                command=lambda idx=i: self.answer_quiz_question(idx)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            self.quiz_buttons.append(btn)
    
    def answer_quiz_question(self, selected_option: int):
        """Processa resposta da pergunta"""
        current_q = self.game_data['current_question']
        question_data = self.game_data['questions'][current_q]
        correct_option = question_data['correct']
        
        # Desabilitar botões
        for btn in self.quiz_buttons:
            btn.configure(state="disabled")
        
        # Colorir botões
        for i, btn in enumerate(self.quiz_buttons):
            if i == correct_option:
                btn.configure(fg_color=self.config.get_color('success'))
            elif i == selected_option and i != correct_option:
                btn.configure(fg_color=self.config.get_color('error'))
        
        # Atualizar pontuação
        if selected_option == correct_option:
            self.game_data['correct_answers'] += 1
        
        # Próxima pergunta após delay
        self.parent.after(2000, self.next_quiz_question)
    
    def next_quiz_question(self):
        """Vai para próxima pergunta ou finaliza quiz"""
        self.game_data['current_question'] += 1
        
        if self.game_data['current_question'] < self.game_data['total_questions']:
            self.show_quiz_question()
        else:
            self.finish_quiz()
    
    def finish_quiz(self):
        """Finaliza quiz e mostra resultados"""
        # Calcular estatísticas
        total_questions = self.game_data['total_questions']
        correct_answers = self.game_data['correct_answers']
        accuracy = (correct_answers / total_questions) * 100
        time_taken = int(time.time() - self.game_data['start_time'])
        xp_earned = correct_answers * 5  # 5 XP por resposta correta
        
        # Limpar área do jogo
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        content = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título dos resultados
        title_label = ctk.CTkLabel(
            content,
            text="🎉 Quiz Concluído!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.config.get_color('success')
        )
        title_label.pack(pady=(0, 20))
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(content, corner_radius=12)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_content = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_content.pack(fill="x", padx=30, pady=25)
        stats_content.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Cards de estatísticas
        stats = [
            ("🎯 Precisão", f"{accuracy:.1f}%", self.config.get_color('primary')),
            ("✅ Acertos", f"{correct_answers}/{total_questions}", self.config.get_color('success')),
            ("⏱️ Tempo", f"{time_taken}s", self.config.get_color('secondary')),
            ("💎 XP Ganho", f"+{xp_earned}", self.config.get_color('accent'))
        ]
        
        for i, (title, value, color) in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_content)
            stat_frame.grid(row=0, column=i, padx=5, sticky="ew")
            
            title_label = ctk.CTkLabel(
                stat_frame,
                text=title,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=color
            )
            title_label.pack(pady=(15, 5))
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            value_label.pack(pady=(0, 15))
        
        # Botões de ação
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Jogar novamente
        play_again_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Jogar Novamente",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color=self.config.get_color('primary'),
            hover_color=self._darken_color(self.config.get_color('primary')),
            command=self.create_quiz_game
        )
        play_again_btn.grid(row=0, column=0, padx=10, sticky="ew")
        
        # Outros jogos
        other_games_btn = ctk.CTkButton(
            buttons_frame,
            text="🎮 Outros Jogos",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="transparent",
            text_color=self.config.get_color('text'),
            hover_color=self.config.get_color('background'),
            border_width=2,
            border_color=self.config.get_color('text_secondary'),
            command=self.back_to_selection
        )
        other_games_btn.grid(row=0, column=1, padx=10, sticky="ew")
        
        # Dashboard
        dashboard_btn = ctk.CTkButton(
            buttons_frame,
            text="🏠 Dashboard",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color=self.config.get_color('secondary'),
            hover_color=self._darken_color(self.config.get_color('secondary')),
            command=lambda: self.main_window.show_screen('dashboard')
        )
        dashboard_btn.grid(row=0, column=2, padx=10, sticky="ew")
        
        # Registrar atividade
        if self.current_user and self.current_user['id'] != 0:
            self.db_manager.record_activity(
                self.current_user['id'],
                'quiz',
                self.game_data['language'],
                int(accuracy),
                100,
                xp_earned,
                time_spent=time_taken,
                correct_answers=correct_answers,
                total_questions=total_questions,
                difficulty_level=self.game_data['difficulty']
            )
            
            # Atualizar XP do usuário
            self.db_manager.update_user_xp(
                self.current_user['id'],
                xp_earned,
                self.game_data['language']
            )
    
    def create_flashcards_game(self):
        """Cria jogo de flashcards"""
        content = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="🃏 Flashcards",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.config.get_color('secondary')
        )
        title_label.pack(side="left")
        
        back_button = ctk.CTkButton(
            header,
            text="← Voltar",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color="transparent",
            text_color=self.config.get_color('text_secondary'),
            hover_color=self.config.get_color('background'),
            command=self.back_to_selection
        )
        back_button.pack(side="right")
        
        # Placeholder para flashcards
        placeholder_label = ctk.CTkLabel(
            content,
            text="🚧 Flashcards em desenvolvimento...\nEm breve você poderá praticar com cartões interativos!",
            font=ctk.CTkFont(size=16),
            text_color=self.config.get_color('text_secondary')
        )
        placeholder_label.pack(expand=True)
    
    def create_association_game(self):
        """Cria jogo de associação"""
        content = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="🔗 Associação",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.config.get_color('success')
        )
        title_label.pack(side="left")
        
        back_button = ctk.CTkButton(
            header,
            text="← Voltar",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color="transparent",
            text_color=self.config
.get_color('text_secondary'),
            hover_color=self.config.get_color('background'),
            command=self.back_to_selection
        )
        back_button.pack(side="right")
        
        # Placeholder para associação
        placeholder_label = ctk.CTkLabel(
            content,
            text="🚧 Jogo de Associação em desenvolvimento...\nEm breve você poderá conectar palavras com suas traduções!",
            font=ctk.CTkFont(size=16),
            text_color=self.config.get_color('text_secondary')
        )
        placeholder_label.pack(expand=True)
    
    def create_fill_blanks_game(self):
        """Cria jogo de completar frases"""
        content = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="📝 Completar Frases",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.config.get_color('accent')
        )
        title_label.pack(side="left")
        
        back_button = ctk.CTkButton(
            header,
            text="← Voltar",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color="transparent",
            text_color=self.config.get_color('text_secondary'),
            hover_color=self.config.get_color('background'),
            command=self.back_to_selection
        )
        back_button.pack(side="right")
        
        # Placeholder para completar frases
        placeholder_label = ctk.CTkLabel(
            content,
            text="🚧 Completar Frases em desenvolvimento...\nEm breve você poderá preencher lacunas em frases!",
            font=ctk.CTkFont(size=16),
            text_color=self.config.get_color('text_secondary')
        )
        placeholder_label.pack(expand=True)
    
    def back_to_selection(self):
        """Volta para seleção de jogos"""
        self.current_game = None
        self.game_data = {}
        
        # Limpar área do jogo
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Mostrar mensagem de boas-vindas
        welcome_label = ctk.CTkLabel(
            self.game_frame,
            text="🎯 Selecione um jogo acima para começar!",
            font=ctk.CTkFont(size=16),
            text_color=self.config.get_color('text_secondary')
        )
        welcome_label.pack(pady=50)
    
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
        self.back_to_selection()