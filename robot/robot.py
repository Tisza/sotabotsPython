import wpilib
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

#hopper piston
hopper1 = wpilib.Solenoid(robotMap.hopperForwardChannel)
hopper2 = wpilib.Solenoid(robotMap.hopperReverseChannel)

#magic Jacks
#magic1 = wpilib.Solenoid(robotMap.magicJackUp)
#magic2 = wpilib.Solenoid(robotMap.magicJackDown)

#Dawg control
dawg1 = wpilib.Solenoid(robotMap.dawgLock)
dawg2 = wpilib.Solenoid(robotMap.dawgRelease)

#drum motor
drumMotor = wpilib.Victor(robotMap.drumMotorChannel)

#arm rotation motor
weeWooMotor = wpilib.Victor(robotMap.weeWooChannel)

#limit switches
armLimitSwitch = wpilib.DigitalInput(robotMap.armLimitSwitch)
liftBottomSwitch = wpilib.DigitalInput(robotMap.liftBottomSwitch)
liftTopSwitch = wpilib.DigitalInput(robotMap.liftTopSwitch)

#compressor
compressor = wpilib.Compressor(robotMap.pressureSwitch,robotMap.compressorSpike)

#encoders
shootEncoder = wpilib.Encoder( robotMap.shootEncoder1 , robotMap.shootEncoder2 , True, wpilib.CounterBase.k4X)
feedEncoder = wpilib.Encoder(robotMap.feedEncoder1, robotMap.feedEncoder2, True, wpilib.CounterBase.k4X)
leftDriveEncoder = wpilib.Encoder( robotMap.leftDriveEncoder1 , robotMap.leftDriveEncoder2 , True, wpilib.CounterBase.k4X)
rightDriveEncoder = wpilib.Encoder( robotMap.rightDriveEncoder1 , robotMap.rightDriveEncoder2 , True, wpilib.CounterBase.k4X)

#variables
frontValue = 0
backValue = 0
direction = 1
lsense = (lstick.GetThrottle() -1)*(-0.5)
rsense = (rstick.GetThrottle() -1)*(-0.5)
ld = {"se":(0),"fe":(0),"ld":0,"rd":0}
fire = False 
#jackItUp = False
doggie = False
hop = False
dire=False 

#drive train
drive = wpilib.RobotDrive(leftMotor,rightMotor)


#network table initilization
table = wpilib.NetworkTable.GetTable("SmartDashboard")

#timer
timer = wpilib.Timer()
start = 0
start2 = 0
start3 = 0

def CheckRestart():
    if lstick.GetRawButton(15):
        raise RuntimeError("Restart")
        print("CheckRestart")

def RateGet(rawDistance, lastDistance):
        rate = ld[lastDistance] - rawDistance
        ld[lastDistance] = rawDistance
        return rate

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
        #magic1.Set(True)
        #magic2.Set(False)
        #dawg1.Set(False)
        #dawg2.Set(True)
        
    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        global frontValue
        global backValue
        global fire
        global start
        #global jackItUp
        global armValue
        global doggie
        global start2
        global hop
        global direction
        global dire
        global lsense
        global rsense
        global start3
        
        #sensitivity
        lsense = (lstick.GetThrottle() -1)*(-0.5)
        rsense = (rstick.GetThrottle() -1)*(-0.5)
        
        # Drive control
        if lstick.GetRawButton(2) and dire==False:
            direction = direction*-1
            dire=True
        if not lstick.GetRawButton(2) and dire==True:
            dire=False
        drive.ArcadeDrive(lstick.GetY()*direction*lsense,lstick.GetX()*lsense)

		#shooter controls
        if rstick.GetRawButton(11):				#right button 11 increments FRONT by 1%
            frontValue+=.05*rsense
            if frontValue > 1:
                frontValue = 1
            print("Front: "+str(int(frontValue*100))+"%")
        elif rstick.GetRawButton(10):				#right button 10 decrements FRONT to by 1%
            frontValue-=.05*rsense
            if frontValue < 0:
                frontValue = 0
            print("Front: "+str(int(frontValue*100))+"%")
        if rstick.GetRawButton(6):				#right button 6 increments BACK by 1%
            backValue+=.05*rsense
            if backValue > 1:
                backValue = 1
            print("Back: "+str(int(backValue*100))+"%")
        elif rstick.GetRawButton(7):				#right button 7 decrements BACK by 1% 
            backValue-=.05*rsense
            if backValue < 0:
                backValue = 0
            print("Back: "+str(int(backValue*100))+"%")
        if rstick.GetRawButton(8):
            backValue = 0
        if rstick.GetRawButton(9):
            frontValue = 0
        if rstick.GetRawButton(3):
            backValue = 0 
            frontValue = 0
        
		
        	
        #AUTO shooter PRESET CONTROLS		(LONG RANGE)		----must hold rstick button 5
        if RateGet(shootEncoder.GetRaw(),"se") - 3000 < 100 and RateGet(shootEncoder.GetRaw(),"se") - 3000 > -100: #front auto
                    frontValue = frontValue
                    print("FIRE")
                elif (RateGet(shootEncoder.GetRaw(),"se")) < 3000:
                    frontValue += 0.001
                elif (RateGet(shootEncoder.GetRaw()),"se") > 3000:
                    frontValue -= 0.001
                if RateGet(feedEncoder.GetRaw(),"fe") - 2700 < 100 and RateGet(feedEncoder.GetRaw(),"fe") - 2700 > -100: #back auto
                    backValue = backValue
                elif RateGet(feedEncoder.GetRaw(),"fe") < 2700:
                    backValue += 0.0015
                elif RateGet(feedEncoder.GetRaw(),"fe") > 2700:
                    backValue -= 0.0015
                # 30,000 front / 17,000 back for tower shot'''
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
            
        #hopper piston control
        if rstick.GetRawButton(2) and hop==False:
            hop = True
            start2 = timer.Get()
        if start2 != 0:
            hopper1.Set(False)
            hopper2.Set(True)
        else:
            hopper1.Set(True)
            hopper2.Set(False)
        if (timer.Get() > start2+.2): #and magic1.Get()==True:  #.2 second interval for hopper piston
            start2 = 0
        #if (timer.Get() > start2+.5) and magic1.Get()==False:
            #start2 = 0
        if start == 0 and not rstick.GetRawButton(2):
            hop = False
            
        #Magic Jacks
        #if lstick.GetRawButton(8) and lstick.GetRawButton(9) and jackItUp==False:	#button 8 and 9 at same time to toggle jacks
        #    magic1.Set(not magic1.Get())
        #    magic2.Set(not magic2.Get())
        #    jackItUp=True
        #if (not lstick.GetRawButton(8) or not lstick.GetRawButton(9)) and jackItUp==True:
        #    jackItUp=False
        
        #lift controls
        if lstick.GetRawButton(10):
            if liftTopSwitch.Get()==1:
                drumMotor.Set(lsense)
            else:
                drumMotor.Set(0)
            if dawg1.Get()==True:
                start3 = timer.Get()
            if timer.Get() > start3+.05:
                dawg1.Set(False)
                dawg2.Set(True)
                start3 = 0
        elif lstick.GetRawButton(11):
            if liftBottomSwitch.Get()==1:
                drumMotor.Set(-lsense)
            else:
                drumMotor.Set(0)
            if dawg1.Get()==False:
                dawg1.Set(True)
                dawg2.Set(False)
        else:
            drumMotor.Set(0)
            
       #arm controls
        if lstick.GetRawButton(6):
            weeWooMotor.Set(lsense)
        elif lstick.GetRawButton(7):
            if armLimitSwitch.Get()==1:
                weeWooMotor.Set(-lsense)
            else:
                weeWooMotor.Set(0)
        else:
            weeWooMotor.Set(0)
        
        #Dawg Controls
        if lstick.GetTrigger() and doggie == False:
            dawg1.Set(not dawg1.Get())
            dawg2.Set(not dawg2.Get())
            doggie = True
            print("Dog Enabled:"+str(dawg1.Get()))
        if not lstick.GetTrigger() and doggie == True:
            doggie = False
        	

def run():
    robot = MyRobot()
    robot.StartCompetition()
