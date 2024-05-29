# AntSDR passive Radar
#### Saab Järfälla 2024

Welcome, to the Saab AntSDR passive radar docs. 

This is a passive radar system for the AntSDR (or any other USRP SDR) ported from the KrakenSDR passive radar.

The system has only been tested for Ubuntu version 20.04, other versions will most likely have trouble setting up the correct Python environment. 

It is recommended to read up on passive radar before use.
For an explanation of how the radar calculates results, see (https://github.com/pyapril/pyapril) -> docs -> april_doc_detector.ipynb -> 2.3 cc_detector_ons

### Description

The passive radar system is installed on the Saab Järfälla roof.
It is mainly capable of detecting aircraft to the west Järfälla,
in practice meaning those arriving to or departing from Bromma airport.

Illuminator/transmitter: Nackamasten digital TV tower

The system uses a set of Python scripts to digitally sample and process the reference and surveillance channels into
Bistatic distance - Doppler matrixes.
Control of the system and display of results is done in a locally hosted GUI.



### Guide


For installation, see Installation.md in /docs

For instructions of use, see Instructions.md in /docs.