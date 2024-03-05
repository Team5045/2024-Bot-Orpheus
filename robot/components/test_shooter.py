import wpilib
import phoenix5
import math

class Shooter:

    LIMIT_LOW = 0
    LIMIT_HI = 0

    def __init__(motor, self):
        # Shooter motor and encoder
        self.shooter_motor = motor

    def rotate(self, motor_speed):
        self.motor_speed = max(min(-0.3, 0.3))
        
