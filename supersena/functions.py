from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from supersena.models import Base, Person, Bet
import random

latest_bet_id = 999

nDraws = 0

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# def add_bet(session, name, cpf, n1, n2, n3, n4, n5):
#     bet = bet(name, cpf, n1, n2, n3, n4, n5)
#     try:
#         session.add(bet)
#         session.commit()
#         print(f"Bet added: {bet}")
#     except Exception as e:
#         print(f"Error adding bet: {e}")
#         session.rollback()
#     finally:
#         session.close()
#         return session

def add_person(session, name, cpf):
    person = Person(name, cpf)
    try:
        session.add(person)
        session.commit()
        print(f"Person added: {person}")
    except Exception as e:
        print(f"Error adding person: {e}")
        session.rollback()
    finally:
        session.close()
        return session
    
def add_bet(session, n1, n2, n3, n4, n5, cpf):

    bet_id = update_bet_id()

    bet = Bet(bet_id, n1, n2, n3, n4, n5, cpf)
    try:
        # person.bets.append(bet)
        session.add(bet)
        session.commit()
        print(f"Bet added: {bet}")
    except Exception as e:
        print(f"Error adding bet: {e}")
        session.rollback()
    finally:
        session.close()
    
def update_bet_id():
    global latest_bet_id
    latest_bet_id += 1
    return latest_bet_id

def list_bets():
    persons = session.query(Person).all()

    text = ""

    for person in persons:
        text += "Nome: " + person.name + "\n"
        text += "CPF: " + person.cpf + "\n"
        for bet in person.bets:
            text += "** " + str(bet.bet_id) + " **"
            text += " | "
            text += str(bet.n1) + " "
            text += str(bet.n2) + " "
            text += str(bet.n3) + " "
            text += str(bet.n4) + " "
            text += str(bet.n5)
            text += " | "
        text += "\n"

    print(text)
    return text

def draw():

    global nDraws
    nDraws += 1

    numbers = []


    for i in range(5):
        numbers.append(random.randint(0, 50))

    return numbers

# def order():
#     # query = query.order_by(Bet.column_name)
#     names = Bet.order_by(Bet.name).all()
#     # print("query: ", query)
#     print("query: ", names)

def verification():
    winners_cpf = []

    # winning_numbers = draw()

    winning_numbers = [1, 1, 1, 1, 1]

    bets = session.query(Bet).all()


    winning_bets = session.query(Bet).filter(   Bet.n1 == winning_numbers[0],
                                                Bet.n2 == winning_numbers[1],
                                                Bet.n3 == winning_numbers[2],
                                                Bet.n4 == winning_numbers[3],
                                                Bet.n5 == winning_numbers[4]
                                            ).all()
    
    print("\n\n winning bets!!!\n\n", winning_bets)

    # for winning_bet in winning_bets:
    #     winners = 


    #          person = session.query(Person).filter(Person.cpf == cpf).all()

    # for bet in bets:
    #     if (bet.n1 == winning_numbers[0] and
    #         bet.n2 == winning_numbers[1] and
    #         bet.n3 == winning_numbers[2] and
    #         bet.n4 == winning_numbers[3] and
    #         bet.n5 == winning_numbers[4]):

    #         winners_cpf.append(bet.person_cpf)

    # persons = session.query(Person).all()

    # for person in persons:
    #     if person.cpf == 


def clear_database():
    session.query(Bet).delete()
    session.query(Person).delete()
    session.commit()


    
def main():
    pass

if __name__ == "__main__":
    main()