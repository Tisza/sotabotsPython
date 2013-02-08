import wpilib
from VelocityPID import PID
from EncoderFilter import encoderFilter

lstick = wpilib.Joystick(1)

leftMotor = wpilib.Jaguar(2)

PIDController = PID()

shootEncoder = wpilib.Encoder(7,8,False,wpilib.CounterBase.k4X)
shootEncoder.SetDistancePerPulse(1)
filterEncoder = encoderFilter(100)

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
        PIDController.__init__(0.5, 0.0, 0.0, 0, 0, 500, -500)
        self.motorOutput = 0.5       

        
    def TeleopPeriodic(self):
	self.GetWatchdog().Feed()
	CheckRestart()
        
	PIDController.setPoint(30) #set setPoint to 30 RPM
        
	rpm  = (shootEncoder.GetRate() / 4096) * 60
	leftMotor.Set(self.motorOutput)
	filterEncoder.update((shootEncoder.GetRate() / 4096) * 60)
	PIDreturn = PIDController.update( (shootEncoder.GetRate() / 4096) * 60 )
	self.motorOutput = ((PIDController.update(shootEncoder.GetRate())) / 15 -1)
	leftMotor.Set(.75)
	print("RPM: ", (shootEncoder.GetRate() / 4096) * 60)

        
        
def run():
    robot = MyRobot()
    robot.StartCompetition()
