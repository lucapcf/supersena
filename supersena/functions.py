from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supersena.models import Base, Person, Bet
import random

latest_bet_id = 999

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

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
        # text += "Nome: " + person.name + "\n"
        # text += "CPF: " + person.cpf + "\n"
        text += f"Nome: {person.name}\n"
        text += f"CPF: {person.cpf}\n"
        for bet in person.bets:
            # text += "** " + str(bet.bet_id) + " **"
            # text += " | "
            # text += str(bet.n1) + " "
            # text += str(bet.n2) + " "
            # text += str(bet.n3) + " "
            # text += str(bet.n4) + " "
            # text += str(bet.n5)
            # text += " | "
            text += f"** {bet.bet_id} ** | {bet.n1} {bet.n2} {bet.n3} {bet.n4} {bet.n5} |\n"
        text += "\n"

    # print(text)
    return text

def draw():
    return random.randint(0, 50)

# def order():
#     # query = query.order_by(Bet.column_name)
#     names = Bet.order_by(Bet.name).all()
#     # print("query: ", query)
#     print("query: ", names)

def verification():
    winners_cpf = []
    winning_numbers = []

    n_draws = 0

    # COMENTADO PARA TESTES
    # for i in range(5):
    #     winning_numbers.append(draw())
    winning_numbers = [1, 1, 1, 1, 1]

    winning_bets = session.query(Bet).filter(   Bet.n1 == winning_numbers[0],
                                                Bet.n2 == winning_numbers[1],
                                                Bet.n3 == winning_numbers[2],
                                                Bet.n4 == winning_numbers[3],
                                                Bet.n5 == winning_numbers[4]
                                            ).all()


    bets = session.query(Bet).all()

    # for bet in bets:
    #     print("\nType:\n", type(bet))
    #     print("\nType:\n", type(bet.to_list()))


    if not winning_bets:
        for n_draws in range(25):
            winning_numbers.append(draw())
            for bet in bets:
                bet_set = set(bet.to_list())
                if bet_set.issubset(winning_numbers):
                    winning_bets.append(bet)
            if winning_bets:
                break



    # if not winning_bets:
    #     for n_draws in range(25):
    #         # winning_numbers = draw()
    #         winning_numbers.append(draw())

    #         winning_bets = session.query(Bet).filter(   Bet.n1 == winning_numbers[0],
    #                                                 Bet.n2 == winning_numbers[1],
    #                                                 Bet.n3 == winning_numbers[2],
    #                                                 Bet.n4 == winning_numbers[3],
    #                                                 Bet.n5 == winning_numbers[4]
    #                                             ).all()

    #         if winning_bets:
    #             break


    # bets = session.query(Bet).all()


    
    # if not winning_bets:

    # print("\n\n winning bets!!!\n\n", winning_bets)

    # for bet in winning_bets:
    #     print(bet.  p)


    # for winning_bet in winning_bets:
    #     winners = 


    #          person = session.query(Person).filter(Person.cpf == cpf).all()


    #         winners_cpf.append(bet.person_cpf)

    # persons = session.query(Person).all()

    # for person in persons:
    #     if person.cpf == 

# 1) numeros sorteados
# 1 1 1 1 1
    numbers_drawn_str = str(winning_numbers)

    # numbers_drawn = []

# 2) numero de rodadas
# Rodadas: 25
    n_draws_str = str(n_draws + 1)
    # print("Rodadas:", nDraw)

# 3) numero de apostas vencedoras
# Apostas vencedoras: 2
    n_winning_bets = len(winning_bets)
    n_winning_bets_str = str(n_winning_bets)

# 4) lista de apostas vencedoras ordenada alfabeticamente ou "sem vencedores"
# Sem vencedores
    winning_bets_string = ""
    # print("n_winning_bets: ", n_winning_bets)
    if not n_winning_bets:
        print("ENTROU")
        winning_bets_string = "Sem vencedores. :("
    else:
        ordered_bets = session.query(Bet).join(Person).order_by(Person.name).all()

        for bet in ordered_bets:
            for winning_bet in winning_bets:
                if bet.bet_id == winning_bet.bet_id:
                    # winning_bets_string += "** " + str(bet.bet_id) + " **"
                    # winning_bets_string += " | "
                    # winning_bets_string += str(bet.n1) + " "
                    # winning_bets_string += str(bet.n2) + " "
                    # winning_bets_string += str(bet.n3) + " "
                    # winning_bets_string += str(bet.n4) + " "
                    # winning_bets_string += str(bet.n5)
                    # winning_bets_string += " | = "
                    # winning_bets_string += str(bet.person.name)
                    # winning_bets_string += " = "
                    # winning_bets_string += "\n"
                    winning_bets_string += f"** {bet.bet_id} ** | {bet.n1} {bet.n2} {bet.n3} {bet.n4} {bet.n5} | = {bet.person.name} = \n"


# 5) lista dos números apostados
# Nro apostado    Qtd de apostas
# 42              28
# 19              25
# 22              18
# 12              6



    text = ("Números sorteados: " + numbers_drawn_str + "\n" +
            "Número de rodadas: " + n_draws_str + "\n" +
            "Número de apostas vencedoras: " + n_winning_bets_str + "\n"
            "winning_bets:\n" + winning_bets_string)

    return text


def clear_database():
    session.query(Bet).delete()
    session.query(Person).delete()
    session.commit()



def main():
    pass

if __name__ == "__main__":
    main()