from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Aposta(Base):
    __tablename__ = "aposta"

    name = Column("name", String, primary_key=True)
    cpf = Column("cpf", String)
    n1 = Column("n1", Integer)
    n2 = Column("n2", Integer)
    n3 = Column("n3", Integer)
    n4 = Column("n4", Integer)
    n5 = Column("n5", Integer)


    def __init__(self, name, cpf, n1, n2, n3, n4, n5):
        self.name = name
        self.cpf = cpf
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.n5 = n5

    def __repr__(self):
        return f"({self.name}) {self.cpf} ({self.n1} {self.n2} {self.n3} {self.n5} {self.n5})"