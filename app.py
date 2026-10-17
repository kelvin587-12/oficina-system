import customtkinter as ctk
from tkinter import ttk

import customtkinter as ctk
import sqlite3
from pathlib import Path
from tkinter import messagebox
from decimal import Decimal, InvalidOperation

# Banco salvo na mesma pasta deste arquivo Python
CAMINHO_BANCO = Path(__file__).resolve().parent / "oficina.db"

# Cria a tabela apenas se ela ainda não existir
with sqlite3.connect(CAMINHO_BANCO) as conexao:
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            documento TEXT,
            telefone TEXT,
            email TEXT
        )
    """)
    
with sqlite3.connect(CAMINHO_BANCO) as conexao:
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            placa TEXT NOT NULL UNIQUE,
            marca TEXT,
            modelo TEXT NOT NULL,
            ano TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)
with sqlite3.connect(CAMINHO_BANCO) as conexao:
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            valor_centavos INTEGER NOT NULL CHECK (valor_centavos >= 0),
            status TEXT NOT NULL DEFAULT 'Aberta'
                CHECK (status IN ('Aberta', 'Em andamento', 'Concluída')),
            data_abertura TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
        )
    """)  

app = ctk.CTk()

app.title("Oficina System")
app.geometry("1100x650")

menu_lateral = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0,
    fg_color="gray"
)

menu_lateral.pack(
    side="left",
    fill="y"
)

menu_lateral.pack_propagate(False)

# Área principal do sistema
area_principal = ctk.CTkFrame(
    app,
    corner_radius=0,
    fg_color="white"
)

area_principal.pack(
    side="right",
    fill="both",
    expand=True
)

# Nome do sistema
titulo = ctk.CTkLabel(
    menu_lateral,
    text="🔧 OFICINA SYSTEM",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=30, padx=20)

def limpar_area_principal():
    for widget in area_principal.winfo_children():
        widget.destroy()
def editar_cliente(cliente):
    janela = ctk.CTkToplevel(app)
    janela.title("Editar cliente")
    janela.geometry("460x420")
    janela.transient(app)

    ctk.CTkLabel(
        janela,
        text="Editar cliente",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    campos = []

    for rotulo, valor in zip(
        ("Nome", "CPF / CNPJ", "Telefone", "E-mail"),
        cliente[1:]
    ):
        ctk.CTkLabel(
            janela,
            text=rotulo
        ).pack(anchor="w", padx=30)

        campo = ctk.CTkEntry(janela, width=400)
        campo.pack(padx=30, pady=(0, 10))
        campo.insert(0, str(valor or ""))
        campos.append(campo)

    def salvar_alteracoes():
        nome, documento, telefone, email = [
            campo.get().strip() for campo in campos
        ]

        if not nome:
            messagebox.showwarning(
                "Campo obrigatório",
                "Preencha o nome do cliente.",
                parent=janela
            )
            campos[0].focus_set()
            return

        try:
            with sqlite3.connect(CAMINHO_BANCO) as conexao:
                conexao.execute("""
                    UPDATE clientes
                    SET nome = ?, documento = ?, telefone = ?, email = ?
                    WHERE id = ?
                """, (nome, documento, telefone, email, cliente[0]))

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro ao atualizar",
                f"Não foi possível atualizar o cliente.\n{erro}",
                parent=janela
            )
            return

        messagebox.showinfo(
            "Cliente atualizado",
            "Alterações salvas com sucesso!",
            parent=janela
        )

        janela.destroy()
        listar_clientes()

    ctk.CTkButton(
        janela,
        text="Salvar alterações",
        command=salvar_alteracoes
    ).pack(pady=15)
    

        
def listar_clientes():
    limpar_area_principal()

    titulo_lista = ctk.CTkLabel(
        area_principal,
        text="Clientes cadastrados",
        font=("Arial", 28, "bold"),
        text_color="black"
    )
    titulo_lista.pack(anchor="w", padx=40, pady=30)

    tabela = ttk.Treeview(
        area_principal,
        columns=("id", "nome", "documento", "telefone", "email"),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("documento", text="CPF / CNPJ")
    tabela.heading("telefone", text="Telefone")
    tabela.heading("email", text="E-mail")

    tabela.column("id", width=45, minwidth=40, stretch=False)
    tabela.column("nome", width=180)
    tabela.column("documento", width=140)
    tabela.column("telefone", width=130)
    tabela.column("email", width=180)

    tabela.pack(
        padx=40,
        pady=10,
        fill="both",
        expand=True
    )

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        clientes = conexao.execute("""
            SELECT id, nome, documento, telefone, email
            FROM clientes
            ORDER BY id DESC
        """).fetchall()

    for cliente in clientes:
        tabela.insert("", "end", values=cliente)
        
    def abrir_edicao(event):
        linha = tabela.identify_row(event.y)

        if not linha:
            return

        cliente = tabela.item(linha, "values")
        editar_cliente(cliente)

    tabela.bind("<Double-1>", abrir_edicao)

    botao_voltar = ctk.CTkButton(
        area_principal,
        text="Novo cliente",
        command=abrir_clientes
    )
    botao_voltar.pack(anchor="w", padx=40, pady=20)

def abrir_clientes():
    
    limpar_area_principal()

    titulo_clientes = ctk.CTkLabel(
        area_principal,
        text="Cadastro de Clientes",
        font=("Arial", 28, "bold"),
        text_color="black"
    )

    titulo_clientes.pack(
        anchor="w",
        padx=40,
        pady=30
    )
    
        # Campo Nome
    campo_nome = ctk.CTkEntry(
        area_principal,
        placeholder_text="Nome completo",
        width=400,
        height=40
    )
    campo_nome.pack(
        anchor="w",
        padx=40,
        pady=10
    )

    # Campo CPF/CNPJ
    campo_documento = ctk.CTkEntry(
        area_principal,
        placeholder_text="CPF ou CNPJ",
        width=400,
        height=40
    )
    campo_documento.pack(
        anchor="w",
        padx=40,
        pady=10
    )

    # Campo Telefone
    campo_telefone = ctk.CTkEntry(
        area_principal,
        placeholder_text="Telefone / WhatsApp",
        width=400,
        height=40
    )
    campo_telefone.pack(
        anchor="w",
        padx=40,
        pady=10
    )

    # Campo E-mail
    campo_email = ctk.CTkEntry(
        area_principal,
        placeholder_text="E-mail",
        width=400,
        height=40
    )
    campo_email.pack(
        anchor="w",
        padx=40,
        pady=10
    )
    
    def salvar_cliente():
        nome = campo_nome.get().strip()
        documento = campo_documento.get().strip()
        telefone = campo_telefone.get().strip()
        email = campo_email.get().strip()

        if not nome:
            messagebox.showwarning(
                "Campo obrigatório",
                "Preencha o nome do cliente."
            )
            campo_nome.focus_set()
            return

        try:
            with sqlite3.connect(CAMINHO_BANCO) as conexao:
                conexao.execute("""
                    INSERT INTO clientes (
                        nome, documento, telefone, email
                    )
                    VALUES (?, ?, ?, ?)
                """, (nome, documento, telefone, email))

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar o cliente.\n{erro}"
            )
            return

        messagebox.showinfo(
            "Cadastro concluído",
            "Cliente salvo com sucesso!"
        )

        # Limpa os campos para o próximo cadastro
        campo_nome.delete(0, "end")
        campo_documento.delete(0, "end")
        campo_telefone.delete(0, "end")
        campo_email.delete(0, "end")

        campo_nome.focus_set()

    # Botão Salvar
    botao_salvar = ctk.CTkButton(
        area_principal,
        text="Salvar Cliente",
        width=200,
        height=45,
        command=salvar_cliente
    )
    botao_salvar.pack(
        anchor="w",
        padx=40,
        pady=20
    )

    botao_listar = ctk.CTkButton(
        area_principal,
        text="Ver clientes cadastrados",
        width=200,
        height=40,
        command=listar_clientes
    )
    botao_listar.pack(
        anchor="w",
        padx=40,
        pady=10
    )
    
def editar_veiculo(veiculo_id):
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        veiculo = conexao.execute("""
            SELECT cliente_id, placa, marca, modelo, ano
            FROM veiculos
            WHERE id = ?
        """, (veiculo_id,)).fetchone()

        clientes = conexao.execute("""
            SELECT id, nome
            FROM clientes
            ORDER BY nome
        """).fetchall()

    if veiculo is None:
        messagebox.showwarning(
            "Veículo não encontrado",
            "Este veículo não está mais cadastrado."
        )
        return

    janela = ctk.CTkToplevel(app)
    janela.title("Editar veículo")
    janela.geometry("460x560")
    janela.transient(app)

    ctk.CTkLabel(
        janela,
        text="Editar veículo",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    opcoes_clientes = {
        f"{id_cliente} - {nome}": id_cliente
        for id_cliente, nome in clientes
    }

    ctk.CTkLabel(
        janela,
        text="Cliente proprietário"
    ).pack(anchor="w", padx=30)

    campo_cliente = ctk.CTkOptionMenu(
        janela,
        values=list(opcoes_clientes),
        width=400
    )
    campo_cliente.pack(padx=30, pady=(0, 10))

    # Seleciona o proprietário atual
    for opcao, cliente_id in opcoes_clientes.items():
        if cliente_id == veiculo[0]:
            campo_cliente.set(opcao)
            break

    campos = []

    for rotulo, valor in zip(
        ("Placa", "Marca", "Modelo", "Ano"),
        veiculo[1:]
    ):
        ctk.CTkLabel(
            janela,
            text=rotulo
        ).pack(anchor="w", padx=30)

        campo = ctk.CTkEntry(janela, width=400)
        campo.pack(padx=30, pady=(0, 10))
        campo.insert(0, str(valor or ""))
        campos.append(campo)

    def salvar_alteracoes():
        cliente_id = opcoes_clientes[campo_cliente.get()]

        placa, marca, modelo, ano = [
            campo.get().strip() for campo in campos
        ]

        placa = placa.upper().replace("-", "").replace(" ", "")

        if not placa or not modelo:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Preencha a placa e o modelo.",
                parent=janela
            )
            return

        if ano and (not ano.isdigit() or len(ano) != 4):
            messagebox.showwarning(
                "Ano inválido",
                "Informe o ano com quatro números, como 2022.",
                parent=janela
            )
            return

        try:
            with sqlite3.connect(CAMINHO_BANCO) as conexao:
                conexao.execute("PRAGMA foreign_keys = ON")

                conexao.execute("""
                    UPDATE veiculos
                    SET cliente_id = ?, placa = ?, marca = ?,
                        modelo = ?, ano = ?
                    WHERE id = ?
                """, (
                    cliente_id, placa, marca,
                    modelo, ano, veiculo_id
                ))

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Alteração não realizada",
                "A placa pertence a outro veículo ou o cliente não existe mais.",
                parent=janela
            )
            return

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro ao atualizar",
                f"Não foi possível atualizar o veículo.\n{erro}",
                parent=janela
            )
            return

        messagebox.showinfo(
            "Veículo atualizado",
            "Alterações salvas com sucesso!",
            parent=janela
        )

        janela.destroy()
        listar_veiculos()

    ctk.CTkButton(
        janela,
        text="Salvar alterações",
        command=salvar_alteracoes
    ).pack(pady=20)

def listar_veiculos():
    limpar_area_principal()

    ctk.CTkLabel(
        area_principal,
        text="Veículos cadastrados",
        font=("Arial", 28, "bold"),
        text_color="black"
    ).pack(anchor="w", padx=40, pady=30)

    tabela = ttk.Treeview(
        area_principal,
        columns=("placa", "marca", "modelo", "ano", "cliente"),
        show="headings"
    )

    tabela.heading("placa", text="Placa")
    tabela.heading("marca", text="Marca")
    tabela.heading("modelo", text="Modelo")
    tabela.heading("ano", text="Ano")
    tabela.heading("cliente", text="Proprietário")

    tabela.column("placa", width=100)
    tabela.column("marca", width=120)
    tabela.column("modelo", width=140)
    tabela.column("ano", width=60)
    tabela.column("cliente", width=200)

    tabela.pack(
        padx=40,
        pady=10,
        fill="both",
        expand=True
    )

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        veiculos = conexao.execute("""
            SELECT
                veiculos.id,
                veiculos.placa,
                veiculos.marca,
                veiculos.modelo,
                veiculos.ano,
                clientes.nome
            FROM veiculos
            JOIN clientes ON clientes.id = veiculos.cliente_id
            ORDER BY veiculos.id DESC
        """).fetchall()

    for veiculo in veiculos:
        tabela.insert(
            "",
            "end",
            iid=str(veiculo[0]),
            values=veiculo[1:]
        )

    def abrir_edicao(event):
        linha = tabela.identify_row(event.y)

        if not linha:
            return

        editar_veiculo(int(linha))

    tabela.bind("<Double-1>", abrir_edicao)

    ctk.CTkButton(
        area_principal,
        text="Novo veículo",
        command=abrir_veiculos
    ).pack(anchor="w", padx=40, pady=20)
    
def abrir_veiculos():
    limpar_area_principal()

    ctk.CTkLabel(
        area_principal,
        text="Cadastro de Veículos",
        font=("Arial", 28, "bold"),
        text_color="black"
    ).pack(anchor="w", padx=40, pady=30)

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        clientes = conexao.execute("""
            SELECT id, nome
            FROM clientes
            ORDER BY nome
        """).fetchall()

    if not clientes:
        ctk.CTkLabel(
            area_principal,
            text="Cadastre um cliente antes de cadastrar um veículo.",
            text_color="black"
        ).pack(anchor="w", padx=40, pady=10)
        return

    # Cada opção guarda o ID do cliente correspondente
    opcoes_clientes = {
        f"{id_cliente} - {nome}": id_cliente
        for id_cliente, nome in clientes
    }

    ctk.CTkLabel(
        area_principal,
        text="Cliente proprietário",
        text_color="black"
    ).pack(anchor="w", padx=40)

    campo_cliente = ctk.CTkOptionMenu(
        area_principal,
        values=list(opcoes_clientes),
        width=400
    )
    campo_cliente.pack(anchor="w", padx=40, pady=10)

    campo_placa = ctk.CTkEntry(
        area_principal,
        placeholder_text="Placa",
        width=400,
        height=40
    )
    campo_placa.pack(anchor="w", padx=40, pady=10)

    campo_marca = ctk.CTkEntry(
        area_principal,
        placeholder_text="Marca — exemplo: Hyundai",
        width=400,
        height=40
    )
    campo_marca.pack(anchor="w", padx=40, pady=10)

    campo_modelo = ctk.CTkEntry(
        area_principal,
        placeholder_text="Modelo — exemplo: HB20",
        width=400,
        height=40
    )
    campo_modelo.pack(anchor="w", padx=40, pady=10)

    campo_ano = ctk.CTkEntry(
        area_principal,
        placeholder_text="Ano — exemplo: 2022",
        width=400,
        height=40
    )
    campo_ano.pack(anchor="w", padx=40, pady=10)

    def salvar_veiculo():
        cliente_id = opcoes_clientes[campo_cliente.get()]
        placa = (
            campo_placa.get()
            .strip()
            .upper()
            .replace("-", "")
            .replace(" ", "")
        )
        marca = campo_marca.get().strip()
        modelo = campo_modelo.get().strip()
        ano = campo_ano.get().strip()

        if not placa or not modelo:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Preencha a placa e o modelo."
            )
            return

        if ano and (not ano.isdigit() or len(ano) != 4):
            messagebox.showwarning(
                "Ano inválido",
                "Informe o ano com quatro números, como 2022."
            )
            return

        try:
            with sqlite3.connect(CAMINHO_BANCO) as conexao:
                conexao.execute("PRAGMA foreign_keys = ON")

                conexao.execute("""
                    INSERT INTO veiculos (
                        cliente_id, placa, marca, modelo, ano
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (cliente_id, placa, marca, modelo, ano))

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Cadastro não realizado",
                "A placa já está cadastrada ou o cliente não existe mais."
            )
            return

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar o veículo.\n{erro}"
            )
            return

        messagebox.showinfo(
            "Cadastro concluído",
            "Veículo salvo com sucesso!"
        )

        for campo in (
            campo_placa,
            campo_marca,
            campo_modelo,
            campo_ano
        ):
            campo.delete(0, "end")

        campo_placa.focus_set()

    ctk.CTkButton(
        area_principal,
        text="Salvar Veículo",
        width=200,
        height=45,
        command=salvar_veiculo
    ).pack(anchor="w", padx=40, pady=20)
    
     # Cole o novo botão aqui
    ctk.CTkButton(
        area_principal,
        text="Ver veículos cadastrados",
        width=200,
        height=40,
        command=listar_veiculos
    ).pack(anchor="w", padx=40, pady=10)
    
def editar_status_ordem(ordem_id):
    try:
        with sqlite3.connect(CAMINHO_BANCO) as conexao:
            ordem = conexao.execute("""
                SELECT status
                FROM ordens_servico
                WHERE id = ?
            """, (ordem_id,)).fetchone()

    except sqlite3.Error as erro:
        messagebox.showerror(
            "Erro ao consultar",
            f"Não foi possível abrir a ordem.\n{erro}"
        )
        return

    if ordem is None:
        messagebox.showwarning(
            "Ordem não encontrada",
            "Esta ordem não está mais cadastrada."
        )
        return

    janela = ctk.CTkToplevel(app)
    janela.title(f"Status da ordem nº {ordem_id}")
    janela.geometry("400x250")
    janela.transient(app)

    ctk.CTkLabel(
        janela,
        text=f"Ordem de Serviço nº {ordem_id}",
        font=("Arial", 22, "bold")
    ).pack(pady=25)

    campo_status = ctk.CTkOptionMenu(
        janela,
        values=["Aberta", "Em andamento", "Concluída"],
        width=280
    )
    campo_status.set(ordem[0])
    campo_status.pack(pady=10)

    def salvar_status():
        try:
            with sqlite3.connect(CAMINHO_BANCO) as conexao:
                cursor = conexao.execute("""
                    UPDATE ordens_servico
                    SET status = ?
                    WHERE id = ?
                """, (campo_status.get(), ordem_id))

                atualizada = cursor.rowcount == 1

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro ao atualizar",
                f"Não foi possível salvar o status.\n{erro}",
                parent=janela
            )
            return

        if not atualizada:
            messagebox.showwarning(
                "Ordem não encontrada",
                "Esta ordem não está mais cadastrada.",
                parent=janela
            )
            return

        messagebox.showinfo(
            "Status atualizado",
            "Status salvo com sucesso!",
            parent=janela
        )

        janela.destroy()
        listar_ordens()

    ctk.CTkButton(
        janela,
        text="Salvar status",
        command=salvar_status
    ).pack(pady=20)
    
def listar_ordens():
    limpar_area_principal()

    ctk.CTkLabel(
        area_principal,
        text="Ordens de Serviço",
        font=("Arial", 28, "bold"),
        text_color="black"
    ).pack(anchor="w", padx=40, pady=25)

    quadro_tabela = ttk.Frame(area_principal)
    quadro_tabela.pack(
        padx=40,
        pady=10,
        fill="both",
        expand=True
    )

    colunas = ("numero", "placa", "cliente", "servico", "valor", "status")

    tabela = ttk.Treeview(
        quadro_tabela,
        columns=colunas,
        show="headings"
    )

    for coluna, titulo, largura in (
        ("numero", "Nº OS", 60),
        ("placa", "Placa", 90),
        ("cliente", "Cliente", 150),
        ("servico", "Serviço", 220),
        ("valor", "Valor", 100),
        ("status", "Status", 130),
    ):
        tabela.heading(coluna, text=titulo)
        tabela.column(coluna, width=largura, minwidth=60)

    rolagem_vertical = ttk.Scrollbar(
        quadro_tabela,
        orient="vertical",
        command=tabela.yview
    )
    rolagem_vertical.pack(side="right", fill="y")

    rolagem_horizontal = ttk.Scrollbar(
        quadro_tabela,
        orient="horizontal",
        command=tabela.xview
    )
    rolagem_horizontal.pack(side="bottom", fill="x")

    tabela.configure(
        yscrollcommand=rolagem_vertical.set,
        xscrollcommand=rolagem_horizontal.set
    )
    tabela.pack(side="left", fill="both", expand=True)

    try:
        with sqlite3.connect(CAMINHO_BANCO) as conexao:
            ordens = conexao.execute("""
                SELECT
                    ordens_servico.id,
                    veiculos.placa,
                    clientes.nome,
                    ordens_servico.descricao,
                    ordens_servico.valor_centavos,
                    ordens_servico.status
                FROM ordens_servico
                JOIN veiculos
                    ON veiculos.id = ordens_servico.veiculo_id
                JOIN clientes
                    ON clientes.id = veiculos.cliente_id
                ORDER BY ordens_servico.id DESC
            """).fetchall()

    except sqlite3.Error as erro:
        messagebox.showerror(
            "Erro ao consultar",
            f"Não foi possível carregar as ordens.\n{erro}"
        )
        return

    for numero, placa, cliente, servico, centavos, status in ordens:
        reais, centavos_restantes = divmod(centavos, 100)
        valor_formatado = (
            f"R$ {reais:,}".replace(",", ".")
            + f",{centavos_restantes:02d}"
        )

        tabela.insert(
            "",
            "end",
            iid=str(numero),
            values=(
                numero,
                placa,
                cliente,
                servico,
                valor_formatado,
                status
            )
        )
        
    def abrir_status(event):
        linha = tabela.identify_row(event.y)

        if not linha:
            return

        editar_status_ordem(int(linha))

    tabela.bind("<Double-1>", abrir_status)    

    if not ordens:
        ctk.CTkLabel(
            area_principal,
            text="Nenhuma ordem de serviço cadastrada.",
            text_color="black"
        ).pack(anchor="w", padx=40, pady=10)

    ctk.CTkButton(
        area_principal,
        text="Nova Ordem de Serviço",
        command=abrir_ordens
    ).pack(anchor="w", padx=40, pady=20)
    
def abrir_ordens():
    limpar_area_principal()

    ctk.CTkLabel(
        area_principal,
        text="Nova Ordem de Serviço",
        font=("Arial", 28, "bold"),
        text_color="black"
    ).pack(anchor="w", padx=40, pady=25)

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        veiculos = conexao.execute("""
            SELECT veiculos.id, veiculos.placa,
                   veiculos.modelo, clientes.nome
            FROM veiculos
            JOIN clientes ON clientes.id = veiculos.cliente_id
            ORDER BY veiculos.placa
        """).fetchall()

    if not veiculos:
        ctk.CTkLabel(
            area_principal,
            text="Cadastre um veículo antes de abrir uma ordem de serviço.",
            text_color="black"
        ).pack(anchor="w", padx=40, pady=10)
        return

    opcoes_veiculos = {
        f"{placa} - {modelo} - {nome}": veiculo_id
        for veiculo_id, placa, modelo, nome in veiculos
    }

    ctk.CTkLabel(
        area_principal,
        text="Veículo e proprietário",
        text_color="black"
    ).pack(anchor="w", padx=40)

    campo_veiculo = ctk.CTkOptionMenu(
        area_principal,
        values=list(opcoes_veiculos),
        width=500
    )
    campo_veiculo.pack(anchor="w", padx=40, pady=(5, 15))

    ctk.CTkLabel(
        area_principal,
        text="Descrição do serviço",
        text_color="black"
    ).pack(anchor="w", padx=40)

    campo_descricao = ctk.CTkTextbox(
        area_principal,
        width=500,
        height=120
    )
    campo_descricao.pack(anchor="w", padx=40, pady=(5, 15))

    campo_valor = ctk.CTkEntry(
        area_principal,
        placeholder_text="Valor em R$ — exemplo: 150,50",
        width=300,
        height=40
    )
    campo_valor.pack(anchor="w", padx=40, pady=10)

    ctk.CTkLabel(
        area_principal,
        text="Status da ordem",
        text_color="black"
    ).pack(anchor="w", padx=40)

    campo_status = ctk.CTkOptionMenu(
        area_principal,
        values=["Aberta", "Em andamento", "Concluída"],
        width=300
    )
    campo_status.set("Aberta")
    campo_status.pack(anchor="w", padx=40, pady=10)

    def salvar_ordem():
        veiculo_id = opcoes_veiculos[campo_veiculo.get()]
        descricao = campo_descricao.get("1.0", "end").strip()
        texto_valor = campo_valor.get().strip().replace(",", ".")
        status = campo_status.get()

        if not descricao:
            messagebox.showwarning(
                "Campo obrigatório",
                "Descreva o serviço que será realizado."
            )
            campo_descricao.focus_set()
            return

        try:
            valor = Decimal(texto_valor)

            if not valor.is_finite() or valor < 0:
                raise ValueError

            centavos = valor * 100

            if centavos != centavos.to_integral_value():
                raise ValueError

            if centavos > 9223372036854775807:
                raise ValueError

            valor_centavos = int(centavos)

        except (InvalidOperation, ValueError):
            messagebox.showwarning(
                "Valor inválido",
                "Informe um valor positivo ou zero, com até duas "
                "casas decimais. Exemplo: 150,50."
            )
            campo_valor.focus_set()
            return

        try:
            with sqlite3.connect(CAMINHO_BANCO) as conexao:
                conexao.execute("PRAGMA foreign_keys = ON")

                cursor = conexao.execute("""
                    INSERT INTO ordens_servico (
                        veiculo_id, descricao, valor_centavos, status
                    )
                    VALUES (?, ?, ?, ?)
                """, (veiculo_id, descricao, valor_centavos, status))

                numero_ordem = cursor.lastrowid

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar a ordem.\n{erro}"
            )
            return

        messagebox.showinfo(
            "Ordem cadastrada",
            f"Ordem de serviço nº {numero_ordem} salva com sucesso!"
        )

        campo_descricao.delete("1.0", "end")
        campo_valor.delete(0, "end")
        campo_status.set("Aberta")
        campo_descricao.focus_set()

    ctk.CTkButton(
        area_principal,
        text="Salvar Ordem de Serviço",
        width=240,
        height=45,
        command=salvar_ordem
    ).pack(anchor="w", padx=40, pady=20)
    
    ctk.CTkButton(
        area_principal,
        text="Ver ordens cadastradas",
        width=240,
        height=40,
        command=listar_ordens
    ).pack(anchor="w", padx=40, pady=5)
    

# Botão Dashboard
botao_dashboard = ctk.CTkButton(
    menu_lateral,
    text="🏠  Dashboard",
    anchor="w",
    height=45
)
botao_dashboard.pack(padx=20, pady=5, fill="x")

# Botão Clientes
botao_clientes = ctk.CTkButton(
    menu_lateral,
    text="👤  Clientes",
    anchor="w",
    height=45,
    command=abrir_clientes
)
botao_clientes.pack(padx=20, pady=5, fill="x")

# Botão Veículos
botao_veiculos = ctk.CTkButton(
    menu_lateral,
    text="🚗  Veículos",
    anchor="w",
    height=45,
    command=abrir_veiculos
)
botao_veiculos.pack(padx=20, pady=5, fill="x")

# Botão Ordens de Serviço
botao_ordens = ctk.CTkButton(
    menu_lateral,
    text="🔧  Ordens de Serviço",
    anchor="w",
    height=45,
    command=abrir_ordens
)
botao_ordens.pack(padx=20, pady=5, fill="x")

# Botão Estoque
botao_estoque = ctk.CTkButton(
    menu_lateral,
    text="📦  Estoque",
    anchor="w",
    height=45
)
botao_estoque.pack(padx=20, pady=5, fill="x")

# Botão Financeiro
botao_financeiro = ctk.CTkButton(
    menu_lateral,
    text="💰  Financeiro",
    anchor="w",
    height=45
)
botao_financeiro.pack(padx=20, pady=5, fill="x")

app.mainloop()