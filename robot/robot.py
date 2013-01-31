import wpilib
from GyroFilter import gyroFilter
from AimFilter import aimFilter

lstick = wpilib.Joystick(1)

leftMotor = wpilib.Jaguar(1)
rightMotor = wpilib.Jaguar(2)

drive = wpilib.RobotDrive(leftMotor,rightMotor)

table = wpilib.NetworkTable.GetTable("SmartDashboard")

gyro = wpilib.Gyro(1)

filterGyro = gyroFilter(150) #untested value for list lenth

filterAim = aimFilter(150) #untested value for list length

shootEncoder = wpilib.Encoder(1,2,false,k4X)



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
        table.PutNumber("T", 1)
        gyro.Reset()

    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        
        # Motor control
        drive.ArcadeDrive(lstick)

        #Print gyro values
        PrintGyro()
        
    def PrintGyro(self):
        filterGyro.update(gyro.GetAngle())
        print("Gyroscope calculated average: ", filterGyro.update())
        print("Raw value: ", gyro.GetAngle())

    def Align(self):
        global target = table.getDouble("CENTER")
        
        while target < -0.05 and target > 0.05:
                
                tarval = filterAim((target^3)/2) #Slows down turning. Changed /3 to /2 -- filterAim gets a moving avg of the values to reduce impact of outliers
                drive.ArcadeDrive(0,tarval)
                target = table.getDouble("CENTER")
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
