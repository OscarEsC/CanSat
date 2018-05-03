/*arduino's TX must be connected with xBee's DIN pin.
 * arduino's RX must be connected with xBee's DOUT pin.
 * Connect SCL with A5 pin.
 * Connect SDA with A4 pin.
 */
 
#include <Wire.h>
#include <Adafruit_BMP085_U.h>      //Barometer
#include <L3G.h>
#include <Adafruit_ADXL345_U.h>     //Acelerometer
#include <Adafruit_Sensor.h>        //Acelerometer & Barometer

#define BMP085_ADDRESS 0x77         // I2C address of BMP085
#define HMC_address 0x1E            //0011110b, I2C 7bit address of HMC5883


//--------Barometer---------        Parameter -> sensor's ID
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
float temperature, pressure, altitude;
float pressure0;

//-------Accelerometer-------
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
float accel_x, accel_y, accel_z;

//------Gyroscope--------
L3G gyro;
float g_x, g_y, g_z;

  
void setup()
{
  Serial.begin(9600);
  Wire.begin();
  
  // Initialise the sensor
  bmp.begin();

  //--------acelerometer----
  accel.begin();
  accel.setRange(ADXL345_RANGE_16_G);
  
  //--------Gyroscope-------
  gyro.init();
  gyro.enableDefault();
  
  //Get the current pressure to set pressure0 as reference
  getPressureZero();
}

void loop()
{
  //------------Barometer-------------Checked
    //Get current pressure, temperature and altitude
    bmp.getPressure(&pressure);
    bmp.getTemperature(&temperature);
    altitude = bmp.pressureToAltitude(pressure0, pressure);
  
  //-------------Accelerometer--------Checked
    accel_x = (float)accel.getX() * ADXL345_MG2G_MULTIPLIER * SENSORS_GRAVITY_STANDARD;;
    accel_y = (float)accel.getY() * ADXL345_MG2G_MULTIPLIER * SENSORS_GRAVITY_STANDARD;
    accel_z = (float)accel.getZ() * ADXL345_MG2G_MULTIPLIER * SENSORS_GRAVITY_STANDARD;

  //---------Gyroscope-----------Checked
    //The sensor's reading must be multiplied by the conversion factor
    //in order to get degrees per second (dps)
    gyro.read();
    g_x = (float)gyro.g.x * 0.00875;
    g_y = (float)gyro.g.y * 0.00875;
    g_z = (float)gyro.g.z * 0.00875;

    Serial.print(pressure);
    Serial.print(',');
    Serial.print(temperature);
    Serial.print(',');
    Serial.print(g_x);
    Serial.print(',');
    Serial.print(g_y);
    Serial.print(',');
    Serial.print(g_z);
    Serial.print(',');
    Serial.print(accel_x);
    Serial.print(',');
    Serial.print(accel_y);
    Serial.print(',');
    Serial.print(accel_z);
    Serial.print(',');
    Serial.println(altitude);
  
    delay(200);
}

void getPressureZero(){
  //Set pressure0 as the initial pressure
   bmp.getPressure(&pressure);
   pressure0 = pressure;
}

