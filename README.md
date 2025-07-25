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

## 🎯 Como Usar

### **Acessar o Sistema**
- **URL:**(https://estoquetihosp-f011be87ebfd.herokuapp.com/login)

### **Credenciais Padrão**
- **Usuário:** `usuario1` / `senha123`

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

```

### 🔧 Configuração do Banco de Dados

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


**🎉 Sistema STOKE configurado com sucesso!**

Agora você tem um sistema completo de controle de estoque com:
- ✅ Autenticação segura
- ✅ Controle de usuários
- ✅ Logs de auditoria
- ✅ Interface moderna
- ✅ Dashboard administrativo
##
