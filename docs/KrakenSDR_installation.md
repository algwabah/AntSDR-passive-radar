# Installation guide for krakenSDR passive radar

# CAUTION Only works with ubuntu version 20.04.6

### Step 1: Install prerequisities
```
sudo apt update
sudo apt install libfftw3-3
sudo apt install libfftw3-dev
```
### Step 2: Install Heimdall DAQ  

#### Step 2.1 Install Heimdall build dependencies  
```
sudo apt update
sudo apt install build-essential git cmake libusb-1.0-0-dev lsof libzmq3-dev
```

#### Step 2.2 Install custom KrakenRF RTL-SDR kernel driver  
```
git clone https://github.com/maxsundstrom98/librtlsdr_krakenSummer23
cd librtlsdr_krakenSummer23
sudo cp rtl-sdr.rules /etc/udev/rules.d/rtl-sdr.rules
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
make
sudo ln -s ~/librtlsdr_krakenSummer23/build/src/rtl_test /usr/local/bin/kraken_test

echo 'blacklist dvb_usb_rtl28xxu' | sudo tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf
```

#### Step 2.3 Restart the system  
```
sudo reboot
```

#### Step 2.4 Install the KFR DSP library  
```
sudo apt-get install clang
```

#### Step 2.5 Build and install the library
```
cd
git clone https://github.com/maxsundstrom98/kfr_summer23
cd kfr_summer23
mkdir build
cd build
cmake -DENABLE_CAPI_BUILD=ON -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release ..
make
```

#### Step 2.6 Copy the built library over to the system library folder  
```
sudo cp ~/kfr_summer23/build/lib/* /usr/local/lib
```


#### Step 2.7 Copy the include file over to the system includes folder  
```
sudo mkdir /usr/include/kfr
sudo cp ~/kfr/include/kfr/capi.h /usr/include/kfr
```

#### Step 2.8 Run ldconfig to reset library cache
```
sudo ldconfig
```

#### Step 2.9 Install Miniforge

```
cd
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
chmod ug+x Miniforge3-Linux-x86_64.sh
./Miniforge3-Linux-x86_64.sh
```

#### Step 2.10 Restart the system
```
sudo reboot
```

#### Step 2.11 Disable the default base environment  
```
conda config --set auto_activate_base false
```



#### Step 2.12 Restart the system
```
sudo reboot
```

##### Step 2.13 Setup the Miniconda Environment
```
conda create -n kraken python=3.9.7
conda activate kraken

conda install scipy==1.9.3
conda install numba==0.56.4
conda install configparser
conda install pyzmq
conda install scikit-rf
```

#### Step 2.14 Create a root folder and clone the Heimdall DAQ Firmware
```
cd
mkdir krakensdr_summer23
cd krakensdr_summer23

git clone https://github.com/maxsundstrom98/heimdall_daq_fw
cd heimdall_daq_fw
```

#### Step 2.15 Build Heimdall C files  

Browse to the _daq_core folder
```
cd ~/krakensdr_summer23/heimdall_daq_fw/Firmware/_daq_core/
```
Copy librtlsdr library and includes to the _daq_core folder  
```
cp ~/librtlsdr_krakenSummer23/build/src/librtlsdr.a .

cp ~/librtlsdr_krakenSummer23/include/rtl-sdr.h .

cp ~/librtlsdr_krakenSummer23/include/rtl-sdr_export.h .

```
Now build Heimdall
```
make
```

## Optional intel opimizations (recommended)  
```
conda activate kraken
conda install "blas=*=mkl"
conda install -c numba icc_rt
```

### Step 3: Setup Miniconda environment
You will have created a Miniconda environment during the Heimdall DAQ install phase.

Please run the installs in this order as we need to ensure a specific version of dash is installed.

```
conda activate kraken

conda install pip
conda install quart
conda install pandas
conda install orjson
conda install matplotlib

pip3 install dash_bootstrap_components
pip3 install quart_compress
pip3 install dash_devices
pip3 install pyapril
pip3 install cython
pip3 install pyfftw
pip3 install geopy
pip3 install Pyargus

conda install dash==1.20.0
conda install werkzeug==2.0.2
```

### Step 4: Clone the krakensdr_pr software
```
cd ~/krakensdr_summer23
git clone https://github.com/citrus13579/kraken_summer23
```
Copy the krakensdr_doa/util/kraken_doa_start.sh and the krakensdr_doa/util/kraken_doa_stop.sh scripts into the krakensdr root folder of the project.  
```
cd ~/krakensdr
cp krakensdr_pr/util/kraken_pr_start.sh .
cp krakensdr_pr/util/kraken_pr_stop.sh .
```
### Step 5: Running the software  

You should now be able to run the software with:
```
./kraken_pr_start.sh
```
Then browse to KRAKEN_IP_ADDR:8080 in a webbrowser on a computer on the same network.

When the GUI loads, make sure to set an appropriate passive radar preconfig ini for the Heimdall DAQ. For example, choose "pr_2ch_2pow21", then click on "Reconfigure and Restart DAQ". This will configure the DAQ for passive radar, and then start the processing.

Please be patient on the first run, at it can take 1-2 minutes for the JIT numba compiler to compile the numba optimized functions, and during this compilation time it may appear that the software has gotten stuck. On subsqeuent runs this loading time will be much faster as it will read from cache.

# Install readsb
To install readsb, run the following command to start the install script:
```
sudo bash -c "$(wget -O - https://github.com/wiedehopf/adsb-scripts/raw/master/readsb-install.sh)"
```



# Known possible issues

Sometimes the "passive radar + ADS-B" tab will not open. 
One of the reasons could be the error message that reads "index out of range at x" where x have been either 6,10 or 11 in past experiences. This has happened multiple times and we do not really know the reason behind it.

The solution is just to run the code again and it usually fixes it. If it doesn't, try to restart kraken, this has solved the problem for us in the past.
