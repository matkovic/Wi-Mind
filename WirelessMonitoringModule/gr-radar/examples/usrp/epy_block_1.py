"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, start_value=1e9, step=1e8, time=5):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=None,
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.start_value = start_value
	self.step = step
	self.time = time
	self.multiplier = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
	time.sleep(self.time)        
	output_items[0][:] = self.multiplier*self.step + self.start_value
	self.multiplier = self.multiplier + 1
        return len(output_items[0])
