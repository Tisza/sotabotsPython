import wpilib
from EncoderFilter import encoderFilter
from VelocityPID import PID

lstick = wpilib.Joystick(1)

PIDController = PID()

shootEncoder = wpilib.Encoder(7, 8, True, wpilib.CounterBase.k4X)
shootEncoder.SetDistancePerPulse(1)
filterEncoder = encoderFilter(100)

leftMotor = wpilib.Jaguar(2)


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
        PIDController.__init__(0.5, 0.0, 0.0, 0, 0, 500, -500)
        PIDController.setPoint(30) #set setPoint to 30 RPM
        self.motorOutput = 0.5       
        
        
    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        leftMotor.Set(self.motorOutput)
        rAverage = filterEncoder.update((shootEncoder.GetRate() / 4096) * 60)
        PIDreturn = PIDController.update( rAverage )
        self.motorOutput = ( self.motorOutput + (PIDreturn / 30) )
	
        print("PID Return: ", PIDreturn, "   RPM:  ", rAverage, "   Motor: ", self.motorOutput)
        leftMotor.Set(self.motorOutput)
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
