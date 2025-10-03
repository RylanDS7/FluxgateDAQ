# FluxgateDAQ

Class to interface with a LabJack to measure magnetic field magnitude using a Barrington magmeter. \
Includes UI to control when measurements are taken and log to a csv file.

###  Setup for LabJack DAQ

Assumed T7 DAQ device.

1. Install the [LJM software](https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fljm-software-installers-t4-t7-digit%2F)
2. Install the LJM python package: `pip install labjack-ljm`

### Setup for Measurement UI

1. Install the PyQt5 python package: `pip install PyQt5`
2. Run magfieldMeasureUI.py to activate system. A Labjack must be connected and detectable via usb for this to work.


# Additional Scripts

- plotFields.py cleans and background subtracts the data for given fields and plots it

- residual_analysis.py interpolates COMSOL simulated field data to calculate the residuals with a measured field