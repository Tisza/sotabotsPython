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
shootEncoder = wpilib.Encoder( robotMap.shootEncoder1 , robotMap.shootEncoder2 , True, wpilib.CounterBase.k1X)
feedEncoder = wpilib.Encoder(robotMap.feedEncoder1, robotMap.feedEncoder2, True, wpilib.CounterBase.k1X)
leftDriveEncoder = wpilib.Encoder( robotMap.leftDriveEncoder1 , robotMap.leftDriveEncoder2 , True, wpilib.CounterBase.k4X)
rightDriveEncoder = wpilib.Encoder( robotMap.rightDriveEncoder1 , robotMap.rightDriveEncoder2 , True, wpilib.CounterBase.k4X)

encoderHighTest = wpilib.DigitalOutput(9)

#initialize smartDashboard
SmartDashboard.init()

#variables
frontValue = 0
deltaFront = 0
backValue = 0
deltaBack = 0
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
updateCycles = 0



#drive train
drive = wpilib.RobotDrive(leftMotor,rightMotor)


#network table initilization
#table = wpilib.NetworkTable.GetTable("SmartDashboard")

#timer
timer = wpilib.Timer()
start = 0
start2 = 0


def CheckRestart():
    if rstick.GetRawButton(15):
        raise RuntimeError("SystemRestart")
        print("CheckRestart")

def RateGet(rawDistance, lastDistance):
    rate = ld[lastDistance] - rawDistance
    ld[lastDistance] = rawDistance
    return rate

def FrontEncoderSet(rate, desiredrate, variance, initVal):             #separate function for encoder-motor logic. NO MORE CONFUSION FOR US!
    if rate - desiredrate > -variance and rate - desiredrate < variance:
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

def BackEncoderSet(rate, desiredrate, variance, initVal):              #separate function for redundancy :D
    if rate - desiredrate > -variance and rate - desiredrate < variance:
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
        global start
        global start2
        global fcount
        self.GetWatchdog().SetEnabled(False)
        leftDriveEncoder.Start()
        rightDriveEncoder.Start()
        compressor.Start()
        shootEncoder.Start()
        feedEncoder.Start()
        timer.Start()
        stage = 1
        leftDriveEncoder.Reset()
        print("Stage 1")
        start = 0
        start2 = 0
        fcount = 0

    def AutonomousPeriodic(self):
        CheckRestart()
        global stage
        global frontValue
        global backValue
        global fire
        global start
        global start2
        global fcount
        global updateCycles
        #frontRate = RateGet(shootEncoder.GetRaw(),"se")
        backRate = RateGet(feedEncoder.GetRaw(),"fe")
        ###variables
        forward = 13500
        turn = 1500
        backAdjust = 5000
        backOff = 16000
        bnum = -2500

        if stage == 0: #Null
            drive.ArcadeDrive(0,0)

        if stage == 1: #First Stage - FORWARD
            drive.ArcadeDrive(-.7,-.1)
            frontValue = .7
            backValue = .7
            if leftDriveEncoder.GetRaw()>forward: #and rightDriveEncoder.GetRaw()>forward:
                print("Stage 2")
                stage = 2
                leftDriveEncoder.Reset()
                rightDriveEncoder.Reset()

        if stage == 2: #Second Stage - TURNING
            drive.ArcadeDrive(0,.7)
            if leftDriveEncoder.GetRaw()>turn: #and rightDriveEncoder.GetRaw()<-turn:
                print("Stage 3")
                stage = 3
                leftDriveEncoder.Reset()
                rightDriveEncoder.Reset()

        if stage == 3: #Third Stage - BACK IT UP
            drive.ArcadeDrive(.7,0)
            if leftDriveEncoder.GetRaw()<-backAdjust: #and rightDriveEncoder.GetRaw()<-backAdjust:
                stage("Stage 4")
                stage = 4
                leftDriveEncoder.Reset()
                rightDriveEncoder.Reset()

        if stage == 4:#Fourth Stage - SHOOT!
            drive.ArcadeDrive(0,0)
            #Encoder speeding
            backValue = .7
            #shoot command
            if (backRate > bnum - 50 and backRate < bnum + 50) and fire == False and start2 == 0:
                fire = True
                start = timer.Get()
            #kill shooting
            if fcount > 3:
                print("Stage 5")
                stage = 5
                frontValue = 0
                backValue = 0

        if stage == 5: #Fifth Stage - TURN BACK
            drive.ArcadeDrive(0,-.7)
            if leftDriveEncoder.GetRaw()<-turn: #and rightDriveEncoder.GetRaw()>turn:
                print("Stage 6")
                stage = 6
                leftDriveEncoder.Reset()
                rightDriveEncoder.Reset()

        if stage == 6: #Sixth Stage - BACK OFF BRO
            drive.ArcadeDrive(.7,0)
            if leftDriveEncoder.GetRaw()<-backOff: #and rightDriveEncoder.GetRaw()<-backOff:
                print("Finished")
                stage = 0

        #Shooter Speed Setting
        forwardShooter.Set(frontValue)
        backShooter.Set(backValue)
        #SmartDrashboard Controls
        #SmartDashboard.PutNumber("FRONT ENCODER VALUE:  ", frontRate)
        #SmartDashboard.PutNumber("FRONT PERCENTAGE VALUE:  ", frontValue*100)
        #SmartDashboard.PutNumber("BACK ENCODER VALUE:  ", backRate)
        #Shooting
        if fire == True:
            loader1.Set(False )
            loader2.Set(True )
        else:
            loader1.Set(True )
            loader2.Set(False )
        #Retract piston after .2 of a second
        if timer.Get() > start + 0.2:
            fire = False
            start2 = timer.Get()
            start = 0
            fcount += 1
        #Wait for a reload
        if timer.Get() > start2 + 1:
            start2 = 0

        if updateCycles < 20:
                updateCycles+=1
        else:
                SmartDashboard.PutNumber("BACK ENCODER VALUE:  ", backRate)
                SmartDashboard.PutNumber("BACK PERCENTAGE VALUE:  ", backValue*100)
                SmartDashboard.PutNumber("DRIVE ENCODER DISTANCE: ", leftDriveEncoder.GetRaw())
                updateCycles = 0

        #forward 13669
        #turn 1534 ~error 30 clicks.
        #-26490

        #autonomous center
        #-14000

    def TeleopInit(self):
        global frontValue
        global deltaFront
        global backValue
        global deltaBack
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
        forwardShooter.Set(0)
        backShooter.Set(0)



        #starting positions
        magic1.Set(False)
        magic2.Set(True)
        hopper1.Set(False)
        hopper2.Set(True)

        SmartDashboard.PutString("DRIVE REVERSAL STATE:  ", "BACKWARD")

    def TeleopPeriodic(self):
        self.GetWatchdog().Feed()
        CheckRestart()
        global frontValue
        global deltaFront
        global backValue
        global deltaBack
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
        global updateCycles

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
            if direction == 1:
                dirstr = "FORWARD"
            if direction == -1:
                dirstr = "BACKWARD"
            SmartDashboard.PutString("DRIVE REVERSAL STATE:  ", dirstr)
        if not lstick.GetRawButton(2) and dire==True:
            dire=False
        drive.ArcadeDrive(lstick.GetY()*direction,lstick.GetX())

		#manual shooter controls
        if rstick.GetRawButton(11):				#right button 11 increments FRONT
            mode = 99
            frontValue += .05*rsense
            if frontValue > 1:
                frontValue = 1
            print("Front: "+str(int(frontValue*100)))
        elif rstick.GetRawButton(10):				#right button 10 decrements FRONT
            mode = 99
            frontValue -= .05*rsense
            if frontValue < 0:
                frontValue = 0
            print("Front: "+str(int(frontValue*100)))
        if rstick.GetRawButton(6):				#right button 6 increments BACK
            mode = 99
            backValue += .05*rsense
            if backValue > 1:
                backValue = 1
            print("Back: "+str(int(backValue*100)))
        elif rstick.GetRawButton(7):				#right button 7 decrements BACK
            mode = 99
            backValue-= .05*rsense
            if backValue < 0:
                backValue = 0
            print("Back: "+str(int(backValue*100 )))

	#Button Control Presets
        if rstick.GetRawButton(3) and mode != 0:                        #shooter off
            mode = 0
            #print("Shooters Off")
        if rstick.GetRawButton(5) and mode!=1 and magic1.Get() == False: #tower angle preset
            mode = 1
            #print("Tower Preset")
            backValue = .7
            frontValue = .75
            #fnum = 1500
            #bnum = 2270
        if rstick.GetRawButton(5) and mode!=2 and magic1.Get() == True: #magic jack preset
            mode = 2
            #print("Magic Preset")
            backValue = .85
            frontValue = .85
            fnum = 2400
            bnum = 880
        if rstick.GetRawButton(2) and mode!=3:                          #tower center preset
            mode = 3
            #print("Tower Center Preset")
            backValue = .7
            frontValue = .72 #1
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
        elif mode != 0 and mode != 99: #Encoder preset at tower                 #############
             frontValue = frontValue      ##
             backValue = backValue      ##change this back to backrate for competition!!!

        if frontValue != deltaFront:
            deltaFront = frontValue
            forwardShooter.Set(frontValue)
            SmartDashboard.PutNumber("FRONT PERCENTAGE VALUE:  ", frontValue*100)
        if backValue != deltaBack:
            deltaBack = backValue
            backShooter.Set(backValue)
            SmartDashboard.PutNumber("BACK PERCENTAGE VALUE:  ", backValue*100)


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


        #Mode setting
        if modey == "":
            modey = "MANUAL SHOOTER CONTROL"
        if mode == 99 and modey != "MANUAL":
            modey = "MANUAL"
            SmartDashboard.PutString("Mode","SHOOTER CONTROL MODE:  " + modey)
        if mode == 0 and modey != "OFF":
            modey = "OFF"
            SmartDashboard.PutString("Mode","SHOOTER CONTROL MODE:  " + modey)
        if mode == 1 and modey != "AUTO: Tower Angle Preset":
            modey = "AUTO: Tower Angle Preset"
            SmartDashboard.PutString("Mode","SHOOTER CONTROL MODE:  " + modey)
        if mode == 2 and modey != "AUTO: Magic Jack Preset":
            modey = "AUTO: Magic Jack Preset"
            SmartDashboard.PutString("Mode","SHOOTER CONTROL MODE:  " + modey)
        if mode == 3 and modey != "AUTO: Tower Center Preset":
            modey = "AUTO: Tower Center Preset"
            SmartDashboard.PutString("Mode","SHOOTER CONTROL MODE:  " + modey)

        if modey != "OFF":                                                          #prints encoder values only when running; every 20 loops
            if updateCycles < 20:
                updateCycles+=1
            else:
                SmartDashboard.PutNumber("FRONT ENCODER VALUE:  ", frontRate)
                SmartDashboard.PutNumber("BACK ENCODER VALUE:  ", backRate)
                updateCycles = 0
                
        encoderHighTest.EnablePWM(1)
        encoderHighTest.Set(1)

def run():
    robot = MyRobot()
    robot.StartCompetition()
