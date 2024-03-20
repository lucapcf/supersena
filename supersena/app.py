from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supersena.models import Base, Aposta


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_bet(session, name, cpf, n1, n2, n3, n4, n5):
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
    
def main():
    pass

if __name__ == "__main__":
    main()