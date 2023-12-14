import random

def get_current_position():
    x = int(random.uniform(0, 4))  # Replace 0 and 100 with your desired range
    y = int(random.uniform(0, 4)  )# Replace 0 and 100 with your desired range
    theta = int(random.uniform(0, 3) ) # Replace 0 and 360 with your desired range

    return x, y, theta