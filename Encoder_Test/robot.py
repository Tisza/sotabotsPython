import wpilib
from EncoderFilter import encoderFilter

lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)


shootEncoder = wpilib.Encoder(7, 8, True, wpilib.CounterBase.k4X)
shootEncoder.SetDistancePerPulse(1)

motor1 = wpilib.Jaguar(2)
endMotorValue = 0.0

filterEncoder = encoderFilter(75)

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
        RPM = filterEncoder.update(RPM)

        print("RPM: ", "%.2f" % float(RPM))

        if endMotorValue > 1:
                endMotorValue = 1
        elif endMotorValue < 0:
                endMotorValue = 0

        
        if lstick.GetRawButton(3):
                endMotorValue = 0
        elif float("%.2f" % RPM) < 30:
                endMotorValue += 0.02
        elif float("%.2f" % RPM) > 30:
                endMotorValue -= 0.02
                

        motor1.Set(endMotorValue)
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
