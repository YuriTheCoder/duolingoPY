#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela do Tradutor do LinguaMaster Pro
Interface principal de tradução com recursos avançados
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, List, Optional
import threading
import time

class TranslatorScreen:
    """Tela principal do tradutor"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db_manager = main_window.get_db_manager()
        self.translation_manager = main_window.get_translation_manager()
        self.logger = main_window.get_logger()
        self.config = main_window.get_config()
        
        # Estado da tela
        self.current_user = None
        self.translation_history = []
        self.is_translating = False
        
        # Criar interface
        self.create_widgets()
    
    def create_widgets(self):
        """Cria widgets da tela do tradutor"""
        # Container principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        
        # Cabeçalho
        self.create_header()
        
        # Seletor de idiomas
        self.create_language_selector()
        
        # Área de tradução principal
        self.create_translation_area()
        
        # Botões de ação
        self.create_action_buttons()
        
        # Recursos extras
        self.create_extra_features()
        
        # Histórico de traduções
        self.create_history_section()
    
    def create_header(self):
        """Cria cabeçalho da tela"""
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="🌍 Tradutor Inteligente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.config.get_color('success')
        )
        title_label.pack(anchor="w")
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Traduza textos entre 4 idiomas com precisão e aprenda no processo!",
            font=ctk.CTkFont(size=14),
            text_color=self.config.get_color('text_secondary')
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
    
    def create_language_selector(self):
        """Cria seletor de idiomas"""
        selector_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        selector_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(selector_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=25, pady=20)
        
        # Container dos seletores
        selectors_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        selectors_frame.pack(fill="x")
        selectors_frame.grid_columnconfigure((0, 2), weight=1)
        
        # Idioma de origem
        source_frame = ctk.CTkFrame(selectors_frame, fg_color="transparent")
        source_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        source_label = ctk.CTkLabel(
            source_frame,
            text="De:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        source_label.pack(anchor="w")
        
        # Opções de idiomas
        languages = self.config.get_supported_languages()
        language_options = []
        for lang_code in languages:
            flag = self.config.get_language_flag(lang_code)
            name = self.config.get_language_name(lang_code)
            language_options.append(f"{flag} {name}")
        
        self.source_combo = ctk.CTkComboBox(
            source_frame,
            values=language_options,
            font=ctk.CTkFont(size=12),
            height=35,
            command=self.on_source_language_change
        )
        self.source_combo.pack(fill="x", pady=(5, 0))
        self.source_combo.set(f"{self.config.get_language_flag('pt')} {self.config.get_language_name('pt')}")
        
        # Botão de troca
        swap_button = ctk.CTkButton(
            selectors_frame,
            text="⇄",
            width=50,
            height=35,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.config.get_color('accent'),
            hover_color=self._darken_color(self.config.get_color('accent')),
            command=self.swap_languages
        )
        swap_button.grid(row=0, column=1, pady=(25, 0))
        
        # Idioma de destino
        target_frame = ctk.CTkFrame(selectors_frame, fg_color="transparent")
        target_frame.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        
        target_label = ctk.CTkLabel(
            target_frame,
            text="Para:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        target_label.pack(anchor="w")
        
        self.target_combo = ctk.CTkComboBox(
            target_frame,
            values=language_options,
            font=ctk.CTkFont(size=12),
            height=35,
            command=self.on_target_language_change
        )
        self.target_combo.pack(fill="x", pady=(5, 0))
        self.target_combo.set(f"{self.config.get_language_flag('en')} {self.config.get_language_name('en')}")
    
    def create_translation_area(self):
        """Cria área principal de tradução"""
        translation_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        translation_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(translation_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Container das áreas de texto
        text_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        text_container.pack(fill="x")
        text_container.grid_columnconfigure((0, 1), weight=1)
        
        # Área de texto de origem
        source_frame = ctk.CTkFrame(text_container)
        source_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        source_label = ctk.CTkLabel(
            source_frame,
            text="📝 Texto para traduzir:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        source_label.pack(fill="x", padx=15, pady=(15, 5))
        
        self.source_text = ctk.CTkTextbox(
            source_frame,
            height=150,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.source_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self.source_text.bind("<KeyRelease>", self.on_text_change)
        
        # Contador de caracteres
        self.char_count_label = ctk.CTkLabel(
            source_frame,
            text="0 caracteres",
            font=ctk.CTkFont(size=10),
            text_color=self.config.get_color('text_secondary')
        )
        self.char_count_label.pack(anchor="e", padx=15, pady=(0, 10))
        
        # Área de texto traduzido
        target_frame = ctk.CTkFrame(text_container)
        target_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        target_label = ctk.CTkLabel(
            target_frame,
            text="✨ Tradução:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        target_label.pack(fill="x", padx=15, pady=(15, 5))
        
        self.target_text = ctk.CTkTextbox(
            target_frame,
            height=150,
            font=ctk.CTkFont(size=14),
            wrap="word",
            state="disabled"
        )
        self.target_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Status da tradução
        self.translation_status = ctk.CTkLabel(
            target_frame,
            text="Digite algo para traduzir...",
            font=ctk.CTkFont(size=10),
            text_color=self.config.get_color('text_secondary')
        )
        self.translation_status.pack(anchor="w", padx=15, pady=(0, 10))
    
    def create_action_buttons(self):
        """Cria botões de ação"""
        buttons_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=25, pady=15)
        content_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Botão traduzir
        self.translate_button = ctk.CTkButton(
            content_frame,
            text="🚀 Traduzir",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=self.config.get_color('success'),
            hover_color=self._darken_color(self.config.get_color('success')),
            command=self.translate_text
        )
        self.translate_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        # Botão limpar
        clear_button = ctk.CTkButton(
            content_frame,
            text="🗑️ Limpar",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color="transparent",
            text_color=self.config.get_color('text_secondary'),
            hover_color=self.config.get_color('background'),
            border_width=2,
            border_color=self.config.get_color('text_secondary'),
            command=self.clear_text
        )
        clear_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Botão copiar
        copy_button = ctk.CTkButton(
            content_frame,
            text="📋 Copiar",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color=self.config.get_color('secondary'),
            hover_color=self._darken_color(self.config.get_color('secondary')),
            command=self.copy_translation
        )
        copy_button.grid(row=0, column=2, padx=5, sticky="ew")
        
        # Botão favoritar
        self.favorite_button = ctk.CTkButton(
            content_frame,
            text="⭐ Favoritar",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color=self.config.get_color('warning'),
            hover_color=self._darken_color(self.config.get_color('warning')),
            command=self.add_to_favorites
        )
        self.favorite_button.grid(row=0, column=3, padx=5, sticky="ew")
    
    def create_extra_features(self):
        """Cria recursos extras"""
        features_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        features_frame.pack(fill="x", padx=20, pady=10)
        
        content_frame = ctk.CTkFrame(features_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=25, pady=15)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text="🔧 Recursos Extras",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Container dos recursos
        extras_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        extras_container.pack(fill="x")
        extras_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Detecção automática de idioma
        auto_detect_frame = ctk.CTkFrame(extras_container)
        auto_detect_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
        
        self.auto_detect_var = ctk.BooleanVar(value=True)
        auto_detect_check = ctk.CTkCheckBox(
            auto_detect_frame,
            text="🔍 Detectar idioma",
            font=ctk.CTkFont(size=11),
            variable=self.auto_detect_var
        )
        auto_detect_check.pack(padx=15, pady=10)
        
        # Tradução instantânea
        instant_frame = ctk.CTkFrame(extras_container)
        instant_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.instant_var = ctk.BooleanVar(value=False)
        instant_check = ctk.CTkCheckBox(
            instant_frame,
            text="⚡ Tradução instantânea",
            font=ctk.CTkFont(size=11),
            variable=self.instant_var,
            command=self.toggle_instant_translation
        )
        instant_check.pack(padx=15, pady=10)
        
        # Salvar no histórico
        history_frame = ctk.CTkFrame(extras_container)
        history_frame.grid(row=0, column=2, padx=(10, 0), pady=5, sticky="ew")
        
        self.save_history_var = ctk.BooleanVar(value=True)
        history_check = ctk.CTkCheckBox(
            history_frame,
            text="💾 Salvar histórico",
            font=ctk.CTkFont(size=11),
            variable=self.save_history_var
        )
        history_check.pack(padx=15, pady=10)
    
    def create_history_section(self):
        """Cria seção do histórico"""
        history_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        history_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        content_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Cabeçalho do histórico
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📚 Histórico de Traduções",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left")
        
        clear_history_button = ctk.CTkButton(
            header_frame,
            text="🗑️ Limpar Histórico",
            font=ctk.CTkFont(size=11),
            height=30,
            fg_color="transparent",
            text_color=self.config.get_color('error'),
            hover_color=self.config.get_color('background'),
            border_width=1,
            border_color=self.config.get_color('error'),
            command=self.clear_history
        )
        clear_history_button.pack(side="right")
        
        # Lista do histórico
        self.history_container = ctk.CTkFrame(content_frame)
        self.history_container.pack(fill="x")
        
        # Carregar histórico inicial
        self.load_history()
    
    def on_source_language_change(self, value):
        """Callback para mudança do idioma de origem"""
        if self.auto_detect_var.get():
            self.detect_language()
    
    def on_target_language_change(self, value):
        """Callback para mudança do idioma de destino"""
        pass
    
    def on_text_change(self, event=None):
        """Callback para mudança no texto"""
        text = self.source_text.get("1.0", tk.END).strip()
        char_count = len(text)
        self.char_count_label.configure(text=f"{char_count} caracteres")
        
        if self.instant_var.get() and text and char_count > 2:
            # Tradução instantânea com delay
            if hasattr(self, '_instant_timer'):
                self.parent.after_cancel(self._instant_timer)
            self._instant_timer = self.parent.after(1000, self.translate_text)
    
    def swap_languages(self):
        """Troca idiomas de origem e destino"""
        source_value = self.source_combo.get()
        target_value = self.target_combo.get()
        
        self.source_combo.set(target_value)
        self.target_combo.set(source_value)
        
        # Trocar textos também
        source_text = self.source_text.get("1.0", tk.END).strip()
        target_text = self.target_text.get("1.0", tk.END).strip()
        
        if target_text:
            self.source_text.delete("1.0", tk.END)
            self.source_text.insert("1.0", target_text)
            
            self.target_text.configure(state="normal")
            self.target_text.delete("1.0", tk.END)
            self.target_text.insert("1.0", source_text)
            self.target_text.configure(state="disabled")
    
    def translate_text(self):
        """Traduz o texto"""
        if self.is_translating:
            return
        
        source_text = self.source_text.get("1.0", tk.END).strip()
        if not source_text:
            self.show_translation_status("Digite algo para traduzir...", "info")
            return
        
        # Obter códigos dos idiomas
        source_lang = self.get_language_code_from_combo(self.source_combo.get())
        target_lang = self.get_language_code_from_combo(self.target_combo.get())
        
        if source_lang == target_lang:
            self.show_translation_status("Selecione idiomas diferentes!", "error")
            return
        
        self.is_translating = True
        self.translate_button.configure(text="⏳ Traduzindo...", state="disabled")
        self.show_translation_status("Traduzindo...", "info")
        
        # Executar tradução em thread separada
        threading.Thread(
            target=self._perform_translation,
            args=(source_text, source_lang, target_lang),
            daemon=True
        ).start()
    
    def _perform_translation(self, text: str, source_lang: str, target_lang: str):
        """Executa tradução em thread separada"""
        try:
            result = self.translation_manager.translate(text, source_lang, target_lang)
            
            # Atualizar UI na thread principal
            self.parent.after(0, self._translation_callback, result, text, source_lang, target_lang)
            
        except Exception as e:
            self.logger.error(f"Erro na tradução: {e}")
            error_result = {
                'translation': None,
                'success': False,
                'error': str(e)
            }
            self.parent.after(0, self._translation_callback, error_result, text, source_lang, target_lang)
    
    def _translation_callback(self, result: Dict, original_text: str, source_lang: str, target_lang: str):
        """Callback da tradução executado na thread principal"""
        self.is_translating = False
        self.translate_button.configure(text="🚀 Traduzir", state="normal")
        
        if result['success'] and result['translation']:
            # Mostrar tradução
            self.target_text.configure(state="normal")
            self.target_text.delete("1.0", tk.END)
            self.target_text.insert("1.0", result['translation'])
            self.target_text.configure(state="disabled")
            
            # Status
            api_used = result.get('api_used', 'desconhecida')
            cached = " (cache)" if result.get('cached', False) else ""
            self.show_translation_status(f"Traduzido com {api_used}{cached}", "success")
            
            # Salvar no histórico
            if self.save_history_var.get():
                self.add_to_history(original_text, result['translation'], source_lang, target_lang)
            
            # Log da tradução
            if self.current_user:
                self.logger.log_translation_request(source_lang, target_lang, len(original_text))
        
        else:
            error_msg = result.get('error', 'Erro desconhecido na tradução')
            self.show_translation_status(f"Erro: {error_msg}", "error")
    
    def get_language_code_from_combo(self, combo_value: str) -> str:
        """Extrai código do idioma do valor do combo"""
        # Mapear valores do combo para códigos
        language_map = {}
        for lang_code in self.config.get_supported_languages():
            flag = self.config.get_language_flag(lang_code)
            name = self.config.get_language_name(lang_code)
            language_map[f"{flag} {name}"] = lang_code
        
        return language_map.get(combo_value, 'pt')
    
    def detect_language(self):
        """Detecta idioma do texto"""
        text = self.source_text.get("1.0", tk.END).strip()
        if not text or len(text) < 10:
            return
        
        detected_lang = self.translation_manager.detect_language(text)
        if detected_lang:
            # Atualizar combo de origem
            flag = self.config.get_language_flag(detected_lang)
            name = self.config.get_language_name(detected_lang)
            self.source_combo.set(f"{flag} {name}")
    
    def clear_text(self):
        """Limpa textos"""
        self.source_text.delete("1.0", tk.END)
        self.target_text.configure(state="normal")
        self.target_text.delete("1.0", tk.END)
        self.target_text.configure(state="disabled")
        self.char_count_label.configure(text="0 caracteres")
        self.show_translation_status("Digite algo para traduzir...", "info")
    
    def copy_translation(self):
        """Copia tradução para clipboard"""
        translation = self.target_text.get("1.0", tk.END).strip()
        if translation:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(translation)
            self.show_translation_status("Tradução copiada!", "success")
        else:
            self.show_translation_status("Nada para copiar", "error")
    
    def add_to_favorites(self):
        """Adiciona tradução aos favoritos"""
        source_text = self.source_text.get("1.0", tk.END).strip()
        translation = self.target_text.get("1.0", tk.END).strip()
        
        if source_text and translation:
            # Implementar lógica de favoritos
            self.show_translation_status("Adicionado aos favoritos!", "success")
        else:
            self.show_translation_status("Complete a tradução primeiro", "error")
    
    def toggle_instant_translation(self):
        """Alterna tradução instantânea"""
        if self.instant_var.get():
            self.show_translation_status("Tradução instantânea ativada", "info")
        else:
            self.show_translation_status("Tradução instantânea desativada", "info")
    
    def add_to_history(self, source_text: str, translation: str, source_lang: str, target_lang: str):
        """Adiciona tradução ao histórico"""
        history_item = {
            'source_text': source_text,
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'timestamp': time.time()
        }
        
        self.translation_history.insert(0, history_item)
        
        # Manter apenas últimas 10 traduções
        if len(self.translation_history) > 10:
            self.translation_history = self.translation_history[:10]
        
        self.update_history_display()
    
    def load_history(self):
        """Carrega histórico de traduções"""
        # Por enquanto, histórico em memória
        # Futuramente, carregar do banco de dados
        self.update_history_display()
    
    def update_history_display(self):
        """Atualiza exibição do histórico"""
        # Limpar histórico atual
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        if not self.translation_history:
            no_history_label = ctk.CTkLabel(
                self.history_container,
                text="Nenhuma tradução no histórico ainda",
                font=ctk.CTkFont(size=12),
                text_color=self.config.get_color('text_secondary')
            )
            no_history_label.pack(pady=20)
            return
        
        # Criar itens do histórico
        for i, item in enumerate(self.translation_history):
            self.create_history_item(self.history_container, item, i == 0)
    
    def create_history_item(self, parent, item: Dict, is_first: bool):
        """Cria item do histórico"""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", padx=10, pady=(10 if is_first else 5, 5))
        
        # Idiomas
        source_flag = self.config.get_language_flag(item['source_lang'])
        target_flag = self.config.get_language_flag(item['target_lang'])
        
        lang_label = ctk.CTkLabel(
            item_frame,
            text=f"{source_flag} → {target_flag}",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lang_label.pack(anchor="w")
        
        # Textos
        text_preview = item['source_text'][:50] + "..." if len(item['source_text']) > 50 else item['source_text']
        translation_preview = item['translation'][:50] + "..." if len(item['translation']) > 50 else item['translation']
        
        source_label = ctk.CTkLabel(
            item_frame,
            text=f"📝 {text_preview}",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        source_label.pack(fill="x", pady=(2, 0))
        
        translation_label = ctk.CTkLabel(
            item_frame,
            text=f"✨ {translation_preview}",
            font=ctk.CTkFont(size=11),
            text_color=self.config.get_color('text_secondary'),
            anchor="w"
        )
        translation_label.pack(fill="x", pady=(2, 0))
        
        # Botão para usar novamente
        use_button = ctk.CTkButton(
            item_frame,
            text="🔄 Usar novamente",
            font=ctk.CTkFont(size=10),
            height=25,
            fg_color="transparent",
            text_color=self.config.get_color('primary'),
            hover_color=self.config.get_color('background'),
            command=lambda: self.use_from_history(item)
        )
        use_button.pack(anchor="e", pady=(5, 0))
    
    def use_from_history(self, item: Dict):
        """Usa tradução do histórico"""
        # Definir idiomas
        source_flag = self.config.get_language_flag(item['source_lang'])
        source_name = self.config.get_language_name(item['source_lang'])
        target_flag = self.config.get_language_flag(item['target_lang'])
        target_name = self.config.get_language_name(item['target_lang'])
        
        self.source_combo.set(f"{source_flag} {source_name}")
        self.target_combo.set(f"{target_flag} {target_name}")
        
        # Definir textos
        self.source_text.delete("1.0", tk.END)
        self.source_text.insert("1.0", item['source_text'])
        
        self.target_text.configure(state="normal")
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", item['translation'])
        self.target_text.configure(state="disabled")
        
        self.show_translation_status("Tradução carregada do histórico", "success")
    
    def clear_history(self):
        """Limpa histórico"""
        self.translation_history.clear()
        self.update_history_display()
        
self.show_translation_status("Tradução carregada do histórico", "success")
    
    def clear_history(self):
        """Limpa histórico"""
        self.translation_history.clear()
        self.update_history_display()
        self.show_translation_status("Histórico limpo", "info")
    
    def show_translation_status(self, message: str, type: str = "info"):
        """Mostra status da tradução"""
        colors = {
            'info': self.config.get_color('text_secondary'),
            'success': self.config.get_color('success'),
            'error': self.config.get_color('error'),
            'warning': self.config.get_color('warning')
        }
        
        self.translation_status.configure(
            text=message,
            text_color=colors.get(type, colors['info'])
        )
    
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
        self.clear_text()
        self.clear_history()