#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Principal do LinguaMaster Pro
Janela principal com navegação e telas do aplicativo
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, Optional
import threading
from datetime import datetime

from src.ui.screens.login_screen import LoginScreen
from src.ui.screens.dashboard_screen import DashboardScreen
from src.ui.screens.lesson_screen import LessonScreen
from src.ui.screens.games_screen import GamesScreen
from src.ui.screens.profile_screen import ProfileScreen
from src.ui.screens.translator_screen import TranslatorScreen
from src.core.translation_api import TranslationManager

class MainWindow:
    """Janela principal da aplicação"""
    
    def __init__(self, db_manager, config, logger):
        self.db_manager = db_manager
        self.config = config
        self.logger = logger
        self.translation_manager = TranslationManager()
        
        # Estado da aplicação
        self.current_user = None
        self.current_screen = None
        self.screens = {}
        
        # Configurar janela principal
        self.root = ctk.CTk()
        self._setup_window()
        self._setup_theme()
        self._create_main_layout()
        self._initialize_screens()
        
        # Mostrar tela de login inicialmente
        self.show_screen('login')
    
    def _setup_window(self):
        """Configura propriedades da janela"""
        self.root.title(self.config.get('app.name', 'LinguaMaster Pro'))
        
        # Dimensões da janela
        width = self.config.get('app.window_width', 1200)
        height = self.config.get('app.window_height', 800)
        min_width = self.config.get('app.min_width', 800)
        min_height = self.config.get('app.min_height', 600)
        
        # Centralizar janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(min_width, min_height)
        
        # Ícone da aplicação (se disponível)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
    
    def _setup_theme(self):
        """Configura tema da aplicação"""
        # Configurar tema CustomTkinter
        ctk.set_appearance_mode(self.config.get('app.theme', 'light'))
        ctk.set_default_color_theme("blue")
        
        # Cores personalizadas do Duolingo
        self.colors = {
            'primary': self.config.get_color('primary'),
            'secondary': self.config.get_color('secondary'),
            'accent': self.config.get_color('accent'),
            'success': self.config.get_color('success'),
            'error': self.config.get_color('error'),
            'warning': self.config.get_color('warning'),
            'background': self.config.get_color('background'),
            'surface': self.config.get_color('surface'),
            'text': self.config.get_color('text'),
            'text_secondary': self.config.get_color('text_secondary')
        }
    
    def _create_main_layout(self):
        """Cria layout principal da aplicação"""
        # Container principal
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra lateral de navegação (inicialmente oculta)
        self.sidebar = ctk.CTkFrame(self.main_container, width=250, corner_radius=15)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar.pack_forget()  # Ocultar inicialmente
        
        # Área de conteúdo principal
        self.content_area = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        self._create_sidebar()
    
    def _create_sidebar(self):
        """Cria barra lateral de navegação"""
        # Logo/Título
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="🎯 LinguaMaster Pro",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack()
        
        # Botões de navegação
        nav_buttons = [
            ("🏠 Dashboard", "dashboard", self.colors['primary']),
            ("📚 Lições", "lessons", self.colors['secondary']),
            ("🎮 Jogos", "games", self.colors['accent']),
            ("🌍 Tradutor", "translator", self.colors['success']),
            ("👤 Perfil", "profile", self.colors['text'])
        ]
        
        self.nav_buttons = {}
        for text, screen_name, color in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=ctk.CTkFont(size=14, weight="bold"),
                height=45,
                corner_radius=10,
                fg_color=color,
                hover_color=self._darken_color(color),
                command=lambda s=screen_name: self.show_screen(s)
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.nav_buttons[screen_name] = btn
        
        # Espaçador
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        # Informações do usuário (quando logado)
        self.user_info_frame = ctk.CTkFrame(self.sidebar, corner_radius=10)
        self.user_info_frame.pack(fill="x", padx=20, pady=20)
        
        # Botão de logout
        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Sair",
            font=ctk.CTkFont(size=12),
            height=35,
            corner_radius=8,
            fg_color=self.colors['error'],
            hover_color=self._darken_color(self.colors['error']),
            command=self.logout
        )
        self.logout_btn.pack(fill="x", padx=20, pady=(0, 20))
    
    def _initialize_screens(self):
        """Inicializa todas as telas da aplicação"""
        self.screens = {
            'login': LoginScreen(self.content_area, self),
            'dashboard': DashboardScreen(self.content_area, self),
            'lessons': LessonScreen(self.content_area, self),
            'games': GamesScreen(self.content_area, self),
            'profile': ProfileScreen(self.content_area, self),
            'translator': TranslatorScreen(self.content_area, self)
        }
    
    def show_screen(self, screen_name: str):
        """Mostra tela específica"""
        if screen_name not in self.screens:
            self.logger.error(f"Tela não encontrada: {screen_name}")
            return
        
        # Ocultar tela atual
        if self.current_screen:
            self.screens[self.current_screen].hide()
        
        # Mostrar nova tela
        self.screens[screen_name].show()
        self.current_screen = screen_name
        
        # Atualizar navegação
        self._update_navigation(screen_name)
        
        self.logger.info(f"Tela alterada para: {screen_name}")
    
    def _update_navigation(self, screen_name: str):
        """Atualiza estado da navegação"""
        # Mostrar/ocultar sidebar baseado na tela
        if screen_name == 'login':
            self.sidebar.pack_forget()
            self.content_area.pack(side="left", fill="both", expand=True)
        else:
            if not self.sidebar.winfo_viewable():
                self.sidebar.pack(side="left", fill="y", padx=(0, 10))
                self.content_area.pack(side="right", fill="both", expand=True)
        
        # Destacar botão ativo
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == screen_name:
                btn.configure(fg_color=self.colors['primary'])
            else:
                # Restaurar cor original baseada no tipo
                original_colors = {
                    'dashboard': self.colors['primary'],
                    'lessons': self.colors['secondary'],
                    'games': self.colors['accent'],
                    'translator': self.colors['success'],
                    'profile': self.colors['text']
                }
                btn.configure(fg_color=original_colors.get(btn_name, self.colors['text']))
    
    def login_success(self, user_data: Dict):
        """Callback para login bem-sucedido"""
        self.current_user = user_data
        self._update_user_info()
        self.show_screen('dashboard')
        
        # Atualizar dados do usuário nas telas
        for screen in self.screens.values():
            if hasattr(screen, 'set_user'):
                screen.set_user(user_data)
        
        self.logger.log_user_action(user_data['id'], 'login')
    
    def logout(self):
        """Faz logout do usuário"""
        if self.current_user:
            self.logger.log_user_action(self.current_user['id'], 'logout')
        
        self.current_user = None
        self._clear_user_info()
        self.show_screen('login')
        
        # Limpar dados das telas
        for screen in self.screens.values():
            if hasattr(screen, 'clear_user'):
                screen.clear_user()
    
    def _update_user_info(self):
        """Atualiza informações do usuário na sidebar"""
        if not self.current_user:
            return
        
        # Limpar frame anterior
        for widget in self.user_info_frame.winfo_children():
            widget.destroy()
        
        # Nome do usuário
        name_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"👋 {self.current_user.get('full_name', self.current_user['username'])}",
            font=ctk.CTkFont(size=12, weight="bold"),
            wraplength=200
        )
        name_label.pack(pady=(10, 5))
        
        # Nível e XP
        level = self.current_user.get('level', 1)
        xp = self.current_user.get('total_xp', 0)
        
        level_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"⭐ Nível {level}",
            font=ctk.CTkFont(size=11)
        )
        level_label.pack()
        
        xp_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"💎 {xp} XP",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['accent']
        )
        xp_label.pack(pady=(0, 10))
        
        # Streak atual
        streak = self.current_user.get('current_streak', 0)
        if streak > 0:
            streak_label = ctk.CTkLabel(
                self.user_info_frame,
                text=f"🔥 {streak} dias",
                font=ctk.CTkFont(size=11),
                text_color=self.colors['error']
            )
            streak_label.pack(pady=(0, 10))
    
    def _clear_user_info(self):
        """Limpa informações do usuário"""
        for widget in self.user_info_frame.winfo_children():
            widget.destroy()
    
    def _darken_color(self, color: str, factor: float = 0.8) -> str:
        """Escurece uma cor para efeito hover"""
        # Implementação simples - pode ser melhorada
        if color.startswith('#'):
            # Converter hex para RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Escurecer
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        
        return color
    
    def show_message(self, title: str, message: str, type: str = "info"):
        """Mostra mensagem para o usuário"""
        # Implementar sistema de notificações/toasts
        print(f"{type.upper()}: {title} - {message}")
    
    def get_current_user(self) -> Optional[Dict]:
        """Retorna usuário atual"""
        return self.current_user
    
    def get_db_manager(self):
        """Retorna gerenciador de banco de dados"""
        return self.db_manager
    
    def get_translation_manager(self):
        """Retorna gerenciador de tradução"""
        return self.translation_manager
    
    def get_config(self):
        """Retorna configurações"""
        return self.config
    
    def get_logger(self):
        """Retorna logger"""
        return self.logger
    
    def run(self):
        """Inicia loop principal da aplicação"""
        try:
            self.logger.info("Interface gráfica iniciada")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Erro na interface gráfica: {e}")
            raise
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Limpa recursos antes de fechar"""
        try:
            if self.translation_manager:
                self.translation_manager.close()
            self.logger.info("Recursos da interface limpos")
        except Exception as e:
            self.logger.error(f"Erro na limpeza: {e}")