import psycopg2
from psycopg2 import Error
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'chave-secreta-estoque'

# Configuração do banco de dados para Heroku ou local
if 'DATABASE_URL' in os.environ:
    url = urlparse(os.environ['DATABASE_URL'])
    DB_CONFIG = {
        'host': url.hostname,
        'port': url.port,
        'database': url.path[1:],
        'user': url.username,
        'password': url.password
    }
else:
    DB_CONFIG = {
        'host': 'localhost',
        'port': '5432',
        'database': 'estoque',
        'user': 'estoque_ti',
        'password': 'admin'
    }

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)  
        return conn
    except Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página!', 'danger')
            return redirect(url_for('login'))
        if session.get('user_type') != 'admin':
            flash('Você não tem permissão para acessar esta página!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def verificar_usuario(username, password):
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, password, nome_completo, tipo, ativo FROM usuarios WHERE username = %s", (username,))
            result = cur.fetchone()
            if result and result[5]:  
                if result[2] == password or check_password_hash(result[2], password):
                    return {
                        'id': result[0],
                        'username': result[1],
                        'nome_completo': result[3],
                        'tipo': result[4]
                    }
        return None
    except Error as e:
        print(f"Erro ao verificar usuário: {e}")
        return None
    finally:
        conn.close()

def registrar_log_acesso(usuario_id, username, nome_completo, tipo_acesso, request,user_agent):
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            
            cur.execute("""
            INSERT INTO logs_acesso (usuario_id, username, nome_completo, tipo_acesso, data_hora, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (usuario_id, username, nome_completo, tipo_acesso, datetime.datetime.now(), ip_address, user_agent))
            conn.commit()
    except Error as e:
        print(f"Erro ao registrar log de acesso: {e}")
    finally:
        conn.close()

def registrar_exclusao_produto(produto_id, nome, quantidade, descricao, status, usuario_id, username, nome_completo):
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO historico_exclusoes (produto_id, nome_produto, quantidade, descricao, status, usuario_id, username, nome_completo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (produto_id, nome, quantidade, descricao, status, usuario_id, username, nome_completo))
            conn.commit()
    except Error as e:
        print(f"Erro ao registrar exclusão: {e}")
    finally:
        conn.close()

def buscar_logs_acesso():
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, nome_completo, tipo_acesso, data_hora, ip_address
                FROM logs_acesso 
                ORDER BY data_hora DESC 
                LIMIT 100
            """)
            logs = [
                {
                    'id': id_, 'username': username, 'nome_completo': nome,
                    'tipo_acesso': tipo, 'data_hora': data_hora, 'ip_address': ip
                }
                for id_, username, nome, tipo, data_hora, ip in cur.fetchall()
            ]
        return logs
    except Error as e:
        print(f"Erro ao buscar logs: {e}")
        return []
    finally:
        conn.close()

def buscar_historico_exclusoes():
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, produto_id, nome_produto, quantidade, descricao, status, 
                       username, nome_completo, data_exclusao
                FROM historico_exclusoes 
                ORDER BY data_exclusao DESC 
                LIMIT 100
            """)
            exclusoes = [
                {
                    'id': id_, 'produto_id': prod_id, 'nome_produto': nome,
                    'quantidade': qtd, 'descricao': desc, 'status': status,
                    'username': username, 'nome_completo': nome_comp, 'data_exclusao': data
                }
                for id_, prod_id, nome, qtd, desc, status, username, nome_comp, data in cur.fetchall()
            ]
        return exclusoes
    except Error as e:
        print(f"Erro ao buscar histórico: {e}")
        return []
    finally:
        conn.close()

def registrar_edicao_produto(produto_id, antigo, novo, usuario_id, username, nome_completo):
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO historico_edicoes (
                    produto_id, nome_antigo, quantidade_antiga, descricao_antiga, status_antigo,
                    nome_novo, quantidade_nova, descricao_nova, status_novo,
                    usuario_id, username, nome_completo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                produto_id,
                antigo['nome'], antigo['quantidade'], antigo['descricao'], antigo['status'],
                novo['nome'], novo['quantidade'], novo['descricao'], novo['status'],
                usuario_id, username, nome_completo
            ))
            conn.commit()
    except Error as e:
        print(f"Erro ao registrar edição: {e}")
    finally:
        conn.close()

from psycopg2 import Error  # ou ajuste conforme seu driver

def buscar_historico_edicoes():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT id, produto_id, nome_antigo, quantidade_antiga, descricao_antiga, status_antigo,
                       nome_novo, quantidade_nova, descricao_nova, status_novo,
                       username, nome_completo, data_edicao
                FROM historico_edicoes
                ORDER BY data_edicao DESC
                LIMIT 100
            ''')
            edicoes = [
                {
                    'id': id_, 'produto_id': prod_id,
                    'nome_antigo': nome_a, 'quantidade_antiga': qtd_a, 'descricao_antiga': desc_a, 'status_antigo': status_a,
                    'nome_novo': nome_n, 'quantidade_nova': qtd_n, 'descricao_nova': desc_n, 'status_novo': status_n,
                    'username': username, 'nome_completo': nome_comp, 'data_edicao': data
                }
                for id_, prod_id, nome_a, qtd_a, desc_a, status_a, nome_n, qtd_n, desc_n, status_n, username, nome_comp, data in cur.fetchall()
            ]
        return edicoes
    except Error as e:
        print(f"Erro ao buscar histórico de edições: {e}")
        return []
    finally:
        if conn:
            conn.close()



def buscar_produtos():
    conn = get_db_connection()
    if not conn:
        flash('Erro ao conectar com o banco de dados!', 'danger')
        return []
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, quantidade, descricao, status FROM produtos ORDER BY id")
            produtos = [
                {'id': id_, 'nome': nome, 'quantidade': qtd, 'descricao': desc, 'status': status}
                for id_, nome, qtd, desc, status in cur.fetchall()
            ]
        return produtos
    except Error as e:
        print(f"Erro ao buscar produtos: {e}")
        flash('Erro ao buscar produtos!', 'danger')
        return []
    finally:
        conn.close()

def buscar_usuarios():
    conn = get_db_connection()
    if not conn:
        flash('Erro ao conectar com o banco de dados!', 'danger')
        return []
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, nome_completo, tipo, ativo FROM usuarios ORDER BY id")
            usuarios = [
                {'id': id_, 'username': username, 'nome_completo': nome, 'tipo': tipo, 'ativo': ativo}
                for id_, username, nome, tipo, ativo in cur.fetchall()
            ]
        return usuarios
    except Error as e:
        print(f"Erro ao buscar usuários: {e}")
        flash('Erro ao buscar usuários!', 'danger')
        return []
    finally:
        conn.close()

@app.route('/')
@login_required
def index():
    produtos = buscar_produtos()
    return render_template('index.html', produtos=produtos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form.get('login_type', 'user')
        
        usuario = verificar_usuario(username, password)
        
        if usuario:
            if login_type == 'admin' and usuario['tipo'] != 'admin':
                flash('Você não tem permissão de administrador!', 'danger')
                return render_template('login.html')
            
            session['user_id'] = usuario['id']
            session['username'] = usuario['username']
            session['nome_completo'] = usuario['nome_completo']
            session['user_type'] = usuario['tipo']
            
            registrar_log_acesso(usuario['id'], usuario['username'], usuario['nome_completo'], 'login', request, request.headers.get('User-Agent'))
            
            if usuario['tipo'] == 'admin':
                flash(f'Bem-vindo, {usuario["nome_completo"]}!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash(f'Bem-vindo, {usuario["nome_completo"]}!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        registrar_log_acesso(session['user_id'], session['username'], session['nome_completo'], 'logout', request, request.headers.get('User-Agent'))
    session.clear()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    usuarios = buscar_usuarios()
    logs_acesso = buscar_logs_acesso()
    historico_exclusoes = buscar_historico_exclusoes()
    historico_edicoes = buscar_historico_edicoes()
    return render_template('admin_dashboard.html', usuarios=usuarios, logs_acesso=logs_acesso, historico_exclusoes=historico_exclusoes, historico_edicoes=historico_edicoes)

@app.route('/admin/cadastrar_usuario', methods=['POST'])
@admin_required
def cadastrar_usuario():
    username = request.form['username']
    password = request.form['password']
    nome_completo = request.form['nome_completo']
    tipo = request.form['tipo']
    
    # Criptografar senha
    password_hash = generate_password_hash(password)
    
    conn = get_db_connection()
    if not conn:
        flash('Erro ao conectar com o banco de dados!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usuarios (username, password, nome_completo, tipo, ativo) VALUES (%s, %s, %s, %s, %s)",
                (username, password_hash, nome_completo, tipo, True)
            )
            conn.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
    except Error as e:
        print(f"Erro ao cadastrar usuário: {e}")
        if "duplicate key" in str(e).lower():
            flash('Nome de usuário já existe!', 'danger')
        else:
            flash('Erro ao cadastrar usuário!', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/excluir_usuario/<int:usuario_id>')
@admin_required
def excluir_usuario(usuario_id):
    # Não permitir excluir o próprio usuário
    if usuario_id == session.get('user_id'):
        flash('Você não pode excluir seu próprio usuário!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db_connection()
    if not conn:
        flash('Erro ao conectar com o banco de dados!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            conn.commit()
        flash('Usuário excluído com sucesso!', 'success')
    except Error as e:
        print(f"Erro ao excluir usuário: {e}")
        flash('Erro ao excluir usuário!', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        descricao = request.form['descricao']
        status = request.form['status']
        
        if quantidade < 0:
            flash('Quantidade não pode ser negativa!', 'danger')
            return redirect(url_for('cadastrar'))
        
        conn = get_db_connection()
        if not conn:
            flash('Erro ao conectar com o banco de dados!', 'danger')
            return redirect(url_for('index'))
        
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO produtos (nome, quantidade, descricao, status) VALUES (%s, %s, %s, %s)",
                    (nome, quantidade, descricao, status)
                )
                conn.commit()
            flash('Produto cadastrado com sucesso!', 'success')
        except Error as e:
            print(f"Erro ao cadastrar produto: {e}")
            flash('Erro ao cadastrar produto!', 'danger')
        finally:
            conn.close()
        
        return redirect(url_for('index'))
    return render_template('cadastrar.html')

@app.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar(produto_id):
    conn = get_db_connection()
    if not conn:
        flash('Erro ao conectar com o banco de dados!', 'danger')
        return redirect(url_for('index'))
    
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            quantidade = int(request.form['quantidade'])
            descricao = request.form['descricao']
            status = request.form['status']
            
            if quantidade < 0:
                flash('Quantidade não pode ser negativa!', 'danger')
                return redirect(url_for('editar', produto_id=produto_id))
            
            # Buscar dados antigos antes de editar
            with conn.cursor() as cur:
                cur.execute("SELECT nome, quantidade, descricao, status FROM produtos WHERE id = %s", (produto_id,))
                antigo = cur.fetchone()
                if not antigo:
                    flash('Produto não encontrado!', 'danger')
                    return redirect(url_for('index'))
                antigo_dict = {
                    'nome': antigo[0],
                    'quantidade': antigo[1],
                    'descricao': antigo[2],
                    'status': antigo[3]
                }
            # Atualizar produto
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE produtos SET nome=%s, quantidade=%s, descricao=%s, status=%s WHERE id=%s",
                    (nome, quantidade, descricao, status, produto_id)
                )
                conn.commit()
            # Registrar edição
            novo_dict = {
                'nome': nome,
                'quantidade': quantidade,
                'descricao': descricao,
                'status': status
            }
            registrar_edicao_produto(
                produto_id, antigo_dict, novo_dict,
                session['user_id'], session['username'], session['nome_completo']
            )
            flash('Produto editado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            with conn.cursor() as cur:
                cur.execute("SELECT nome, quantidade, descricao, status FROM produtos WHERE id = %s", (produto_id,))
                result = cur.fetchone()
                if not result:
                    flash('Produto não encontrado!', 'danger')
                    return redirect(url_for('index'))
                produto = {
                    'id': produto_id,
                    'nome': result[0],
                    'quantidade': result[1],
                    'descricao': result[2],
                    'status': result[3]
                }
            return render_template('editar.html', produto=produto)
    except Error as e:
        print(f"Erro ao editar produto: {e}")
        flash('Erro ao editar produto!', 'danger')
        return redirect(url_for('index'))
    finally:
        conn.close()

@app.route('/excluir/<int:produto_id>')
@login_required
def excluir(produto_id):
    conn = get_db_connection()
    if not conn:
        flash('Erro ao conectar com o banco de dados!', 'danger')
        return redirect(url_for('index'))
    
    try:
        with conn.cursor() as cur:
            # Buscar dados do produto antes de excluir
            cur.execute("SELECT nome, quantidade, descricao, status FROM produtos WHERE id = %s", (produto_id,))
            produto = cur.fetchone()
            
            if produto:
                nome, quantidade, descricao, status = produto
                
                # Excluir o produto
                cur.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
                conn.commit()
                
                # Registrar a exclusão no histórico
                registrar_exclusao_produto(
                    produto_id, nome, quantidade, descricao, status,
                    session['user_id'], session['username'], session['nome_completo']
                )
                
                flash('Produto excluído com sucesso!', 'success')
            else:
                flash('Produto não encontrado!', 'danger')
    except Error as e:
        print(f"Erro ao excluir produto: {e}")
        flash('Erro ao excluir produto!', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)