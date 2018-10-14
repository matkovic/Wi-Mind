#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Test Split Cc
# Generated: Sat Jan 20 17:21:10 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import radar
import wx


class test_split_cc(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Test Split Cc")

        ##################################################
        # Variables
        ##################################################
        self.samp_up = samp_up = 512
        self.samp_rate = samp_rate = 1024
        self.samp_down = samp_down = 512
        self.samp_cw = samp_cw = 1024

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.radar_static_target_simulator_cc_0 = radar.static_target_simulator_cc((10, ), (5, ), (1e12, ), (0, ), (0,), samp_rate, 2.4e9, -10, True, True, "packet_len")
        self.radar_split_cc_0_1 = radar.split_cc(2, ((samp_cw, samp_up, samp_down)), "packet_len")
        self.radar_split_cc_0_0 = radar.split_cc(1, ((samp_cw, samp_up, samp_down)), "packet_len")
        self.radar_split_cc_0 = radar.split_cc(0, ((samp_cw, samp_up, samp_down)), "packet_len")
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(samp_rate, samp_up, samp_down, samp_cw, 0, 250, 1, "packet_len")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_xx_0, 0), (self.radar_split_cc_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.radar_split_cc_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.radar_split_cc_0_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.radar_static_target_simulator_cc_0, 0))
        self.connect((self.radar_split_cc_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.radar_split_cc_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.radar_split_cc_0_1, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.blocks_multiply_xx_0, 0))

    def get_samp_up(self):
        return self.samp_up

    def set_samp_up(self, samp_up):
        self.samp_up = samp_up

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.radar_static_target_simulator_cc_0.setup_targets((10, ), (5, ), (1e12, ), (0, ), (0,), self.samp_rate, 2.4e9, -10, True, True)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_samp_down(self):
        return self.samp_down

    def set_samp_down(self, samp_down):
        self.samp_down = samp_down

    def get_samp_cw(self):
        return self.samp_cw

    def set_samp_cw(self, samp_cw):
        self.samp_cw = samp_cw


def main(top_block_cls=test_split_cc, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
