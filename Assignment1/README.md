Research Track 1 : Assignment Undertaken Number #1
====================================================

## Aim Of The Assignment 

On this repository, I have the privilege to sahre whith you my modest response to the Research Track's first assignment, wherein we tasked a robot to move autonomously around its environment and pick up a silver box afterwards deposite it next a golden one until all six pairings were completed.


## Our Grabber Robot

When a token is placed in front of the robot and within 0.4 meters of its center, our robot, which contains a grabber, will grab this token using the "R.grab" function. If a token was successfully picked up, the "R.grab" function returns "True," or "False" in the opposite case.


```python
 R.grab()
```
In order to drop a token we use the method:

```python
 R.release()
```

## The Global Variables:

<br>a_th : The threshold for controlling the linear distance. </br>
d_th : The threshold for controlling the orientation.

<br> Silver_Codes = [] : list of silver tokens codes that are grabbed.</br>
Golden_Codes = [] : list of golden tokens codes that are paired.	

In order to process the aimed task of our robot, each function created in our program has its speacial role to execute, and all together are used in the main function :

## Drive and Turn functions:

These two functions are mainly to control the behaviour of motors, they make our robot to drive forward with a fixed speed or Turning with a specific orientation and they were given by the environement maker.
<pre>
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    </pre>
<pre>
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
</pre>
    
## fetch_ungrabbed_silver_block:

This function allows us to find the closest silver token and grabbing it. Meanwhile, it will never pick up an already taken silver token. In other words, this function has the role to look for a silver token and verify if it was grabbed before or not by checking the token code stored in the Silver_Codes list.  

<pre>
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
</pre>

The following line should be added to the previous if loop in order to display the grabbed box ID
<pre>
print (MARKER_TOKEN_SILVER)
</pre>

## fetch_unpaired_golden_block :

This function allows us to find the closest unpaired golden tokens by checking if the token code is already paired in the Golden_Codes list. In case of a paired token, our robot will look for another golden token.
<pre>
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
</pre>

## Sign:

This function simply returns 1 for positive number and -1 for negative number.
<pre>
def sign(a):
	return -1 if a < 0 else 1
</pre>

## pair_silver_block_with_golden_block:

This is the main function of our code that combines all the above mentioned functions, it has the role to make our robot release silver token near to golden token six times (which is the number of silver and golden tokens) then ending the task when there is no silver token lef and printing at the end task completed. 
<pre>
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
</pre>

