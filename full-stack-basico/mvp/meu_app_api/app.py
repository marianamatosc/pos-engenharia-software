from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Escala
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
escala_tag = Tag(name="Escala", description="Adição, visualização e remoção de férias à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/escala', tags=[escala_tag],
          responses={"200": EscalaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_escala(form: EscalaSchema):
    """Adiciona um novo Escala à base de dados

    Retorna uma representação dos escalas e comentários associados.
    """
    escala = Escala(
        nome_funcionario=form.nome_funcionario,
        data_inicio=form.data_inicio,
        data_fim=form.data_fim)
    logger.debug(f"Adicionando escala de nome_funcionario: '{escala.nome_funcionario}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando escala
        session.add(escala)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado escala de nome_funcionario: '{escala.nome_funcionario}'")
        return apresenta_escala(escala), 200

    except IntegrityError as e:
        # como a duplicidade do nome_funcionario é a provável razão do IntegrityError
        error_msg = "Escala de mesmo nome_funcionario já salvo na base :/"
        logger.warning(f"Erro ao adicionar escala '{escala.nome_funcionario}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar escala '{escala.nome_funcionario}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/escala', tags=[escala_tag],
         responses={"200": EscalaViewSchema, "404": ErrorSchema})
def get_escala(query: EscalaBuscaSchema):
    """Faz a busca por um Escala a partir do id do escala

       """
    escala_nome = query.nome_funcionario
    logger.debug(f"Coletando dados sobre escala #{escala_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    escala = session.query(Escala).filter(Escala.nome_funcionario == escala_nome).first()

    if not escala:
        # se o escala não foi encontrado
        error_msg = "Escala não encontrado na base :/"
        logger.warning(f"Erro ao buscar escala '{escala_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Escala econtrado: '{escala.nome_funcionario}'")
        # retorna a representação de escala
        return apresenta_escala(escala), 200


@app.delete('/escala', tags=[escala_tag],
            responses={"200": EscalaDelSchema, "404": ErrorSchema})
def del_escala(query: EscalaBuscaSchema):
    """Deleta um Escala a partir do nome_funcionario de escala informado

    Retorna uma mensagem de confirmação da remoção.
    """
    escala_nome_funcionario = unquote(unquote(query.nome_funcionario))
    print(escala_nome_funcionario)
    logger.debug(f"Deletando dados sobre escala #{escala_nome_funcionario}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Escala).filter(Escala.nome_funcionario == escala_nome_funcionario).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado escala #{escala_nome_funcionario}")
        return {"mesage": "Escala removida", "id": escala_nome_funcionario}
    else:
        # se o escala não foi encontrado
        error_msg = "Escala não encontrado na base :/"
        logger.warning(f"Erro ao deletar escala #'{escala_nome_funcionario}', {error_msg}")
        return {"mesage": error_msg}, 404

