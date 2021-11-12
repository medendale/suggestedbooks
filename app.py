from models import (Base, session, Book, engine)
import csv
import datetime
import time

def menu():
    while True:
        print(''' 
              \nPROGRAMING BOOKS
              \r1) Add book
              \r2) View all books
              \r3) Search for book
              \r4) Book Analysis
              \r5) Exit''')
        choice = input('What would you like to do? ')
        if choice in ['1','2','3','4','5']:
            return choice
        else:
            print('''
                  \rPlease choose one of the options above
                  \rA number between 1 and 5.
                  \rPress enter to try again.
                  ''')


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 
              'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
              \n***** DATE ERROR *****
              \rThe date format should include a valid month date and year.
              \rEX: October 25, 2017
              \rPress enter to try again.
              \r**********************
              ''')
        return
    else:
        return return_date

    
def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
         input('''
              \n***** PRICE ERROR *****
              \rThe Price format should include a valid price.
              \rEX: 25.56
              \rPress enter to try again.
              \r**********************
              ''')
    else:
        return int(price_float * 100)
def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
              \n***** ID ERROR *****
              \rThe Id format should include a valid Id.
              \rPress enter to try again.
              ''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input('''
              \n***** ID ERROR *****
              \roptions: {options}.
              \rPress enter to try again.
              ''')
            return 

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()




def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            #add_book()
            title= input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date: (Ex: october 25, 2017):')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price: (Ex: 25.64):')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book was added')
            time.sleep(1.5)
        elif choice == '2':
            #View_allbooks()
            for book in session.query(Book):
                print(f'{book.id} {book.title} {book.author} {book.published_date} {book.price}')
            input('\nPress enter to return to main menu.')
        elif choice == '3':
            #Search_book()
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input('''
                    \nId Options:{id_options}
                    \rBook Id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                        id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
                  \n{the_book.title} {the_book.author} 
                  \rPublished: {the_book.published_date} 
                  \rPrice: ${the_book.price /100 }''')
            input('\nPress enter to return to main menu.')
            
        elif choice == '4':
            #Book_Analysis()
            pass
        else: 
            print('GOODBYE!')
            app_running = False
        



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    
    
    for book in session.query(Book):
        print(book)