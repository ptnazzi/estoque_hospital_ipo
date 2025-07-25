# 🚀 SISTEMA STOKE - Controle de Estoque de TI

https://estoquetihosp-f011be87ebfd.herokuapp.com/login

Sistema completo de controle de estoque com autenticação, logs e administração.

## 📋 Funcionalidades

### 🔐 **Sistema de Autenticação**
- Login como usuário ou administrador
- Senhas criptografadas
- Controle de sessões
- Logout seguro

### 📦 **Controle de Estoque**
- Cadastrar produtos
- Editar produtos
- Excluir produtos
- Pesquisar produtos
- Controle de status (Disponível, Em uso, Manutenção)

### 👨‍💼 **Área Administrativa**
- Gerenciar usuários
- Visualizar logs de acesso
- Histórico de exclusões
- Dashboard com estatísticas

### 📊 **Logs e Auditoria**
- Logs de login/logout
- Histórico de produtos excluídos
- Rastreamento de ações dos usuários

## 🛠️ Instalação e Configuração

### **Pré-requisitos**
- Python 3.7+
- PostgreSQL
- pgAdmin4

### **Passo 1: Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **Passo 2: Configurar Banco de Dados**
1. **Abra o pgAdmin4**
2. **Conecte-se ao banco `estoque`**
3. **Abra o Query Tool** (ícone de lupa)
4. **Copie e cole o conteúdo do arquivo `setup_database.sql`**
5. **Execute o script**

### **Passo 3: Executar o Sistema**
```bash
# Opção 1: Script de inicialização (recomendado)
python start.py

# Opção 2: Execução direta
python app.py
```

## 🎯 Como Usar

### **Acessar o Sistema**
- **URL:** `http://localhost:5050/login`

### **Credenciais Padrão**
- **Admin:** `admin` / `admin123`
- **Usuário:** `usuario` / `user123`

### **Funcionalidades por Tipo de Usuário**

#### **👤 Usuário Normal**
- Visualizar estoque
- Cadastrar produtos
- Editar produtos
- Excluir produtos
- Pesquisar produtos

#### **👨‍💼 Administrador**
- Todas as funcionalidades do usuário
- Gerenciar usuários (criar, excluir)
- Visualizar logs de acesso
- Histórico de exclusões
- Dashboard administrativo

## 📁 Estrutura do Projeto

```
stoke2/
├── app.py                    # Aplicação principal
├── start.py                  # Script de inicialização
├── requirements.txt          # Dependências Python
├── setup_database.sql        # Script de configuração do banco
├── README.md                # Documentação principal
├── GUIA_LOGS.md             # Guia detalhado dos logs
└── templates/               # Templates HTML
    ├── login.html           # Tela de login
    ├── index.html           # Tela principal do estoque
    ├── cadastrar.html       # Cadastro de produtos
    ├── editar.html          # Edição de produtos
    └── admin_dashboard.html # Dashboard administrativo
```

## 🔧 Configuração do Banco de Dados

### **Tabelas Criadas**
- `usuarios` - Usuários do sistema
- `produtos` - Produtos do estoque
- `logs_acesso` - Logs de login/logout
- `historico_exclusoes` - Histórico de exclusões

### **Usuário do Banco**
- **Usuário:** `estoque_ti`
- **Senha:** `admin`
- **Banco:** `estoque`

## 🎨 Interface

### **Design**
- Interface moderna e responsiva
- Cores: Azul (#0d6efd) para usuários, Vermelho (#dc3545) para admin
- Bootstrap 5.3.2
- Bootstrap Icons

### **Navegação**
- Menu superior fixo
- Abas organizadas no dashboard admin
- Modais para confirmações
- Alertas de sucesso/erro

## 🔒 Segurança

### **Implementada**
- Senhas criptografadas com Werkzeug
- Sessões seguras com Flask
- Controle de acesso por roles
- Logs de auditoria
- Proteção contra SQL injection

### **Dados Coletados**
- IP do usuário
- Data/hora das ações
- Nome do usuário
- Tipo de ação realizada

## 📊 Dashboard Administrativo

### **Cards de Estatísticas**
- Total de usuários
- Total de logs de acesso
- Total de itens excluídos
- Logins do dia atual

### **Abas Disponíveis**
1. **Usuários** - Gerenciar usuários do sistema
2. **Logs de Acesso** - Visualizar login/logout
3. **Histórico de Exclusões** - Ver produtos excluídos

## 🚨 Troubleshooting

### **Problemas Comuns**

#### **Erro de Conexão com Banco**
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no `app.py`
- Teste a conexão no pgAdmin4

#### **Tabelas Não Existem**
- Execute o script `setup_database.sql` no pgAdmin4
- Verifique se as permissões foram concedidas

#### **Login Não Funciona**
- Confirme se os usuários foram criados
- Verifique se a senha está correta
- Execute novamente o script SQL

#### **Logs Não Aparecem**
- Verifique se as tabelas de logs existem
- Confirme se está logado como admin
- Teste fazendo login/logout

## 🔄 Atualizações

### **Versão Atual**
- Sistema de autenticação completo
- Logs de acesso e exclusões
- Dashboard administrativo
- Interface responsiva

### **Próximas Funcionalidades**
- Exportação de relatórios
- Filtros avançados
- Backup automático
- Notificações por email

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs do console
2. Confirme a configuração do banco
3. Teste a conexão com scripts separados
4. Execute o script SQL no pgAdmin4

---

**🎉 Sistema STOKE configurado com sucesso!**

Agora você tem um sistema completo de controle de estoque com:
- ✅ Autenticação segura
- ✅ Controle de usuários
- ✅ Logs de auditoria
- ✅ Interface moderna
- ✅ Dashboard administrativo 
