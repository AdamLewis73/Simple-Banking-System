import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

random.seed()
card_nums = []
pins = []
balances = []
menu_option = None
log_menu = None
index_val = None
new_id = None
id_val = 0
account_id = 0
cur.execute('''CREATE TABLE IF NOT EXISTS card
        (id integer, number text, pin text, balance integer DEFAULT 0)''')
# cur.execute('''INSERT INTO card
#               VALUES(-1, 'temp','temp', 0)''')
conn.commit()

class Account:
    def __init__(self):
        sum_of_nums = 0
        luhn_num = []
        luhn_num2 = []
        final_luhn_num = ''
        check_sum = 0
        pin_temp = None
        for _ in range(9):
            luhn_num.append(random.randrange(9))
        luhn_num2 = luhn_num.copy()
        for index, value in enumerate(luhn_num):
            if index % 2 == 0:
                luhn_num[index] = value * 2
            if luhn_num[index] > 9:
                luhn_num[index] = luhn_num[index] - 9
        print(luhn_num)
        print((sum(luhn_num)+8) % 10)
        if (sum(luhn_num)+8) % 10 != 0:
            check_sum = 10 - ((sum(luhn_num)+8) % 10)
        else:
            check_sum = 0
        for val in luhn_num2:
            final_luhn_num = ''.join(final_luhn_num + str(val))
        final_num = str(400000) + final_luhn_num + str(check_sum)
        self.card_num = final_num
        pin_temp = str(random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9))
        self.pin = pin_temp
        self.balance = 0

def main_menu_print():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    return int(input())

def log_menu_print():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    return int(input())

def log_menu_action(log_menu,log_card,conn,cards_list):
    cur = conn.cursor()
    if log_menu == 1:
        cur.execute('SELECT balance FROM card WHERE number = ?', (log_card,))
        account_val = cur.fetchone()[0]
        print("Balance: {}".format(account_val))
        conn.commit()
        return 0
    elif log_menu == 2:
        print('Enter the amount of money deposited')
        add_income = int(input())
        cur.execute('SELECT balance FROM card WHERE number = ?', (log_card,))
        account_bal = cur.fetchone()[0]
        print(add_income)
        print(log_card)
        cur.execute('UPDATE card SET Balance = ? WHERE number = ?', ((account_bal+add_income),log_card))
        conn.commit()
        print('Income added')
        return 0
    elif log_menu == 3:
        print('Enter the card number of the account transferred to')
        transfer_num = input()
        transfer_num_list = [int(i) for i in list(transfer_num)]
        transfer_num_list = [2*i if j%2==0 else i for j,i in enumerate(transfer_num_list)]
        transfer_num_list = [i-9 if i>9 else i for i in transfer_num_list]
        print(transfer_num_list)
        if sum(transfer_num_list)%10 != 0:
            print('Probably you made a mistake in the card number. Please try again!')
            return 0
        elif transfer_num == log_card:
            print("You can't transfer money to the same account!")
            return 0
        elif transfer_num not in cards_list:
            print("Such a card does not exist.")
            return 0
        else:
            if transfer_num in cards_list:
                print('Enter the amount of money to transfer')
                transfer_amount = int(input())
                cur.execute('SELECT balance FROM card WHERE number = ?', (log_card,))
                account_bal = cur.fetchone()[0]
                if account_bal<transfer_amount:
                    print('Not enough money!')
                else:
                    cur.execute('SELECT balance FROM card WHERE number = ?', (transfer_num,))
                    transfer_account_bal = cur.fetchone()[0]
                    transfer_account_bal +=transfer_amount
                    cur.execute('UPDATE card SET Balance = ? WHERE number = ?', (transfer_account_bal,transfer_num))
                    cur.execute('UPDATE card SET Balance = ? WHERE number = ?', ((account_bal-transfer_amount),log_card))
                    conn.commit()
                return 0

    elif log_menu == 4:
        print('The account has been closed!\n')
        cur.execute('DELETE FROM card WHERE number = ?',(log_card,))
        conn.commit()
        return 1
    elif log_menu == 5:
        return 1
    else:
        return 1

def data_insert(conn, data):
    sql = '''INSERT INTO card(id, number, pin, balance)
    VALUES (?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

def account_create(conn):
    global account_id, new_id, id_val
    temp1 = Account()
    card_nums.append(temp1.card_num)
    pins.append(temp1.pin)
    balances.append(temp1.balance)
    print('Your card has been created')
    print('Your card number:')
    print(card_nums[-1])
    print('Your card PIN:')
    print(pins[-1])
    cur = conn.cursor()
    cur.execute('SELECT id FROM card ORDER BY id DESC LIMIT 1')
    id_val = cur.fetchone()
    # print(id_val[0])
    if id_val:
        account_id = id_val[0] + 1
    else:
        account_id = 0
    temp_data = (account_id, card_nums[-1], pins[-1], 0)
    new_id = data_insert(conn, temp_data)
    
def log_in(conn):
    global log_menu
    log_result = 0
    cur = conn.cursor()
    print("Enter your card number:")
    log_card = input()
    print("Enter your PIN:")
    log_pin = input()
    #print(log_card)
    #print(type(log_pin))
    #print(card_nums[-1])
    #print(type(pins[-1]))
    cur.execute('SELECT number FROM card')
    # cards_list = cur.fetchall()
    cards_list = [row[0] for row in cur.fetchall()]
    print(cards_list)
    # cur.execute('SELECT pin FROM card')
    # pins_list = cur.fetchall()
    # cur.execute('SELECT pin FROM card')
    # balance_list = cur.fetchall()

    if log_card in cards_list:
        # index_val = card_nums.index(log_card)
        cur.execute('SELECT pin, balance FROM card WHERE number = ?', (log_card,))
        account_vals = cur.fetchone()
        # if log_pin == pins_list[index_val]:
        if log_pin == account_vals[0]:
            print('You have successfully logged in!')
            while log_menu !=0:
                log_menu = log_menu_print()
                log_result = log_menu_action(log_menu,log_card,conn, cards_list)
                if log_result == 1:
                    break
        else:
            print("\nWrong card number or PIN!")
    else:
        print("\nWrong card number or PIN!")



while menu_option != 0:
    menu_option = main_menu_print()

    if menu_option == 1:
        account_create(conn)
    elif menu_option == 2:
        log_in(conn)
        if log_menu == 0:
            break
    elif menu_option == 0:
        continue 
    else:
        print("Not a menu option")
conn.close()
print("Bye!") 
