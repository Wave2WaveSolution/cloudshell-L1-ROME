# ROME L1 Driver

## Overview
The ROME L1 Driver provides CloudShell Resource Manager with the capability to communicate with switches that are part of the CloudShell inventory.

End users will be able to create routes, configure port settings, and read values from the switch using the CloudShell Portal, Resource Manager client, or the CloudShell API.


### Supported Devices/Firmwares
The driver has been verified with the following devices and software versions:
ROME500 1.9.1.1

### Installation
"Rome.exe", "rome_runtime_configuration.json", and RomeResourceConfiguration.xml are the only files required. 

1) Copy "Rome.exe" and "rome_runtime_configuration.json" 
   to "c:\Program Files (x86)\QualiSystems\CloudShell\Server\Drivers"
   
2) Open Cloudshell Resource Manager

3) Right-click resource families folder and select import

4) Import "RomeResourceConfiguration.xml"

### Supported Functionality
*
* AutoLoad : Creates the sub-resources of the L1 switch
* MapBidi : Creates a bi-directional connection between two ports
* MapUni : Creates a uni-directional connection between two ports
* MapClear : Clears any connection ending in this port
* MapClearTo : Clears a uni-directional connection between two ports

