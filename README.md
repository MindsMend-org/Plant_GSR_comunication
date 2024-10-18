# Plant_GSR_comunication:
Plants my suprize you and maybe they are more than most think they are.

 If you wanted to see an aspect of your plant try this code, you will need a Arduino UNO or similar and a GSR sensor Plus your plant.
 The Arduino C .ino file code for your Arduino or SBC Bellow

 Connect The 2 GSR sensors to plant, 
  - One connected to metal rod in the earth/pot -conducts via moisture to roots
  - One connected to the plants stem, crockidile clip
  - -----------------------------------------------------

 void setup() {
  // Initialize serial communication at 115200 baud rate
  Serial.begin(115200);

  // Set pin A0 as an input for the GSR sensor
  pinMode(A0, INPUT);
}

void loop() {
  // Variable to store the sum of readings
  int total = 0;
  int loops = 100;
  float last = 0.0;
  float loopf = float(loops); // Correct conversion to float for division
  float offset = 200.0;       // Offset to avoid negative values

  float extract_decimal = 0.0; // Added missing semicolon

  // Read the value from A0 a certain number of times and accumulate the sum
  for (int i = 0; i < loops; i++) {
    total += offset + analogRead(A0); // Use analogRead to get a range of values (0-1023)
    delayMicroseconds(10); // Small delay to space out the readings, adjust as needed
  }

  // Calculate the average by dividing the total by loopf
  float average = total / loopf;

  // Print the averaged value to the Serial Plotter if it's different from the last value
  if (average != last) {
    Serial.println(average);
    last = average; // Update the last value after printing
    delayMicroseconds(798); // Small delay to space out the readings, adjust as needed
  }

  // Optional delay to control the output frequency (adjust as needed)
  delay(39); // Adjust to control the rate of output (in milliseconds)
}

