from math import cos, sin


def client_position(initial_position, distance, angle):
    """
    Simulate robot movement and calculate the new position.

    Parameters:
    - initial_position (tuple): Initial position (x, y)
    - distance (float): Distance traveled
    - angle (float): Angle turned (in radians)

    Returns:
    - tuple: New position (x, y)
    """
    x, y = initial_position

    # Update the position based on movement
    x += distance * cos(angle)
    y += distance * sin(angle)

    return x, y