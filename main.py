
import speedtest as sptst
import hashlib
import os
from PIL import Image
import random
from openai import OpenAI, OpenAIError
import requests.exceptions


def login_portal_sim():
    
    # User database (dictionary to store usernames and hashed passwords with salts)
    users = {
        'Games': {'hashed_password': 'af0f1fd30c8509bebddd1c61d1018fad36ca0b76df48360e0ad9a983218e105a', 'salt': '33e8da59a20f831182ac78f0e056c4d86e6ffa22006768b0dd4e9a7c1c056f0e', 'status': False, 'pre_registered': True},
        'Tools': {'hashed_password': '2a8a10f82f6e69bd396c5d01decd8d31e93b0379082ddb472de78620a19ced40', 'salt': '5b7c345ac3d809bf2e8a2596ae7396259bbf1a5781acac13fdc452345b1d600f', 'status': False, 'pre_registered': True}
        } # Some pre-registered users


    def nav_logportal():
        print("~~~~"*10)
        try:
            move_to = int(input("1) Register\n2) Login\n99) Exit\n\n-->"))
        except ValueError:
            print("-->Wrong Input")
            return nav_logportal()
        except EOFError:
            print("-->Wrong Input")
            return nav_logportal()
        
        if move_to in [1, 2, 99]:
            
            if move_to == 1:
                return register()
            elif move_to == 2:
                return login()
            elif move_to == 99:
                return "Shutting Down..."
            else:
                print(" 'la la la lala la la la lala la la la, I dare you'   - Shakira")

        else:
            print("-->Wrong Input")
            return nav_logportal()
    

    def check_requirments(usrnm= None, passwd= None): # Checks if the password meets the standards
        
        special_characters = "!@#$%^&*()_-+=<>?/[]{}|" # Set of allowed speacial characters
    
        if len(passwd) < 8:
            return False, "Password Must Be At Least 8 Characters Long."

        has_uppercase = any(c.isupper() for c in passwd)
        has_lowercase = any(c.islower() for c in passwd)
        has_digit = any(c.isdigit() for c in passwd)
        has_special = any(c in special_characters for c in passwd)

        if not (has_uppercase and has_lowercase and has_digit and has_special):
            return False, "Password Must Contain At Least One Uppercase Letter, One Lowercase Letter, One Digit, And One Special Character."

        # Check if the username is not part of the password
        if usrnm.lower() in passwd.lower():
            return False, "Password Cannot Contain The Username."

        return True


    def register():
        try:
            username = input("Enter username: ")
        except EOFError:
            print("-->Action Canceled.")
            return nav_logportal()
        
        if username in users:
            print("\nUsername already in use. Please choose a different username.")
            return register()


        print("-->Password Must Be At Least 8 Char Long, Contain: [Upper, Lower, Digit, Special Char], Must NOT Contain The Username.")
        try:
            password_r = input("Enter password: ")
        except EOFError:
            print("-->Action Canceled.")
            return nav_logportal()

        passed = check_requirments(username ,password_r)

        if passed == True:
           
                # Generate a random salt
                salt = os.urandom(32)  # 32 bytes (256 bits) salt
                
                # Hash the password with salt using SHA-256
                hashed_password = hashlib.sha256(salt + password_r.encode()).hexdigest()

        else:
            print(f"-->{passed[1]}\n")
            return register()
        
        
        # Store the username, hashed password, and salt in the database
        users[username] = {
            'hashed_password': hashed_password,
            'salt': salt.hex(),
            'status': False, # False by default
            'pre_registered': False # False for users who are registered after execution of the code
        }
        print("\n-->Registration successful. ;)")
        return nav_logportal()
    

    def login():
        try:
            username = input("Enter username: ")
            password_l = input("Enter password: ")
        except EOFError:
            print("-->Action Canceled.")
            return nav_logportal()

        # Check if the username exists in the database
        if username in users:
            stored_hashed_password = users[username]['hashed_password']
            stored_salt = users[username]['salt']            
            stored_salt_bytes = bytes.fromhex(stored_salt) # Convert hex string to bytes
            hashed_password = hashlib.sha256(stored_salt_bytes + password_l.encode()).hexdigest() # Hash the password with salt using SHA-256           
            if hashed_password == stored_hashed_password:  # Compare the hashed passwords
                print("\n-->Login Successful. :)")
                user_status = users[username]['status'] = True # It switches to True indicating the user is logged in
                pre_registered = users[username]['pre_registered']
                return user_data(username, pre_registered, user_status)
            else:
                print("\n-->Incorrect Password. :/")
                return nav_logportal()

        else:
            print("\n-->Username Not Found. :(")
            return nav_logportal()
        

    def logout(username):
        users[username]['status'] = False # It switches back to False indicating the user is logged out
        return nav_logportal()
    

    def user_data(username, pre_registered, status):
        
        def user_general():
            
            def nav_general():
                print("===="*10, end="\n\n\n")
                try:
                    move_to = int(input("1) To-Do List\n2) Notepad\n3) AI Assistant\n99) Log Out\n\n-->"))
                except ValueError:
                    print("-->Wrong Input.")
                    return nav_general()
                except EOFError:
                    print("-->Wrong Input.")
                    return nav_general()

                if move_to in [1, 2, 3, 99]:
                    
                    if move_to == 1:
                        return todo_list()
                    elif move_to == 2:
                        return notepad()
                    elif move_to == 3:
                        return ai_assistant()
                    elif move_to == 99:
                        return logout(username)
                    else:
                        print("tools are useful you know?")

                else:
                    print("-->Wrong Input")
                    return nav_general()
            

            def todo_list():
                print("Welcome To The TO-DO LIST")
                todo_items = []


                def nav_todo_list(todo_items):
                    print("===="*10, end="\n\n\n")
                    try:
                        move_to = int(input("1) Add Task\n2) Edit Task\n3) Delete Task\n4) List All Tasks\n5) Mark Task as Completed\n6) Save Tasks\n99) Exit\n\n--> "))
                    except ValueError:
                        print("-->Wrong Input")
                        return nav_todo_list(todo_items)
                    except EOFError:
                        print("-->Wrong Input")
                        return nav_todo_list(todo_items)
                    

                    if move_to in [1, 2, 3, 4, 5, 6, 99]:
                        
                        if move_to == 1:
                            return add_task(todo_items)
                        elif move_to == 2:
                            return edit_task(todo_items)
                        elif move_to == 3:
                            return delete_task(todo_items)
                        elif move_to == 4:
                            return list_tasks(todo_items)
                        elif move_to == 5:
                            return mark_completed(todo_items)
                        elif move_to == 6:
                            return save_tasks(todo_items)
                        elif move_to == 99:
                            return  nav_general()
                        else:
                            print("I really almost always have tasks to do.....")

                    else:
                        print("-->Wrong Input")
                        return nav_todo_list(todo_items)

                def add_task(todo_items):
                    try:
                        task_title = input("-->Enter the title of the task: ")
                        task_description = input("-->Enter an optional description for the task: ")
                    except EOFError:
                        print("-->Action Canceled.")
                        return nav_todo_list(todo_items)
                    if task_title:
                        todo_items.append({"title": task_title, "description": task_description, "completed": False})
                        print("Task added successfully.")
                    else:
                        print("Task title cannot be empty.")
                    return nav_todo_list(todo_items)

                def edit_task(todo_items):
                    task_index = get_task_index(todo_items)
                    if task_index is not None:
                        print(f"-->Editing Task '{todo_items[task_index]["title"]}'.")
                        while True:
                            try:
                                new_title = input("-->Enter the new title for the task: ")
                                new_description = input("-->Enter the new description for the task: ")
                                break
                            except EOFError:
                                print("-->Action Canceled.")
                                return nav_todo_list(todo_items)
                        todo_items[task_index]["title"] = new_title
                        todo_items[task_index]["description"] = new_description
                        print("Task edited successfully.")
                    return nav_todo_list(todo_items)


                def delete_task(todo_items):
                    task_index = get_task_index(todo_items)
                    if task_index is not None:
                        print(f"Task '{todo_items[task_index]["title"]}' Deleted Successfully.")
                        del todo_items[task_index]
                    return nav_todo_list(todo_items)

                def list_tasks(todo_items):
                    print("-->List Of Tasks:", end="\n\n")
                    for idx, task in enumerate(todo_items):
                        print(f"{idx + 1}) Title: {task['title']}")
                        if task["description"]:
                            print(f"   Description: {task['description']}")
                        print(f"   Completed: {'Yes' if task['completed'] else 'No'}")
                        print()
                    return nav_todo_list(todo_items)

                def mark_completed(todo_items):
                    task_index = get_task_index(todo_items)
                    if task_index is not None:
                        todo_items[task_index]["completed"] = True
                        print(f"Task '{todo_items[task_index]["title"]}' Marked As Completed.")
                    return nav_todo_list(todo_items)

                def save_tasks(todo_items):
                    with open("todo.txt", "w") as file:
                        for task in todo_items:
                            file.write(f"Title: {task['title']}\n")
                            file.write(f"Description: {task['description']}\n")
                            file.write(f"Completed: {'Yes' if task['completed'] else 'No'}\n\n")
                            file.write("===="*10 + "\n\n")  # Delimiter to separate tasks
                    print("Tasks Saved To 'todo.txt'.")
                    return nav_todo_list(todo_items)


                def get_task_index(todo_items):
                    while True:
                        try:
                            task_index = int(input("-->Enter the index of the task: ")) - 1
                            if 0 <= task_index < len(todo_items):
                                return task_index
                            else:
                                print("-->Invalid task index. No Task With Such Index")
                        except ValueError:
                            print("-->Invalid Input. Please Enter A Valid Integer Index.")
                        except EOFError:
                            print("-->Action Canceled.")
                            return None
                    
                return nav_todo_list(todo_items)
            

            def notepad():
                print("Welcome To The NOTEPAD!")
                notes = {}

                def nav_notepad(notes):
                    print("====" * 10, end="\n\n\n")
                    try:
                        move_to = int(input("1) New Note\n2) Edit Note\n3) Delete Note\n4) List All Notes\n5) Read A Note\n6) Save Notes\n99) Exit\n\n-->"))
                    except ValueError:
                        print("-->Wrong Input")
                        return nav_notepad(notes)
                    except EOFError:
                        print("-->Wrong Input")
                        return nav_notepad(notes)
                    

                    if move_to in [1, 2, 3, 4, 5, 6, 99]:
                        if move_to == 1:
                            return create_note(notes)
                        elif move_to == 2:
                            return edit_note(notes)
                        elif move_to == 3:
                            return delete_note(notes)
                        elif move_to == 4:
                            return list_notes(notes)
                        elif move_to == 5:
                            return read_note(notes)
                        elif move_to == 6:
                            return save_notes(notes)
                        elif move_to == 99:
                            return nav_general()
                        else:
                            print("I really almost never take notes.....")
                    else:
                        print("-->Wrong Input")
                        return nav_notepad(notes)

                def create_note(notes):
                    try:
                        title = input("-->Enter A Title For The Note: ").upper()
                    except EOFError:
                            print("-->Action Canceled.")
                            return nav_notepad(notes)

                    print("-->Enter The Content For Your Note (Press Enter On An Empty Line To Finish, Ctrl+D To Cancel [Ctrl+Z On Windows]): ")
                    note_content = []
                    while True:
                        try:
                            line = input("--] ")
                        except EOFError:
                            print("Note Creation Canceled.")
                            return nav_notepad(notes)

                        if not line:
                            notes[title] = '\n'.join(note_content)
                            print("Note Saved Successfully.")
                            return nav_notepad(notes)
                        note_content.append(line)

                def edit_note(notes):
                    try:
                        title = input("-->Enter The Title Of The Note: ")
                    except EOFError:
                            print("-->Action Canceled.")
                            return nav_notepad(notes)
                    if title not in notes:
                        print(f"No note with title '{title}' found.")
                        return nav_notepad(notes)

                    print(f"Editing Note '{title}'. Enter The New Content (Press Enter On An Empty Line To Finish, Ctrl+D To Cancel [Ctrl+Z On Windows]):")
                    note_content = []
                    try:
                        while True:
                            try:
                                line = input("--] ")
                            except EOFError:
                                print("-->Action Canceled.")
                                return nav_notepad(notes)
                            if not line:
                                while True:
                                    try:
                                        save = input("-->Do you want to save changes to this note? (y/n): ")
                                    except EOFError:
                                        print("-->Action Canceled.")
                                        return nav_notepad(notes)

                                    if save.lower() in ["y", "n"]: # Checks input
                                        if save.lower() == "y":
                                            notes[title] = '\n'.join(note_content)
                                            print(f"\n-->Note '{title}' Saved Changes successfully.")
                                            break
                                        elif save.lower() == "n":
                                            print("\n-->Changes Canceled.")
                                            break
                                    else:
                                        print("-->Wrong Input.\n")
                                        continue
                                return nav_notepad(notes)
                            note_content.append(line)
                    except EOFError:
                        print("-->Action canceled.")

                def delete_note(notes):
                    try:
                        title = input("-->Enter The Title Of The Note: ")
                    except EOFError:
                            print("-->Action Canceled.")
                            return nav_notepad(notes)
                    if title in notes:
                        while True:
                            try:
                                confirm = input(f"-->Are You Sure You Want To Delete The Note '{title}'? (y/n): ")
                            except EOFError:
                                print("-->Action Canceled.")
                                return nav_notepad(notes)

                            if confirm.lower() in ["y", "n"]:
                                if confirm.lower() == "y":
                                    del notes[title]
                                    print(f"-->Note '{title}' Deleted Successfully.")
                                    break
                                elif confirm.lower() == "n":
                                    print("-->Action Canceled.")
                                    break
                            else:
                                print("-->Wrong Input.\n")
                    else:
                        print(f"-->No Note With Title '{title}' Found.")
                    return nav_notepad(notes)

                def read_note(notes):
                    try:
                        title = input("-->Enter The Title Of The Note: ").upper()
                    except EOFError:
                            print("-->Action Canceled.")
                            return nav_notepad(notes)
                    if title in notes:
                        print("\n", f"--- {title} ---", "\n")
                        print(notes[title])
                        print("----"*10, "\n")
                    else:
                        print("-->Note Not Found.")
                    return nav_notepad(notes)

                def list_notes(notes):
                    print("-->List Of Notes:", end="\n\n")
                    for i, title in enumerate(notes, start=1):
                        print(f"{i}) {title}")
                    return nav_notepad(notes)

                def save_notes(notes):
                    with open("notes.txt", "w") as file:
                        for title, content in notes.items():
                            file.write(f"Title: {title}\n")
                            file.write(f"Content:\n{content}\n\n")
                            file.write("===="*10 + "\n\n")  # Delimiter to separate notes
                    print("Notes Saved To 'notes.txt'.")
                    return nav_notepad(notes)

                return nav_notepad(notes)



                


            

            def ai_assistant():
                print("===="*10, end="\n\n\n")

                try:
                    # Set up your OpenAI API key
                    openai = OpenAI(api_key='sk-pag-assistant-jzp99wmYwtzZpR7OAlZIT3BlbkFJzRnj1PPG5vZjIDzwGI3D')
                    
                    with open('Documentation.txt', 'r') as file1:
                        instructions1 = file1.read()

                    with open('main.py', 'r') as file2:
                        instructions2 = file2.read()
                    
                    instructions = instructions1 + "The project script is:" + instructions2

                    # Create an assistant
                    assistant = openai.beta.assistants.create(
                        name="Pag",
                        instructions=instructions,
                        tools=[{'type': 'code_interpreter'}],
                        model="gpt-3.5-turbo"
                    )

                    # Create a conversation thread
                    thread = openai.beta.threads.create()

                    # Main loop for conversation
                    print("Welcome to Pag-Assistant! (Use Ctrl+D To Exit [Ctrl+Z On Windows]).")
                    while True:
                        # Prompt user for input
                        try:
                            user_input = input("You: ")
                        except EOFError:
                            print("-->Exiting...")
                            break
                        
                        
                        # Create a message from the user
                        message = openai.beta.threads.messages.create(
                            thread_id=thread.id,
                            role='user',
                            content=user_input
                        )

                        # Run the assistant on the conversation thread
                        run = openai.beta.threads.runs.create(
                            thread_id=thread.id,
                            assistant_id=assistant.id
                        )

                        while run.status != "completed":
                            keep_retrieving_run = openai.beta.threads.runs.retrieve(
                                thread_id=thread.id,
                                run_id=run.id
                            )
                            print(f"Run status: {keep_retrieving_run.status}")
                        
                            if keep_retrieving_run.status == "completed":
                                print("\n")
                                break
                            elif keep_retrieving_run == "failed":
                                break

                        # Retrieve messages added by the Assistant to the thread
                        all_messages = openai.beta.threads.messages.list(
                            thread_id=thread.id
                        )

                        # Print the messages from the user and the assistant
                        print("###################################################### \n")
                        print(f"YOU: {message.content[0].text.value}")
                        print(f"PAG: {all_messages.data[0].content[0].text.value}\n")

                        
                # Handle the error gracefully, maybe retry or inform the user
                except requests.exceptions.RequestException as e:
                    print("-->An Error Occurred While Connecting To The OpenAI API:", e)
                except OpenAIError as e:
                    print("-->An Error Occurred While Connecting To The OpenAI API:", e)
                except Exception as e:
                    print("-->An Unknown Error Occurred While Connecting To The OpenAI API:", e)



                
                return nav_general()
            
            return nav_general()


        

        def user_games():
            
            def nav_games():
                print("===="*10, end="\n\n\n")
                try:
                    move_to = int(input("1) Bulls And Cows\n2) Message\n99) Log Out\n\n-->"))
                except ValueError:
                    print("-->Wrong Input")
                    return nav_games()
                except EOFError:
                    print("-->Wrong Input")
                    return nav_games()

                if move_to in [1, 2, 99]:
                    
                    if move_to == 1:
                        return bulls_and_cows()
                    elif move_to == 2:
                        print('--]"I haven\'t worked much on games since it isn\'t the focus of my project, and adding more of them won\'t add much to my project."\n--] - Issa Joudeh')
                        return nav_games()
                    elif move_to == 99:
                        return logout(username)
                    else:
                        print("I Hope These Are Fun Games.....")

                else:
                    print("-->Wrong Input")
                    return nav_games()
        
            def bulls_and_cows():

                print("_-_-"*10, "Bulls & Cows!", "RULES:\n\tThe Engine Will Pick A 4 Digit Number That Has No Dublicate Digits, For Example 1233 Is Illegal.\n\tYour Job Is To Enter Educated Guesses To Guess The Full Number In The Lowest Tries.\n\tIf You Guess A Correct Number With A Wrong Index(Digit) You Will Get A Cow\n\tIf You Guess A Right Number With The Right Index(Digit) You Will Get A Bull", sep="\n", end="\n\n\n")

                try_count = 0
                #this part picks a random 4 numbers without duplications
                num_list=[1,2,3,4,5,6,7,8,9,0]
                random.shuffle(num_list)
                num_list = [num_list[0],num_list[1],num_list[2],num_list[3]]



                def matching_numbers_check(n, x):
                    list_of_matches = []
                    n = str(n)
                    x = ''.join(str(elem) for elem in x)
                    win = "You won!"
                    for i in n:
                        if i in x:
                            if n.find(i) == x.find(i):
                                list_of_matches.append("+")
                            else:
                                list_of_matches.append("-")
                        else:
                            pass
                    if list_of_matches.count("+") == 4:
                        return win
                    else:
                        bulls = list_of_matches.count("+")
                        cows = list_of_matches.count("-")
                        return f"You Got {bulls} Bulls And {cows} Cows"


                #this part checks the num you pick matches the requirments
                while True:

                    try:
                        num_try = input("Enter A Guess: ")
                        num_try_str = num_try
                        num_try = int(num_try)
                    except ValueError:
                        print("-->Use Only Integers.")
                        continue
                    except EOFError:
                        print("-->Exiting...")
                        return nav_games()
                    
                    if len(num_try_str)!= 4:
                        print("-->Lenth is 4.")
                        continue
                    elif len(set(num_try_str)) != len(num_try_str):
                        print("-->No Dubs.")
                        continue
                    else:
                        
                        try_count += 1
                        if matching_numbers_check(num_try, num_list) == "You won!":
                            print("\n\n-->You won!" + f" The number is {num_try}")
                            print(f"-->it took you {try_count} tries!", end="\n\n\n")
                            return nav_games()
                            
                        else:
                            print(matching_numbers_check(num_try, num_list))

            print(nav_games())
            
		

        def user_tools():

            def nav_tools():
                print("===="*10, end="\n\n\n")
                try:
                    move_to = int(input("1) Internet Speed Test\n2) Steganography Tools\n3) Password Hashing And Salting Tool\n99) Log Out\n\n-->"))
                except ValueError:
                    print("-->Wrong Input")
                    return nav_tools()
                except EOFError:
                    print("-->Wrong Input")
                    return nav_tools()

                if move_to in [1, 2, 3, 99]:
                    
                    if move_to == 1:
                        return internet_speed_test()
                    elif move_to == 2:
                        return steganography_tools()
                    elif move_to == 3:
                        return password_hashing_salting()
                    elif move_to == 99:
                        return logout(username)
                    else:
                        print("tools are useful you know?")

                else:
                    print("-->Wrong Input")
                    return nav_tools()
                
            
            def internet_speed_test():

                def run_speed_test():
                    try:
                        # Create Speedtest object
                        st = sptst.Speedtest()
                        
                        # Get best server
                        st.get_best_server()

                        # Perform download speed test
                        download_speed = st.download() / 1024 / 1024  # Convert from bits to megabits

                        # Perform upload speed test
                        upload_speed = st.upload() / 1024 / 1024  # Convert from bits to megabits
                        
                        # Get network name (ISP)
                        network_name = st.results.client['isp']

                        # Get server details
                        server_name = st.results.server['name']

                        # Return results
                        return download_speed, upload_speed, network_name, server_name

                    except sptst.SpeedtestException as e:
                        print(f"An error occurred during the speed test: {e}")
                        return None, None, None, None

                
                print("\nSpeed Test Is Running...\n")
                results = run_speed_test()
                
                if results[0] is not None and results[1] is not None: # Check if the test was successful
                    print(f"Download Speed: {results[0]:.2f} Mbps", f"Upload Speed: {results[1]:.2f} Mbps", f"Network Name (ISP): {results[2]}", f"Server Used: {results[3]}", sep="\n", end="\n\n\n\n")
                else:
                    print("Speed test failed. Please check your internet connection.", end="\n\n\n\n")

                return nav_tools()


            def steganography_tools():

                def stega_nav():
                    print("~~~~"*10, "This Is A Steganography Tool", sep="\n", end="\n\n\n")
                    try:
                        move_to = int(input("1) Encode\n2) Decode\n99) Exit\n\n-->"))
                    except ValueError:
                        print("-->Wrong Input")
                        return stega_nav()
                    except EOFError:
                        print("-->Wrong Input")
                        return stega_nav()

                    if move_to in [1, 2, 99]:
                        
                        if move_to == 1:
                            return encode_image()
                        elif move_to == 2:
                            return decode_image()
                        elif move_to == 99:
                            return nav_tools()
                        else:
                            print("okay i kinda overused this joke.....")

                    else:
                        print("-->Wrong Input")
                        return stega_nav()


                def text_to_bin(text):
                    #Convert text to binary
                    return "".join(format(ord(char), "08b") for char in text)


                def bin_to_text(binary):
                    #Convert binary to text
                    bytes_list = [binary[i:i+8] for i in range(0, len(binary), 8)]
                    characters = []
                    for byte in bytes_list:
                        characters.append(chr(int(byte, 2)))
                    message = ''.join(characters)
                    print(f"The Secret Message is: {message}.", "\n\n\n")
                    return stega_nav()


                def encode_image():
                    #Encode a message into an image
                    try:
                        image_path = input("Original Image Path: ")
                    except EOFError:
                        print("-->Action Canceled")
                        return stega_nav()
                    try:
                        img = Image.open(image_path)
                    except OSError:
                        print('Error: Re-Check The Entered Path (Make Sure To Not Use "" When You Enter The Path)', end="\n\n")
                        return encode_image()
                    
                    try:
                        message = input("Message: ")
                    except EOFError:
                        print("-->Action Canceled")
                        return stega_nav()
                    binary = text_to_bin(message) + "1111111111111110"  # Delimiter to indicate end of message
                    img = img.convert("RGBA")
                    datas = img.getdata()
                    
                    newData = []
                    digit = 0
                    for item in datas:
                        if digit < len(binary):
                            newpix = item[0], item[1], item[2], 128 + int(binary[digit])
                            digit += 1
                        else:
                            newpix = item
                        newData.append(newpix)
                    
                    while True:
                        try:
                            output_path = input("Encoded Image Path (IT WILL SAVE IN 'PNG' FORMAT): ")
                            img.putdata(newData)
                            img.save(output_path + ".png", format = "PNG")
                        except FileNotFoundError:
                            print('FileNotFoundError: Re-Check The Entered Path (Make Sure To Not Use "" When You Enter The Path)', end="\n\n")
                            continue
                        except EOFError:
                            print("-->Wrong Input")
                            continue
                        break
                    
                    print("Message Encoded Successfully.", "\n\n")
                    return stega_nav()
                

                def decode_image():
                    #Decode a message from an image.
                    try:
                        image_path = input("Encoded Image Path: ")
                        img = Image.open(image_path)
                    except OSError:
                        print('Error: Re-Check The Entered Path (Make Sure To Not Use "" When You Enter The Path)', end="\n\n")
                        return decode_image()
                    except EOFError:
                        print("-->Action Canceled")
                        return stega_nav()
                    
                    img = img.convert("RGBA")
                    datas = img.getdata()
                    
                    binary = ''
                    for item in datas:
                        alpha = item[3]
                        if alpha == 128 or alpha == 129:  # Only two valid alpha values
                            binary += str(alpha % 2)
                        elif binary:  # Stop reading when alpha values are no longer valid
                            break
                    
                    # Find the delimiter
                    delimiter = binary.find("1111111111111110")
                    if delimiter != -1:
                        binary = binary[:delimiter]

                    try:
                        return bin_to_text(binary)
                    except Exception as e:
                        print(f"Error during decoding: {e}")
                        return "Decoding Failed."
                
                return stega_nav()




            def password_hashing_salting():

                def hash_password(password, salt=None):
            
                    if salt is None:
                    # Generate a random salt
                        salt = os.urandom(32)  # 32 bytes (256 bits) salt
                    else:
                        try:
                            salt = bytes.fromhex(salt)  # Convert hex string to bytes
                        except ValueError:
                            return False    # If it fails to covert it it returns False

                    # Hash the password with salt using SHA-256
                    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

                    # Return the hashed password and salt for output
                    return hashed_password, salt.hex()
                
                def want_salt():
                    try:
                        salt = input("Wanna Use A Random Salt (Recomended) [y/n]: ")
                    except EOFError:
                        print("-->Action Cnaceled")
                        return nav_tools()
                
                    if salt in ["y", "Y", "n", "N"]: # Checks input
                    
                        if salt in ["y", "Y"]: # Hashes with a random salt 
                            result = hash_password(password) 
                            print("" ,f"Your Password: {password}", f"Your Hashed Password: {result[0]}", f"Your Salt: {result[1]}", sep="\n", end="\n")
                            print("\n\n")
                            return nav_tools()
                        elif salt in ["n", "N"]: # Hashes with a custom salt
                            salt = input("Enter A Hex String For The Salt: ")
                            result = hash_password(password, salt)
                            
                            if result != False:
                                print("", f"Your Password: {password}", f"Your Hashed Password: {result[0]}", f"Your Salt: {result[1]}", sep="\n", end="\n")
                                return nav_tools()
                            else:
                                print("-->Wrong Input")
                                return want_salt() 
                        else:
                            print("Hello Instructor! or anyone else reading this really...")
                                
                    else:
                        print("-->Wrong Input")
                        return want_salt()
                
                
                print("\n\n***THIS SCRIPT HASHES USING SHA256 AND SALTS WITH A 32 BYTE (256 BITS) SALT***\n", end="\n")
                try:
                    password = input("The Password To Be Hashed: ")
                except EOFError:
                            print("-->Action Canceled.")
                            return nav_tools()

                print(want_salt())

            return nav_tools()
        






        if pre_registered is True:
            username_formatted = username.replace(" ", "_").lower() # Replace spaces with underscores and lowercase the username
            call_user_function = f"user_{username_formatted}()" # Construct the function name that is needed as a string
            print("", f"Logged In As: {username}", sep="\n")
            return eval(call_user_function) # Use [eval] to execute the string
        elif pre_registered is False:
            print("", f"Logged In As: {username}", sep="\n")
            return user_general()



    
    print("~~~~"*10)
    print("\n   ***WELCOME TO THE LOGIN PORTAL***\n")
    return nav_logportal()
    




print(login_portal_sim())
