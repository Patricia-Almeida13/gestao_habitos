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

# Função para criar um novo hábito
def adicionar_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    habito = input("Nome do Hábito: ")
    categoria = input("Categoria: ")
    frequencia = input("Frequência: ")
    data_registro = input("Data de Inicio (DD/MM/AAAA): ")
    status = input("Status: ")
    duracao = input("Duração em minutos: ")
    
    try:
        nova_linha = {
            "Hábito": habito,
            "Categoria": categoria,
            "Frequência": frequencia,
            "Data de Inicio": pd.to_datetime(data_registro, format="%d/%m/%Y"),
            "Status": status,
            "Duração (minutos)": int(duracao)
        }
        df.loc[len(df)] = nova_linha
        usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
        print("Hábito adicionado com sucesso!")
    except ValueError:
        print("Erro ao adicionar! Verifique os dados.")

# Função para filtrar hábitos por categoria
def filtrar_por_categoria():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    categoria = input("Digite a categoria que deseja filtrar: ")
    filtro = df[df["Categoria"] == categoria]
    print(f"Hábitos na categoria '{categoria}':")
    print(filtro if not filtro.empty else "Nenhum hábito encontrado.")

# Função para atualizar o status de um hábito
def atualizar_status():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print(df)
    try:
        indice = int(input("Indique o índice do hábito que deseja atualizar: "))
        novo_status = input("Novo status (Concluído, Pendente, Em progresso): ")
        
        if indice not in df.index:
            print("Erro! Índice inválido.")
            return
        
        df.at[indice, "Status"] = novo_status
        usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
        print("Status atualizado com sucesso!")
    except ValueError:
        print("Erro! Índice inválido.")

# Função para mostrar estatísticas dos hábitos
def estatisticas_habitos():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print("Estatísticas gerais dos hábitos:")
    print(df[["Duração (minutos)"]].describe())
    
def exportar_para_excel():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    if df.empty:
        print("Não há dados para exportar!")
        return
    
    # Definir o nome do arquivo Excel
    nome_arquivo = f"{nome_usuario}_dados_habitos.xlsx"
    
    # Exportar o DataFrame para Excel
    try:
        df.to_excel(nome_arquivo, index=False, engine="openpyxl")
        print(f"Arquivo Excel gerado com sucesso! O arquivo está em: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao gerar o arquivo Excel: {e}")


# Função para remover um hábito
def remover_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return

    global usuarios
    df = usuarios[nome_usuario]
    
    print("Lista de hábitos disponíveis: ")
    print(df["Hábito"].to_string(index=False))

    habito = input("Digite o nome do hábito que deseja remover: ").strip()

    if habito not in df["Hábito"].values:
        print(f"Erro! O hábito '{habito}' não consta no Data Frame!")
        return

    df.drop(df[df["Hábito"] == habito].index, inplace=True)
    usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
    print(f"Hábito '{habito}' removido com sucesso!")
    print()

# Função para atualizar um hábito
def atualizar_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print("Lista de hábitos disponíveis: ")
    print(df["Hábito"].to_string(index=False))

    habito = input("Digite o nome do hábito que deseja atualizar: ").strip()

    if habito not in df["Hábito"].values:
        print(f"Erro! O hábito '{habito}' não consta no Data Frame!")
        return

    index_habito = df[df["Hábito"] == habito].index[0]

    print("Colunas disponíveis para edição:", ", ".join(df.columns))
    coluna = input("Digite o nome da coluna que deseja atualizar: ").strip()

    if coluna not in df.columns:
        print(f"Erro! A coluna '{coluna}' não existe!")
        return

    novo_valor = input(f"Digite o novo valor para '{coluna}' no hábito '{habito}': ").strip()

    try:
        tipo_dado = df[coluna].dtype.type
        df.at[index_habito, coluna] = tipo_dado(novo_valor)
        usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
        print(f"Hábito '{habito}' atualizado com sucesso na coluna '{coluna}'!")
    except ValueError:
        print("Erro! O valor inserido não corresponde ao tipo de dado da coluna.")

# Função para renomear um hábito
def renomear_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return

    global usuarios
    df = usuarios[nome_usuario]

    print("Lista de hábitos disponíveis:")
    print(df["Hábito"].to_string(index=False))

    habito_atual = input("Digite o nome do hábito que deseja renomear: ").strip()

    if habito_atual not in df["Hábito"].values:
        print(f"Erro! O hábito '{habito_atual}' não consta no Data Frame!")
        return

    novo_nome = input("Digite o novo nome para o hábito: ").strip()

    # Verificar se o novo nome já existe
    if novo_nome in df["Hábito"].values:
        print(f"Erro! Já existe um hábito com o nome '{novo_nome}'!")
        return

    # Renomear o hábito
    df.loc[df["Hábito"] == habito_atual, "Hábito"] = novo_nome
    usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
    print(f"Hábito '{habito_atual}' renomeado para '{novo_nome}' com sucesso!")

# Função para calcular estatísticas personalizadas
def calcular_estatistica_personalizada():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print("Colunas disponíveis:", ", ".join(df.columns))
    coluna = input("Digite o nome da coluna para calcular estatísticas: ").strip()

    if coluna not in df.columns:
        print(f"Erro! A coluna '{coluna}' não existe!")
        return

    print("Opções de Estatística:")
    print("1. Média")
    print("2. Mediana")
    print("3. Desvio Padrão")
    print("4. Mínimo")
    print("5. Máximo")
    escolha = input("Escolha o tipo de estatística (1-5): ").strip()

    try:
        if df[coluna].dtype in ['int64', 'float64']:
            if escolha == "1":
                resultado = df[coluna].mean()
                print(f"Média de {coluna}: {resultado:.2f}")
            elif escolha == "2":
                resultado = df[coluna].median()
                print(f"Mediana de {coluna}: {resultado:.2f}")
            elif escolha == "3":
                resultado = df[coluna].std()
                print(f"Desvio Padrão de {coluna}: {resultado:.2f}")
            elif escolha == "4":
                resultado = df[coluna].min()
                print(f"Valor Mínimo de {coluna}: {resultado}")
            elif escolha == "5":
                resultado = df[coluna].max()
                print(f"Valor Máximo de {coluna}: {resultado}")

    except Exception as e:
        print(f"Erro ao calcular estatística: {e}")
        
def validar_colunas(colunas):
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return False
    
    global usuarios
    df = usuarios[nome_usuario]
    
    for col in colunas:
        if col not in df.columns:
            print(f"Erro! A coluna '{col}' não existe no DataFrame!")
            return False
    return True

# Função para gerar gráfico de barra
def grafico_barra():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    print("Colunas do Data Frame: ", list(df.columns))
    x_col = input("Indique a coluna para o eixo X: ")
    y_col = input("Indique a coluna para o eixo Y: ")
    if validar_colunas([x_col, y_col]):
        plt.figure(figsize=(10, 6))
        df.plot(kind='bar', x=x_col, y=y_col, legend=True)
        plt.title("Gráfico de Barra")
        plt.legend(title=y_col)
        plt.show()
        
while True:
    print("Gestão de Hábitos Pessoais")
    print("1. Criar Utilizador")
    print("2. Criar Hábito")
    print("3. Consultar Hábitos")
    print("4. Adicionar Hábito")
    print("5. Filtrar por Categoria")
    print("6. Atualizar Status")
    print("7. Estatísticas")
    print("8. Remover Hábito")
    print("9. Atualizar Hábito")
    print("10. Gráfico de Barra")
    print("11. Exportar Dados para Excel")
    print("12. Sair")
    
    escolha = input("Escolha uma opção: ")
    
    if escolha == "1":
        criar_usuario()
    elif escolha == "2":
        criar_dataframe()
    elif escolha == "3":
        consultar_dataframe()
    elif escolha == "4":
        adicionar_habito()
    elif escolha == "5":
        filtrar_por_categoria()
    elif escolha == "6":
        atualizar_status()
    elif escolha == "7":
        estatisticas_habitos()
    elif escolha == "8":
        remover_habito() 
    elif escolha == "9":
        atualizar_habito()
    elif escolha == "10":
        grafico_barra()
    elif escolha == "11":  
        exportar_para_excel() 
    elif escolha == "12":
        print("Obrigado por usar o gestor de hábitos, até logo!")
        break
    else:
        print("Opção inválida, tente novamente!")




