# ROME L1 Driver

## Overview
The ROME L1 Driver provides CloudShell Resource Manager with the capability to communicate with switches that are part of the CloudShell inventory.

End users will be able to create routes, configure port settings, and read values from the switch using the CloudShell Portal, Resource Manager client, or the CloudShell API.


### Supported Devices/Firmwares
The driver has been verified with the following devices and software versions:
ROME500 1.9.4.1

### Installation
"Rome.exe", "rome_runtime_configuration.json", and RomeResourceConfiguration.xml are the only files required. 

1) Copy "Rome.exe" and "rome_runtime_configuration.json" 
   to "c:\Program Files (x86)\QualiSystems\CloudShell\Server\Drivers"
   
2) Open Cloudshell Resource Manager

3) Right-click resource families folder and select import

4) Import "RomeResourceConfiguration.xml"

5) While specifying the address for the resource, specify it as IPAddress:RequiredMatrix. 
	Example: 192.168.10.111:MatrixA (for A-matrix selection, MatrixA(with out any spaces inbetween)

### Usage
1) When creating new resources using resource manager. Specify the IP address as follows: [IP]:[Matrix]. 
   Specifying the matrix is not case sensitive.
	Ex.) 255.255.55.1:MatrixA   The name of the matrix is separated by a colon

2) It is also possible to specify the matrix using a single letter.
	Ex.) 192.168.1.254:A

### Supported Functionality

* AutoLoad : Creates the sub-resources of the L1 switch
* MapBidi : Creates a bi-directional connection between two ports
* MapUni : Creates a uni-directional connection between two ports
* MapClear : Clears any connection ending in this port
* MapClearTo : Clears a uni-directional connection between two ports

