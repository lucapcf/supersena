from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship

Base = declarative_base()

# The class Person relates to Bet with a relation of one to many
class Person(Base):
    __tablename__ = "persons"

    cpf = Column("cpf", String, primary_key=True, nullable=False)
    name = Column("name", String, nullable=False)
    bets = Relationship("Bet", back_populates="person")

    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def __repr__(self):
        return f"({self.cpf}) ({self.name})"

# The class Bet
class Bet(Base):
    __tablename__ = "bets"

    bet_id = Column("bet_id", String, primary_key=True, nullable=False)
    n1 = Column("n1", Integer, nullable=False)
    n2 = Column("n2", Integer, nullable=False)
    n3 = Column("n3", Integer, nullable=False)
    n4 = Column("n4", Integer, nullable=False)
    n5 = Column("n5", Integer, nullable=False)
    person_cpf = Column("person_cpf", String, ForeignKey("persons.cpf", ondelete="CASCADE"), nullable=False)

    person = Relationship("Person", back_populates="bets")

    def __init__(self, bet_id, n1, n2, n3, n4, n5, person_cpf):
        self.bet_id = bet_id
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.n5 = n5
        self.person_cpf = person_cpf
        

    def __repr__(self):
        return f"ID da aposta: {self.bet_id} | Números: {self.n1} {self.n2} {self.n3} {self.n4} {self.n5} | CPF do apostador: {self.person_cpf}"

    def to_list(self):
        """Return the bet numbers as a list."""
        return [self.n1, self.n2, self.n3, self.n4, self.n5]