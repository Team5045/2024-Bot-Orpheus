import wpilib
from magicbot import MagicRobot
import phoenix6
from phoenix6 import hardware
from phoenix6 import controls
from components import swervedrive, swervemodule

ModuleConfig = swervemodule.ModuleConfig

#NOTE: Download and Installs for RoboRIO
# make sure imaging is up to date
'''
python -m robotpy installer download python
python -m robotpy installer install python
python -m robotpy installer download robotpy[phoenix5]
python -m robotpy installer install robotpy[phoenix5]
python -m robotpy installer download robotpy[rev]
python -m robotpy installer install robotpy[rev]

--------------- PERSONAL INSTALLS --------------------

pip install robotpy[phoenix5]
pip install robotpy[rev]
'''
# NOTE: Deployment instructions
'''
1. cd robot
2. python robot.py deploy --skip-tests (OPTION 1, with CD)
3. python robot/robot.py deploy --skip-tests (OPTION 2, without CD)
'''

# BRAKE_MODE = NeutralMode(2)
# COAST_MODE = NeutralMode(1)
class MyRobot(MagicRobot):


    def createObjects(self):

        # NetworkTables.initialize(server='roborio-5045-frc.local')
        # self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')
        self.controller = wpilib.XboxController(1)

        self.frontLeftModule_rotateMotor = phoenix6.hardware.talon_fx.TalonFX(1)
        self.frontLeftModule_rotateMotor = phoenix6.hardware.talon_fx.TalonFX(2)
        # self.frontLeftModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.frontRightModule_driveMotor = phoenix6.hardware.talon_fx.TalonFX(3)
        self.frontRightModule_rotateMotor = phoenix6.hardware.talon_fx.TalonFX(4)
        # self.frontRightModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.rearRightModule_driveMotor = phoenix6.hardware.talon_fx.TalonFX(5)
        self.rearRightModule_rotateMotor = phoenix6.hardware.talon_fx.TalonFX(6)
        # self.rearRightModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.rearLeftModule_driveMotor = phoenix6.hardware.talon_fx.TalonFX(7)
        self.rearLeftModule_rotateMotor = phoenix6.hardware.talon_fx.TalonFX(8)
        # self.rearLeftModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.frontLeftModule_encoder = phoenix6.hardware.cancoder.CANcoder(11) 
        self.frontRightModule_encoder = phoenix6.hardware.cancoder.CANcoder(12) 
        self.rearLeftModule_encoder = phoenix6.hardware.cancoder.CANcoder(14) 
        self.rearRightModule_encoder = phoenix6.hardware.cancoder.CANcoder(13)

        self.frontLeftModule_cfg = {"sd_prefix":'frontLeft_Module', "zero": 0, "inverted":True, "allow_reverse":True, "encoder":self.frontLeftModule_encoder}
        self.frontRightModule_cfg = {"sd_prefix":'frontRight_Module', "zero": 0, "inverted":False, "allow_reverse":True, "encoder":self.frontRightModule_encoder}
        self.rearLeftModule_cfg = {"sd_prefix":'rearLeft_Module', "zero": 0, "inverted":False, "allow_reverse":True, "encoder":self.rearLeftModule_encoder}
        self.rearRightModule_cfg = {"sd_prefix":'rearRight_Module', "zero": 0, "inverted":False, "allow_reverse":True, "encoder":self.rearRightModule_encoder}

        self.frontLeftModule = swervemodule.SwerveModule(self.frontLeftModule_cfg, self.frontLeftModule_rotateMotor, self.frontLeftModule_rotateMotor)
        self.frontRightModule = swervemodule.SwerveModule(self.frontRightModule_cfg, self.frontRightModule_driveMotor, self.frontRightModule_rotateMotor)
        self.rearLeftModule = swervemodule.SwerveModule(self.rearLeftModule_cfg, self.rearLeftModule_driveMotor, self.rearLeftModule_rotateMotor)
        self.rearRightModule = swervemodule.SwerveModule(self.rearRightModule_cfg, self.rearRightModule_driveMotor, self.rearRightModule_rotateMotor)

        self.drive = swervedrive.SwerveDrive(self.frontRightModule, self.frontLeftModule, self.rearRightModule, self.rearLeftModule)
        self.deg = 0

    def autonomousInit(self):
        # self.drive.flush()
        pass
    
    def teleopInit(self):
        # self.drive.flush()
        pass
    
    def move(self, y, x, rcw):
        self.drive.move(y, x, rcw)

    def teleopPeriodic(self):
        self.move(self.controller.getLeftY(), self.controller.getLeftX(), self.controller.getRightX())
        self.drive.execute()
        # if(self.controller.getAButtonReleased()):
        #     self.deg -= 90

        # self.rearRightModule.move(0, self.deg)
        # self.rearRightModule.execute()
        print(self.frontLeftModule_encoder.get_position())
        # if(self.controller.getAButton()):
        #     self.frontRightModule_rotateMotor.set_control(controls.DutyCycleOut(0.1))
        # else:
        #     self.frontRightModule_rotateMotor.set_control(controls.DutyCycleOut(0))
        # print(self.frontRightModule_encoder.get_position().value)

if __name__ == "__main__":
    wpilib.run(MyRobot)