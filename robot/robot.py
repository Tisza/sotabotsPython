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
fnum = 0
bnum = 0
lsense = (lstick.GetThrottle() -1)*(-0.5)
rsense = (rstick.GetThrottle() -1)*(-0.5)
mode = 0
stage = 0 
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

def CheckRestart():
    if lstick.GetRawButton(15):
        raise RuntimeError("Restart")
        print("CheckRestart")

def RateGet(rawDistance, lastDistance):
	global C
	C += 1
	if C<6:
		return ld[lastDistance]
	else:
            rate = ld[lastDistance] - rawDistance
            ld[lastDistance] = rawDistance
            C=0
            return abs(rate)

class MyRobot(wpilib.IterativeRobot):
    def DisabledContinuous(self):
        wpilib.Wait(0.01)
    def AutonomousContinuous(self):
        wpilib.Wait(0.01)
    def TeleopContinuous(self):
        wpilib.Wait(0.01)
        global stage
        global frontValue
        global backValue
        global hop
        global fire
        if stage == 0:
            drive.ArcadeDrive(1,0)
            c=0
            if leftDriveEncoder.GetRaw()>3000 and rightDriveEncoder.GetRaw()>3000:
                stage=1
        if stage == 1:
            #hopper piston control
            if hop==False:
                hop = True
                start2 = timer.Get()
            drive.ArcadeDrive(0,.1)
            if leftDriveEncoder.GetRaw()>4000 or rightDriveEncoder.GetRaw()>4500:
                stage=2
        if stage == 2:
            if start2 == 0:
                hop = False
            drive.ArcadeDrive(0,0)
            if RateGet(shootEncoder.GetRaw(),"se") + 380 < 10 and RateGet(shootEncoder.GetRaw(),"se") + 380 > -10: #front auto
                    frontValue = frontValue
                    #Shooter piston control
                    if fire==False: 			#if trigger pulled and currently not firing
                        fire = True
                        start = timer.Get() #mark the time
            elif (RateGet(shootEncoder.GetRaw(),"se")) > -380:
                    frontValue += 0.001
            elif (RateGet(shootEncoder.GetRaw(),"se")) < -380:
                    frontValue -= 0.001
            elif RateGet(feedEncoder.GetRaw(),"fe") + 250 < 10 and RateGet(feedEncoder.GetRaw(),"fe") + 250 > -10: #back auto
                    backValue = backValue
            elif RateGet(feedEncoder.GetRaw(),"fe") < -250:
                    backValue += 0.0015
            elif RateGet(feedEncoder.GetRaw(),"fe") > -250:
                    backValue -= 0.0015

        #Modulated processes
        if start != 0: #Shooting
            loader1.Set(False ) #marked time = fire
            loader2.Set(True )
            c += 1
        else:
            loader1.Set(True )
            loader2.Set(False )
        if timer.Get() > start+0.2: #if half a second has passed, stop firing
            start = 0
            fire = False
            start2 = timer.Get()

        if start2 != 0:#Loading
                hopper1.Set(False)
                hopper2.Set(True)
        else:
                hopper1.Set(True)
                hopper2.Set(False)
        if (timer.Get() > start2+.5): #and magic1.Get()==True:  #.2 second interval for hopper piston
                start2 = 0
    def DisabledPeriodic(self):
        CheckRestart()

    def AutonomousInit(self):
        self.GetWatchdog().SetEnabled(False)

    def AutonomousPeriodic(self):
        CheckRestart()

    def TeleopInit(self):
    	global frontValue
    	global backValue
        dog = self.GetWatchdog()
        dog.SetEnabled(True)
        dog.SetExpiration(0.25)
        compressor.Start()
        shootEncoder.Start()
        feedEncoder.Start()
        leftDriveEncoder.Start()
        rightDriveEncoder.Start()
        timer.Start()
        frontValue = 0
        backValue = 0 
        
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
        global mode
        global fnum
        global bnum
        
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

		#manual shooter controls
        if rstick.GetRawButton(11):				#right button 11 increments FRONT
            mode = 99
            fnum += 10*rsense
            if frontValue > 1:
                frontValue = 1
            print("Front: "+str(int(fnum)))
        elif rstick.GetRawButton(10):				#right button 10 decrements FRONT
            mode = 99
            fnum -= 10*rsense
            if frontValue < 0:
                frontValue = 0
            print("Front: "+str(int(fnum)))
        if rstick.GetRawButton(6):				#right button 6 increments BACK
            mode = 99
            bnum += 10*rsense
            if backValue > 1:
                backValue = 1
            print("Back: "+str(int(bnum)))
        elif rstick.GetRawButton(7):				#right button 7 decrements BACK
            mode = 99
            bnum-= 10*rsense
            if backValue < 0:
                backValue = 0
            print("Back: "+str(int(bnum)))
        
	#Button Control Presets
        if rstick.GetRawButton(3) and mode != 0:
            mode = 0
            print("Shooters Off")
        if rstick.GetRawButton(5) and mode != 1:
            mode = 1
            print("Tower Preset")
            backValue = .45
            frontValue = .75

        #AUTO shooter PRESET CONTROLS
        if mode == 0: #Turn off the shooter
            if frontValue != 0:
            	frontValue = 0
            if backValue != 0:
            	backValue = 0
            if fnum != 0:
            	fnum = 0
            if bnum != 0:
            	bum = 0
        elif mode == 1: #Encoder preset at tower
            if RateGet(shootEncoder.GetRaw(),"se") + 380 < 10 and RateGet(shootEncoder.GetRaw(),"se") + 380 > -10: #front auto
                    frontValue = frontValue
                    print("FIRE")
            elif (RateGet(shootEncoder.GetRaw(),"se")) > -380:
                    frontValue += 0.001
            elif (RateGet(shootEncoder.GetRaw(),"se")) < -380:
                    frontValue -= 0.001
            if RateGet(feedEncoder.GetRaw(),"fe") + 250 < 10 and RateGet(feedEncoder.GetRaw(),"fe") + 250 > -10: #back auto
                    backValue = backValue
            elif RateGet(feedEncoder.GetRaw(),"fe") < -250:
                    backValue += 0.0015
            elif RateGet(feedEncoder.GetRaw(),"fe") > -250:
                    backValue -= 0.0015
            # 30,000 front / 17,000 back for tower shot'''
        elif mode == 99: 
            if RateGet(shootEncoder.GetRaw(),"se") + fnum < 10 and RateGet(shootEncoder.GetRaw(),"se") + fnum > -10: #front auto
                    frontValue = frontValue
            elif (RateGet(shootEncoder.GetRaw(),"se")) > -fnum:
                    frontValue += 0.001
            elif (RateGet(shootEncoder.GetRaw(),"se")) < -fnum:
                    frontValue -= 0.001
            if RateGet(feedEncoder.GetRaw(),"fe") + bnum < 10 and RateGet(feedEncoder.GetRaw(),"fe") + bnum > -10: #back auto
                    backValue = backValue
            elif RateGet(feedEncoder.GetRaw(),"fe") < -bnum:
                    backValue += 0.0015
            elif RateGet(feedEncoder.GetRaw(),"fe") > -bnum:
                    backValue -= 0.0015
        else:
            frontValue = 0
            backValue = 0
            
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
            hop = True
            start2 = timer.Get()
            
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
        if (timer.Get() > start2+.5): #and magic1.Get()==True:  #.2 second interval for hopper piston
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
            dawg1.Set(False)
            dawg2.Set(True)
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
        if lstick.GetRawButton(5): #Unhitch the dog.
            drumMotor.Set(lsense)
            dawg1.Set(True)
            dawg2.Set(False)
            
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
