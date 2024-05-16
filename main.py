from main1 import AirplaneTicketReservation
import sqlite3

#object creation
ar=AirplaneTicketReservation()
ar.create_tables()

#default administrators and their passwords --- sample
user_database = {
    "Dharani": "1234567890",
    "Priya": "Priya1234",
    "Kothuri": "Kothuri1234"
}

#Operations performed by the administrator
def operations():
    while True:
        print("-----------------------------------------------")
        print("\nChoose from below:")
        print("1.Add a Flight\n2.Add details of seats\n3.Exit\n")
        dp=int(input("Enter your choice: "))
        if dp==1:
            dept_city=input("\nEnter Departure place: ")
            dept_date=input("Enter Departure date(YYYY-MM-DD): ")
            dept_time=input("Enter Departure time(HH:MM:SS): ")
            dept_time=dept_date+" "+dept_time
            arr_city=input("Enter Arrival place: ")
            arr_date=input("Enter Arrival date(YYYY-MM-DD): ")
            arr_time=input("Enter Arrival time(HH:MM:SS): ")
            arr_time=arr_date+" "+arr_time
            aircraft_type=input("Enter type of aircraft(Boeing, Airbus, Bombardier): ")
            ar.add_flight(dept_city,dept_time,arr_city,arr_time,aircraft_type)
            print("\nInserted successfully!\n")
        elif dp==2:
            flight_id=input("\nEnter flight id: ")
            seat_num=input("Enter seat id: ")
            class1=input("Enter class name(Economy, Business, First Class): ")
            ar.add_seats(flight_id,seat_num,class1)
        else:
            break

def administrator_operations(userID,password):
    if userID in user_database:
        if password == user_database[userID]:
            print("\nYou are logged in successfully. Perform respective operations.")
            operations()
        else:
            print("\nIncorrect password. Please try again.")
            return False
    else:
        print("\nNo user with that ID.")
        # return False
    return True
    

#Operations performed by the user
def existing_user_operations():
    while True:
        print("-----------------------------------------------")
        print("Choose from below:")
        print("\n1.Search for a flight\n2.Book ticket\n3.Cancel ticket\n4.Exit\n")
        dp=int(input("Enter your choice: "))
        if dp==1:
            print("\nEnter the respective details:")
            a=input("Departure place: ")
            b=input("Arrival place: ")
            c=input("Depature Date(YYYY-MM-DD): ")
            req=ar.find_flights(c,a,b)
            ar.flight_details(req)
        elif dp==2:
            a=input("Enter your Customer ID: ")
            b=input("Enter Flight ID(only from the available flights): ")
            d=input("Enter your departure date(YYYY-MM-DD): ")
            e=input("Enter class type(Economy, Business, First Class): ")
            ar.book_ticket(a,b,d,e)
        elif dp==3:
            a=input("\nEnter your Customer ID: ")
            b=input("Enter Flight ID(only from the available flights): ")
            c=input("Enter your seat ID: ")
            ar.cancel_ticket(a,b,c)
        elif dp==4:
            break
    
def User_Login(email,password):
    if ar.user_check(email,password):
        print("\nLogin Successful!")
        return True
    else:
        print("\nNo user found, please register!")
        return False

#start
if __name__ == '__main__':
    while True:
        print("-----------------------------------------------")
        print("\nwho you are:")
        print("1.Administrator\n2.Guest User\n3.Exit\n")
        choice=int(input("Enter your choice: "))
        if choice==1:
            userID=input("\nEnter your user id: ")
            password=input("Enter your password: ")
            administrator_operations(userID,password)
        elif choice==2:
            # ar.create_tables()
            while True:
                print("-----------------------------------------------")
                print("\nChoose from below:")
                print("\n1.Search for a flight\n2.Login\n3.Register\n4.Exit\n")
                dp=int(input("Enter your choice: "))
                if dp==1:
                    print("\nEnter the respective details:")
                    a=input("Departure place: ")
                    b=input("Arrival place: ")
                    c=input("Depature Date (YYYY-MM-DD): ")
                    req=ar.find_flights(c,a,b)
                    ar.flight_details(req)
                if dp==2:
                    print("\nLogin:")
                    a=input("Enter your email: ")
                    b=input("Enter password to login:")
                    if User_Login(a,b):
                        existing_user_operations()
                if dp==3:
                    print("\nRegister:")
                    name=input("Enter your name: ")
                    email=input("Enter your mail id: ")
                    password=input("Enter password: ")
                    phoneno=input("Enter your phone number: ")
                    address=input("Enter your address: ")
                    if ar.add_customer(name,email,password,phoneno,address):
                        print("\nLogin:")
                        a=input("Enter your email: ")
                        b=input("Enter password to login:")
                        if User_Login(a,b):
                            existing_user_operations()
                    else:
                        existing_user_operations()
                elif dp==4:
                    break
        elif choice==3:
            break
                
                
                
                
                
                
                
                
                
                
                