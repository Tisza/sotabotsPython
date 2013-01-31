import wpilib

lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)


shootEncoder = wpilib.Encoder(7, 8, True, wpilib.CounterBase.k4X)
shootEncoder.SetDistancePerPulse(1)

motor1 = wpilib.Jaguar(2)
endMotorValue = 0.0

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


        global endMotorValue
        global rate
        rate = shootEncoder.GetRate()
        global RPM
        RPM = 60 * (rate/4096)

        print("RPM: ", "%.2f" % float(RPM))



        if lstick.GetRawButton(1):              #Button 2 sets to magic number
                endMotorValue = -0.47
        else:                                   #Joystick y axis controls incrementally
                if lstick.GetY() > 0.05 or lstick.GetY() < -0.05:
                        endMotorValue += lstick.GetY()/100
        if lstick.GetRawButton(3):
                endMotorValue = 0

        motor1.Set(endMotorValue)
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
