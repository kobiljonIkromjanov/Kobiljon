//#!/usr/bin/env node
///////////////
var spawn = require('child_process').spawn;
////////////////
var unlockedState = 1000;
var lockedState = 2200;

var motorPin = 14;
var buttonPin = 10;
var ledPin = 9;

var blynkToken = '98987772f49c40b59a82cdc427a01aa3';

// *** Start code *** //

var locked = true;


//Setup servo
var Gpio = require('pigpio').Gpio,
  motor = new Gpio(motorPin, {mode: Gpio.OUTPUT}),
  button = new Gpio(buttonPin, {
   mode: Gpio.INPUT,
 pullUpDown: Gpio.PUD_DOWN,
  edge: Gpio.FALLING_EDGE
  })
  ,
  led = new Gpio(ledPin, {mode: Gpio.OUTPUT});


//Setup blynk
var Blynk = require('blynk-library');
var blynk = new Blynk.Blynk(blynkToken);
var v0 = new blynk.VirtualPin(0);
var v1 = new blynk.VirtualPin(1);
var v2 = new blynk.VirtualPin(2);

console.log("locking door")
lockDoor()
button.on('interrupt', function (level) {
	console.log("level: " + level + " locked:  " + locked)
	if (level == 0) {
		if (locked) {
			unlockDoor()
		} else {
			lockDoor()
		}
	}
});

v0.on('write', function(param) {
	console.log('V0:', param);
  	if (param[0] === '0') { //unlocked
  		unlockDoor()
  	} else if (param[0] === '1') { //locked
  		lockDoor()                               
  	} else {
  		blynk.notify("Door lock button was pressed with unknown parameter");
  	}
});
v1.on('write', function(param1) {
  
  console.log('V1:', param1);
        if (param1[0] === '0') { //locked
	        data = [getRandomInt(10),getRandomInt(10),getRandomInt(10),getRandomInt(10)];
		dataString='';
		blynk.notify(data);
		numAsked= true;
		askNum()

       } else if (param1[0] === '1') { //unlocked
	      	numAsked=false;
		dataString='';
		pas='';
	       blynk.notify("Door is locked");
        } else {
                blynk.notify("Door lock button was pressed with unknown parameter");
        }
});
v2.on('write', function(param2) {
  	if (param2[0] === '0') {                     //Fingerprint off
                blynk.notify("Fingerprint is on");    
  	} else if (param2[0] === '1') {              //Fingerprint on
                blynk.notify("Fingerprint is on");
                getFnum()                
  	} else {
  		blynk.notify("Door lock button was pressed with unknown parameter");
  	}
});

blynk.on('connect', function() { console.log("Blynk ready."); });
blynk.on('disconnect', function() { console.log("DISCONNECT"); });

function lockDoor() {
	motor.servoWrite(lockedState);
	led.digitalWrite(1);
	locked = true

	//notify
  	blynk.notify("Door locked");
  	
  	//After 1.5 seconds, the door lock servo turns off to avoid stall current
  	setTimeout(function(){motor.servoWrite(0)}, 1500)
}

//for keypad
function askNum(){
var py = spawn('python', ['test/connector.py']);

	if(numAsked== true){
		console.log('Enter 4 digits:');
		 console.log('Random number is ', data);
		py.stdout.on('data', function(data){
		 dataString += data.toString();
		});
		py.stdout.on('end', function(){
		  console.log('key=',dataString);
		  check() 
		});
		   pas=dataString;
		py.stdin.write(JSON.stringify(data));
		py.stdin.end();
	
	}

}
// for Fingerprint
function getFnum(){
var py = spawn('python', ['test/Fconn.py']);

	Fdata=[1,2]
	FdataString='none'
        Fpas=''
	console.log('Finger data is ', Fdata);
	py.stdout.on('Fdata', function(Fdata){
            FdataString += Fdata.toString();
	});
	py.stdout.on('end', function(){
	    console.log('key=',FdataString);
	});
	Fpas=FdataString;
	py.stdin.write(JSON.stringify(Fdata));
	py.stdin.end();
	
	

}

function unlockDoor() {
	motor.servoWrite(unlockedState);
	led.digitalWrite(0);
	locked = false

	//notify
  	blynk.notify("Door has been unlocked!"); 

  	//After 1.5 seconds, the door lock servo turns off to avoid stall current
  	setTimeout(function(){motor.servoWrite(0)}, 1500)
}

// get random number
function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}
// check keypad digits to unlock
function check() {
	var d=1;
	var text= dataString;

	var b=parseInt(text,10);	
	if (b === d){
		console.log('Matched');
		unlockDoor();
 //               Blynk.setProperty(v0, "onLabel", "ON");
//                Blynk.setProperty(V0, "onLabel", "ON");
	}else{console.log('pity ');}

}

