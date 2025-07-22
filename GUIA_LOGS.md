# 🚀 Sistema de Logs e Histórico - STOKE

Este guia explica como configurar e usar as novas funcionalidades de logs e histórico para o administrador.

## 📋 Funcionalidades Implementadas

### 🔍 **Logs de Acesso dos Usuários**
- Registra quando cada usuário faz login/logout
- Armazena data/hora, IP e informações do usuário
- Permite ao admin monitorar a atividade dos usuários

### 🗑️ **Histórico de Itens Excluídos**
- Registra todos os produtos excluídos do estoque
- Armazena quem excluiu, quando e quais dados do produto
- Permite auditoria completa das exclusões

### 📊 **Dashboard Administrativo Melhorado**
- Interface com abas para organizar as informações
- Cards de estatísticas em tempo real
- Visualização clara e organizada dos dados

## 🔧 Configuração

### **Passo 1: Executar Script SQL**

1. **Abra o pgAdmin4**
2. **Conecte-se ao banco `estoque`**
3. **Abra o Query Tool** (ícone de lupa)
4. **Copie e cole o conteúdo do arquivo `setup_completo_com_logs.sql`**
5. **Execute o script**

### **Passo 2: Verificar Configuração**

Execute o script de verificação:

```bash
python setup_logs.py
```

### **Passo 3: Executar o Sistema**

```bash
python app.py
```

## 🎯 Como Usar

### **Acessar o Dashboard Administrativo:**

1. **Faça login como admin:**
   - Usuário: `admin`
   - Senha: `admin123`

2. **Acesse:** `http://localhost:5050/admin`

### **Navegar pelas Abas:**

#### **📊 Aba "Usuários"**
- Lista todos os usuários do sistema
- Permite cadastrar novos usuários
- Permite excluir usuários
- Mostra status e tipo de cada usuário

#### **📈 Aba "Logs de Acesso"**
- Mostra todos os logins e logouts
- Exibe data/hora, usuário, tipo de acesso e IP
- Ordenado por data mais recente
- Limite de 100 registros mais recentes

#### **🗑️ Aba "Histórico de Exclusões"**
- Lista todos os produtos excluídos
- Mostra dados completos do produto excluído
- Exibe quem excluiu e quando
- Ordenado por data mais recente
- Limite de 100 registros mais recentes

### **📊 Cards de Estatísticas:**

- **Usuários:** Total de usuários cadastrados
- **Logs de Acesso:** Total de registros de acesso
- **Itens Excluídos:** Total de produtos excluídos
- **Logins Hoje:** Quantidade de logins no dia atual

## 🔍 Funcionalidades Detalhadas

### **Logs de Acesso:**
- ✅ Registra automaticamente cada login
- ✅ Registra automaticamente cada logout
- ✅ Armazena IP do usuário
- ✅ Armazena data/hora exata
- ✅ Mostra nome completo do usuário

### **Histórico de Exclusões:**
- ✅ Registra dados completos do produto excluído
- ✅ Armazena quem fez a exclusão
- ✅ Registra data/hora da exclusão
- ✅ Mantém histórico mesmo após exclusão do usuário

### **Dashboard:**
- ✅ Interface responsiva
- ✅ Navegação por abas
- ✅ Estatísticas em tempo real
- ✅ Filtros automáticos por data

## 🛡️ Segurança

### **Proteções Implementadas:**
- ✅ Apenas admins podem acessar os logs
- ✅ Logs são mantidos mesmo após exclusão de usuário
- ✅ Dados sensíveis são protegidos
- ✅ Auditoria completa de ações

### **Dados Coletados:**
- ✅ Nome do usuário
- ✅ Data/hora da ação
- ✅ IP do usuário
- ✅ Tipo de ação (login/logout/exclusão)
- ✅ Dados do produto excluído

## 📁 Estrutura dos Arquivos

```
stoke2/
├── app.py                           # Aplicação principal (atualizada)
├── templates/
│   ├── admin_dashboard.html        # Novo dashboard administrativo
│   ├── login.html                  # Tela de login
│   └── index.html                  # Tela principal
├── setup_completo_com_logs.sql     # Script SQL completo
├── setup_logs.py                   # Script de configuração
└── GUIA_LOGS.md                    # Este arquivo
```

## 🔧 Troubleshooting

### **Erro: "Tabela não existe"**
- Execute o script SQL no pgAdmin4
- Verifique se as permissões foram concedidas

### **Erro: "Permissão negada"**
- Execute o script como superusuário (postgres)
- Verifique se o usuário `estoque_ti` tem permissões

### **Logs não aparecem**
- Verifique se as tabelas foram criadas
- Confirme se o usuário está logado como admin
- Teste fazendo login/logout para gerar logs

### **Dashboard não carrega**
- Verifique se todas as tabelas existem
- Confirme se há dados nas tabelas
- Teste a conexão com o banco

## 🎯 Próximos Passos

Para melhorar ainda mais o sistema, considere:

1. **Filtros Avançados:** Filtrar logs por data, usuário, tipo
2. **Exportação:** Exportar logs para CSV/PDF
3. **Alertas:** Notificações para atividades suspeitas
4. **Backup:** Backup automático dos logs
5. **Relatórios:** Relatórios mensais/anuais

## 📞 Suporte

Em caso de problemas:

1. **Verifique os logs do console**
2. **Confirme a configuração do banco**
3. **Teste a conexão com scripts separados**
4. **Execute o script SQL no pgAdmin4**

---

**🎉 Sistema de logs configurado com sucesso!**

Agora o administrador tem controle total sobre:
- ✅ Quem acessa o sistema
- ✅ Quando os usuários entram e saem
- ✅ Quais produtos foram excluídos
- ✅ Quem excluiu cada produto
- ✅ Histórico completo de atividades 