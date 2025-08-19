#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinguaMaster Pro - Sistema de Aprendizado de Idiomas Gamificado
Desenvolvido com Python + Tkinter + CustomTkinter

Autor: Kilo Code
Versão: 1.0.0
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    import customtkinter as ctk
    from src.core.database import DatabaseManager
    from src.ui.main_window import MainWindow
    from src.utils.logger import Logger
    from src.utils.config import Config
except ImportError as e:
    print(f"Erro ao importar dependências: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

class LinguaMasterApp:
    """Classe principal da aplicação LinguaMaster Pro"""
    
    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.db_manager = None
        self.main_window = None
        
    def initialize_database(self):
        """Inicializa o banco de dados"""
        try:
            self.db_manager = DatabaseManager()
            self.db_manager.initialize_database()
            self.logger.info("Banco de dados inicializado com sucesso")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao inicializar banco de dados: {e}")
            return False
    
    def setup_theme(self):
        """Configura o tema da aplicação"""
        ctk.set_appearance_mode("light")  # "light" ou "dark"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
    def run(self):
        """Executa a aplicação principal"""
        try:
            self.logger.info("Iniciando LinguaMaster Pro...")
            
            # Configurar tema
            self.setup_theme()
            
            # Inicializar banco de dados
            if not self.initialize_database():
                return False
            
            # Criar janela principal
            self.main_window = MainWindow(self.db_manager, self.config, self.logger)
            
            # Iniciar loop principal
            self.main_window.run()
            
            self.logger.info("LinguaMaster Pro encerrado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro crítico na aplicação: {e}")
            return False
    
    def cleanup(self):
        """Limpa recursos antes de encerrar"""
        if self.db_manager:
            self.db_manager.close()
        self.logger.info("Recursos limpos com sucesso")

def main():
    """Função principal"""
    app = LinguaMasterApp()
    
    try:
        success = app.run()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nEncerrando aplicação...")
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()