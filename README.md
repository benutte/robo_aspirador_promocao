# Grupo Promoção

Este programa tem como objetivo monitorar o preço de um produto em um site, neste caso, da Amazon, e enviar notificações via Telegram com os preços atual e anterior.

📋 Funcionalidades

    Acessa automaticamente o site da Amazon para obter o preço de um produto específico.
    Compara o preço atual com os registros anteriores.
    Envia notificações no Telegram informando:
        O preço atual do produto.
        O maior preço registrado anteriormente.

🛠️ Tecnologias Utilizadas

    Python: Linguagem principal do projeto.
    Requests: Para realizar as requisições HTTP ao site.
    BeautifulSoup: Para fazer o scraping de dados do site.
    SQLite: Para armazenamento local dos preços registrados.
    Telegram Bot API: Para enviar notificações.
    Dotenv: Para gerenciar variáveis de ambiente.

📂 Estrutura do Projeto

    grupo_promocao/
    ├── app.py              # Código principal do programa
    ├── requirements.txt    # Dependências do projeto
    ├── .env                # Variáveis de ambiente (não deve ser commitado)
    ├── README.md           # Documentação do projeto
    └── robo_aspirador.db   # Banco de dados SQLite para armazenamento dos preços

🛡️ Aviso Legal

    Este programa foi desenvolvido apenas para fins educacionais. O scraping de sites pode violar os Termos de Serviço das plataformas. Certifique-se de obter permissão antes de        utilizá-lo em produção.

📧 Contato

    Se tiver dúvidas ou sugestões, sinta-se à vontade para entrar em contato:

    Email: benutte20@gmail.com
