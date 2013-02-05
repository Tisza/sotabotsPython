import wpilib


lstick = wpilib.Joystick(1)

wpilib.NetworkTable.SetIPAddress(ip)
wpilib.NetworkTable.SetClientMode()
wpilib.NetworkTable.Initialize()

table = wpilib.NetworkTable.GetTable("SmartDashboard")

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


    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        try:
        	print("SmartDashboard::test: %s" % table.GetNumber('DISTANCE'))
        except:
        	print("No value yet")

        
        
    
def run():
    robot = MyRobot()
    robot.StartCompetition()
