import wpilib
from EncoderFilter import encoderFilter

lstick = wpilib.Joystick(1)

shootEncoder = wpilib.Encoder(7, 8, True, wpilib.CounterBase.k4X)
shootEncoder.SetDistancePerPulse(1)

motor1 = wpilib.Jaguar(2)


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
        
        shootEncoder.Start()
        shootEncoder.Reset()
        
    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()

        print("Raw Encoder:  ", shootEncoder.GetRate())
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
