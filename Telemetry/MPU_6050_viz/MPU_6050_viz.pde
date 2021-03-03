import processing.serial.*;

Serial gyro;
String dataline;
String[] newdata;
float yaw;
float pitch, roll;
PImage rear, top, side;

void setup() {
  // Initalize serial connection to arduino
  gyro = new Serial(this, "COM9", 115200);
  gyro.bufferUntil('\n');
  
  // Initialize canvas and 3D mode
  size(600, 600, P3D);
  
  // Load images
  rear = loadImage("planeRear.png");
  side = loadImage("planeSide.png");
  top = loadImage("planeTop.png");
  
  // Position mode center instead of corner
  rectMode(CENTER);
  textAlign(CENTER, TOP);
  imageMode(CENTER);
}

void draw() {
  background(0);

  // Read data from serial
  dataline = gyro.readStringUntil('\n');
  //println(dataline);
  
  // Process data
  if (dataline != null) {
    //newdata = dataline.split(" |\n"); // Break split string along spaces
      newdata = dataline.split(" |\n");  
  //println('{'+newdata[0]+'}'+' '+newdata.length); // Print first value and array length (helps with testing)
    printArray(newdata);
    if (newdata[0] != "") {
      pitch = float(newdata[1]);
      yaw = float(newdata[3]);
      roll = float(newdata[5]);
      //println("Pitch "+pitch+" Yaw "+yaw+" Roll "+roll);
      //println(newdata[5]);  
    }
  }

  // Gui settings
  int r = 75; // Circle radius
  int e = 10; // Buffer from edge


  // 2D Indicator backgrounds
  fill(255);
  text("Roll : "+roll, r+e, 2*(r+e));
  circle(r+e, r+e, 2*r);
  text("Pitch : "+pitch, width/2, 2*(r+e));
  circle(width/2, r+e, 2*r);
  text("Yaw : "+yaw, width-(r+e), 2*(r+e));
  circle(width-(r+e), r+e, 2*r);


  // Roll indicator //
  push();
  // Move origin to center of circle
  translate(r+e, r+e);
  
  // Draw reference lines
  stroke(0);
  strokeWeight(1);
  line(-r, 0, r, 0);
  line(0,-r, 0, r);
  
  // Draw indicator lines and image
  rotateZ(radians(-roll));
  stroke(0, 0, 255);
  strokeWeight(2);
  line(-r, 0, r, 0);
  image(rear, 0, e*0.75, 1.8*r-e, 2*e);
  pop();

  // Pitch indicator //
  push();
  // Move origin to center of circle
  translate(width/2, r+e);
  // Draw reference lines
  stroke(0);
  strokeWeight(1);
  line(-r, 0, r, 0);
  line(0,-r, 0, r);
  
  // Draw indicator lines and image
  rotateZ(radians(pitch));
  stroke(0, 255, 0);
  strokeWeight(2);
  line(-r, 0, r, 0);
  image(side, 0, 0, 1.5*r-e, 4*e);
  pop();

  // Yaw indicator //
  push();
  // Move origin to center of circle
  translate(width-(r+e), r+e);
  
  // Draw reference lines
  stroke(0);
  strokeWeight(1);
  line(-r, 0, r, 0);
  line(0,-r, 0, r);
  
  // Draw indicator lines and image (This could probably be improved by making it a function)
  rotateZ(radians(-yaw));
  stroke(255, 0, 0);
  strokeWeight(2);
  line(0,-r,0,r);
  image(top, 0, 0, r, r);
  pop();

  // 3D representation  //
  translate(width/2, 5*height/8, 200);

  // Rotate 3d model based on gyro readings (ROTATION ORDER IS IMPORTANT)
  rotateZ(radians(-roll));
  rotateX(radians(-pitch));
  rotateY(radians(yaw));
  stroke(0);
  fill(255);

  // Draw all faces of the 3D model (processing doesnt have a built-in triangular prism shape)
  beginShape();
  vertex(0, 5, -120);
  vertex(-60, 5, 120);
  vertex(60, 5, 120);
  endShape();

  beginShape();
  vertex(0, -5, -120);
  vertex(-60, -5, 120);
  vertex(60, -5, 120);
  endShape();

  beginShape();
  vertex(0, -5, -120);
  vertex(0, 5, -120);
  vertex(-60, 5, 120);
  vertex(-60, -5, 120);
  endShape();

  beginShape();
  vertex(0, -5, -120);
  vertex(0, 5, -120);
  vertex(60, 5, 120);
  vertex(60, -5, 120);
  endShape();

  beginShape();
  vertex(-60, -5, 120);
  vertex(-60, 5, 120);
  vertex(60, 5, 120);
  vertex(60, -5, 120);
  endShape();
}
