# Flaskr

O tutorial oficial de Flask para uso de uma aplicação com pacotes (packages) python ao invés dos tradicionais módulos (arquivos python). Usamos banco de dados em arquivo (sqlite3). A descrição de cada um dos arquivos é o seguinte

>schema.sql: para criar as tabelas em sqlite
>db.py: para criar o banco de dados
>auth.py: blueprint de autenticação
>__init.py__: para rodar o aplicativo, estando devidamente configurado segundo os passos abaixo

Para isso, faz-se necessário o seguinte:

1. Incluir um arquivo __init__.py, que é equivalente a um módulo app.py;

2. Fora do pacote, ou seja, da pasta que contém o arquivo __init__.py, deve-se iniciar um "flask run" desde que a variável de ambiente "flask_app" esteja configurada como 'flaskr', ou seja, o nome do pacote;  
  * Para criar uma variável de ambiente no powershell, deve usar $env:flask_app = 'flaskr'
  * (Opcionalmente) configurar a variável de ambiente 'flask_env' para 'development'

3. Rode o "flask run" no terminal powershell propriamente dito;
