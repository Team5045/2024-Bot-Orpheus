import math
import wpilib
import phoenix6
from phoenix6 import controls
from wpimath.controller import PIDController
from collections import namedtuple

ModuleConfig = namedtuple('ModuleConfig', ['sd_prefix', 'zero', 'inverted', 'allow_reverse'])


class SwerveModule:

    def __init__(self, config, drive, rotate):

        self.driveMotor = drive
        self.rotateMotor = rotate

        self.cfg = config

        self.encoder = self.cfg["encoder"]

        self.encoder_zero = self.cfg["zero"]

        self.inverted = self.cfg["inverted"]
        self.allow_reverse = self.cfg["allow_reverse"]

        # self.driveMotor.setInverted(self.inverted)

        self.requested_speed = 0

        self.pid_controller = PIDController(0.25, 0.0, 0.0)
        # I TUNE DAMPER -- SUB 0.00035 TEMP VALUE FOR 2/12/24
        self.pid_controller.enableContinuousInput(0, 1)
        self.pid_controller.setTolerance(0.005, 0.2)
        
    def get_encoder_rotations(self):
        return self.encoder.get_position().value

    def flush(self): 
        self.pid_controller.setSetpoint(self.encoder_zero) #self.encoder.getSelectedSensorPosition()
        self.requested_speed = 0
        self.pid_controller.reset()
    
    @staticmethod
    def rotations_to_degrees(rotations):
        isNegative = rotations < 0
        deg = rotations % 1
        if isNegative:
            deg *= -1
        deg *= 360
        return deg
 
    @staticmethod                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def degree_to_rotations(degree):
        return (degree / 360)
    
    def set_deg(self, value):
        self.pid_controller.setSetpoint((self.degree_to_rotations(value) + self.encoder_zero) % 1)
        # print((self.degree_to_rotations(value) + self.encoder_zero) % ENCODER_SIZE)

    def move(self, speed, deg):

        if self.allow_reverse:

            if abs(deg - self.rotations_to_degrees(self.get_encoder_rotations())) > 90:
                speed *= -1
                deg += 180
                deg %= 360
            
        self.requested_speed = speed        
        # print(f"{deg=}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        self.set_deg(deg)
        
    def execute(self):
        self.error = self.pid_controller.calculate(self.encoder.get_position().value, self.pid_controller.getSetpoint()) 
        output = 0

        if self.pid_controller.atSetpoint():
            output = 0
        elif not self.pid_controller.atSetpoint():
            output = max(min(self.error, 1), -1)
        
        self.motor_request = controls.DutyCycleOut(1)
        self.motor_request.output = output

        # print(output)
        self.rotateMotor.set_control(self.motor_request)
        self.driveMotor.set_control(controls.DutyCycleOut(max(min(self.requested_speed, 0.6), -0.6)))
        # ORIGINAL VALUE AT 0.5 SUBJECT TO CHANGE
            

        
        