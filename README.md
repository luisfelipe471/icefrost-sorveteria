# IceFrost Sorveteria

Aplicação web de uma sorveteria fictícia, feita com Django. O projeto reúne páginas públicas, galeria de imagens e gerenciamento de sabores para a equipe.

## Funcionalidades

- Páginas públicas de início, cardápio e galeria; o feedback fica disponível após login.
- Cadastro e login de usuários.
- Cadastro, edição e exclusão de sorvetes para usuários administradores.
- Fotos opcionais por sabor e filtros por nome, categoria e opção alimentar.
- Galeria com visualização ampliada por clique, teclado ou toque.
- Feedback com validação de formulário; feedbacks enviados são armazenados e exibidos do mais recente para o mais antigo apenas para a equipe administrativa.
- Sabores cadastrados com nomes conhecidos exibem fotos locais do Pexels; a equipe pode enviar uma foto específica para substituir a padrão.

As fotos enviadas pela equipe ficam em `media/sorvetes/` no ambiente local. Em produção, configure armazenamento persistente para arquivos de mídia.
As fontes das fotos do cardápio estão em [IMAGE_SOURCES.md](IMAGE_SOURCES.md); consulte também a [licença do Pexels](https://www.pexels.com/license/).

## Requisitos

- Python 3.12 ou superior.
- Dependências listadas em `requirements.txt`.

## Executar localmente

No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000/. Para acessar o Django Admin, crie um usuário administrador:

```powershell
python manage.py createsuperuser
```

## Testes

```powershell
python manage.py test
```

## Configuração para publicação

Defina as variáveis de ambiente no serviço de hospedagem:

- `DJANGO_SECRET_KEY`: uma chave longa, aleatória e exclusiva para produção.
- `DJANGO_DEBUG`: use `false` em produção.
- `DJANGO_ALLOWED_HOSTS`: nomes de host separados por vírgula, por exemplo `www.exemplo.com,exemplo.com`.

Os valores padrão de `SECRET_KEY` e `DEBUG` servem apenas para desenvolvimento local. Não use esses padrões em produção. Antes do deploy, confira também a lista de verificação de implantação do Django e configure HTTPS e arquivos estáticos no serviço escolhido.