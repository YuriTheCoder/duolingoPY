# 🎯 LinguaMaster Pro

## Sistema de Aprendizado de Idiomas Gamificado

O **LinguaMaster Pro** é um sistema completo de aprendizado de idiomas desenvolvido em Python, com interface moderna usando CustomTkinter. Inspirado no Duolingo, oferece uma experiência gamificada e interativa para aprender idiomas de forma divertida e eficaz.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Características Principais

### 🌍 **Múltiplos Idiomas**
- **4 idiomas suportados**: Português, Inglês, Espanhol e Alemão
- Sistema de tradução com APIs gratuitas
- Cache offline para traduções frequentes
- Detecção automática de idioma

### 🎮 **Sistema Gamificado**
- **Sistema XP e Níveis**: Ganhe experiência e suba de nível
- **Streaks Diários**: Mantenha sua sequência de estudos
- **Conquistas**: 50+ badges para desbloquear
- **Ranking Global**: Compare seu progresso com outros usuários

### 🎯 **Jogos Educativos**
- **Quiz Interativo**: Perguntas de múltipla escolha adaptativas
- **Flashcards Inteligentes**: Sistema de repetição espaçada
- **Associação de Palavras**: Conecte palavras com traduções
- **Completar Frases**: Preencha lacunas em contexto
- **Batalhas de Vocabulário**: Duelos em tempo real

### 📚 **Lições Estruturadas**
- Conteúdo organizado por nível (Iniciante, Intermediário, Avançado)
- Mais de 1000 palavras por idioma
- Exemplos contextuais e pronúncia
- Progresso salvo automaticamente

### 🎨 **Interface Moderna**
- Design inspirado no Duolingo
- Tema colorido e animações fluidas
- Interface responsiva e intuitiva
- Feedback visual e sonoro

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.9 ou superior
- Windows 10+ (para executável)

### Instalação para Desenvolvimento

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/linguamaster-pro.git
cd linguamaster-pro
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o programa**
```bash
python main.py
```

### Gerar Executável (.exe)

1. **Execute o script de build**
```bash
python build_exe.py
```

2. **Distribua o executável**
- O arquivo `LinguaMaster_Pro.exe` será criado na pasta `dist/`
- Inclui script de instalação automática
- Totalmente standalone (não requer Python instalado)

## 📁 Estrutura do Projeto

```
LinguaMaster/
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências Python
├── build_exe.py              # Script para gerar .exe
├── config.json               # Configurações da aplicação
├── src/                      # Código fonte
│   ├── core/                 # Módulos principais
│   │   ├── database.py       # Gerenciador de banco de dados
│   │   └── translation_api.py # APIs de tradução
│   ├── ui/                   # Interface gráfica
│   │   ├── main_window.py    # Janela principal
│   │   └── screens/          # Telas da aplicação
│   │       ├── login_screen.py
│   │       ├── dashboard_screen.py
│   │       ├── translator_screen.py
│   │       ├── games_screen.py
│   │       ├── lesson_screen.py
│   │       └── profile_screen.py
│   └── utils/                # Utilitários
│       ├── config.py         # Sistema de configuração
│       └── logger.py         # Sistema de logging
├── data/                     # Dados da aplicação
│   └── vocabulary/           # Vocabulário por idioma
├── assets/                   # Recursos (ícones, sons)
└── logs/                     # Arquivos de log
```

## 🎯 Funcionalidades Implementadas

### ✅ **Core System**
- [x] Sistema de autenticação completo
- [x] Banco de dados SQLite robusto
- [x] Sistema de configuração flexível
- [x] Logging avançado
- [x] Arquitetura modular

### ✅ **Interface**
- [x] Tela de login/registro
- [x] Dashboard interativo
- [x] Tradutor com múltiplas APIs
- [x] Sistema de jogos (Quiz funcional)
- [x] Perfil do usuário
- [x] Lições estruturadas

### ✅ **Gamificação**
- [x] Sistema XP e níveis
- [x] Streaks diários
- [x] Sistema de conquistas
- [x] Progresso por idioma
- [x] Estatísticas detalhadas

### ✅ **Tradução**
- [x] APIs gratuitas (Google, MyMemory, LibreTranslate)
- [x] Cache offline
- [x] Histórico de traduções
- [x] Detecção automática de idioma

## 🚧 Funcionalidades em Desenvolvimento

### 🔄 **Jogos Avançados**
- [ ] Flashcards com algoritmo de repetição espaçada
- [ ] Jogo de associação visual
- [ ] Batalhas multiplayer
- [ ] Desafios diários automatizados

### 🔄 **Recursos Extras**
- [ ] Sistema de áudio/pronúncia
- [ ] Reconhecimento de voz
- [ ] Chat entre usuários
- [ ] Exportação de progresso
- [ ] Sincronização na nuvem

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**: Linguagem principal
- **CustomTkinter**: Interface gráfica moderna
- **SQLite**: Banco de dados local
- **Requests**: Requisições HTTP para APIs
- **Pillow**: Processamento de imagens
- **Pygame**: Sistema de áudio (futuro)
- **PyInstaller**: Geração de executável

## 🎨 APIs de Tradução

O sistema utiliza múltiplas APIs gratuitas para garantir disponibilidade:

1. **Google Translate (Free)**: API não oficial gratuita
2. **MyMemory**: API gratuita com limite diário
3. **LibreTranslate**: API open-source gratuita

## 📊 Estatísticas do Projeto

- **Linhas de código**: ~3000+
- **Arquivos Python**: 15+
- **Telas implementadas**: 6
- **Idiomas suportados**: 4
- **Palavras no vocabulário**: 1000+
- **Conquistas disponíveis**: 50+

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Kilo Code**
- GitHub: [@kilocode](https://github.com/kilocode)
- Email: contato@kilocode.dev

## 🙏 Agradecimentos

- Inspiração no design do Duolingo
- Comunidade Python pela excelente documentação
- Desenvolvedores do CustomTkinter
- APIs gratuitas de tradução

---

**Desenvolvido com ❤️ e muito ☕ por Kilo Code**

## 📸 Screenshots

*Screenshots serão adicionados em breve...*

## 🔄 Changelog

### v1.0.0 (2024-01-19)
- 🎉 Lançamento inicial
- ✅ Sistema completo de autenticação
- ✅ Dashboard interativo
- ✅ Tradutor funcional
- ✅ Quiz educativo
- ✅ Sistema de gamificação
- ✅ Interface moderna

---

*Para mais informações, consulte a [documentação completa](docs/) ou abra uma [issue](https://github.com/seu-usuario/linguamaster-pro/issues).*