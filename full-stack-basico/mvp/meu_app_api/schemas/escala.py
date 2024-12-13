from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from model.escala import Escala

class EscalaSchema(BaseModel):
    """ Define como um novo escala a ser inserido deve ser representado
    """
    nome_funcionario: str = "Mariana"
    data_inicio: datetime = datetime.strptime("2024-12-14", "%Y-%m-%d")
    data_fim: datetime = datetime.strptime("2024-12-14", "%Y-%m-%d")


class EscalaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome_funcionario do escala.
    """
    nome_funcionario: str = "Teste"


class ListagemEscalasSchema(BaseModel):
    """ Define como uma listagem de escalas será retornada.
    """
    escalas:List[EscalaSchema]


def apresenta_escalas(escala: List[Escala]):
    """ Retorna uma representação do escala seguindo o schema definido em
        EscalaViewSchema.
    """
    result = []
    for escala in escalas:
        result.append({
            "nome_funcionario": escala.nome_funcionario,
            "data_inicio": escala.data_inicio,
            "data_fim": escala.data_fim
        })

    return {"escala": result}


class EscalaViewSchema(BaseModel):
    """ Define como um escala será retornado: escala 
    """
    nome_funcionario: str = "Mariana"
    data_inicio: datetime = datetime.strptime("2024-12-20", "%Y-%m-%d") 
    data_fim: datetime = datetime.strptime("2024-12-26", "%Y-%m-%d") 


class EscalaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_funcionario: str

def apresenta_escala(escala: Escala):
    """ Retorna uma representação do escala seguindo o schema definido em
        EscalaViewSchema.
    """
    return {
        "nome_funcionario": escala.nome_funcionario,
        "data_inicio": escala.data_inicio,
        "data_fim": escala.data_fim    
    }
