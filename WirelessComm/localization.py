import random

def get_current_position():
    x = random.uniform(0, 100)  # Replace 0 and 100 with your desired range
    y = random.uniform(0, 100)  # Replace 0 and 100 with your desired range
    theta = random.uniform(0, 360)  # Replace 0 and 360 with your desired range

    return x, y, theta