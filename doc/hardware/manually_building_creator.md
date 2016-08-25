![Imagination Technologies Limited logo](../images/img.png)

----

## Creator System Test Framework

----

### Building creator (OpenWRT) on the host machine

####  Building OpenWRT

Firstly, follow the [Building from source code instructions](https://docs.imgcreator.io/creator/creator-kit/toolbox/#building-from-source-code) on the host machine to build the 
creator kit development environment(OpenWRT with cross-compiled Awa and Contiki packages). 

Make sure to install **version 1.34** of the MPLAB XC32 compiler (available from [here](http://ww1.microchip.com/downloads/en/DeviceDoc/xc32-v1.34-full-install-linux-installer.run))

You may also need to install the following in order to successfully build OpenWRT:
    
    sudo apt-get install texinfo

#### Adding required dependencies

At this point you should have an OpenWRT build. However, there are additional dependencies required by the Test Framework that must be packed into our image.

Firstly, enter your OpenWRT directory:

    $ cd dist/openwrt

Edit openwrt/feeds.conf  and/or feeds.conf.default and add the following line:

    src-git pickleprog https://github.com/datachi7d/openwrt-pickle

Then update the OpenWRT feeds:

    $ scripts/feeds update
    $ scripts/feeds install -a

Run the following command to enter the OpenWRT menu configuration:

    $ make menuconfig

Then select the following packages (press 'y' on each package giving a * indicating that the package will be built into the image):

    Python (Languages -> Python):
        python <*>
        python-pip <*> (optional)
        python-enum34 <*>
        python-pyserial <*>
        python-yaml <*>

    FTDI usb to serial driver (Kernel modules -> USB support -> kmod-usb-serial):
        kmod-usb-serial-ftdi <*>
    
    stty (Base system -> busybox -> Customize busybox options -> Coreutils):
        stty <*>
    
    nfs-utils (Utilities->Filesystem)
        nfs-utils <*>
    
    pickle (Utilities -> pickle)
        pickle <*>
    
    kmod-fs-nfs (Kernel Modules->Filesystems)
        kmod-fs-nfs <*>
        kmod-fs-nfs-common <*>
    
    minicom (Utilities->minicom)
        minicom <*>
    
Exit out of menuconfig, making sure to save the changes to the configuration.

#### Choosing a version of Awa to test against

By default, the latest *tested with creator* version of Awa will be pulled into the build. This will most likely **not** be the latest version available.

Edit feeds/ckt/awalwm2m/Makefile and find the line below:
        
    PKG_VERSION:=0.1.7
        
Change this to master (or whatever version tag / commit ID of Awa you wish to test):
        
    PKG_VERSION:=master
            
If the current version is below 0.1.8 and you wish to upgrade to 0.1.8 or above (eg. master),
the following modification is also required within the same file (Due to a change in how Awa is installed):
            
    add /usr to the $(CP) $(PKG_INSTALL_DIR)/bin/* $(1)/bin/:

    $(CP) $(PKG_INSTALL_DIR)/usr/bin/* $(1)/bin/
    
#### Rebuilding OpenWRT with the above changes
rebuild openwrt by typing the following command in the openwrt directory:
    
        $ make -j6

#### Removing awa services
The Test Framework relies on the fact that no Awa daemons are already running on the Ci40.

Re-open feeds/ckt/awalwm2m/Makefile and find "define Package/awalwm2m/install"

Comment out the line near the bottom of the definition, which will stop the awa services from being started:

    $(CP) files/etc/* $(1)/etc/

### Flashing your new OpenWRT image onto the Ci40 using Sysupgrade

Follow the instructions [here](https://github.com/CreatorDev/creator-system-test-framework/tree/master/doc/hardware/flashing_openwrt.md) to flash your gateway device.

### Updating Awa / OpenWRT

If you use "repo sync", it will wipe your modified OpenWRT menuconfig. It is better to update each branch manually.

If you have already built Awa into OpenWRT before, you will need to delete the cached awa file located in the dl/ folder of openWRT.

    $ rm /repos/creator/dist/openwrt/dl/awalwm2m-master.tar.gz
