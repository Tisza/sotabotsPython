import wpilib

lstick = wpilib.Joystick(1)

motor = wpilib.Jaguar(1)
encoder = wpilib.Encoder(1,2,k4X)

class MotorOutput(wpilib.PIDOutput):
    def __init__(self, motor):
        super().__init__()
        self.motor = motor

    def PIDWrite(self, output):
        self.motor.Set(output)

class AnalogSource(wpilib.PIDSource):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder

    def PIDGet(self):
        return (encoder.GetRate() / 4096) * 60

pidSource = AnalogSource(encoder)
pidOutput = MotorOutput(motor)
pidController = wpilib.PIDController(1.0, 0.2, 0.0, pidSource, pidOutput)

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

        pidController.Enable()

        while self.IsOperatorControl() and self.IsEnabled():
            dog.Feed()
            CheckRestart()

            # Motor control
            pidController.SetSetpoint(200) #sets to 200rpm
            print("Reading: " + pidSource)
            print("Output: " + pidOutput)

            wpilib.Wait(0.04)

def run():
    robot = MyRobot()
    robot.StartCompetition()
