import flet as ft
import requests
import threading

# URL do servidor Flask
server_url = "http://localhost:5000"

def main(page: ft.Page):
    page.title = "Chat de Conversa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.LIGHT_BLUE
    
    page.update()
    # Variável para armazenar o nome do usuário
    user_name = ""

    # Área onde as mensagens serão exibidas dentro de um ListView
    messages = ft.ListView(expand=True)

    # Variável para armazenar a última mensagem processada
    last_message_id = 0

    # Função para adicionar uma mensagem ao chat
    def send_message(e):
        if msg_input.value:
            try:
                response = requests.post(f"{server_url}/send", json={"user": user_name, "message": msg_input.value})
                if response.status_code == 200:
                    print(f"Mensagem enviada: {msg_input.value}")  # Log para depuração
                    msg_input.value = ""
                    page.update()
            except requests.exceptions.RequestException as e:
                print(f"Erro ao enviar mensagem: {e}")

    # Função para registrar o nome do usuário e indicar que ele entrou no chat
    def register_name(e):
        nonlocal user_name
        user_name = name_input.value
        if user_name:
            try:
                response = requests.post(f"{server_url}/send", json={"user": "usuario(a)", "message": f"{user_name} entrou no chat."})
                if response.status_code == 200:
                    print(f"{user_name} entrou no chat.")  # Log para depuração
                    dialog.open = False
                    name_input.visible = False
                    name_button.visible = False
                    msg_input.visible = True
                    send_button.visible = True
                    messages.visible = True
                    enter_chat_button.visible = False  # Esconder o botão "Entrar no chat"
                    page.update()
                    start_polling()  # Iniciar o polling de mensagens após o registro
            except requests.exceptions.RequestException as e:
                print(f"Erro ao registrar nome: {e}")

    # Função para fazer o polling de mensagens
    def poll_messages():
        nonlocal last_message_id
        while True:
            try:
                response = requests.get(f"{server_url}/poll")
                if response.status_code == 200:
                    messages_list = response.json()
                    # Adicionar as novas mensagens à lista existente
                    for i, message in enumerate(messages_list[last_message_id:], start=last_message_id):
                        print(f"Nova mensagem recebida: {message}")  # Log para depuração
                        messages.controls.append(ft.Text(f"{message['user']}: {message['message']}"))
                    last_message_id = len(messages_list)
                    page.update()
            except requests.exceptions.RequestException as e:
                print(f"Erro ao obter mensagens: {e}")

    # Função para iniciar o polling de mensagens
    def start_polling():
        threading.Thread(target=poll_messages, daemon=True).start()

    # Entrada de texto para o nome do usuário
    name_input = ft.TextField(hint_text="Digite seu nome aqui...", width=200, text_style=ft.TextStyle(color=ft.colors.RED))
    
    # Botão para registrar o nome do usuário
    name_button = ft.ElevatedButton(text="Entrar", on_click=register_name)

    # Entrada de texto para digitar as mensagens (inicialmente oculta)
    msg_input = ft.TextField(hint_text="Digite sua mensagem aqui...", expand=True, visible=False, text_style=ft.TextStyle(color=ft.colors.RED))

    # Botão para enviar a mensagem (inicialmente oculto)
    send_button = ft.ElevatedButton(text="Enviar", on_click=send_message, visible=False)

    # Botão inicial para abrir o pop-up de entrada
    def open_dialog(e):
        dialog.open = True
        page.update()

    enter_chat_button = ft.ElevatedButton(
        text="Entrar no chat",
        on_click=open_dialog,
        width=250,  # Aumenta a largura do botão
        height=70,  # Aumenta a altura do botão
    )

    # Pop-up de entrada do nome do usuário
    dialog = ft.AlertDialog(
        title=ft.Text("Entrar no Chat"),
        content=ft.Column([
            name_input,
            name_button,
        ], tight=True),
        on_dismiss=lambda _: None,
    )

    # Adicionando o texto "FRANK-CHAT" ao centro da tela
    frank_chat_text = ft.Text(
        "FRANK-CHAT",
        size=80,
        weight="bold",
        color=ft.colors.WHITE,
    )

    # Adicionando os componentes à página
    page.add(
        ft.Column(
            [
                frank_chat_text,
                ft.Container(
                    content=ft.Column([
                        ft.Row([msg_input, send_button], alignment=ft.MainAxisAlignment.END),
                        messages,
                    ]),
                    padding=20,
                    width=600,
                    height=500,
                    border_radius=10,
                    border=ft.BorderSide(1),
                    bgcolor=ft.colors.LIGHT_BLUE_50,
                ),
                ft.Row(
                    [enter_chat_button],
                    alignment=ft.MainAxisAlignment.CENTER  # Centraliza o botão
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Adicionar o pop-up à página
    page.dialog = dialog

# Iniciar a aplicação Flet
ft.app(target=main, view=ft.AppView.WEB_BROWSER)





