from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supersena.models import Base, Person, Bet
import random

latest_bet_id = 999

winning_numbers = []

n_winning_bets = 0

winning_bets = []

# Knobs to change the outcome
bet_price = 10
profit = 0.5

# DB setup
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_person(session, name, cpf):
    """
    Adds a new person to the database.
    """

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
    """
    Adds a new bet to the database associated with a person's CPF.
    """

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
    """
    Updates and returns the next available bet ID.
    """

    global latest_bet_id
    latest_bet_id += 1
    return latest_bet_id


def list_bets():
    """
    Retrieves and formats a list with the info
    about all the bets entered.
    """

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
    """
    Draws a random number not already contained in the provided list.
    """

    rand_num = random.randint(0, 50)
    while rand_num in numbers:
        rand_num = random.randint(0, 50)

    return rand_num


def verification():
    """
    Verifies bets against drawn numbers to identify winning bets,
    then calls extract_data to return data about the draw and winners.
    """

    global winning_numbers

    winning_numbers = []

    global winning_bets

    for i in range(5):
        winning_numbers.append(draw(winning_numbers))

    # for tests
    # winning_numbers = [1, 2, 3, 4, 5]

    

    bets = session.query(Bet).all()
    # if not winning_bets:
    for n_draws in range(1, 26):
        for bet in bets:
            bet_set = set(bet.to_list())
            if bet_set.issubset(winning_numbers):
                winning_bets.append(bet)
        if winning_bets:
            break
        winning_numbers.append(draw(winning_numbers))
    
    text = extract_data(winning_numbers, n_draws, winning_bets)

    return text

def extract_data(winning_numbers, n_draws, winning_bets):
    """
    Extracts and formats information about the raffle.
    """

# 1) Winning numbers
    numbers_drawn_str = str(winning_numbers)

# 2) Number of draws
    n_draws_str = str(n_draws + 1)

# 3) Number of winning bets
    global n_winning_bets

    n_winning_bets = len(winning_bets)
    n_winning_bets_str = str(n_winning_bets)

# 4) Lists winning bets in alphabetical order or displays "sem vencedores"
    winning_bets_string = ""
    print(n_winning_bets)
    if not n_winning_bets:
        winning_bets_string = "Sem vencedores. :("
    else:
        ordered_bets = session.query(Bet).join(Person).order_by(Person.name).all()

        for bet in ordered_bets:
            for winning_bet in winning_bets:
                if bet.bet_id == winning_bet.bet_id:
                    winning_bets_string += f"{bet.__repr__()} | Nome do apostador: {bet.person.name}\n"


# 5) Lists numbers bet and their frequency
    number_counts = {}
    num_occur = ""

    # Analyses the occurences for each number in each bet
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
    # """
    # Decide how the prize is divided amongst the winners.
    # In this case...
    # """

    global n_winning_bets
    global bet_price
    global profit
    global winning_bets

    bets = session.query(Bet).all()

    n_bets = len(bets)

    if not n_winning_bets:
        text = f"Sem vencedores. :("
    else:
        whole_prize =  float(n_bets) * float(bet_price) * profit

        individual_prize = whole_prize / float(n_winning_bets)

        # winner_points = {}

        # for bet in winning_bets:
        #     print("betttttttt:   ", bet)
        #     for num in bet.to_list():
        #         if is_prime(num):
        #             name = bet.person.name
        #             winner_points[name] += 1


# _________________________________________________________
#         # nao consegui terminar :(
#         # achei que bet em winning_bets era uma estrutura, mas não é :(
# _________________________________________________________



        text = f"Prêmio total: R${whole_prize}\nPrêmio individual: R${individual_prize}"

        # for key, value in winner_points.items():
        #     mult = 5/value
        #     prize = individual_prize * mult
        #     text += f"\nPrêmiação de {key}: R${prize}"

    return text

def is_prime(n):
    """
    Checks if a number is prime.
    """

    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def clear_database():
    """
    Clears all data from the bets and persons tables in the database.
    """

    session.query(Bet).delete()
    session.query(Person).delete()
    session.commit()