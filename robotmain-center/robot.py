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

    def AutonomousPeriodic(self):
        CheckRestart()
        global stage
        global frontValue
        global backValue
        global fire
        global start
        global start3
        global fcount
        frontRate = RateGet(shootEncoder.GetRaw(),"se")
        backRate = RateGet(feedEncoder.GetRaw(),"fe")

        #Modulated processes
        if fire==False and fcount < 3:
            fire = True
            start = timer.Get()
        if start != 0: #Shooting
            loader1.Set(False) #marked time = fire
            loader2.Set(True)
            print("Fire")
        else:
            loader1.Set(True )
            loader2.Set(False )
        if timer.Get() > start+0.2 and fire==True and start3 == 0: #if half a second has passed, stop firing
            start = 0
            fcount += 1
            start3 = timer.Get()
            print("Wait...")
        if timer.Get() > start3 + 3 and start3!=0:
            fire = False
            start3 = 0
			
			
        ######autonomous center######
        if stage == 0:
            start = 0 
            frontValue = 1
            backValue = 0.58
            drive.ArcadeDrive(0,0)
            fcount=1
            start3 = timer.Get()
            fire = True
            stage = 1
            print("Inisialized")
        if stage == 1:
            drive.ArcadeDrive(0,0)
            if(backRate - 2400 < 50 and backRate - 2400 > -50):
                    if fire==False: 			#if trigger pulled and currently not firing
                        fire = True
                        start = timer.Get() #mark the time
                        print("Fire "+str(fcount)+"|||"+str(frontRate)+" | "+str(backRate))
                    backValue = backValue
            elif backRate > 2400:
                    backValue -= 0.003
            elif backRate < 2400:
                    backValue += 0.003
            else:
                frontValue = 0
                backValue = 0
            if frontValue >1:
                frontValue = 1
            if backValue >1:
                backValue = 1
            if frontValue < 0:
                frontValue = 0
            if backValue < 0:
                backValue = 0
            forwardShooter.Set(frontValue)
            backShooter.Set(backValue)

            if fcount > 2:
                stage = 3
                forwardShooter.Set(0)
                backShooter.Set(0)
                frontValue = 0
                backValue = 0
                print("Stage 2")
        if stage == 2:
            drive.ArcadeDrive(0.7,0)
            if leftDriveEncoder.GetRaw()<-8000:
                drive.ArcadeDrive(0,0)
                leftDriveEncoder.Reset()
                stage=3
                print("Finished")

        if stage == 3:
            drive.ArcadeDrive(0,0)

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
        drive.ArcadeDrive(lstick.GetY()*direction*lsense,lstick.GetX()*lsense)

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
        if rstick.GetRawButton(3) and mode != 0:
            mode = 0
            print("Shooters Off")
        if rstick.GetRawButton(5) and mode!=1 and magic1.Get() == False:
            mode = 1
            print("Tower Preset")
            backValue = .531
            frontValue = 1
            fnum = 1500
            bnum = 2270
        if rstick.GetRawButton(5) and mode!=2 and magic1.Get() == True:
            mode = 2
            print("Magic Preset")
            backValue = .636
            frontValue = 1
            fnum = 2400
            bnum = 880
        if rstick.GetRawButton(2) and mode!=3:
            mode = 3
            print("Tower Center Preset")
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
            if frontRate + fnum < 10 and frontRate + fnum > -10: #front auto
                    frontValue = frontValue
            elif frontRate > fnum:
                    frontValue += 0.0015
            elif frontRate < fnum:
                    frontValue -= 0.0015
            if backRate - bnum < 10 and backRate - bnum > -10: #back auto
                    backValue = backValue
            elif backRate > bnum:
                    backValue -= 0.0015
            elif backRate < bnum:
                    backValue += 0.0015
        if frontValue >1:
            frontValue = 1
        if backValue >1:
            backValue = 1
        if frontValue < 0:
            frontValue = 0
        if backValue < 0:
            backValue = 0
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

        #hopper piston control
        """if rstick.GetRawButton(2) and hop==False:
            hop = True
            start2 = timer.Get()
        if start2 != 0:
            hopper1.Set(False)
            hopper2.Set(True)
        else:
            hopper1.Set(True)
            hopper2.Set(False)
        if (timer.Get() > start2+.5) and magic1.Get()==True: #and magic1.Get()==True:  #.2 second interval for hopper piston
            start2 = 0
        if (timer.Get() > start2+.5) and magic1.Get()==False:
            start2 = 0
        if start == 0 and not rstick.GetRawButton(2):
            hop = False"""
        #claws Repurposed from Hopper
        if lstick.GetRawButton(9) and hop==False:
            hopper1.Set(not hopper1.Get())
            hopper2.Set(not hopper2.Get())
            hop=True
        if not lstick.GetRawButton(9) and hop==True:
            hop=False


        #Magic Jacks
        if ((lstick.GetRawButton(8)) or (rstick.GetRawButton(8))) and jackItUp==False:	#button 8 and 9 at same time to toggle jacks
            magic1.Set(not magic1.Get())
            magic2.Set(not magic2.Get())
            jackItUp=True
        if ((not lstick.GetRawButton(8)) and (not rstick.GetRawButton(8))) and jackItUp==True:
            jackItUp=False

        #lift controls
        """if rstick.GetRawButton(10):
            if liftTopSwitch.Get()==1:
                drumMotor.Set(rsense)
            else:
                drumMotor.Set(0)
            dawg1.Set(False)
            dawg2.Set(True)
        elif rstick.GetRawButton(11):
            if liftBottomSwitch.Get()==1:
                drumMotor.Set(-rsense)
            else:
                drumMotor.Set(0)
            if dawg1.Get()==False:
                dawg1.Set(True)
                dawg2.Set(False)
        else:
            drumMotor.Set(0)
        if rstick.GetRawButton(4): #Unhitch the dog.
            drumMotor.Set(rsense)
            dawg1.Set(True)
            dawg2.Set(False)

       #arm controls
        if rstick.GetRawButton(6):
            weeWooMotor.Set(rsense)
        elif rstick.GetRawButton(7):
            if armLimitSwitch.Get()==1:
                weeWooMotor.Set(-rsense)
            else:
                weeWooMotor.Set(0)
        else:
            weeWooMotor.Set(0)

        #Dawg Controls
        if rstick.GetRawButton(9) and doggie == False:
            dawg1.Set(not dawg1.Get())
            dawg2.Set(not dawg2.Get())
            doggie = True
            print("Dog Enabled:"+str(dawg1.Get()))
        if not rstick.GetRawButton(9) and doggie == True:
            doggie = False"""


def run():
    robot = MyRobot()
    robot.StartCompetition()