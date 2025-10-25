import csv
import os



class Color:
    RED = '\033[91m'
    RESET = '\033[0m'


class Pizza:
    def __init__(self, id_file_path, menu_file_path, order_history_file_path, current_order_file_path, order_id_file_path, current_order_id_path):
        self.id_file_path = id_file_path
        self.menu_file_path_csv = menu_file_path
        self.order_history_file_path = order_history_file_path
        self.current_order_file_path = current_order_file_path
        self.order_id_file_path = order_id_file_path
        self.current_order_id_path = current_order_id_path

    def assign_new_id(self):
        #change ths fucntion so that it only opens the file once.
        with open(self.id_file_path, 'r')as id_read:
            content = int(id_read.read().strip())
            new_id = content + 1
        with open(self.id_file_path, 'w') as id_write:
            id_write.write(str(new_id))
        pizza_console.add_menu_item(new_id)


    def add_menu_item(self, new_id):
        print("==== Add Menu Item ====")
        name = input("Enter item name: ")
        desc = input("Enter item description: ")
        while True:
            try:
                price = float(input("Enter Price: "))
            except ValueError:
                print("Invalid Answer, Must be a Number.")
            if price == float(price):
                break
        category = input("Enter Category: ")
        menu = {'Id': str(new_id),
                'Name': name, 
                'Desc': desc, 
                'Price': str(price), 
                'Cat': category}
                
        file_exists = os.path.isfile(self.menu_file_path_csv)

        with open(self.menu_file_path_csv,'a', newline='') as menu_file:
            fieldnames = ['Id','Name','Desc','Price','Cat']
            writer = csv.DictWriter(menu_file, fieldnames= fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(menu)
        print(f"Item Added Succesfully")
        go_back = input("Press ENTER to go back to main menu ")


    def read_menu(self):
        with open(self.menu_file_path_csv, 'r', newline='') as csvfile:
            csvfile_reader = csv.DictReader(csvfile)
            for row in csvfile_reader:
                print(row)
        go_back = input("Press ENTER to go back to main menu")

    def change_menu_item(self, row_id, menu_changes):
        rows_to_keep = []
        found_item= False
        with open(self.menu_file_path_csv, 'r', newline='') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                if int(row['Id'].strip()) == row_id.strip():
                    rows_to_keep.append(menu_changes)
                    found_item = True
                else:
                    rows_to_keep.append(row)

        if found_item:
            with open(self.menu_file_path_csv, 'w', newline='') as outfile:
                fieldnames = ['Id', 'Name', 'Desc', 'Price', 'Cat']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows_to_keep)
            print(f"Menu item with ID {row_id} has been updated.")
        else:
            print(f"Item with ID {row_id} not found.")


    def start_order(self):
        with open(self.order_id_file_path, 'r')as id_read:
            content = int(id_read.read().strip())
            self.current_order_id = content + 1
        with open(self.order_id_file_path, 'w') as id_write:
            id_write.write(str(self.current_order_id))
        with open(current_order_id_path, 'w') as current_id_file:
            current_id_file.write(str(self.current_order_id))

        print(f"Starting new order with ID: {self.current_order_id}")
        with open(self.current_order_file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Order_id', 'Id', 'Name', 'Desc', 'Price', 'Cat'])
            writer.writeheader()


    def add_item_order(self, row_id):
        item_to_keep = []
        with open(self.menu_file_path_csv, 'r',newline='') as menu_read:
            reader = csv.DictReader(menu_read) 
            for row in reader:
                if row['Id'].strip() == str(row_id).strip():
                    item_to_keep = row
                    found_item = True
                    break
        if found_item:
            item_to_keep['Order_id'] = self.current_order_id
            with open(self.current_order_file_path,'a', newline='') as current_order_write:
                fieldnames = ['Order_id','Id', 'Name', 'Desc', 'Price', 'Cat']
                writer = csv.DictWriter(current_order_write, fieldnames=fieldnames)
                writer.writerow(item_to_keep)
    def finish_order(self): 
        with open(self.current_order_file_path,'r', newline='') as current_order_file:
            
            current_order_read = list(csv.DictReader(current_order_file))
        order_price = 0.0
        for line in current_order_read:
            order_price += float(line["Price"])

        with open(self.order_history_file_path, 'a', newline='') as order_history_file:
            fieldnames = ['Order_id','Id', 'Name', 'Desc', 'Price', 'Cat']
            order_history_write = csv.DictWriter(order_history_file, fieldnames=fieldnames)
            is_empty = order_history_file.tell() == 0
            if is_empty:
                order_history_write.writeheader()
            order_history_write.writerows(current_order_read)
    
        
        print(f"Order {self.current_order_id} has been finished and saved to history.")
        print(f"The total price is {order_price}.")
        with open(self.current_order_file_path, 'w', newline='') as current_order_file:
            pass    
        go_back = input("Press ENTER to go back to the main menu.")
    def total_sales(self):
        with open(self.order_history_file_path, 'r', newline='') as order_history_f:
            order_history_read = csv.DictReader(order_history_f)
            total_price = 0.0
            for line in order_history_read:
                total_price += float(line["Price"])
        print(f"The total price is {total_price}")
        go_back = input("Press ENTER to go back to the main menu")
    
    def order_history(self):
        with open(self.order_history_file_path, 'r', newline='') as order_history_f:
            order_history_r = csv.DictReader(order_history_f)
            for row in order_history_r:
                print(row)
        go_back = input("Press ENTER to go back to the main menu.")
    def current_order(self):
        with open(self.current_order_file_path, 'r', newline='') as order_history_f:
            order_history_r = csv.DictReader(order_history_f)
            for row in order_history_r:
                print(row)
        go_back = input("Press ENTER to go to main menu")


                

id_file_path = "C:/code/python_work/mini_projects/pizza_ordering_console/menu_id.txt"
menu_file_path = "C:/code/python_work/mini_projects/pizza_ordering_console/pizza_menu.csv"
order_history_file_path = "C:/code/python_work/mini_projects/pizza_ordering_console/order_history.csv"
current_order_file_path = "C:/code/python_work/mini_projects/pizza_ordering_console/current_order.csv"
order_id_file_path = "C:/code/python_work/mini_projects/pizza_ordering_console/order_id.txt"
current_order_id_path = "C:/code/python_work/mini_projects/pizza_ordering_console/current_order_id.txt"

pizza_console = Pizza(id_file_path, menu_file_path, order_history_file_path, current_order_file_path,order_id_file_path, current_order_file_path)

while True:

    try:
        print(
    f"{Color.RED}==== PIZZA === SHOP ===={Color.RESET}" \
    "\n1. Add Menu Item" \
    "\n2. Change Menu Item" \
    "\n3. Read Menu" \
    "\n4. Start Order" \
    "\n5. Complete Order"   \
    "\n6. Add to Order" \
    "\n7. Show Order History" \
    "\n8. Show Current Order" \
    "\n9. Show Total Sales" \
    "\n10. Exit"
    "\n========================"
    )
        user_input = int(input("\nPlease Select an Action: "))
    except ValueError:
        print("Invalid Answer, Use a Valid Integer")
    else:
        if user_input == 1:
            pizza_console.assign_new_id()
        elif user_input == 2:
            row_id = str(input("What is the ID of the item you want to change? "))
            name = input("Enter item name: ")
            desc = input("Enter item description: ")
            while True:
                try:
                    price = float(input("Enter Price: "))
                except ValueError:
                    print("Invalid Answer, Must be a Number.")
                if price == float(price):
                    break
            category = input("Enter Category: ")
            menu_changes = {'Id': row_id,
                'Name': name, 
                'Desc': desc, 
                'Price': str(price), 
                'Cat': category}
            pizza_console.change_menu_item(row_id, menu_changes)
        elif user_input == 3:
            pizza_console.read_menu()        
        elif user_input == 4:
            pizza_console.start_order()
        elif user_input == 5:
            pizza_console.finish_order()
        elif user_input == 6:
            row_id = int(input("What is the ID of the item you want to add to the order? "))
            pizza_console.add_item_order(row_id)
        elif user_input == 7:
            pizza_console.order_history()
        elif user_input == 8:
            pizza_console.current_order()
        elif user_input == 9:
            pizza_console.total_sales()
        elif user_input == 10:
            print("Stopping Program...")
            print("Program Closed")
            exit()
