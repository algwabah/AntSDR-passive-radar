VERBOSE = False

import uhd
import numpy as np
import matplotlib.pyplot as plt

from struct import pack,unpack
import logging
import sys
import time


class AntSDRReceiver():
    def __init__(self,samp_rate, center_freq, gain_0, gain_1,packet_size,n_packets):
        #Create useful attributes
        self.name = 'AntSDR'
        self.samp_rate = samp_rate
        self.daq_center_freq = center_freq
        self.daq_rx_gain = [gain_0,gain_1]
        self.iq_samples = None

        self.iq_header = AntIqHeader()
        self.M = 2


        #Initializing a bunch of attributes for usrp data collection
        self.rec_ip_addr = None
        self.usrp = None
        self.st_args = None
        self.metadata = None
        self.streamer = None
        self.recv_buffer = None
        self.stream_cmd = None
        self.streamer = None

        #Samples per buffer dump and number of buffer dumps per get_iq_online()
        self.packet_size = packet_size
        self.n_packets = n_packets

    def start_receiving(self):
        #Create Usrp receiver object
        self.usrp = uhd.usrp.MultiUSRP("addr=192.168.1.10")
        
        #Set options
        self.usrp.set_rx_rate(self.samp_rate)
        #Channel 1
        self.usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(self.daq_center_freq), 0)
        self.usrp.set_rx_gain(self.daq_rx_gain[0], 0)
        #Channel 2
        self.usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(self.daq_center_freq), 1)
        self.usrp.set_rx_gain(self.daq_rx_gain[1], 1)


        # Set up buffers and iq data holders
        self.recv_buffer = np.zeros((2, self.packet_size), dtype=np.complex64)
        self.iq_in = np.zeros((2, self.n_packets*self.packet_size), dtype=np.complex64)
        self.iq_samples = self.iq_in.copy()

        #setup args
        self.st_args = uhd.usrp.StreamArgs("fc32", "sc16")  # Data format: complex float32
        self.st_args.channels = [0, 1]
        self.rx_streamer = self.usrp.get_rx_stream(self.st_args)
        self.metadata = uhd.types.RXMetadata()

        # Start streaming with a specific time
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = False  # We will specify the start time explicitly
        stream_cmd.time_spec = uhd.types.TimeSpec(self.usrp.get_time_now().get_real_secs() + 0.1)  # Start 0.1 seconds in the future
        self.rx_streamer.issue_stream_cmd(stream_cmd)


    def set_iq_header(self):
        # Sets the iq header with correct info

        #Entering data in iq_header
        self.iq_header.adc_sampling_freq = self.samp_rate
        self.iq_header.sampling_freq = self.samp_rate
        self.iq_header.rf_center_freq = self.daq_center_freq
        self.iq_header.if_gains = self.daq_rx_gain

        self.iq_header.time_stamp = int(time.time()*10**3)

        #NOT SURE ABOUT FORMAT FOR THIS ONE
        self.iq_header.frame_type = 0
        self.iq_header.active_ant_chs = 2 #TODO: FIGURE THIS OUT
        self.iq_header.cpi_length = 0   # Figure out what this means, can be left as zero because only for display, SHOULD PROB NOT BE 0
        self.iq_header.cpi_index +=1

        self.iq_header.check_sync_word = False
        self.iq_header.adc_overdrive_flags = False

        # Random controls hard coded for Kraken to make code run anyway
        self.iq_header.frame_type = 0
        self.iq_header.delay_sync_flag = True
        self.iq_header.iq_sync_flag = True

        
    def next_iq_frame(self):
        #Receives iq samples and iq_header, one get_iq_online is followed by one RD_matrix created       
        for i in range(self.n_packets):
            self.rx_streamer.recv(self.recv_buffer, self.metadata)
            self.iq_in[:,i*self.packet_size:(i+1)*self.packet_size] = self.recv_buffer
        self.in_iq_samples = self.iq_in.copy()
        if VERBOSE:
            print('Got a new iq frame of size ',self.iq_samples.size/2)
        #self.set_iq_header()


    def get_iq_online(self):
        self.iq_samples = self.in_iq_samples.copy()
        self.set_iq_header()

    def stop_receiving(self):
        #Stop ANT from streaming samples
        self.stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        self.rx_streamer.issue_stream_cmd(self.stream_cmd)


    def set_center_freq(self,freq):
        pass

    def set_if_gain(self,gain):
        pass


class AntIqHeader():
    #Information package to include in queue packet sent to web interface
    
    def __init__(self) -> None:

        self.SYNC_WORD = 0x2bf7b95a
        self.FRAME_TYPE_DATA  = 0
        self.FRAME_TYPE_DUMMY = 1
        self.FRAME_TYPE_RAMP  = 2
        self.FRAME_TYPE_CAL   = 3
        self.FRAME_TYPE_TRIGW = 4

        self.logger = logging.getLogger(__name__)
        self.header_size = 1024 # size in bytes
        self.reserved_bytes = 192        

        self.sync_word=self.SYNC_WORD        # uint32_t        
        self.frame_type=0                    # uint32_t 
        self.hardware_id=""                  # char [16]
        self.unit_id=0                       # uint32_t 
        self.active_ant_chs=0                # uint32_t 
        self.ioo_type=0                      # uint32_t 
        self.rf_center_freq=0                # uint64_t 
        self.adc_sampling_freq=0             # uint64_t 
        self.sampling_freq=0                 # uint64_t 
        self.cpi_length=0                    # uint32_t 
        self.time_stamp=0                    # uint64_t 
        self.daq_block_index=0               # uint32_t
        self.cpi_index=0                     # uint32_t 
        self.ext_integration_cntr=0          # uint64_t 
        self.data_type=0                     # uint32_t 
        self.sample_bit_depth=0              # uint32_t 
        self.adc_overdrive_flags=True           # uint32_t 
        self.if_gains=[0]*32                 # uint32_t x 32
        self.delay_sync_flag=False               # uint32_t
        self.iq_sync_flag=False                  # uint32_t
        self.sync_state=0                    # uint32_t
        self.noise_source_state=False            # uint32_t        
        self.reserved=[0]*self.reserved_bytes# uint32_t x reserverd_bytes
        self.header_version=0                # uint32_t 
        self.check_sync_word = True
