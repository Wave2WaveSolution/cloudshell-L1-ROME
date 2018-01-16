# Shell L1 Driver Standard

**Usage:**

1. Start a new project with [shellfoundry](https://github.com/QualiSystems/shellfoundry):
```bash
$ shellfoundry new DriverName --template layer-1-switch
```
2. Install requirements (from the new project folder):
```bash
$ pip install -r requirements.txt

```

3. Implement all driver functions in driver_handler.py module

4. Add/Modify variables and their values in the configuration/configuration.json file. This file will be compiled into the driver.
You can add more variables to the runtime_configuration.json file to either override any variable from the configuration.json in runtime, or add other inputs that you'll be able to get from there in runtime.

5. Update the driver version and metadata in version.txt

**Compile the driver:**

1. download required packages from requirements.txt and uncompress them at the same level as the project folder (next to it). Note: [cloudshell-core](https://github.com/QualiSystems/cloudshell-core) and [cloudshell_l1_networking_core](https://github.com/QualiSystems/cloudshell-L1-networking-core) are required packages and must have the next paths:

cloudshell-core package: "../cloudshell-core"

cloudshell_l1_networking_core package: "../cloudshell-L1-networking-core"

(the latest ones that were used to compile the driver are available under the dependencies folder)

2. [install pyinstaller](http://pyinstaller.readthedocs.io/en/latest/installation.html):
```bash
$ pip install pyinstaller

```

3. run compile_driver.bat (the compiled driver will be created in a "dist" directory)

**Test in CloudShell:**

1. Copy the compiled driver and the runtime_configuration.json file into the CloudShell Server installation folder, to the Drivers folder (usually "C:\\Program Files (x86)\\QualiSystems\\CloudShell\\Server\\Drivers")

2. [Follow this guide](http://help.quali.com/Online%20Help/8.1.0.4291/Portal/Content/Admn/Cnct-Ctrl-L1-Swch.htm) to import the new datamodel, create a resource, set the timeout period, auto load it and configure its physical connections

  1. When you execute the auto load (or any other command later), the log files will get created under the Server\\Logs folder

3. After validating the auto load, you can validate the mapping functions either from Resource Manager or in the CloudShell Portal, [build a blueprint](http://help.quali.com/Online%20Help/8.1.0.4291/Portal/Content/CSP/LAB-MNG/Rsc-Cnct/Phys-Ntwrk-Crt.htm) with 2 resources and a route, then reserve this blueprint and connect the route.
