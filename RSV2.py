#!/usr/bin/python3

from inputs import get_gamepad
import subprocess

def getStickPos(x, y):
	position = -1
	xmovedleft = False  # x centre position = 128
	xmovedright = False
	ymovedup = False  # y centre position = 128
	ymoveddown = False

	if x<50:
		xmovedleft = True
	if x>200:
		xmovedright = True
	if y<50:
		ymovedup = True
	if y>200:
		ymoveddown = True

	if ymovedup and not xmovedright and not xmovedleft:
		position = 0
	if ymovedup and xmovedright:
		position = 1
	if not ymovedup and not ymoveddown and xmovedright:
		position = 2
	if ymoveddown and xmovedright:
		position = 3
	if ymoveddown and not xmovedright and not xmovedleft:
		position = 4
	if ymoveddown and xmovedleft:
		position = 5
	if not ymoveddown and not ymovedup and xmovedleft:
		position = 6
	if ymovedup and xmovedleft:
		position = 7

	return(position)

def DOIR(command):
	print(command)
	subprocess.call(["irsend", "SEND_ONCE", "RSV2", command])

leftStickMoved = False
rightStickMoved = False
leftStickX = 128
leftStickY = 128
rightStickX = 128
rightStickY = 128

shiftButtons = 0
leftStickPreviousPos = -1
rightStickPreviousPos = -1

R = ("HEAD_UPPER_BODY", "RIGHT_ARM", "LEFT_ARM", "BOTH_ARMS", "HIP_WAIST", "HEAD_ONLY", "HEAD+UB", "UPPER_BODY") 
D = ("DANCE_DEMO", "MOVEMENT_DEMO", "DOWN_UP_DOWN_UP", "HIGH_FIVE", "OOPS", "HEY_BABY", "BURP", "DONT_PRESS")
S = ("STOP", "RESET", "SLEEP_WAKEUP", "CLEAR_PROGRAM", "GET_UP", "BULLDOZER_FORWARD", "BULLDOZER_BACKWARD", "POWER_DOWN")
a = ("SONIC_SENSORS_ON_OFF", "RIGHT_ARM_THROW", "LEFT_ARM_THROW", "SOUND_PROGRAM", "RIGHT_KICK", "LAUGH", "ROAR", "ROBOSAPIEN_V2_INTERACT")
b = ("VISION_SYSTEMS_ON_OFF", "RIGHT_ARM_LOW_PICKUP", "LEFT_ARM_LOW_PICKUP", "VISION_PROGRAM", "RIGHT_PUSH", "INSULT", "DIODE", "ROBORAPTOR_INTERACT")
c = ("POSITIONAL_PROG_ENTRY", "RIGHT_ARM_HIGH_PICKUP", "LEFT_ARM_HIGH_PICKUP", "MAIN_PROGRAM", "RIGHT_CHOP", "RIGHT_ARM_DROP", "FETCH", "ROBOPET_INTERACT")
x = ("POSITIONAL_PROG_PLAY", "RIGHT_ARM_GRAB", "LEFT_ARM_GRAB", "PERFORM_PROGRAM", "LEFT_CHOP", "LEFT_ARM_DROP", "DANGER", "COLOUR_MODE_DAYLIGHT")
y = ("GAIT_CHANGE", "RIGHT_ARM_GIVE", "LEFT_ARM_GIVE", "GUARD_MODE", "LEFT_PUSH", "PLAN", "CALM_DOWN", "COLOUR_MODE_YELLOW")
z = ("FREE_ROAM", "RIGHT_ARM_ROLL", "LEFT_ARM_ROLL", "CLEAR_ENTRY", "LEFT_KICK", "SPARE_CHANGE", "HUG", "COLOUR_MODE_WHITE")

while True:

	events = get_gamepad()
	for event in events:

		# Capture state of the shift buttons
		# 0 to 7 to use with each button's tuple
		if event.code == "BTN_WEST":
			if event.state == 1:
				shiftButtons += 1
			else:
				shiftButtons -= 1
		if event.code == "BTN_Z":
			if event.state == 1:
				shiftButtons += 2
			else:
				shiftButtons -= 2
		if event.code == "BTN_TL":
			if event.state == 1:
				shiftButtons += 4
			else:
				shiftButtons -= 4
		# b button
		if event.code == "ABS_HAT0Y":
			if event.state == 1:
				DOIR(b[shiftButtons])
		# S button
			if event.state == -1:
				DOIR(S[shiftButtons])
		# c button
		if event.code == "ABS_HAT0X":
			if event.state == 1:
				DOIR(c[shiftButtons])
		# a button
			if event.state == -1:
				DOIR(a[shiftButtons])
		# D button
		if event.code == "BTN_NORTH":
			if event.state == 1:
				DOIR(D[shiftButtons])
		# x button
		if event.code == "BTN_SOUTH":
			if event.state == 1:
				DOIR(x[shiftButtons])
		# y button
		if event.code == "BTN_EAST":
			if event.state == 1:
				DOIR(y[shiftButtons])
		# z button
		if event.code == "BTN_C":
			if event.state == 1:
				DOIR(z[shiftButtons])
		# Left stick
		if event.code == "ABS_X":
			leftStickX = event.state
			leftStickMoved = True
		if event.code == "ABS_Y":
			leftStickY = event.state
			leftStickMoved = True
		if leftStickMoved:
			leftStickPos = getStickPos(leftStickX, leftStickY)
			if leftStickPos != -1 and leftStickPreviousPos != leftStickPos:
				DOIR("WALKING_" + str(leftStickPos))
			leftStickMoved = False
			leftStickPreviousPos = leftStickPos
		# Right stick
		if event.code == "ABS_Z":
			rightStickX = event.state
			rightStickMoved = True
		if event.code == "ABS_RZ":
			rightStickY = event.state
			rightStickMoved = True
		if rightStickMoved:
			rightStickPos = getStickPos(rightStickX, rightStickY)
			if rightStickPos != -1 and rightStickPreviousPos != rightStickPos:
				DOIR(R[shiftButtons] + "_" + str(rightStickPos))
			rightStickMoved = False
			rightStickPreviousPos = rightStickPos
