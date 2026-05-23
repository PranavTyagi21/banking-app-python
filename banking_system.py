#   BANKING MANAGEMENT SYSTEM
#   MODULE 1: ACCOUNT CREATION
#WILL START WITH A FUNCTION TO SHOW WELCOME MESSAGE
from getpass import getpass

# HELPER FUNCTION TO LOG TRANSACTIONS
def add_transaction(acc_no, type_, amount, other_acc=None):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"transactions_{acc_no}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        if other_acc:
            f.write(f"{timestamp} || {type_} || ₹{amount} || Related Acc: {other_acc}\n")
        else:
            f.write(f"{timestamp} || {type_} || ₹{amount}\n")
def welcome_screen():
    print("="*50)
    print("      WELCOME TO HARI BHARI BANK      ")
    print("="*50)
    print("Developed by: Pranav Tyagi and Sachin Kumar, IT sec B")
    print("Module 1 : Account Creation and File Handling")
    print("-"*50)

#CREATING A FUNCTION TO CHECK IF ACCOUNT NUMBER IS NEW OR PRE EXISTING
def acc_exists(acc_no):
    try:
        with open("accounts.txt", "r") as f:
            for line in f:
                details = line.strip().split("||")
                if details[0] == acc_no:
                    return True
    except FileNotFoundError:
        return False
    
    return False

    #STARTING WITH FUNCTION TO CREATE A NEW ACCOUNT
def create_account():
    print("\n====== CREATE NEW ACCOUNT ======\n")
    # --- AUTO GENERATE ACCOUNT NUMBER ---
    try:
        with open("accounts.txt", "r" , encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                # Find the last valid line with an actual account number
                last_line = lines[-1]
                parts = last_line.split("||")
                last_acc_no = ''.join(ch for ch in parts[0] if ch.isdigit())
                if last_acc_no:
                    acc_no = str(int(last_acc_no) + 1)
                else:
                    acc_no = "1001"
            else:
                acc_no = "1001"
    except FileNotFoundError:
        acc_no = "1001"
    print(f"Your account number is: {acc_no}")
#account details user inpu200
    name = input("Enter your full name: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: M/F/O: ")
    nationality = input("Enter your nationality: ")
    contact_number = input("Enter your contact number: ")
    password = getpass("Set your account password (*): ")
    try:
        balance = float(input("Enter initial deposit amount (minimum:1000) : "))
        if balance < 1000:
            print("❌ Ammount is less than minimum required balance.")
            return
    except ValueError:
        print("❌ Invalid amount entered.")
        return
    with open("accounts.txt", "a", encoding="utf-8") as f:
        f.write(f"{acc_no}||{name}||{age}||{gender}||{nationality}||{contact_number}||{password}||{balance}\n")
    print("\n✅ Your account has been successfully created.")
    print(f"Your account number is: {acc_no}")

#main menu function 
def main_menu():
    while True:
        print("\n====== MAIN MENU ======")
        print("1. Create a New Account")
        print("2. Login to Existing Account")
        print("3. Exit")
        print("========================")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            user_details = login()
            if user_details:
                user_menu(user_details)
        elif choice == '3':
            print("Thank you for visiting Hari Bhari Bank. Aapka din shubh ho!, keemti samay dene ke liye dhanyawaad!")
            break
        else:
            print("😛 Please enter the choice we have mentioned, usse bahar ka nahi krenge")

def login():
    print("      Sign In To Your Account     ")
    acc_no = input("Enter your account number: ")
    password = getpass("Enter your password (hidden):")
    try:
        with open("accounts.txt" , "r") as f:
            for line in f:
                details = line.strip().split("||")
                if details[0] == acc_no and details[6] == password:
                    print(f"✅ Login successful. Welcome back, {details[1]}!")
                    return details #gives back user info
        print("Please enter correct credentials")
        return None   
    except FileNotFoundError:
        print("You have not created an account yet, Please create one now.")
        return None

def check_balance(user_details):
    balance = float(user_details[7])
    print(f"\n Your available balance is: ₹{balance}")
def deposit(user_details):
    try:
        amount = float(input("Enter amount : ₹"))
        if amount <= 0:
            print("You can only deposit positive amounts.")
            return
    except ValueError:
        print("Invalid amount entered.")
        return
    new_balance = float(user_details[7]) + amount
    user_details[7] = str(new_balance)
    #updating or sasving data in the file
    with open("accounts.txt", "r" , encoding="utf-8") as f:
        lines = f.readlines()
    with open("accounts.txt", "w") as f:
        for line in lines:
            details = line.strip().split("||")
            if details[0] == user_details[0]:
                f.write("||".join(user_details) + "\n")
            else:
                f.write(line)
    print(f"\n THANKS! YOUR AMOUNT IS SUCCESSFULLY DEPOSITED. YOUR UPDATED BALANCE IS: {new_balance}")
    add_transaction(user_details[0], "Deposit", amount)
def withdraw(user_details):
    try:
        amount = float(input("Enter withdrawl amount: ₹"))
        if amount <= 0:
            print("You can only withdraw positive amounts.")
            return
    except ValueError:
        print("Invalid Input")
        return
    current_balance = float(user_details[7])
    if current_balance - amount <1000:
        print("❌ Insufficient balance. Minimum balance of ₹1000 must be maintained.")
        return
    #updating balance now
    new_balance = current_balance - amount
    user_details[7] = str(new_balance)

    #updating files
    with open("accounts.txt", "r" , encoding="utf-8") as f:
        lines = f.readlines()

    with open("accounts.txt", "w" , encoding="utf-8") as f:
        for line in lines:
            details = line.strip().split("||")
            if details[0] == user_details[0]:
                f.write("||".join(user_details) + "\n")
            else:
                f.write(line)
    print(f"\n ✅ Please collect your cash. Your updated balance is: ₹{new_balance}")
    add_transaction(user_details[0], "Withdraw", amount)

def transfer_money(user_details):
    print("\n------ MONEY TRANSFER ------")
    receiver_acc_no = input("Enter receiver's account number: ")
    if receiver_acc_no == user_details[0]:
        print("❌ You cannot transfer money to your own account.")
        return
    amount = float(input("Enter amount to transfer: ₹"))

    if amount <= 0:
        print("❌ Invalid amount entered.")
        return
    sender_balance = float(user_details[7])
    if sender_balance - amount < 1000:
        print("Insuffient funds. Minimum balance of ₹1000 must be maintained.")
        return
    #read accounts file
    with open("accounts.txt", "r" , encoding="utf-8") as f:
        lines = f.readlines()
    sender_found = False
    receiver_found = False
    updated_lines = []

    for line in lines:
        details = line.strip().split("||")
        if details[0] == user_details[0]:
            #sender
            details[7] = str(float(details[7]) - amount)
            user_details[7] = details[7]
            sender_found = True
            updated_lines.append("||".join(details) + "\n")
        elif details[0] == receiver_acc_no:
            #receiver
            details[7] = str(float(details[7]) + amount)
            receiver_found = True
            updated_lines.append("||".join(details) + "\n")
        else:
            updated_lines.append(line)
        
    if not receiver_found:
        print("❌ Receiver account not found. Transaction Failed.")
        return
    #update accounts file
    with open("accounts.txt", "w" , encoding="utf-8") as f:
        f.writelines(updated_lines)
    # Log the transaction for both sender and receiver
    add_transaction(user_details[0], "Transfer Sent", amount, receiver_acc_no)
    add_transaction(receiver_acc_no, "Transfer Received", amount, user_details[0])
    print(f"\n✅ Successfully transferred ₹{amount} to account {receiver_acc_no}.\n Your updated balance is: ₹{user_details[7]}")



# MINI STATEMENT FUNCTION
def mini_statement(user_details):
    print("\n------ MINI STATEMENT (Last 5 Transactions) ------")
    acc_no = user_details[0]
    transactions_file = f"transactions_{acc_no}.txt"
    try:
        with open(transactions_file, "r", encoding="utf-8") as f:
            transactions = f.readlines()
            if not transactions:
                print("No transactions found.")
                return
            # Show last 5 transactions
            last_five = transactions[-5:]
            for tx in last_five:
                print(tx.strip())
    except FileNotFoundError:
        print("No transactions found for your account yet.")

#user menu daalenge so that after login user can choose what to do
def user_menu(user_details):
    while True:
        print("\n###### USER MENU ######")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Passbook")
        print("5. Transfer Money")
        print("6. Logout")
        print("7. Mini Statement")
        choice = input("Choose an option: ")

        if choice == '1':
            check_balance(user_details)
        elif choice == '2':
            deposit(user_details)
        elif choice == '3':
            withdraw(user_details)
        elif choice == '4':
            print("\n-------- YOUR PASSBOOK --------")
            print(f"Account Number: {user_details[0]}")
            print(f"Name: {user_details[1]}")
            print(f"Age: {user_details[2]}")
            print(f"Gender: {user_details[3]}")
            print(f"Nationality: {user_details[4]}")
            print(f"Contact Number: {user_details[5]}")
            print(f"Current Balance: ₹{user_details[7]}")
            print("-------------------------------")
        elif choice == '5':
            transfer_money(user_details)
        elif choice == '6':
            print("Logging out...Thanks for banking with us!!")
            break
        elif choice == '7':
            mini_statement(user_details)
        else:
            print("❌ Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    welcome_screen()
    main_menu()
    # end of the program and final