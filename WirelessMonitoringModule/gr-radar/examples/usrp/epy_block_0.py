"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import matplotlib.pyplot as plt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=None,
            out_sig=[np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        #self.example_param = example_param
	self.message_port_register_in(pmt.intern('msg_in'))
	self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

	self.phase = 0	
	self.time = 0
	#self.power = 0
	#plt.ion()



    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #output_items[0][:] = input_items[0] * self.example_param
	#print input_items[0]
	output_items[0][:] = self.phase
	output_items[1][:] = self.time
	#output_items[2][:] = self.power
        return 1  # len(output_items[0])

    def handle_msg(self, msg):
	d_size_msg = pmt.length(msg);  # rx_time, frequency, power, phase
	
	time_tuple = pmt.nth(1, pmt.nth(0, msg))
	time_s = pmt.to_uint64(pmt.tuple_ref(time_tuple,0))	
	time_ms = pmt.to_double(pmt.tuple_ref(time_tuple,1))	
	timestamp = time_s + time_ms

	phase_val_vec = pmt.nth(1, pmt.nth(d_size_msg-1, msg))
	phase_val = pmt.f32vector_elements(phase_val_vec)[0]
	
	#plt.scatter(timestamp, phase_val)
	#plt.pause(0.05)

	#power_val_vec = pmt.nth(1, pmt.nth(d_size_msg-2, msg))
	#power_val = pmt.f32vector_elements(power_val_vec)[0]
	
	self.phase = phase_val
	self.time = timestamp
	#self.power = power_val
	#print phase_val_vec
