from sr.robot import *
import time

R = Robot()
a_th = 1.5  # The threshold for controlling the linear distance
d_th = 0.4  # The threshold for controlling the orientation

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

Silver_Codes = []  # list of silver tokens codes that are grabbed.
Golden_Codes = []  # list of golden tokens codes that are paired.

def fetch_ungrabbed_silver_block():
    dist = 100
    for token in R.see():
        if (
            token.dist < dist
            and token.info.marker_type is MARKER_TOKEN_SILVER
            and token.info.code not in Silver_Codes
        ):
            dist = token.dist
            rot_y = token.rot_y
            Token_Codes = token.info.code
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, Token_Codes

def fetch_unpaired_golden_block():
    dist = 100
    for token in R.see():
        if (
            token.dist < dist
            and token.info.marker_type is MARKER_TOKEN_GOLD
            and token.info.code not in Golden_Codes
        ):
            dist = token.dist
            rot_y = token.rot_y
            Token_Codes = token.info.code
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, Token_Codes

def sign(a):
    return -1 if a < 0 else 1

def pair_silver_block_with_golden_block():
    while len(Golden_Codes) < 7:
        dist, rot_y, Token_Codes = fetch_ungrabbed_silver_block()
        if dist == -1:
            turn(10, 0.1)
            continue

        while dist < 0:
            turn(-5, 0.01)
            dist, rot_y, Token_Codes = fetch_ungrabbed_silver_block()

        while rot_y >= a_th or rot_y <= -a_th:
            turn(sign(rot_y - a_th) * 10, 0.001)
            dist, rot_y, Token_Codes = fetch_ungrabbed_silver_block()

        while dist >= d_th:
            drive(30, 0.01)
            dist, rot_y, Token_Codes = fetch_ungrabbed_silver_block()

        Silver_Codes.append(Token_Codes)
        print("Found your silver box number:", len(Silver_Codes))
        R.grab()
        turn(20, 0.1)

        print("Let's pair you with an unpaired golden box!")
        dist, rot_y, Token_Codes = fetch_unpaired_golden_block()

        while dist < 0:
            turn(-5, 0.01)
            dist, rot_y, Token_Codes = fetch_unpaired_golden_block()

        while rot_y >= a_th or rot_y <= -a_th:
            turn(sign(rot_y - a_th) * 10, 0.001)
            dist, rot_y, Token_Codes = fetch_unpaired_golden_block()

        while dist >= 1.5 * d_th:
            drive(40, 0.01)
            dist, rot_y, Token_Codes = fetch_unpaired_golden_block()

        R.release()
        Golden_Codes.append(Token_Codes)
        print("Gotcha golden box number:", len(Golden_Codes))
        drive(-50, 0.8)

        if len(Golden_Codes) == 6:
            print("Task completed")
            exit()

pair_silver_block_with_golden_block()

