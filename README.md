
# Hardware
The transceiver module is a SX1276/7/8/9
It is mounted on a prototyping board to a Raspberry Pi rev 2\3 model B.

| Proto board pin | RaspPi GPIO | Direction |
|:----------------|:-----------:|:---------:|
|  DIO0    | GPIO 22     |    IN     |
|  DIO1    | GPIO 23     |    IN     |
|  DIO2    | GPIO 24     |    IN     |
|  DIO3    | GPIO 25     |    IN     |
|  Reset   | GPIO ?      |    OUT    |
|  vcc     | GPIO 1      |    POWER  |
|  GND     | whaterver   |    GND    |
|  MISO    | GPIO09      |   IN      |
|  MOSI    | GPIO10      |    IN     |
|  SLCK    | GPIO11      |   IN      |
|  NSS     | GPIO08      |   IN      |
|          | GPIO 4      |    IN     |

# Code Examples
test.py

this code file contain sending and recieving messages between adrinouo.


# Eorror you may get:
1:no module named "SPI":


make sure you Open the SPI (sudo raspi-config   ---> interface *** ---->open the SPI )

2:asseration error:


make sure you had connected the Raspberry right!!!!!!!!!!!!!\n


# References:
