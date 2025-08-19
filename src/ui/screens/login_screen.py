#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela de Login do LinguaMaster Pro
Interface de autenticação e registro de usuários
"""

import tkinter as tk
import customtkinter as ctk
from typing import Optional
import threading
import re

class LoginScreen:
    """Tela de login e registro"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db_manager = main_window.get_db_manager()
        self.logger = main_window.get_logger()
        self.config = main_window.get_config()
        
        # Estado da tela
        self.is_login_mode = True
        self.is_loading = False
        
        # Criar interface
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets da tela de login"""
        # Container principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # Container centralizado
        self.center_frame = ctk.CTkFrame(
            self.main_frame,
            width=450,
            height=600,
            corner_radius=20,
            fg_color=self.config.get_color('surface')
        )
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)
        
        # Logo e título
        self.create_header()
        
        # Formulário
        self.create_form()
        
        # Botões de ação
        self.create_action_buttons()
        
        # Link para alternar modo
        self.create_toggle_link()
        
        # Mensagem de status
        self.create_status_message()
    
    def create_header(self):
        """Cria cabeçalho com logo e título"""
        header_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(40, 20))
        
        # Logo emoji grande
        logo_label = ctk.CTkLabel(
            header_frame,
            text="🎯",
            font=ctk.CTkFont(size=60)
        )
        logo_label.pack(pady=(0, 10))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="LinguaMaster Pro",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.config.get_color('primary')
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Aprenda idiomas de forma divertida!",
            font=ctk.CTkFont(size=14),
            text_color=self.config.get_color('text_secondary')
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_form(self):
        """Cria formulário de login/registro"""
        self.form_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=40, pady=20)
        
        # Campo de usuário
        self.username_label = ctk.CTkLabel(
            self.form_frame,
            text="👤 Nome de usuário",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            self.form_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Digite seu nome de usuário",
            corner_radius=10
        )
        self.username_entry.pack(fill="x", pady=(0, 15))
        
        # Campo de email (apenas para registro)
        self.email_label = ctk.CTkLabel(
            self.form_frame,
            text="📧 Email",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        
        self.email_entry = ctk.CTkEntry(
            self.form_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Digite seu email",
            corner_radius=10
        )
        
        # Campo de nome completo (apenas para registro)
        self.fullname_label = ctk.CTkLabel(
            self.form_frame,
            text="✨ Nome completo",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        
        self.fullname_entry = ctk.CTkEntry(
            self.form_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Digite seu nome completo",
            corner_radius=10
        )
        
        # Campo de senha
        self.password_label = ctk.CTkLabel(
            self.form_frame,
            text="🔒 Senha",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            self.form_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Digite sua senha",
            show="*",
            corner_radius=10
        )
        self.password_entry.pack(fill="x", pady=(0, 15))
        
        # Campo de confirmação de senha (apenas para registro)
        self.confirm_password_label = ctk.CTkLabel(
            self.form_frame,
            text="🔒 Confirmar senha",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        
        self.confirm_password_entry = ctk.CTkEntry(
            self.form_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Confirme sua senha",
            show="*",
            corner_radius=10
        )
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.handle_submit())
        self.password_entry.bind("<Return>", lambda e: self.handle_submit())
    
    def create_action_buttons(self):
        """Cria botões de ação"""
        self.button_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=40, pady=20)
        
        # Botão principal (Login/Registrar)
        self.main_button = ctk.CTkButton(
            self.button_frame,
            text="🚀 Entrar",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.config.get_color('primary'),
            hover_color=self._darken_color(self.config.get_color('primary')),
            corner_radius=12,
            command=self.handle_submit
        )
        self.main_button.pack(fill="x", pady=(0, 10))
        
        # Botão de demo/convidado
        self.demo_button = ctk.CTkButton(
            self.button_frame,
            text="👁️ Modo Demo",
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=self.config.get_color('text_secondary'),
            hover_color=self.config.get_color('background'),
            border_width=2,
            border_color=self.config.get_color('text_secondary'),
            corner_radius=10,
            command=self.handle_demo_mode
        )
        self.demo_button.pack(fill="x")
    
    def create_toggle_link(self):
        """Cria link para alternar entre login e registro"""
        self.toggle_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.toggle_frame.pack(fill="x", padx=40, pady=10)
        
        self.toggle_label = ctk.CTkLabel(
            self.toggle_frame,
            text="Não tem uma conta? Registre-se aqui",
            font=ctk.CTkFont(size=12),
            text_color=self.config.get_color('secondary'),
            cursor="hand2"
        )
        self.toggle_label.pack()
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_mode())
    
    def create_status_message(self):
        """Cria área para mensagens de status"""
        self.status_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=40, pady=(10, 20))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=350
        )
        self.status_label.pack()
    
    def toggle_mode(self):
        """Alterna entre modo login e registro"""
        self.is_login_mode = not self.is_login_mode
        self.update_form_mode()
        self.clear_status()
    
    def update_form_mode(self):
        """Atualiza formulário baseado no modo atual"""
        if self.is_login_mode:
            # Modo Login
            self.main_button.configure(text="🚀 Entrar")
            self.toggle_label.configure(text="Não tem uma conta? Registre-se aqui")
            
            # Ocultar campos extras
            self.email_label.pack_forget()
            self.email_entry.pack_forget()
            self.fullname_label.pack_forget()
            self.fullname_entry.pack_forget()
            self.confirm_password_label.pack_forget()
            self.confirm_password_entry.pack_forget()
            
        else:
            # Modo Registro
            self.main_button.configure(text="📝 Registrar")
            self.toggle_label.configure(text="Já tem uma conta? Faça login aqui")
            
            # Mostrar campos extras
            self.email_label.pack(fill="x", pady=(0, 5), after=self.username_entry)
            self.email_entry.pack(fill="x", pady=(0, 15), after=self.email_label)
            self.fullname_label.pack(fill="x", pady=(0, 5), after=self.email_entry)
            self.fullname_entry.pack(fill="x", pady=(0, 15), after=self.fullname_label)
            self.confirm_password_label.pack(fill="x", pady=(0, 5), after=self.password_entry)
            self.confirm_password_entry.pack(fill="x", pady=(0, 15), after=self.confirm_password_label)
            
            # Bind Enter key para novos campos
            self.email_entry.bind("<Return>", lambda e: self.handle_submit())
            self.fullname_entry.bind("<Return>", lambda e: self.handle_submit())
            self.confirm_password_entry.bind("<Return>", lambda e: self.handle_submit())
    
    def handle_submit(self):
        """Processa submissão do formulário"""
        if self.is_loading:
            return
        
        if self.is_login_mode:
            self.handle_login()
        else:
            self.handle_register()
    
    def handle_login(self):
        """Processa login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validação básica
        if not username or not password:
            self.show_status("Por favor, preencha todos os campos", "error")
            return
        
        self.set_loading(True)
        self.show_status("Fazendo login...", "info")
        
        # Executar login em thread separada
        threading.Thread(
            target=self._perform_login,
            args=(username, password),
            daemon=True
        ).start()
    
    def _perform_login(self, username: str, password: str):
        """Executa login em thread separada"""
        try:
            user_data = self.db_manager.authenticate_user(username, password)
            
            # Atualizar UI na thread principal
            self.parent.after(0, self._login_callback, user_data)
            
        except Exception as e:
            self.logger.error(f"Erro no login: {e}")
            self.parent.after(0, self._login_callback, None)
    
    def _login_callback(self, user_data: Optional[dict]):
        """Callback do login executado na thread principal"""
        self.set_loading(False)
        
        if user_data:
            self.show_status("Login realizado com sucesso!", "success")
            self.main_window.login_success(user_data)
        else:
            self.show_status("Usuário ou senha incorretos", "error")
    
    def handle_register(self):
        """Processa registro"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validação
        validation_error = self._validate_registration(username, email, fullname, password, confirm_password)
        if validation_error:
            self.show_status(validation_error, "error")
            return
        
        self.set_loading(True)
        self.show_status("Criando conta...", "info")
        
        # Executar registro em thread separada
        threading.Thread(
            target=self._perform_registration,
            args=(username, password, email, fullname),
            daemon=True
        ).start()
    
    def _validate_registration(self, username: str, email: str, fullname: str, 
                              password: str, confirm_password: str) -> Optional[str]:
        """Valida dados de registro"""
        if not username or not password:
            return "Nome de usuário e senha são obrigatórios"
        
        if len(username) < 3:
            return "Nome de usuário deve ter pelo menos 3 caracteres"
        
        if len(password) < 6:
            return "Senha deve ter pelo menos 6 caracteres"
        
        if password != confirm_password:
            return "Senhas não coincidem"
        
        if email and not self._is_valid_email(email):
            return "Email inválido"
        
        return None
    
    def _is_valid_email(self, email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _perform_registration(self, username: str, password: str, email: str, fullname: str):
        """Executa registro em thread separada"""
        try:
            user_id = self.db_manager.create_user(username, password, email, fullname)
            
            if user_id:
                # Buscar dados do usuário criado
                user_data = self.db_manager.authenticate_user(username, password)
                self.parent.after(0, self._registration_callback, user_data)
            else:
                self.parent.after(0, self._registration_callback, None)
                
        except Exception as e:
            self.logger.error(f"Erro no registro: {e}")
            self.parent.after(0, self._registration_callback, None)
    
    def _registration_callback(self, user_data: Optional[dict]):
        """Callback do registro executado na thread principal"""
        self.set_loading(False)
        
        if user_data:
            self.show_status("Conta criada com sucesso!", "success")
            self.main_window.login_success(user_data)
        else:
            self.show_status("Erro ao criar conta. Nome de usuário pode já existir.", "error")
    
    def handle_demo_mode(self):
        """Ativa modo demo"""
        demo_user = {
            'id': 0,
            'username': 'demo',
            'full_name': 'Usuário Demo',
            'level': 1,
            'total_xp': 0,
            'current_streak': 0,
            'native_language': 'pt'
        }
        
        self.main_window.login_success(demo_user)
    
    def show_status(self, message: str, type: str = "info"):
        """Mostra mensagem de status"""
        colors = {
            'info': self.config.get_color('text_secondary'),
            'success': self.config.get_color('success'),
            'error': self.config.get_color('error'),
            'warning': self.config.get_color('warning')
        }
        
        self.status_label.configure(
            text=message,
            text_color=colors.get(type, colors['info'])
        )
    
    def clear_status(self):
        """Limpa mensagem de status"""
        self.status_label.configure(text="")
    
    def set_loading(self, loading: bool):
        """Define estado de carregamento"""
        self.is_loading = loading
        
        if loading:
            self.main_button.configure(state="disabled", text="⏳ Aguarde...")
            self.demo_button.configure(state="disabled")
        else:
            self.main_button.configure(state="normal")
            self.demo_button.configure(state="normal")
            self.update_form_mode()  # Restaura texto do botão
    
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
    
    def hide(self):
        """Oculta a tela"""
        self.main_frame.pack_forget()
    
    def clear_user(self):
        """Limpa dados do usuário (para logout)"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if hasattr(self, 'email_entry'):
            self.email_entry.delete(0, tk.END)
        if hasattr(self, 'fullname_entry'):
            self.fullname_entry.delete(0, tk.END)
        if hasattr(self, 'confirm_password_entry'):
            self.confirm_password_entry.delete(0, tk.END)
        self.clear_status()