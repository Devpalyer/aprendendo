from flask import Flask, render_template, request # Importa a biblioteca Flask para criar um aplicativo web simples
from flask_sqlalchemy import SQLAlchemy     # Importa a biblioteca Flask-SQLAlchemy para interagir com o banco de dados
from flask_bcrypt import Bcrypt  # Importa a biblioteca Flask-Bcrypt para criptografia de senhas
bcrypt = Bcrypt()  # Cria uma instância do Bcrypt para criptografia de senhas


app = Flask(__name__) # Importa a biblioteca Flask para criar um aplicativo web simples
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Configura o URI do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa o rastreamento de modificações do SQLAlchemy para economizar recursos
app.config['SQLALCHEMY_ECHO'] = True  # Ativa o log de consultas SQL para depuração
db = SQLAlchemy(app)  # Cria uma instância do SQLAlchemy com o aplicativo

class User(db.Model):
    __tablename__ = 'user'  # Define o nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Define a coluna 'id' como chave primária
    username = db.Column(db.String(80), unique=True, nullable=False)  # Define a coluna 'username' como string de até 80 caracteres, única e não nula
    email = db.Column(db.String(120), unique=True, nullable=False)  # Define a coluna 'email' como string de até 120 caracteres, única e não nula
    password = db.Column(db.String(60), nullable=False)  # Define a coluna 'password' como string de até 128 caracteres, não nula

    def __repr__(self): 
        return f'<User {self.username}>'  # Representação do objeto User para facilitar a visualização

with app.app_context():
    db.create_all()  # Cria todas as tabelas no banco de dados, se ainda não existirem

@app.route("/")
def home():
    # Define a rota raiz do aplicativo
    return render_template("index.html") #renderiza o template index.html

@app.route("/form")
def show_form():
    return render_template("form.html")

@app.route("/processar", methods=["POST"])  # Aceita apenas POST
def handle_form():
    nome = request.form.get("nome")  # Pega o valor do campo 'nome'
    return f"Olá, {nome}! Formulário recebido com sucesso."

@app.route("/add_user/<username>/<email>")
def add_user(username, email):
    # Rota para adicionar um usuário ao banco de dados
    new_user = User(username=username, email=email)
    db.session.add(new_user)  # Adiciona o novo usuário à sessão do banco de dados
    db.session.commit()  # Salva as alterações no banco de dados
    return f"Usuário {username} adicionado com sucesso!"   

@app.route("/users")
def list_users():
    # Rota para listar todos os usuários do banco de dados
    users = User.query.all()
    return render_template("users.html", users=users)  # Renderiza o template 'users.html' com a lista de usuários

@app.route("/register", methods=["GET", "POST"])   
def register():
    if request.method == "POST":
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=hashed_password
        )
        db.session.add(new_user)  # Adiciona o novo usuário à sessão do banco de dados
        db.session.commit()  # Salva as alterações no banco de dados
        return redirect("/login")
    return render_template("register.html")  # Renderiza o template 'register.html' para registro de usuários
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            return f"Bem-vindo, {user.username}!"
        else:
            return "Login bem-sucedido!."
    return render_template("login.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)#!/usr/bin/env python3
# Importa a biblioteca Flask para criar um aplicativo web simples  

