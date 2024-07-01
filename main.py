from functions import book_operations, user_operations

def main():

    while True:

        option = input('''
                       
Welcome to the Library Management System with Database Integration!

  
                  
                -----------main menu------------
                            
                        1. book operations
                        2. user operations
                        3. quit
                            
                ---------select number----------
                       
''')
        

        if option == "3":
            break

        elif option == "2":
            user_operations()

        elif option == "1":
            book_operations()

main()