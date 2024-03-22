from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supersena.models import Base, Person, Bet
import random

latest_bet_id = 999

# winning_bets = ""

winning_numbers = []

n_winning_bets = 0

winning_bets = []

bet_price = 10

profit = 0.5

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
        text += f"Nome: {person.name}\n"
        text += f"CPF: {person.cpf}\n"
        for bet in person.bets:
            index = (bet.__repr__()).find("CPF do apostador:")
            text += bet.__repr__()[:index]
        text += "\n"

    return text


def draw(numbers):

    rand_num = random.randint(0, 50)

    while rand_num in numbers:
        rand_num = random.randint(0, 50)

    return rand_num


def verification():
    global winning_numbers

    global winning_bets

    n_draws = 0

    for i in range(5):
        winning_numbers.append(draw(winning_numbers))

    bets = session.query(Bet).all()
    if not winning_bets:
        for n_draws in range(25):
            winning_numbers.append(draw(winning_numbers))
            for bet in bets:
                bet_set = set(bet.to_list())
                if bet_set.issubset(winning_numbers):
                    winning_bets.append(bet)
            if winning_bets:
                print("WINNING BET", winning_bets)
                break
    
    text = extract_data(winning_numbers, n_draws, winning_bets)

    return text

def extract_data(winning_numbers, n_draws, winning_bets):

# 1) numeros sorteados
    numbers_drawn_str = str(winning_numbers)

# 2) numero de rodadas
    n_draws_str = str(n_draws + 1)

# 3) numero de apostas vencedoras

    global n_winning_bets

    n_winning_bets = len(winning_bets)
    n_winning_bets_str = str(n_winning_bets)

# 4) lista de apostas vencedoras ordenada alfabeticamente ou "sem vencedores"
    winning_bets_string = ""
    if not n_winning_bets:
        winning_bets_string = "Sem vencedores. :("
    else:
        ordered_bets = session.query(Bet).join(Person).order_by(Person.name).all()

        for bet in ordered_bets:
            for winning_bet in winning_bets:
                if bet.bet_id == winning_bet.bet_id:
                    winning_bets_string += f"{bet.__repr__()} | Nome do apostador: {bet.person.name}\n"


# 5) lista dos números apostados e n de ocorrencias

    number_counts = {}
    num_occur = ""

    # Iterate over each number in the list
    bets = session.query(Bet).all()
    for bet in bets:
        for number in bet.to_list():
            # If the number is already in the dictionary, it is incremented
            if number in number_counts:
                number_counts[number] += 1
            # Otherwise, the number is added to the dictionary with 1 occurence
            else:
                number_counts[number] = 1

    num_occur += (f"{'Número apostado':^15}  |  {'Quantidade de apostas':^20}\n")

    for number, count in number_counts.items():
        num_occur +=  (f"{number:^15}  |  {count:^20}\n")


    # Assembling the data
    text = ("Números sorteados: " + numbers_drawn_str + "\n" +
            "Número de rodadas: " + n_draws_str + "\n" +
            "Número de apostas vencedoras: " + n_winning_bets_str + "\n" +
            "Apostas vencedoras ordenadas alfabeticamente:\n" +
            winning_bets_string + "\n" +
            num_occur)

    return text

def awards():
    """
    Decide how the prize is divided amongst the winners.
    In this case, the more you bet the number "1", the more you will win
    """
    global n_winning_bets
    global bet_price
    global profit
    global winning_bets

    print(type(winning_bets))

    if not n_winning_bets:
        text = f"Sem vencedores. :("
    else:
        whole_prize =  float(n_winning_bets) * float(bet_price) * profit

        individual_prize = whole_prize / float(n_winning_bets)

        text = f"Prêmio total: {whole_prize}\n"

    return text


def clear_database():
    session.query(Bet).delete()
    session.query(Person).delete()
    session.commit()