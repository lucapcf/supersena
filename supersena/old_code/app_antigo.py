from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Aposta

def create_session():
    engine = create_engine("sqlite:///mydb.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

def add_bet(session, name, cpf, n1, n2, n3, n4, n5):
    session = create_session()
    aposta = Aposta(name, cpf, n1, n2, n3, n4, n5)
    try:
        session.add(aposta)
        session.commit()
        print(f"Aposta added: {aposta}")
    except Exception as e:
        print(f"Error adding aposta: {e}")
        session.rollback()
    finally:
        session.close()
        return session

if __name__ == "__main__":
    session = create_session()
    session = add_bet(session, "luca", "032.607.973-11", 2, 34, 22, 12, 5)
    session = add_bet(session, "joao", "032.607.973-11", 2, 34, 22, 12, 5)