import random
from getpass import getpass

class Train:

    def __init__(self, train_no, train_name, seats):

        self.train_no = train_no
        self.train_name = train_name
        self.seats = seats

class ReservationSystem:
    def __init__(self):
       self.trains = [
            Train(101,"Rajdhani",5),
            Train(102,"Shatabdi",5),
            Train(103,"Duronto",5)
    ]
       self.tickets = {}
       self.current_user = None
       self.load_tickets() 

    def signup(self):

       username = input("Enter Username: ")
       password = getpass("Enter Password : ")

       if username == "":
            print("Username cannot be empty")
            return

       if password == "":
            print("Password cannot be empty")
            return

       try:
           with open("users.txt", "r") as file:
              for line in file:
                  
                  line = line.strip()

                  if line == "":
                      continue
                  data = line.split(",")

                  if len(data) != 2:
                      continue
                  
                  user, pwd = data
                  if user == username:
                    print("Username Already Exists")
                    return

       except FileNotFoundError:
            pass
       
       with open("users.txt", "a") as file:
           file.write(f"{username},{password}\n")

       print("Signup Successful")

    def login(self):
       username = input("Enter Username: ")
       password = input("Enter Password: ")

       try:
          with open("users.txt", "r") as file:
            for line in file:
                      line = line.strip()

                      if line == "":
                        continue
                      data = line.split(",")

                      if len(data) != 2:
                        continue
                  
                      user, pwd = data

                      if username == user:
                            if password == pwd:
                                self.current_user = username
                                print("Login Successful")
                                return True

                            else:
                                    print("Incorrect Password")
                                    return False
            print("User Not Found")
            return False
          
       except FileNotFoundError:
            print("users.tst file Not Found")
            return False   

    def show_trains(self):

        print("\nAvailable Trains\n")

        for train in self.trains:
            print(train.train_no,
                train.train_name,
                train.seats) 
    
    def book_ticket(self):
        self.show_trains()

        try:
          train_no = int(input("Enter Train Number: "))

        except ValueError:
            print("Please Enter Numbers Only")
            return
          
        name = input("Enter Passenger Name: ")

        try:
           age = int(input("Enter Passenger Age: "))
           if age < 1 or age > 120:
              print("Age must be greater than 0")
              return
           
        except ValueError:
            print("Please Enter Numbers Only")
            return
        
        found = False
        for train in self.trains:
           if train.train_no == train_no:
               found = True
               
               if train.seats > 0:
                   print("Seat Available")
                   train.seats -= 1
                   while True:
                      pnr = random.randint(100000, 999999)

                      if pnr not in self.tickets:
                          break
                    
                   self.tickets[pnr] = {
                       "username": self.current_user,
                       "name": name,
                       "age": age,
                       "train": train.train_name
                    }               
                   with open("tickets.txt", "a") as file:
                       file.write(f"{pnr},{self.current_user},{name},{age},{train.train_name}\n")

                   print("Ticket Booked Successfully")
                   print("PNR:", pnr)
               else:
                   print("No Seats Available")
               break
        if not found:
               print("Invalid Train Number") 
                   
    def view_tickets(self):
            
            found = False

            for pnr, details in self.tickets.items():

                if details["username"] == self.current_user:
                    found = True

                    print("---------------------------")
                    print("PNR :", pnr)
                    print("Name :", details["name"])
                    print("Age :", details["age"])
                    print("Train :", details["train"])

            if not found:
                print("No Tickets Found")         

    def cancel_ticket(self):
        try:
          pnr = int(input("Enter PNR Number: "))

        except ValueError:
           print("Please Enter Numbers Only")
           return
        
        if pnr in self.tickets:
           train_name = self.tickets[pnr]["train"]       
           for train in self.trains:
                    if train.train_name == train_name:
                        train.seats += 1 
                        break
           del self.tickets[pnr]

           with open("tickets.txt", "r") as file:
               lines = file.readlines()

           with open("tickets.txt", "w") as file:
               for line in lines:
                   if not line.startswith(str(pnr) + ","):
                       file.write(line)
           print("Ticket Cancelled Successfully")

        else:
           print("PNR Not Found")   

    def load_tickets(self):

        try:
          with open("tickets.txt", "r") as file:
              for line in file:
                line = line.strip() #strip kya karata hai
                if line == "":
                    continue

                data = line.strip().split(",")
                pnr = int(data[0])
                self.tickets[pnr] = {
                    "username": data[1],
                    "name": data[2],
                    "age": int(data[3]),
                    "train": data[4]
                }
                for train in self.trains:
                    if train.train_name == data[4]:
                        train.seats -= 1 
        except FileNotFoundError:
          print("No previous bookings found.")           

system = ReservationSystem() 

while True:

    print("\n===== Railway Reservation System =====")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        system.signup()

    elif choice == "2":
        if system.login():
            break

    elif choice == "3":
        exit()

    else:
        print("Invalid Choice")

while True:

    print("\n===== Booking Menu =====")
    print("1. Show Trains")
    print("2. Book Ticket")
    print("3. View Tickets")
    print("4. Cancel Ticket")
    print("5. Logout")

    choice = input("Enter Choice: ")

    if choice == "1":
        system.show_trains()

    elif choice == "2":
        system.book_ticket()

    elif choice == "3":
        system.view_tickets()

    elif choice == "4":
        system.cancel_ticket()

    elif choice == "5":
        break  

    else:
        print("Invalid Choice")


        
