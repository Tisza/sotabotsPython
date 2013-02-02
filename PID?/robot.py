import wpilib
from EncoderFilter import encoderFilter

lstick = wpilib.Joystick(1)

motor = wpilib.Jaguar(2)
encoder = wpilib.Encoder(7,8,True,wpilib.CounterBase.k4X)

filterEncoder = encoderFilter(100)


class MotorOutput(wpilib.PIDOutput):
    def __init__(self, motor):
        super().__init__()
        self.motor = motor

    def PIDWrite(self, output):
        self.motor.Set(abs(output))
        print("Output: ", output)

class AnalogSource(wpilib.PIDSource):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder

    def PIDGet(self):
        return filterEncoder.update((encoder.GetRate() / 4096) * 60)


pidSource = AnalogSource(encoder)
pidOutput = MotorOutput(motor)
pidController = wpilib.PIDController(0.05, 0.005, 0.0, pidSource, pidOutput)

def CheckRestart():
    if lstick.GetRawButton(10):
        raise RuntimeError("Restart")

class MyRobot(wpilib.SimpleRobot):
    def Disabled(self):
        while self.IsDisabled():
            CheckRestart()
            wpilib.Wait(0.01)

    def Autonomous(self):
        self.GetWatchdog().SetEnabled(False)
        while self.IsAutonomous() and self.IsEnabled():
            CheckRestart()
            wpilib.Wait(0.01)

    def OperatorControl(self):
        dog = self.GetWatchdog()
        dog.SetEnabled(True)
        dog.SetExpiration(0.25)
        encoder.Start()
        pidController.Enable()

        while self.IsOperatorControl() and self.IsEnabled():
            dog.Feed()
            CheckRestart()

            # Motor control
            pidController.SetSetpoint(5) #sets to 5rpm
            #print("Reading: ", AnalogSource(encoder).PIDGet())


            wpilib.Wait(0.04)

def run():
    robot = MyRobot()
    robot.StartCompetition()
