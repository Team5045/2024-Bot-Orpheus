import wpilib
import phoenix5
from magicbot import MagicRobot
from phoenix5 import NeutralMode

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

BRAKE_MODE = NeutralMode(2)
COAST_MODE = NeutralMode(1)
class MyRobot(MagicRobot):


    def createObjects(self):

        # NetworkTables.initialize(server='roborio-5045-frc.local')
        # self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')
        self.controller = wpilib.XboxController(1)

        self.frontLeftModule_driveMotor = phoenix5.WPI_TalonSRX(1)
        self.frontLeftModule_rotateMotor = phoenix5.WPI_TalonSRX(2)
        self.frontLeftModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.frontRightModule_driveMotor = phoenix5.WPI_TalonSRX(3)
        self.frontRightModule_rotateMotor = phoenix5.WPI_TalonSRX(4)
        self.frontRightModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.rearRightModule_driveMotor = phoenix5.WPI_TalonSRX(5)
        self.rearRightModule_rotateMotor = phoenix5.WPI_TalonSRX(6)
        self.rearRightModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.rearLeftModule_driveMotor = phoenix5.WPI_TalonSRX(7)
        self.rearLeftModule_rotateMotor = phoenix5.WPI_TalonSRX(8)
        self.rearLeftModule_rotateMotor.setNeutralMode(BRAKE_MODE)

        self.frontLeftModule_encoder = self.frontLeftModule_rotateMotor
        self.frontRightModule_encoder = self.frontRightModule_rotateMotor
        self.rearLeftModule_encoder = self.rearLeftModule_rotateMotor
        self.rearRightModule_encoder = self.rearRightModule_rotateMotor

        self.frontLeftModule_cfg = {"sd_prefix":'frontLeft_Module', "zero": -55, "inverted":True, "allow_reverse":True, "encoder":self.frontLeftModule_encoder}
        self.frontRightModule_cfg = {"sd_prefix":'frontRight_Module', "zero": -45, "inverted":True, "allow_reverse":True, "encoder":self.frontRightModule_encoder}
        self.rearLeftModule_cfg = {"sd_prefix":'rearLeft_Module', "zero": -9, "inverted":False, "allow_reverse":True, "encoder":self.rearLeftModule_encoder}
        self.rearRightModule_cfg = {"sd_prefix":'rearRight_Module', "zero": -26, "inverted":True, "allow_reverse":True, "encoder":self.rearRightModule_encoder}

        self.frontLeftModule = swervemodule.SwerveModule(self.frontLeftModule_cfg, self.frontLeftModule_driveMotor, self.frontLeftModule_rotateMotor)
        self.frontRightModule = swervemodule.SwerveModule(self.frontRightModule_cfg, self.frontRightModule_driveMotor, self.frontRightModule_rotateMotor)
        self.rearLeftModule = swervemodule.SwerveModule(self.rearLeftModule_cfg, self.rearLeftModule_driveMotor, self.rearLeftModule_rotateMotor)
        self.rearRightModule = swervemodule.SwerveModule(self.rearRightModule_cfg, self.rearRightModule_driveMotor, self.rearRightModule_rotateMotor)

        self.drive = swervedrive.SwerveDrive(self.frontRightModule, self.frontLeftModule, self.rearRightModule, self.rearLeftModule)

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

        # # Encoder Positions % 4096
        # self.sd.putValue("FL_encoder_pos", ((self.frontLeftModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        # self.sd.putValue("FR_encoder_pos", ((self.frontRightModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        # self.sd.putValue("RL_encoder_pos", ((self.rearLeftModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        # self.sd.putValue("RR_encoder_pos", ((self.rearRightModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        # # Module setpoints
        # self.sd.putValue("FL_setpoint", self.frontLeftModule.pid_controller.getSetpoint())
        # self.sd.putValue("FR_setpoint", self.frontRightModule.pid_controller.getSetpoint())
        # self.sd.putValue("RL_setpoint", self.rearLeftModule.pid_controller.getSetpoint())
        # self.sd.putValue("RR_setpoint", self.rearRightModule.pid_controller.getSetpoint())

        print(((self.frontLeftModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        print(((self.frontRightModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        print(((self.rearLeftModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        print(((self.rearRightModule_encoder.getSelectedSensorPosition() % 4096) + 4096) % 4096)
        print(" ")
        print(self.frontLeftModule.pid_controller.getSetpoint())
        print(self.frontRightModule.pid_controller.getSetpoint())
        print(self.rearLeftModule.pid_controller.getSetpoint())
        print(self.rearRightModule.pid_controller.getSetpoint())
        print("________________________________________________")


if __name__ == "__main__":
    wpilib.run(MyRobot)