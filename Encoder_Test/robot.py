import wpilib

lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)


shootEncoder = wpilib.Encoder(7, 8, True, wpilib.CounterBase.k4X)
shootEncoder.SetDistancePerPulse(1)

rate = 0;
RPM  = 0;

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
        
        global rate
        rate = shootEncoder.GetRate()
        global RPM
        RPM = 60 * (rate/4096)

        print("RPM: ", "%.2f" % float(RPM))
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
