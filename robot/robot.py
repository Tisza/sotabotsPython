import wpilib
from GyroFilter import gyroFilter
from AimFilter import aimFilter
import robotMap

#joysticks
lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)

#drive motors
leftMotor = wpilib.Jaguar(1)
rightMotor = wpilib.Jaguar(2)

#shooter motors
forwardShooter = wpilib.Jaguar(robotMap.forwardShooterChannel)
backShooter = wpilib.Jaguar(robotMap.backShooterChannel)

#lift motor
liftMotor = wpilib.Jaguar(robotMap.liftMotorChannel)

#loader piston
loader = wpilib.DoubleSolenoid( robotMap.pistonForwardChannel, robotMap.pistonReverseChannel )

#encoders
shootEncoder = wpilib.Encoder( robotMap.shootEncoder1 , robotMap.shootEncoder2 , True, wpilib.CounterBase.k4X)
leftDriveEncoder = wpilib.Encoder( robotMap.leftDriveEncoder1 , robotMap.leftDriveEncoder2 , True, wpilib.CounterBase.k4X)
rightDriveEncoder = wpilib.Encoder( robotMap.rightDriveEncoder1 , robotMap.rightDriveEncoder2 , True, wpilib.CounterBase.k4X)
drumEncoder = wpilib.Encoder( robotMap.drumEncoder1 , robotMap.drumEncoder2 , True, wpilib.CounterBase.k4X)

#shooter motor value
motorValue = 0.0

#drive train
drive = wpilib.RobotDrive(leftMotor,rightMotor)

#network table initilization
table = wpilib.NetworkTable.GetTable("SmartDashboard")

#averaging filter for encoder values with array of length 100
filterEncoder = aimFilter(100)



def CheckRestart():
    if lstick.GetRawButton(10):
        raise RuntimeError("Restart")
        print("CheckRestart")


class MyRobot(wpilib.IterativeRobot):
    def DisabledContinuous(self):
        wpilib.Wait(0.01)
    def AutonomousContinuous(self):
        wpilib.Wait(0.01)
    def TeleopContinuous(self):
        wpilib.Wait(0.01)

    def DisabledPeriodic(self):
        CheckRestart()

    def AutonomousInit(self):
        self.GetWatchdog().SetEnabled(False)

    def AutonomousPeriodic(self):
        CheckRestart()

    def TeleopInit(self):
        dog = self.GetWatchdog()
        dog.SetEnabled(True)
        dog.SetExpiration(0.25)

        global motorValue

    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        
        # Drive control
        drive.ArcadeDrive(lstick)

	#shooter controls
	if rstick.GetY() > 0.05 or rstick.GetY() < -0.05:
                motorValue += rstick.GetY()/100
	elif rstick.GetRawButton(3):
		motorValue = 0
        if motorValue > 1.0:                    #Keeps increments at or under +/-100%
                motorValue = 1.0
        elif motorValue < -1.0:
                motorValue = -1.0
        
        forwardShooter.Set(motorValue)
        backShooter.Set(motorValue)
        
        #Shooter piston control
        if rstick.GetTrigger(): 
        	loader.Set( wpilib.DoubleSolenoid.Value.kForward )
        	wpilib.Timer.Delay( 1 )
        	loader.Set( wpilib.DoubleSolenoid.Value.kReverse )
        	

def run():
    robot = MyRobot()
    robot.StartCompetition()
