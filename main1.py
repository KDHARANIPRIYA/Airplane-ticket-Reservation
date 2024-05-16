import sqlite3
import threading
from datetime import datetime
import hashlib
class AirplaneTicketReservation:
    def __init__(self):
        self.conn=sqlite3.connect('database.db')
        self.cur=self.conn.cursor()
        # self.lock=threading.Lock()
        self.conn=sqlite3.connect('database.db')
        self.cur=self.conn.cursor()

    def create_tables(self):
        self.cur.execute("create table if not exists customer (customer_id integer primary key autoincrement, name varchar(100) not null, email varchar(100) not null, password varchar(100) not null, phoneno varchar(20), address varchar(255))");
        self.cur.execute("create table if not exists flights (flight_id integer primary key autoincrement, departure_city varchar(100) not null, arrival_city varchar(100) not null, departure_time datetime not null, arrival_time datetime not null, aircraft_type varchar(100) not null)");
        self.cur.execute("create table if not exists seats (seat_id int not null, flight_id int not null, class varchar(20) not null, availability tinyint(1) not null default 1, foreign key (flight_id) references flights(flight_id),primary key(seat_id,flight_id))");
        self.cur.execute("create table if not exists reservations (reservation_id integer primary key autoincrement, customer_id int not null, flight_id int not null, seat_id int not null, reservation_date datetime not null, status varchar(20) not null, class_type varchar(100) not null, ticket_price int not null,foreign key (customer_id) references customer(customer_id), foreign key (flight_id) references flights(flight_id), foreign key (seat_id) references seats(seat_id))");
    
    #for new user registration
    def add_customer(self, name, email, password, phoneno, address):
        # passwd=hashlib.sha256(password.encode()).hexdigest()
        # print(passwd)
        i=0
        self.cur.execute("select * from customer where email=? and phoneno=?",(email,phoneno))
        c=self.cur.fetchone()
        if c:
            print("User already exists!")
            return False
        self.cur.execute("insert into customer (name,email,password,phoneno,address) values (?,?,?,?,?)",(name,email,password,phoneno,address))
        a=list(self.cur.execute("select * from customer"))
        print("\nYour Customer ID: ",a[i][0])
        i+=1
        print("Registration successful!, User can login now.")
        return True
    
    def add_flight(self,departure_city,departure_time,arrival_city,arrival_time,aircraft_type):
        self.cur.execute("insert into flights (arrival_city,departure_city,arrival_time,departure_time,aircraft_type) values (?,?,?,?,?)",(arrival_city,departure_city,arrival_time,departure_time,aircraft_type))

    def add_seats(self,flight_id,seat_num,class1):
        for seat in seat_num:
            self.cur.execute("select * from seats where flight_id=? and seat_id=?",(flight_id,seat))
            existing_seat=self.cur.fetchone()
            if existing_seat:
                print(f"\nseat {seat} already exists for flight {flight_id}!")
            else:
                self.cur.execute("insert into seats (flight_id,seat_id,class,availability) values (?,?,?,?)",(flight_id,seat_num,class1,1))
                print("\nInserted successfully!\n")

    def find_flights(self,departure_date,departure_city,arrival_city):
        self.cur.execute("select * from flights where departure_city=? and DATE(departure_time)=? and arrival_city=?",(departure_city,departure_date,arrival_city))
        required=self.cur.fetchall()
        # print(required)
        return required
    
    def flight_details(self,flights):
        print("Flight details: \n")
        if not flights:
            print("Sorry, no flights available!")
        else:
            for f in flights:
                print("Flight ID: ",f[0])
                print("Departure city: ",f[1])
                print("Arrival city: ",f[2])
                print("Dept time: ",f[3])
                print("Arrival time: ",f[4])
                print("Aircraft type: ",f[5])
                print("\nRequesting to note down the Filght ID!")
                print("\n")

    def user_check(self,email,password):
        self.cur.execute("select * from customer where email=?",(email,))
        c=self.cur.fetchone()
        if c:
            passwd=c[3]
            if passwd==password:
                return True
            else:
                print("Wrong password! Login again ")
                return
        else:
            return False
        
    def calculate_amount(self,class_type):
        sum=0
        if class_type=="Economy":
            sum=10000
        elif class_type=="Business":
            sum=20000
        elif class_type=="First Class":
            sum=50000
        else:
            print("\nInvalid class type. Please select Economy, Business, or First Class\n")
            return None
        return sum

    def book_ticket(self,customer_id,flight_id,reservation_date,class_type):
        self.cur.execute("select flight_id from seats where flight_id=?",(flight_id,))
        req=self.cur.fetchall()
        self.cur.execute("select DATE(departure_time) from flights where DATE(departure_time)=?",(reservation_date,))
        req1=self.cur.fetchall()
        # self.cur.execute("select ")
        if req and req1:
            self.cur.execute("select seat_id from seats where flight_id=? and class=? and availability=?",(flight_id,class_type,1))
            seat_availability=self.cur.fetchall()
            lst=[]
            if seat_availability:
                print("Available seats for class",class_type,"on Flight",flight_id,": ")
                for s in seat_availability:
                    lst.append(s[0])
                    print("Seat ID:",s[0])
                # print(lst)
                choice=int(input("\nEnter the seat ID you want to book: "))
                if choice in lst:
                    self.cur.execute("update seats set availability=? where seat_id=?",(0,choice))
                    ar1=AirplaneTicketReservation()
                    ticket_price=ar1.calculate_amount(class_type)
                    if ticket_price is not None:
                        self.cur.execute("insert into reservations (customer_id,flight_id,seat_id,reservation_date,status,class_type,ticket_price) values (?,?,?,?,?,?,?)",(customer_id,flight_id,choice,reservation_date,"Reserved",class_type,ticket_price))
                    
                        print("\nYour ticket is booked successfully!\nAmount: $",ticket_price)
                
                        (self.cur.execute("select * from reservations where customer_id=? and seat_id=?",(customer_id,choice)))
                        req=self.cur.fetchone()
                        print("\nyour booking details:")
                        print("Reservation ID: ",req[0])
                        print("Customer ID: ",req[1])
                        print("Flight ID: ",req[2])
                        print("Seat ID: ",req[3])
                        print("Reservation Date: ",req[4])
                        print("Class : ",req[6])
                        print("Ticket price: $",req[7])
                else:
                    print("\nInvalid Seat ID, pelase choose an available seat\n")
                
            # flag=False
            else:
                print(f"\nNo available seats found for {class_type} class\n")
        else:
            print("\nSorry, No flights found!\n")
        
    #for cancelling a ticket
    def cancel_ticket(self,customer_id,flight_id,seat_id):
        self.cur.execute("select * from reservations where customer_id=? and flight_id=? and seat_id=?",(customer_id,flight_id,seat_id))
        reservations=self.cur.fetchall()
        if reservations:
            print("\nDetails of your reservation: ")
            for i,j in enumerate(reservations):
                # print("---->reservations ",list(j))
                print(f"Reservation ID: {j[0]}, Date: {j[4]}, Status: {j[5]}")
                
            # asking the user which is to be Cancelled
            choice=int(input("Enter your Reservation ID which has to be cancelled: "))
            for reservation in reservations:
                if reservation[0] == choice:
                    if reservation[5] == "Cancelled":
                        print("\nAlready cancelled ticket.\n")
                    else:
                        self.cur.execute("update reservations set status=? where customer_id=? and flight_id=? and seat_id=? and reservation_id=?",("Cancelled",customer_id,flight_id,seat_id,choice))
                        self.cur.execute("update seats set availability = ? where seat_id=?",(1,seat_id))
    
                        print("\nYour request for cancellation is successful!\n")  
        else:
            print("\nNo reservation found for the provided details!\n")




        