# AntSDR passive radar usage guide

This document describes how to use the AntSDR passive radar system.

## Setup

### 1. Install software

See installation guide 

### 2. Connect hardware

Ensure the AntSDR is in SD mode, this is determined by a switch on the side of the AntSDR next to the USB-C port.

Connect AntSDR to the PC using ethernet.

Power on the AntSDR by inserting USB-C cable. This should turn on a light on the SDR.

### 3. Check connection

The AntSDR is located at ip 192.168.1.10. To establish a connection with the PC,
set the PCs ip to some other 192.168.1.x adress.

Now, ensure the PC and SDR are connected using 'ping 192.168.1.10'.
If the ping is succesful, check firmware connection using ' uhd_find_devices --args="addr="192.168.1.10"" '



## Settings

In 'AntSDR_pr/Antsdr_pr/settings.json', choose settings. Useful settings include:

### Radar display settings

- 'max_bistatic_range' sets the distance range of the radar. The value represents the number of bistatic distance blocks to be used.
Each block will correspond to *ΔR =  c / f<sub>s</sub>* bistatic distance (c is speed of light and f<sub>s</sub> is sampling frequency).
Eg. if *f<sub>s</sub> = 8 MHz*, each block will be approximately 31 meters.
This means the total bistatic distance range of the radar will be (max_bistatic_range×ΔR).
For performance reasons, 'max_range' is recommended to be a power of 2, eg. 256.


- 'max_doppler' sets the velocity range of the radar. The value represents the number of doppler shift blocks to be used per direction (positive and negative).
Each block will correspond to *Δv = -(c × f<sub>s</sub>) / (N × f<sub>c</sub>)* bistatic velocity (c is speed of light, f<sub>s</sub> is sampling frequency, f<sub>c</sub> is center frequency and N is number of samples round of processing).
Eg. if *N / f<sub>s</sub>* is 0.5 and *f<sub>c</sub>* is 490 MHz, each block will be approximately *-1.2 m/s*.
This means the total bistatic velocity range of the radar will be (max_doppler×Δv) in each direction.
For performance reasons, 'max_doppler' is recommended to be a power of 2, eg. 256.

### Sampling settings

- 'gain_0' is the reference channel gain.
- 'gain_1' is the surveillance channel gain.
- 'center_freq' is the center frequency, eg. 490 MHz which is a Nackamasten channel. Possible range should be 70 MHz - 6 GHz.
- 'sampling_freq' is the sampling frequency, maximum should be 61.44 MHz, but has only been tested up to 8MHz.
- 'n_samps' is the number of samples the AntSDR records at a time, recommended value 1000
- 'per_package' is the number of collection rounds per sample package sent to processing. This means (n_samps×per_package) will be the total number of samples per round of processing.

- **IMPORTANT:** For processing to work, (n_samps×per_package) must be divisible by max_bistatic_range.
Eg. if n_samps=1000, per_package=4000, and max_range=256, then (n_samps×per_package)/max_bistatic_range = 15625.

Other useful settings determine such things as decay speed of results in display etc.

## Operation

### 1. Start program

In terminal, navigate to the main folder and start the program with

'./Ant_pr_start.sh'

Wait about 15 seconds for the program to start fully.

### 2. Start processing

Navigate to the GUI by opening a web browser and going to 'localhost:8080'.

Hopefully, a GUI page will be shown with the config tab selected.

Click on 'Start processing' and wait about 10 seconds. If all but one of the status texts turn green, the system is working.

### 3. Observe results

In the GUI, navigate to either the 'Passive radar' tab or the 'ADSB+Passive Radar' tab.

Hopefully, the display will now begin filling up with measurements.

The x-axis of the display represents bistatic distance, each cell in the x direction corresponds to a *ΔR* bistatic distance block.

The y-axis of the display represents bistatic velocity, each cell in the y direction corresponds to a *Δv* bistatic velocity block.

### 4. Stopping the system

When finished, in order to stop the system properly, go back to the config tab and click 'Stop Processing'.

Now the program may be stopped by in console by navigating to 'AntSDR_pr/kraken_pr' and using

'./Ant_pr_stop'



## Notes

- Bistatic distance range for the system with current antennas is about 4 km.
- **The system can only detect aircraft to the west**. In practice, this means aircraft travelling to and from Bromma.


- Many buttons left over from the KrakenSDR system are marked as N/A, do not click these
- If the system is not stopped properly, the AntSDR will have to be restarted by disconnecting and reconnecting the USB-C power cable. 
- If the sampling frequency is set high so the system does not have time to process all sampled data, excess sample packages will be discarded automatically.
- Occasionally, some unknown error with ADSB will halt the system if it is in ADSB mode. If this occurs, restart the system and try again.
- A log document in 'Antsdr_pr/Antsdr_pr/ui.log' can be used to troubleshoot
- A verbose mode of the program which prints all it is doing in the console is available. Enable it in the top row of the main 'kraken_web_interface' script.