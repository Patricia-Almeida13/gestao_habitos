import pandas as pd # usado para manipulação de DataFrame
from datetime import datetime # permite trabalhar com datas e horas
import matplotlib.pyplot as plt #cração de gráficos e visualizar os dados
import numpy as np #efectua calculos e operações com arrays

# Dicionário para armazenar os dados dos usuários
usuarios = {}

# Função para criar um novo usuário
def criar_usuario():
    global usuarios
    print("Criar Novo Utilizador")
    
    nome_usuario = input("Digite o nome do usuário: ").strip()
    
    # Verifica se o usuário já existe
    if nome_usuario in usuarios:
        print(f"Usuário '{nome_usuario}' já existe!")
        return
    
    # Solicita a criação do DataFrame para o novo usuário
    print(f"Usuário '{nome_usuario}' criado com sucesso!")
    usuarios[nome_usuario] = pd.DataFrame(columns=["Hábito", "Categoria", "Frequência", "Data de Inicio", "Status", "Duração (minutos)"])
    
    print(f"Agora pode começar a adicionar hábitos para o usuário '{nome_usuario}'.")

# Função para selecionar um usuário
def selecionar_usuario():
    global usuarios
    if not usuarios:
        print("Nenhum usuário cadastrado!")
        return None
    
    print("Usuários disponíveis: ", list(usuarios.keys()))
    nome_usuario = input("Digite o nome do usuário que deseja selecionar: ").strip()
    
    if nome_usuario not in usuarios:
        print("Usuário não encontrado!")
        return None
    
    print(f"Usuário '{nome_usuario}' selecionado com sucesso!")
    return nome_usuario

# Modificar funções que usam o DataFrame de hábitos para trabalhar com o usuário selecionado

def criar_dataframe():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    data = {
        "Hábito": [],
        "Categoria": [],
        "Frequência": [],
        "Data de Inicio": [],
        "Status": [],
        "Duração (minutos)": []
    }
    
    while True:
        habito = input("Nome do Hábito: ")
        categoria = input("Categoria (Saúde, Produtividade, Lazer, etc.): ")
        frequencia = input("Frequência (Diária, Semanal, Mensal): ")
        data_registro = input("Data de Inicio (DD/MM/AAAA): ")
        status = input("Status (Concluído, Pendente, Em progresso): ")
        duracao = input("Duração apróximada em minutos: ")
        
        try:
            data["Hábito"].append(habito)
            data["Categoria"].append(categoria)
            data["Frequência"].append(frequencia)
            data["Data de Inicio"].append(pd.to_datetime(data_registro, format="%d/%m/%Y"))
            data["Status"].append(status)
            data["Duração (minutos)"].append(int(duracao))
        except ValueError:
            print("Erro! Certifique-se de seguir os formatos indicados.")
            continue
        
        mais = input("Deseja adicionar mais algum hábito? (s/n): ").strip().lower()
        if mais != 's':
            break
    
    # Atualizar o DataFrame do usuário
    usuarios[nome_usuario] = pd.DataFrame(data)
    print(f"Data Frame criado com sucesso para o usuário '{nome_usuario}'!")
    print(usuarios[nome_usuario])


def consultar_dataframe():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    if df.empty:
        print("Data Frame vazio!")
    else:
        print(df)




