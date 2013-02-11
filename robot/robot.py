import wpilib
from GyroFilter import gyroFilter
from AimFilter import aimFilter
import robotMap

#joysticks
lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)

#drive motors
leftMotor = wpilib.Jaguar(robotMap.leftDrive)
rightMotor = wpilib.Jaguar(robotMap.rightDrive)

#shooter motors
forwardShooter = wpilib.Jaguar(robotMap.forwardShooterChannel)
backShooter = wpilib.Jaguar(robotMap.backShooterChannel)

#loader piston 
loader1 = wpilib.Solenoid(robotMap.pistonForwardChannel)
loader2 = wpilib.Solenoid(robotMap.pistonReverseChannel)

#lift motor
liftMotor = wpilib.Jaguar(robotMap.liftMotorChannel)

#compressor
compressor = wpilib.Compressor(robotMap.pressureSwitch,robotMap.compressorSpike)

#encoders
shootEncoder = wpilib.Encoder( robotMap.shootEncoder1 , robotMap.shootEncoder2 , True, wpilib.CounterBase.k4X)
feedEncoder = wpilib.Encoder(robotMap.feedEncoder1, robotMap.feedEncoder2, True, wpilib.CounterBase.k4X)
leftDriveEncoder = wpilib.Encoder( robotMap.leftDriveEncoder1 , robotMap.leftDriveEncoder2 , True, wpilib.CounterBase.k4X)
rightDriveEncoder = wpilib.Encoder( robotMap.rightDriveEncoder1 , robotMap.rightDriveEncoder2 , True, wpilib.CounterBase.k4X)
drumEncoder = wpilib.Encoder( robotMap.drumEncoder1 , robotMap.drumEncoder2 , True, wpilib.CounterBase.k4X)

#shooter motor value
frontValue = 0
backValue = 0

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
        compressor.Start()
        shootEncoder.Start()
        feedEncoder.Start()

    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        global frontValue
        global backValue
        
        # Drive control
        drive.ArcadeDrive(lstick)

	#shooter controls
        if rstick.GetRawButton(11):
            frontValue+=1
            if frontValue > 1:
                frontValue = 1
            print("Front: "+str(int(frontValue*100))+"%")
            wpilib.Timer.Delay(1)
        if rstick.GetRawButton(10):
            frontValue-=1
            if frontValue < 0:
                frontValue = 0
            print("Front: "+str(int(backValue*100))+"%")
            wpilib.Timer.Delay(1)
        if rstick.GetRawButton(6):
            backValue+=1
            if backValue > 1:
                backValue = 1
            print("Back: "+str(int(frontValue*100))+"%")
            wpilib.Timer.Delay(1)
        if rstick.GetRawButton(7):
            backValue-=1
            if backValue < 0:
                backValue = 0
            print("Back: "+str(int(backValue*100))+"%")
            wpilib.Timer.Delay(1)
        forwardShooter.Set(frontValue)
        backShooter.Set(backValue)
        
        #Shooter piston control
        if rstick.GetTrigger():
            #loader.Set( wpilib.DoubleSolenoid.Value.kForward )
            loader1.Set(True )
            loader2.Set(False )
            wpilib.Timer.Delay( 1 )
            #loader.Set( wpilib.DoubleSolenoid.Value.kReverse )
            loader1.Set(False )
            loader2.Set(True )
        	
        #lift controls
        if lstick.GetRawButton(10):
        	liftMotor.Set(-0.4)
        elif lstick.GetRawButton(11):
        	liftMotor.Set(0.4)
        	
        #prints encoder value
        print("Shooter: "+str(shootEncoder.GetRate())+" Feeder: "+str(feedEncoder.GetRate()))
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
