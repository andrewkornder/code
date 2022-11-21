from amazon_account import AmazonAccount, AmazonItem
import tkinter
from tkinter.ttk import Treeview


def main():
    def _atb(account):
        account.add_gift_amount(int(input('how much money?\n')))

    def _purchase(account):
        # letting the user do whatever so far, a final ui would have a list of items to pick from 
        item = input('type the item details as "item $amount" below:\n').split()
        item[1] = float(item[1][1:])
        account.purchase_item(AmazonItem(*item))

    def _change_email(account):
        account.change_email()
        account.show_info()

    def _new_acc():
        details = [input(a) for a in ['name? ', 'email? ', 'password']]
        if input('add money to the balance? (Y/N)').lower()[0] == 'y':
            money = input('how much? ')
            details.append(int(money))
        amazon_customers.append(AmazonAccount(*details))

    def _show_all():
        root = tkinter.Tk()

        # code index found on stack overflow for bringing window to front
        # not really sure why it's this complicated, but it works
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)

        root.geometry('785x280')

        table = Treeview(root, columns=('account', 'email address', 'password', 'balance ($)'),
                     show='headings')
        for heading in table['columns']:
            table.heading(heading, text=heading.upper())
        for i, cust in enumerate(amazon_customers):
            table.insert('', 'end', values=tuple(cust.__dict__.values()))

        table.pack()
        root.mainloop()

    def _choose_account():
        acc = int(input('select account:\n' + '\n'.join([f'{i + 1}. {a.name}' for i, a in enumerate(amazon_customers)]) + '\n'))
        return amazon_customers[acc - 1]
        
    amazon_customers = [AmazonAccount('name1', 'email@gmail.com', 'pass1', 100),
                        AmazonAccount('name2', 'email2@gmail.com', 'pass2', 0),
                        AmazonAccount('name3', 'email3@gmail.com', 'pass3')]

    operations = {
        '1. add to balance': _atb,
        '2. purchase item': _purchase,
        '3. change_email': _change_email,
        '4. add an account': _new_acc,
        '5. show all accounts': _show_all,
        '6. quit': None
    }

    while True:
        selected = int(input('\n'.join(operations.keys()) + '\n\n').lstrip()) - 1
        if selected == 5:
            break
        func = list(operations.values())[selected]
        if selected < 4:
            func(_choose_account())
        else:
            func()


if __name__ == '__main__':
    main()
