# AntSDR passive radar installation

The system has only been tested with a Linux PC using Ubuntu 20.04.
Any other Ubuntu version will likely experience issues with installation.

## KrakenSDR passive radar installation

Due to this passive radar system being originally created for the KrakenSDR, that passive radar system must be installed first
in order to set up all correct python environments etc.

Follow the installation guide in (Do this in a seperate repository) 'Kraken_SDR_installation.md'

## AntSDR installation

Now, the AntSDR software must be installed on the PC.

The AntSDR supports two different firmwares, this system uses UHD USRP. To install, follow the instructions in the following repository:
https://github.com/MicroPhase/antsdr_uhd

## AntSDR passive radar

With all the previous steps completed, this system should now be usuable.

Clone this repository if you have not yet done so, and refer to 'Instructions.md' for a usage guide.

