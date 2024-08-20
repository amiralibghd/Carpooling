from tabulate import tabulate
from datetime import datetime, timedelta

students_list = []
trip_info= []
comment = {}
no_allocated = {}

today = datetime.now()
tomorrow = datetime(today.year,today.month,today.day) + timedelta(days=1)

### Functions----------------------------------------------------------

def convert_date(text):
    global today, date, tomorrow
    while True:
        if text == "":
            return tomorrow
        try:
            date_value = text.split("-")
            if datetime(int(date_value[0]),int(date_value[1]),int(date_value[2])) > today:
                date = datetime(int(date_value[0]),int(date_value[1]),int(date_value[2]))
                break
            else:
                print(text,"is not valid!!!")
                text = input("enter date: ")
        except ValueError:
            print("it is not valid!!!")
    return date


# Just for register and modify comment
def basic_convert_date(text):
    if text == "":
        return tomorrow
    text = text.split("-")
    date = datetime(int(text[0]),int(text[1]),int(text[2]))
    return date


def distance(x1,y1,x2,y2):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance


def record(new_record):
    global students_list, tommrow
    if len(new_record) == 4:
        students_list.append([int(new_record[0]),int(new_record[1]),int(new_record[2]),new_record[3],tomorrow])
    else:
        students_list.append([int(new_record[0]),int(new_record[1]),int(new_record[2]),new_record[3],convert_date(new_record[4])])

# Command 1----------------------------------------------
def register_request():
    global students_list, tomorrow
    req_type = input("How do you record request individually(i) or in groups(g)?")

    if req_type == "i":
        new_record = input("Please enter the request([id, X, Y, Type, Date]) : ")
        new_record = new_record[1:-1].split(",")
        record(new_record)

    elif req_type == "g":
        new_record = input("Please enter the requests ([[id, X, Y, Type, Date],[...],...,[...]]) : ")
        new_record = new_record[2:-2].split("],[")
        for i in range(len(new_record)):
            x = new_record[i].split(",")
            record(x)

    else:
        print("it is not correct!!!")

    students_list.sort(key=lambda x: x[4])

    table = tabulate(students_list, headers=["STU ID", "  X  ", "  Y  ", "Type", "Date"], tablefmt="pretty")
    print(table)


# Command 2-----------------------------------------------
def modify_request():
    global students_list
    if len(students_list) == 0:
        print("List of students is empty!!!")
        return
    
    student_number = int(input("Which student's request do you want to process?"))
    student_request = []
    modify_index = []

    for i in range(len(students_list)):
        if student_number == students_list[i][0]:
            student_request.append(students_list[i])
            modify_index.append(i)
        if len(student_request) == 3:
            break

    if len(student_request) == 0 :
        print("This ID is not existed!!!")
        return
    
    print("Studend's requests:")
    student_request_table = tabulate(student_request, headers=["stu id","  X  ","  Y  "," type "," date "], tablefmt="pretty")
    print(student_request_table)

    process_number = int(input("Which one do you want to process: "))
    command = int(input("Do you want to edit or remove?(modify : 1, remove : 2)"))
    if command == 1:
        print("Please edit request:")
        modify_request = input("Please enter new request: ")
        modify_request = modify_request[1:-1].split(",")
        if len(modify_request) == 3:
            students_list[modify_index[process_number-1]] = [student_number, int(modify_request[0]), int(modify_request[1]), modify_request[2], tomorrow]
        else: 
            students_list[modify_index[process_number-1]] = [student_number, int(modify_request[0]), int(modify_request[1]), modify_request[2], convert_date(modify_request[3])]
        
                
    elif command == 2:
        students_list.pop(modify_index[process_number-1])

    else:
        print("Command is not defined!!!")

    table = tabulate(students_list, headers=["STU ID", "  X  ", "  Y  ", "Type", "Date"], tablefmt="pretty")
    print(table)

    print("Back to Menu:")



# Command 3--------------------------------------------------------
def allocate_passengers():
    global students_list, trip_info, comment, no_allocated

    trip_info.clear()
    no_allocated.clear()
    comment.clear()
    allocate_list = []
    unique_date = []    
    trip_id = 0
    capacity = 4

    if len(students_list) == 0:
        print("List of students is empty!!!")
        return

    for i in range(len(students_list)):
        unique_date.append(students_list[i][4])
    unique_date = set(unique_date)
    
    for i in unique_date:
        allocate_list.append([i,[],[],[]])
        
    for i in range(len(students_list)):
        for j in range(len(allocate_list)):
            if students_list[i][4] == allocate_list[j][0]:
                if students_list[i][3] == "R":
                    allocate_list[j][1].append([students_list[i][0],students_list[i][1],students_list[i][2]])  
                elif students_list[i][3] == "P":
                    allocate_list[j][2].append([students_list[i][0],students_list[i][1],students_list[i][2]])
                else:
                    allocate_list[j][3].append([students_list[i][0],students_list[i][1],students_list[i][2]])

    allocate_list.sort(key = lambda x: x[0])

    for i in range(len(allocate_list)):
        allocate_list[i][1].sort(key = lambda x: (x[1]**2 + x[2]**2)**0.5, reverse = True)
        allocate_list[i][3].sort(key = lambda x: (x[1]**2 + x[2]**2)**0.5, reverse = True)
        while capacity * len(allocate_list[i][1]) < (len(allocate_list[i][2]) + len(allocate_list[i][3])) and len(allocate_list[i][3]) > 0:
            allocate_list[i][1].append(allocate_list[i][3].pop(0))

    for j in range(len(allocate_list)):
        while len(allocate_list[j][1]) > 0:
            capacity = 4
            trip = []
            passenger = []
            trip_id += 1
            trip.append(allocate_list[j][0])
            trip.append(trip_id)
            trip.append(allocate_list[j][1].pop(0))
            while capacity > 0 :
                if len(allocate_list[j][2]) > 0:
                    capacity -= 1
                    allocate_list[j][2].sort(key = lambda x: distance(x[1],x[2],trip[2][1],trip[2][2]))
                    passenger.append(allocate_list[j][2].pop(0)[0])
                    
                elif len(allocate_list[j][3]) > 0:
                    capacity -= 1
                    allocate_list[j][3].sort(key = lambda x: distance(x[1],x[2],trip[2][1],trip[2][2]))
                    passenger.append(allocate_list[j][3].pop(0)[0])
                    
                else:
                    break
            trip[2] = trip[2][0]
            trip.extend(passenger)
            trip_info.append(trip)  

    for i in range(len(allocate_list)):
        if len(allocate_list[i][2]) > 0:
            no_allocated.update({allocate_list[i][0]:[x[0] for x in allocate_list[i][2]]})  


    # Tables-------------------------------------------------------------------------
    formatted_list = []
    for row in trip_info:
        row.extend(["-" for _ in range(7 - len(row))]) 
        formatted_list.append(row)

    headers = ["date", "trip number", "driver id", "pass 1 id","pass 2 id","pass 3 id","pass 4 id"]
    table = tabulate(formatted_list, headers=headers, tablefmt="pretty")
    print(table)

    no_allocated_table_data = [(key, ' , '.join(map(str, values))) for key, values in no_allocated.items()]
    no_allocated_table = tabulate(no_allocated_table_data, headers=['Date', 'not allocated persons'], tablefmt='pretty', stralign='center')
    print(no_allocated_table)
    # ---------------------------------------------------------------------------------


# Command 4--------------------------------------------------------

def register_comment():
    global trip_info, comment

    if len(trip_info) == 0:
        print("No allocation has been made!!!")
        return

    student_number = int(input("Enter your student number: "))
    date = input("Please enter date of trip: ")
    date = basic_convert_date(date)
    
    trip_id = 0
    for i in trip_info:
        if student_number in i[2:] and date == i[0]:
            trip_id = i[1]
            break

    if trip_id == 0:
        print("There is no trip with this information!!!")
        return

    if trip_id not in comment:
        comment[trip_id] = []

    for i in comment[trip_id]:
        if student_number == i[0]:
            print("This student has already registered a comment for this trip!!!")
            return

    text_comment = input("How was your trip? Register your feedback: ")
    comment[trip_id].append([student_number, text_comment])


    # Table--------------------------------------------------------------------------
    table_data = []
    for key, values in comment.items():
        for value in values:
            table_data.append([key, date, value[0], value[1]])
    headers = ["Trip ID", "Date", "student ID", "comment"]
    comment_table = tabulate(table_data, headers = headers, tablefmt="pretty")
    print(comment_table)
    #---------------------------------------------------------------------------------


# Command 5--------------------------------------------------------
def modify_comment():
    global trip_info, comment

    if len(comment) == 0:
        print("There is no comment!!!")
        return

    student_number = int(input("Please enter your student number: "))
    date = input("Please enter date of trip: ")
    date = basic_convert_date(date)
    trip_id_mod = 0
    for i in trip_info:
        if student_number in i[2:] and date == i[0]:
            trip_id_mod = i[1]
            break 

    if trip_id_mod == 0:
        print("There is no trip with this information!!!")
        return

    if trip_id_mod not in comment:
        print("There is not any information for this trip!!!") 
        return
    
    for i in comment[trip_id_mod]:
        if student_number == i[0]:
            print("stu ID (", i[0],") :",i[1])
            text_comment = input("How was your trip? Register your feedback :")
            i[1] = text_comment
    # Table--------------------------------------------------------------------------
    table_data = []
    for key, values in comment.items():
        for value in values:
            table_data.append([key, date, value[0], value[1]])
    headers = ["Trip ID", "Date", "student ID", "comment"]
    comment_table = tabulate(table_data, headers = headers, tablefmt="pretty")
    print(comment_table)
    #---------------------------------------------------------------------------------


### Create a Menu------------------------------------------------------
menu_text = """
What would you like to do:
1. Register request
2. Modify request
3. Allocate passengers to drivers
4. Register user comments
5. Modify user comments
0. Exit the Menu
"""

menu_lines = menu_text.strip().split('\n')
formatted_menu = tabulate([(line,) for line in menu_lines], tablefmt="fancy_grid", headers=["Menu"])


while True:
    print(formatted_menu)
    choice = int(input("What do you choose?"))
    
    if choice == 1:
        register_request()
    elif choice == 2:
        modify_request()
    elif choice == 3:
        allocate_passengers()
    elif choice == 4:
        register_comment()
    elif choice == 5:
        modify_comment()
    elif choice == 0:
        break
