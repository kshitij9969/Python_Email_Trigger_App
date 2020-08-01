import pandas


def withdraw(CUSTOMER_ID, amount):
    database = pandas.read_excel('database.xlsx', sheet_name='user_data')
    if CUSTOMER_ID in database['CUSTOMER_ID']:
        ids = database['CUSTOMER_ID'].to_list()
        balances = database['BALANCE'].to_list()
        balance = balances[ids.index(CUSTOMER_ID)]
        if balance >= amount:
            balances[ids.index(CUSTOMER_ID)] = balance - amount
            df = pandas.DataFrame(
                {
                    'CUSTOMER_ID':ids,
                    'BALANCE': balances
                }
            )
            df.to_excel('database.xlsx', 'user_data', index=False)
            return "Transaction successful, current balance " + str(balances[ids.index(CUSTOMER_ID)])
        else:
            return 'Insufficient balance!'
    else:
        return 'User not registered!'


def deposit(CUSTOMER_ID, amount):
    database = pandas.read_excel('database.xlsx', sheet_name='user_data')
    print(CUSTOMER_ID)
    print(CUSTOMER_ID in database['CUSTOMER_ID'])
    if CUSTOMER_ID in database['CUSTOMER_ID']:
        ids = database['CUSTOMER_ID'].to_list()
        balances = database['BALANCE'].to_list()
        balance = balances[ids.index(CUSTOMER_ID)]
        balances[ids.index(CUSTOMER_ID)] = balance + amount
        df = pandas.DataFrame(
            {
                'CUSTOMER_ID': ids,
                'BALANCE': balances
            }
        )
        df.to_excel('database.xlsx', 'user_data', index=False)
        return "Transaction successful, current balance " + str(balances[ids.index(CUSTOMER_ID)])
    else:
        return 'User not registered!'

