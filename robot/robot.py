import wpilib
from GyroFilter import gyroFilter
from AimFilter import aimFilter
import robotMap

#joysticks
lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)

#drive motors
leftMotor = wpilib.Jaguar(robotMap.leftDrive)
rightMotor = wpilib.Jaguar(robotMap.rightDrive)

#shooter motors
forwardShooter = wpilib.Jaguar(robotMap.forwardShooterChannel)
backShooter = wpilib.Jaguar(robotMap.backShooterChannel)

#loader piston 
loader1 = wpilib.Solenoid(robotMap.pistonForwardChannel)
loader2 = wpilib.Solenoid(robotMap.pistonReverseChannel)

#magic Jacks
magic1 = wpilib.Solenoid(robotMap.magicJackUp)
magic2 = wpilib.Solenoid(robotMap.magicJackDown)

#Dawg control
dawg1 = wpilib.Solenoid(robotMap.dawgLock)
dawg2 = wpilib.Solenoid(robotMap.dawgRelease)

#drum motor
drumMotor = wpilib.Victor(robotMap.drumMotorChannel)

#arm rotation motor
weeWooMotor = wpilib.Victor(robotMap.weeWooChannel)

#arm limit switch
armLimitSwitch = wpilib.DigitalInput(robotMap.armLimitSwitch)

#compressor
compressor = wpilib.Compressor(robotMap.pressureSwitch,robotMap.compressorSpike)

#encoders
shootEncoder = wpilib.Encoder( robotMap.shootEncoder1 , robotMap.shootEncoder2 , True, wpilib.CounterBase.k4X)
feedEncoder = wpilib.Encoder(robotMap.feedEncoder1, robotMap.feedEncoder2, True, wpilib.CounterBase.k4X)
leftDriveEncoder = wpilib.Encoder( robotMap.leftDriveEncoder1 , robotMap.leftDriveEncoder2 , True, wpilib.CounterBase.k4X)
rightDriveEncoder = wpilib.Encoder( robotMap.rightDriveEncoder1 , robotMap.rightDriveEncoder2 , True, wpilib.CounterBase.k4X)
drumEncoder = wpilib.Encoder( robotMap.drumEncoder1 , robotMap.drumEncoder2 , True, wpilib.CounterBase.k4X)

#variables
frontValue = 0
backValue = 0
fire = False 
jackItUp = False
doggie = False

#drive train
drive = wpilib.RobotDrive(leftMotor,rightMotor)


#network table initilization
table = wpilib.NetworkTable.GetTable("SmartDashboard")

#averaging filter for encoder values with array of length 100
filterEncoder = aimFilter(100)

#timer
timer = wpilib.Timer()
start = 0

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
        compressor.Start()
        shootEncoder.Start()
        feedEncoder.Start()
        timer.Start()
        
        #starting positions
        magic1.Set(False)
        magic2.Set(True)
        dawg1.Set(False)
        dawg2.Set(True)
        
    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        global frontValue
        global backValue
        global fire
        global start
        global jackItUp
        global armValue
        global doggie
        
        # Drive control
        drive.ArcadeDrive(lstick)

	#shooter controls
        if rstick.GetRawButton(11):				#right button 11 increments FRONT by 1%
            frontValue+=.01
            if frontValue > 1:
                frontValue = 1
            print("Front: "+str(int(frontValue*100))+"%")
        elif rstick.GetRawButton(10):				#right button 10 decrements FRONT to by 1%
            frontValue-=.01
            if frontValue < 0:
                frontValue = 0
            print("Front: "+str(int(backValue*100))+"%")
        if rstick.GetRawButton(6):				#right button 6 increments BACK by 1%
            backValue+=.01
            if backValue > 1:
                backValue = 1
            print("Back: "+str(int(frontValue*100))+"%")
        elif rstick.GetRawButton(7):				#right button 7 decrements BACK by 1% 
            backValue-=.01
            if backValue < 0:
                backValue = 0
            print("Back: "+str(int(backValue*100))+"%")
        forwardShooter.Set(frontValue)
        backShooter.Set(backValue)
        
        #Shooter piston control
        if rstick.GetTrigger() and fire==False: 			#if trigger pulled and currently not firing
            fire = True
            start = timer.Get() #mark the time
            print("Shooter: "+str(shootEncoder.GetRate())+" Feeder: "+str(feedEncoder.GetRate()))
        if start != 0:
            loader1.Set(False ) #marked time = fire
            loader2.Set(True )
        else:
            loader1.Set(True )
            loader2.Set(False )    
        if timer.Get() > start+0.2: #if half a second has passed, stop firing
            start = 0
        if start == 0 and not rstick.GetTrigger() and fire == True: #finish the cycle
            fire = False
        
        #Magic Jacks
        if lstick.GetRawButton(8) and lstick.GetRawButton(9) and jackItUp==False:	#button 8 and 9 at same time to toggle jacks
            magic1.Set(!magic1.Get())
            magic2.Set(!magic2.Get())
            jackItUp=True
        if (not lstick.GetRawButton(8) or not lstick.GetRawButton(9)) and jackItUp==True:
            jackItUp=False
        
        #lift controls
        if lstick.GetRawButton(10):				#left button 10 retracts lift
            drumMotor.Set(-0.5)
        elif lstick.GetRawButton(11):				#left button 11 extends lift
            drumMotor.Set(0.5)
        else:
            drumMotor.Set(0)
            
        #arm controls
        if lstick.GetRawButton(6) and armLimitSwitch==False:
            weeWooMotor.Set(1)
        elif lstick.GetRawButton(7):
            weeWooMotor.Set(-1)
        else:
            weeWooMotor.Set(0)
        
        #Dawg Controls
        if lstick.GetTrigger() and doggie == False:
            dawg1.Set(!dawg1.Get())
            dawg2.Set(!dawg2.Get())
            doggie = True
        if not lstick.GetTrigger() and doggie == True:
            doggie = False
        	

def run():
    robot = MyRobot()
    robot.StartCompetition()
