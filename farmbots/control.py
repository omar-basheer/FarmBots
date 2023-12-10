# from farmbots.comms import decode_message


# def assign_task(client_name):
#     """
#     Assigns a task to a client based on the current fruit state.

#     Parameters:
#     - client_name (str): The name of the client to assign the task.

#     Returns:
#     tuple or None: The location of the assigned fruit or None if no task is available.
#     """
#     for fruit_location, state in fruit_state.items():
#         if not state['picked'] and fruit_location not in assigned_fruits:
#             state['assigned_agent'] = client_name
#             assigned_fruits.add(fruit_location)
#             return fruit_location

# def reassign_task(client_name, fruit_location):
#     return fruit_location

# def assign_new_task(client_name):
#     pass


# def process_message(client_name, message, fruit_number):
#     """
#     Processes a message from a client, updating the fruit state and assigning tasks accordingly.

#     Parameters:
#     - client_name (str): The name of the client sending the message.
#     - message (str): The message received from the client.

#     Returns:
#     tuple or None: The location of the assigned task or None.
#     """

#      # Convert string of list back to list
#     print("processing message...")
#     message_list = decode_message(message)

#     status, task_state, client_position, fruit_location = message_list

#     if  fruit_location:
#         fruit_state[fruit_location]['picked'] = True if task_state == 'completed' else False
#         # fruit_number = fruit_number -1 if task_state == 'completed' else fruit_number
#         fruit_state[fruit_location]['assigned_agent'] = client_name 
#         if task_state == 'completed' and fruit_state[fruit_location]['picked']:
#             fruit_number -= 1
#     print("current fruit states...")
#     print_fruit_state()

#     if fruit_number == 0:
#         return None

#     if status == 'free':
#         # client is waiting for fresh task to execute
#         assigned_task = assign_task(client_name)
#         if assigned_task: 
#             print("Assigned task to " + client_name +": " + "Go to fruit at " + str(assigned_task))
#             return assigned_task
        
#     elif status == 'busy' and task_state == 'in progress':
#         # client is waiting for redirection
#         reassigned_task = reassign_task(client_name, fruit_location)
#         if reassigned_task: 
#             print("Reassigned task to " + client_name +": " + "Go to fruit at " + str(reassigned_task))
#             return reassigned_task