import wpilib

lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)

Motor = wpilib.Jaguar(1)
Motor2 = wpilib.Jaguar(2)

motorValue = 0
motorOld = 0
endMotorValue = 0
endMotorOld = 0

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
        global motorValue
        global motorOld
        global endMotorValue
        global endMotorOld

        if lstick.GetRawButton(0):              #Trigger sets shooter to 100%
                endMotorValue = -1
        if rstick.GetRawButton(0):
                motorValue = -1
        if lstick.GetRawButton(1):              #Button 2 sets to magic number
                endMotorValue = -0.47
        else:                                   #Joystick y axis controls incrementally
                if lstick.GetY() > 0.05 or lstick.GetY() < -0.05:
                        endMotorValue += lstick.GetY()/100
        if rstick.GetRawButton(1):
                motorValue = -0.47
        else:
                if rstick.GetY() > 0.05 or rstick.GetY() < -0.05:
                        motorValue += rstick.GetY()/100
        if abs(lstick.GetX() > 0.5) or lstick.GetRawButton(3):            #Shake joystick x-axis or press button 3 to e-stop motors
                endMotorValue = 0
        if abs(rstick.GetX() > 0.5) or rstick.GetRawButton(3):
                motorValue = 0
        
        if motorValue > 1.0:                    #Keeps increments at or under +/-100%
                motorValue = 1.0
        elif motorValue < -1.0:
                motorValue = -1.0
        if endMotorValue > 1.0:
                endMotorValue = 1.0
        elif motorValue < -1.0:
                endMotorValue = -1.0
        
        Motor.Set(motorValue)
        Motor2.Set(endMotorValue)
        if endMotorValue != endMotorOld:              #prints motor values prettier
            print("End Motor: "+str(endMotorValue)*100+"%")
            endMotorOld = endMotorValue
        if motorValue != motorOld:
            print("Feed Motor: "+str(motorValue)*100+"%")
            motorOld = motorValue
        

def run():
    robot = MyRobot()
    robot.StartCompetition()
