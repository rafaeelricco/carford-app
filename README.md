<p align="center">
  <img src="https://res.cloudinary.com/dnqiosdb6/image/upload/v1665622923/cover/caford-cover_copy_nbjdvs.png" alt="Cover">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
</p>

# Carford - Management System

Está é uma aplicação web simples feita para ajudar a loja de carros Carford em Nork-Town. Ela possui os mais básicos recursos da maioria dos aplicativos da web, como, login, rotas autenticadas, CRUD e um pouco de interatividade.

### Docker

Usando `docker compose` você pode simplesmente executar:

    docker compose build --no-cache
    docker compose up

E o aplicativo será executado em http://localhost:3333/

### Manualmente

Se você preferir executá-lo diretamente em sua máquina local, sugiro usar
[venv](https://docs.python.org/3/library/venv.html).

    pip install --no-cache-dir -r requirements.txt
    FLASK_APP=wsgi.py
    flask run

Agora você pode acessar em:
http://127.0.0.1:5000

## Principais Funcionalidades

- Login e Logout
- Registro de Usuários
- Operações CRUD
- Rotas Autenticadas
- Testes Unitários

## Licença

[MIT]()
