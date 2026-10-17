# Oficina System

MVP de um sistema desktop para gestão de oficina mecânica, desenvolvido como projeto acadêmico do curso de Análise e Desenvolvimento de Sistemas.

## Objetivo

Centralizar informações de clientes, veículos e ordens de serviço, reduzindo a dependência de anotações manuais na rotina da oficina.

## Funcionalidades implementadas

- Cadastro, consulta e alteração de clientes.
- Cadastro, consulta e alteração de veículos.
- Cadastro e listagem de ordens de serviço.
- Atualização do status das ordens por duplo clique na listagem.
- Validação de valores monetários.
- Persistência local com SQLite.

Dashboard, Estoque e Financeiro aparecem no menu, mas ainda não possuem funcionalidades implementadas.

## Tecnologias

- Python
- CustomTkinter
- Tkinter / ttk
- SQLite
- unittest
- GitHub Actions

## Como executar no Windows

É necessário ter Python com Tkinter e Git instalados.

No terminal, execute um comando por vez:

```powershell
git clone https://github.com/kelvin587-12/oficina-system.git
cd oficina-system
```

Enquanto o Pull Request inicial estiver aberto, acesse a branch de implementação:

```powershell
git switch implementacao-mvp
```

Crie o ambiente virtual e instale a dependência:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install customtkinter
```

Execute o sistema:

```powershell
.\venv\Scripts\python.exe app.py
```

O arquivo oficina.db será criado automaticamente na pasta do programa. Para começar, cadastre um cliente, depois um veículo e, por fim, uma ordem de serviço.

## Testes automatizados

Na pasta do projeto, execute:

```powershell
python -m unittest -v test_validacoes test_banco
```

Os testes verificam:

- Conversão de valores monetários válidos.
- Rejeição de valores inválidos e acima do limite.
- Gravação e persistência de ordens.
- Rejeição de veículo inexistente, status inválido e valor negativo.

Os testes de integração utilizam um banco temporário com estrutura reduzida, sem acessar o banco local da aplicação. Eles não substituem os testes manuais da interface.

## Integração Contínua

O GitHub Actions executa os testes automaticamente nos eventos push e pull_request.

Configuração: .github/workflows/testes.yml.

## Privacidade

O banco local, o ambiente virtual e arquivos temporários são excluídos do versionamento pelo .gitignore.

Utilize dados fictícios nas demonstrações e nos testes. Não envie cadastros reais ao repositório público.

## Limitações e próximos passos

- Melhorar rótulos, navegação por teclado e acesso às ações de edição.
- Ampliar a cobertura dos testes.
- Realizar duas rodadas de validação com representante externo.
- Documentar os feedbacks e os ajustes realizados.

## Autor

Kelvin Almeida — estudante de Análise e Desenvolvimento de Sistemas.
