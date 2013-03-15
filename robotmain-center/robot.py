from wpilib import SmartDashboard
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
magic1 = wpilib.Solenoid(robotMap.magicJackUp)
magic2 = wpilib.Solenoid(robotMap.magicJackDown)

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

#initialize smartDashboard
SmartDashboard.init()

#variables
frontValue = 0
backValue = 0
direction = -1
fnum = 0
bnum = 0
lsense = (lstick.GetThrottle() -1)*(-0.5)
rsense = (rstick.GetThrottle() -1)*(-0.5)
mode = 0
stage = 0
fcount = 1
ld = {"se":0,"fe":0,"ld":0,"rd":0}
fire = False
jackItUp = False
doggie = False
hop = False
dire=False
modey = "MANUAL"
incrementValue = 0.003



#drive train
drive = wpilib.RobotDrive(leftMotor,rightMotor)


#network table initilization
#table = wpilib.NetworkTable.GetTable("SmartDashboard")

#timer
timer = wpilib.Timer()
start = 0
start2 = 0
start3 = 0


def CheckRestart():
    if rstick.GetRawButton(15):
        raise RuntimeError("SystemRestart")
        print("CheckRestart")

def RateGet(rawDistance, lastDistance):
    rate = ld[lastDistance] - rawDistance
    ld[lastDistance] = rawDistance
    return rate

def FrontEncoderSet(rate, desiredrate, range, initVal):             #separate function for encoder-motor logic. NO MORE CONFUSION FOR US!
    if rate - desiredrate > -range and rate - desiredrate < range:
        motorVal = initVal
    elif rate < desiredrate:
        motorVal = initVal
        motorVal+=incrementValue
    elif rate > desiredrate:
        motorVal = initVal
        motorVal-=incrementValue
    if motorVal > 1:
        motorVal = 1
    if motorVal < 0:
        motorVal = 0
    return motorVal
    
def BackEncoderSet(rate, desiredrate, range, initVal):              #separate function for redundancy :D
    if rate - desiredrate > -range and rate - desiredrate < range:
        motorVal = initVal
    elif rate < desiredrate:
        motorVal = initVal
        motorVal+=incrementValue
    elif rate > desiredrate:
        motorVal = initVal
        motorVal-=incrementValue
    if motorVal > 1:
        motorVal = 1
    if motorVal < 0:
        motorVal = 0
    return motorVal

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
        global stage
        global fcount
        global frontValue
        self.GetWatchdog().SetEnabled(False)
        leftDriveEncoder.Start()
        rightDriveEncoder.Start()
        compressor.Start()
        shootEncoder.Start()
        feedEncoder.Start()
        timer.Start()
        stage = 0
        leftDriveEncoder.Reset()
        print("Stage 1")
        start = 0

    def AutonomousPeriodic(self):
        CheckRestart()
        global stage
        global frontValue
        global backValue
        global fire
        global start
        global start2
        global start3
        global fcount
        global modey
        frontRate = RateGet(shootEncoder.GetRaw(),"se")
        backRate = RateGet(feedEncoder.GetRaw(),"fe")


        #forward 13669
        #turn 1534 ~error 30 clicks.
        #-26490

        #autonomous center
        #-14000

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
        magic1.Set(False)
        magic2.Set(True)
        hopper1.Set(False)
        hopper2.Set(True)
        
        SmartDashboard.PutString("DRIVE REVERSAL STATE:  ", "LALALAL BLANDA")

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
        global start2
        global hop
        global direction
        global dire
        global lsense
        global rsense
        global mode
        global fnum
        global bnum
        global modey

        #Rates
        frontRate = RateGet(shootEncoder.GetRaw(),"se")
        backRate = RateGet(feedEncoder.GetRaw(),"fe")


        #sensitivity
        lsense = (lstick.GetThrottle() -1)*(-0.5)
        rsense = (rstick.GetThrottle() -1)*(-0.5)

        # Drive control
        if lstick.GetRawButton(2) and dire==False:
            direction = direction*-1
            dire=True
        if not lstick.GetRawButton(2) and dire==True:
            dire=False
        drive.ArcadeDrive(lstick.GetY()*direction,lstick.GetX())

		#manual shooter controls
        if rstick.GetRawButton(11):				#right button 11 increments FRONT
            modey = "MANUAL"
            mode = 99
            frontValue += .05*rsense
            if frontValue > 1:
                frontValue = 1
            print("Front: "+str(int(frontValue*100)))
        elif rstick.GetRawButton(10):				#right button 10 decrements FRONT
            modey = "MANUAL"
            mode = 99
            frontValue -= .05*rsense
            if frontValue < 0:
                frontValue = 0
            print("Front: "+str(int(frontValue*100)))
        if rstick.GetRawButton(6):				#right button 6 increments BACK
            modey = "MANUAL"
            mode = 99
            backValue += .05*rsense
            if backValue > 1:
                backValue = 1
            print("Back: "+str(int(backValue*100)))
        elif rstick.GetRawButton(7):				#right button 7 decrements BACK
            modey = "MANUAL"
            mode = 99
            backValue-= .05*rsense
            if backValue < 0:
                backValue = 0
            print("Back: "+str(int(backValue*100 )))

	#Button Control Presets
        if rstick.GetRawButton(3) and mode != 0:                        #shooter off
            mode = 0
            #print("Shooters Off")
            modey = "OFF"
        if rstick.GetRawButton(5) and mode!=1 and magic1.Get() == False: #tower angle preset
            mode = 1
            #print("Tower Preset")
            modey = "AUTO: Tower Angle Preset" 
            backValue = .531
            frontValue = 1
            fnum = 1500
            bnum = 2270
        if rstick.GetRawButton(5) and mode!=2 and magic1.Get() == True: #magic jack preset
            mode = 2
            #print("Magic Preset")
            modey = "AUTO: Magic Jack Preset"
            backValue = .636
            frontValue = 1
            fnum = 2400
            bnum = 880
        if rstick.GetRawButton(2) and mode!=3:                          #tower center preset
            mode = 3
            #print("Tower Center Preset")
            modey = "AUTO: Tower Center Preset"
            backValue = .380
            frontValue = .8 #1
            fnum = 1500
            bnum = 2400


        #AUTO shooter PRESET CONTROLS
        if mode == 0: #Turn off the shooter
            if frontValue != 0:
            	frontValue = 0
            if backValue != 0:
            	backValue = 0
            if fnum != 0:
            	fnum = 0
            if bnum != 0:
            	bnum = 0
        elif mode != 0 and mode != 99: #Encoder preset at tower
             frontValue = FrontEncoderSet(frontRate, fnum, 10, frontValue)
             backValue = BackEncoderSet(backRate, bnum, 10, backValue)
        forwardShooter.Set(frontValue)
        backShooter.Set(backValue)

        #Shooter piston control
        if rstick.GetTrigger() and fire==False: 			#if trigger pulled and currently not firing
            fire = True
            start = timer.Get() #mark the time
            #print("Shooter: "+str(RateGet(shootEncoder.GetRaw(),"se"))+" Feeder: "+str(RateGet(feedEncoder.GetRaw(),"fe")))
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

        if rstick.GetRawButton(4):
            print(str(frontRate)+":"+str(shootEncoder.GetRaw())+":"+str(frontValue)+"|"+str(backRate)+":"+str(feedEncoder.GetRaw())+":"+str(backValue))

       
        if lstick.GetTrigger() and hop==False:
            hopper1.Set(not hopper1.Get())
            hopper2.Set(not hopper2.Get())
            hop=True
        if not lstick.GetTrigger() and hop==True:
            hop=False


        #Magic Jacks
        if ((lstick.GetRawButton(7)) or (rstick.GetRawButton(8))) and jackItUp==False:	#button 8 and 9 at same time to toggle jacks
            magic1.Set(not magic1.Get())
            magic2.Set(not magic2.Get())
            jackItUp=True
        if ((not lstick.GetRawButton(7)) and (not rstick.GetRawButton(8))) and jackItUp==True:
            jackItUp=False
        
        if modey == "":
            modey = "MANUAL SHOOTER CONTROL"
        
        SmartDashboard.PutString("Mode","SHOOTER CONTROL MODE:  " + modey) #         Display shooter control mode
        SmartDashboard.PutNumber("FRONT ENCODER VALUE:  ", frontRate)
        SmartDashboard.PutNumber("FRONT PERCENTAGE VALUE:  ", frontValue*100)
        SmartDashboard.PutNumber("BACK ENCODER VALUE:  ", backRate)
        SmartDashboard.PutNumber("BACK PERCENTAGE VALUE:  ", backValue*100)
        SmartDashboard.PutString("DRIVE REVERSAL STATE:  ", str(dire))
        
        
        


def run():
    robot = MyRobot()
    robot.StartCompetition()