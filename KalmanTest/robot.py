import wpilib
import kalman


lstick = wpilib.Joystick(1)

leftMotor = wpilib.Jaguar(1)

gyro = wpilib.Gyro(1)

kalmanFilter = Kalman(50)


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
        gyro.Reset()

    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
       
        #Print gyro values
        print("Plain gyro value: " + gyro.GetAngle())
        print(kalmanFilter.update(gyro.GetAngle())
        
def run():
    robot = MyRobot()
    robot.StartCompetition()
