# ROME L1 Driver

## Overview
The ROME L1 Driver provides CloudShell Resource Manager with the capability to communicate with switches that are part of the CloudShell inventory.

End users will be able to create routes, configure port settings, and read values from the switch using the CloudShell Portal, Resource Manager client, or the CloudShell API.


### Supported Devices/Firmwares
The driver has been verified with the following devices and software versions:
ROME500 1.9.1.1

### Installation

Follow the instructions in the link below for installation:
http://help.quali.com/Online%20Help/7.0.0.0/Portal/Content/Admn/Cnct-Ctrl-L1-Swch.htm

In step 7 at the above guide, you will need to copy only one exe file, and instead of the runtimeConfig.xml file please copy the rome_runtime_configuration.json file.

### Supported Functionality
*
| AutoLoad | Creates the sub-resources of the L1 switch |
| MapBidi | Creates a bi-directional connection between two ports |
| MapUni | Creates a uni-directional connection between two ports |
| MapClear | Clears any connection ending in this port |
| MapClearTo | Clears a uni-directional connection between two ports |

