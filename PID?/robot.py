import wpilib
from EncoderFilter import encoderFilter
from VelocityPID import PID

lstick = wpilib.Joystick(1)


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
        self.motorOutput = 0.5       
        
        
    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        
        if filterEncoder.update(((shootEncoder.GetRate() / 4096) * 60) ) - 6 < 0.5 and (((shootEncoder.GetRate() / 4096) * 60) ) - 6 > -0.5:
        	self.motorOutput = self.motorOutput
        elif filterEncoder.update( (shootEncoder.GetRate() / 4096) * 60) < 6:
        	self.motorOutput += 0.001
        elif filterEncoder.update((shootEncoder.GetRate() / 4096) * 60) > 6:
        	self.motorOutput -= 0.001
        	
        print("RPM: ", filterEncoder.update((shootEncoder.GetRate() / 4096) * 60), "    Motor:  ", self.motorOutput)

        leftMotor.Set(self.motorOutput)
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
