Assignement number #1
=================

I uploaded on this repository my humble solution to the first assignement of Research Track 1 where we ask a robot in a some environement to drive itself and pick up a silver box and put it next a golden one, until all 6 pairs are done!

### The Grabber

The robot has a grabber that can pick up a token that is in front of it and within 0.4 meters of its center. We invoke the "R.grab" method to grab a token. In the event that a token was successfully picked up, the "R.grab" method returns "True," else "False."

```python
 R.grab()
```
To release the token we use the method:

```python
 R.release()
```

### Global variables:

<br>a_th : The threshold for controlling the linear distance. </br>
d_th : The threshold for controlling the orientation.

<br> silverList = [] : List contains the codes of silver boxes.</br>
goldenList = [] : List contains the codes of golden boxes.	

I created several functions to be used in the main function :

### Drive and Turn functions:

These functions were kindly provided by the environement maker and are the same of exercise 1.

### find_ungrabbed_silver_token:

This function searches for silver tokens and checks if the token code is already stored in the Silver_Codes list, Which means that the token is already grabbed, so it doesn't grab it and look for another token.
<pre>
find_silver_token():
 	dist=100
	for token in R.see(): 
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.info.code not in Silver_Codes:
			dist=token.dist
			rot_y=token.rot_y
			Token_Codes=token.info.code
	if dist==100:
		return -1, -1 ,-1
	else:    
		return dist, rot_y, Token_Codes
</pre>

The following line should be added to the previous if loop in order to display the grabbed box ID
<pre>
print (MARKER_TOKEN_SILVER)
</pre>

### find_unpaired_golden_token:

This function searches for golden tokens and checks if the token code is already paired in the Golden_Codes list, which means that the token is already paired, so it looks for another golden token.
<pre>
dist=100
	for token in R.see(): 
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.code not in Golden_Codes:
			dist=token.dist
			rot_y=token.rot_y
			Token_Codes=token.info.code
	if dist==100:
		return -1, -1, -1
	else:
		
		return dist, rot_y, Token_Codes
</pre>

### Sign:

This function simply returns 1 for positive number and -1 for negative number.
<pre>
def sign(a):
	if a < 0:
		return -1
	else:
		return 1
</pre>

### put_silver_with_golden:

This function is basically the main function, it combines all the previously mentioned functions and combine them in a way to make the robot do the "put silver with golden" six times (which is the number of silver and golden boxes) and print at the end task completed. 
<pre>
while (len(Golden_Codes)<7):
		dist, rot_y, Token_Codes = find_ungrabbed_silver_token() 
		if dist==-1:
		    turn(10,0.1)
		    continue
		while(dist<0):   
			turn(-5,0.01)
			dist, rot_y, Token_Codes = find_ungrabbed_silver_token()
		while (rot_y >= a_th or rot_y<=-a_th) : 
			turn(sign(rot_y-a_th) * 10,0.001) 
			dist, rot_y,Token_Codes = find_ungrabbed_silver_token()
		while (dist >= d_th) : 
			drive(30,0.01)
			dist, rot_y, Token_Codes = find_ungrabbed_silver_token()
	    	Silver_Codes.append(Token_Codes)
	    	print("Found you silver box number:",len(Silver_Codes))
	    	R.grab()
	    	turn(20,0.1)
		print("Let's pair you with an unpaired golden box!")
		dist, rot_y, Token_Codes = find_unpaired_golden_token()
		while(dist<0):
			turn(-5,0.01)
			dist, rot_y, Token_Codes = find_unpaired_golden_token()
	    	while (rot_y >= a_th or rot_y<=-a_th) :
			turn(sign(rot_y-a_th) * 10,0.001)
			dist, rot_y, Token_Codes= find_unpaired_golden_token()
	    	while (dist >= 1.5*d_th) :
			drive(40,0.01)
			dist, rot_y, Token_Codes= find_unpaired_golden_token()
	    	R.release()
	    	Golden_Codes.append(Token_Codes)
	    	print("Gotcha golden box number:",len(Golden_Codes))
	    	drive(-50,0.8)
		if (len(Golden_Codes)==6):
			print("Task completed")
			exit() 
</pre>

