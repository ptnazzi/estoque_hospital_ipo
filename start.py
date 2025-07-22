
import os
import sys
import subprocess

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ é necessário!")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK!")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import flask
        import psycopg2
        import werkzeug
        print("✅ Dependências instaladas - OK!")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def check_database_connection():
    """Testa a conexão com o banco de dados"""
    try:
        import psycopg2
        from psycopg2 import Error
        
        DB_CONFIG = {
            'host': 'localhost',
            'port': '5432',
            'database': 'estoque',
            'user': 'estoque_ti',
            'password': 'admin'
        }
        
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        print("✅ Conexão com banco de dados - OK!")
        return True
    except Error as e:
        print(f"❌ Erro de conexão com banco: {e}")
        print("💡 Verifique se:")
        print("   - PostgreSQL está rodando")
        print("   - Banco 'estoque' existe")
        print("   - Usuário 'estoque_ti' existe")
        print("   - Execute o script 'setup_database.sql' no pgAdmin4")
        return False

def start_application():
    """Inicia a aplicação"""
    print("\n🚀 Iniciando Sistema STOKE...")
    print("=" * 40)
    
    if not check_python_version():
        return False
    
    if not check_dependencies():
        return False
    
    if not check_database_connection():
        return False
    
    print("\n🎉 Sistema pronto para iniciar!")
    print("📋 Informações:")
    print("   - URL: http://localhost:5050/login")
    print("   - Admin: admin / admin123")
    print("   - Usuário: usuario / user123")
    print("\n⏹️  Para parar o sistema, pressione Ctrl+C")
    print("=" * 40)
    
    try:
        # Importar e executar a aplicação
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5050)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar aplicação: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("🔧 Sistema STOKE - Verificação de Configuração")
    print("=" * 50)
    
    success = start_application()
    
    if not success:
        print("\n❌ Falha na inicialização do sistema.")
        print("💡 Verifique os erros acima e tente novamente.")
        sys.exit(1)

if __name__ == '__main__':
    main() 