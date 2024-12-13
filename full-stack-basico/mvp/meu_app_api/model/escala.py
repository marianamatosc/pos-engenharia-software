from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Escala(Base):
    __tablename__ = 'escala'

    id = Column("pk_escala", Integer, primary_key=True)
    nome_funcionario = Column(String(140), unique=True)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, nome_funcionario:str, data_inicio:DateTime, data_fim: DateTime, 
                     data_insercao:Union[DateTime, None] = None):
        """
        Cria um Escala

        Arguments:
            nome_funcionario: nome_funcionario do escala.
            data_inicio: data_inicio que se espera comprar daquele escala
            data_insercao: data de quando o escala foi inserido à base
        """
        self.nome_funcionario = nome_funcionario
        self.data_inicio = data_inicio
        self.data_fim = data_fim

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao



