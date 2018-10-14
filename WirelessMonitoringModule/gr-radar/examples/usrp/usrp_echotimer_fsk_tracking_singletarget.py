#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrp Echotimer Fsk Tracking Singletarget
# Generated: Wed Jan 31 16:37:26 2018
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

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import radar
import sys
from gnuradio import qtgui


class usrp_echotimer_fsk_tracking_singletarget(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Usrp Echotimer Fsk Tracking Singletarget")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Usrp Echotimer Fsk Tracking Singletarget")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_fsk_tracking_singletarget")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10000000
        self.samp_per_freq = samp_per_freq = 2
        self.decim_fac = decim_fac = 2**12
        self.block_per_tag = block_per_tag = 2**20
        self.samp_rate_red = samp_rate_red = samp_rate/2/samp_per_freq/decim_fac
        self.packet_len_red = packet_len_red = block_per_tag/decim_fac
        self.freq_res = freq_res = samp_rate_red/float(packet_len_red)
        self.fac_corr = fac_corr = 2
        self.delta_freq = delta_freq = 11000000
        self.center_freq = center_freq = 2450000000
        self.wait_to_start = wait_to_start = 0.02
        self.vel_res = vel_res = freq_res/2.0/center_freq*3e8
        self.threshold = threshold = -200
        self.samp_protect = samp_protect = 1
        self.range_time = range_time = 60
        self.range_res = range_res = 3e8/2/delta_freq*fac_corr
        self.min_output_buffer = min_output_buffer = 2*samp_per_freq*block_per_tag*2
        self.measure_time = measure_time = (block_per_tag*samp_per_freq*2)/float(samp_rate)
        self.gain_tx = gain_tx = 10
        self.gain_rx = gain_rx = 10
        self.delay_samp = delay_samp = 39

        ##################################################
        # Blocks
        ##################################################
        self._threshold_range = Range(-200, 100, 1, -200, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, 'Find peak threshold', "counter_slider", float)
        self.top_grid_layout.addWidget(self._threshold_win, 1,0)
        self._samp_protect_range = Range(0, 100, 1, 1, 200)
        self._samp_protect_win = RangeWidget(self._samp_protect_range, self.set_samp_protect, 'Find peak protected samples', "counter_slider", float)
        self.top_grid_layout.addWidget(self._samp_protect_win, 1,1)
        self._gain_tx_range = Range(0, 100, 1, 10, 200)
        self._gain_tx_win = RangeWidget(self._gain_tx_range, self.set_gain_tx, 'TX gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_tx_win, 0,0)
        self._gain_rx_range = Range(0, 100, 1, 10, 200)
        self._gain_rx_win = RangeWidget(self._gain_rx_range, self.set_gain_rx, 'RX gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_rx_win, 0,1)
        self._delay_samp_range = Range(0, 100, 1, 39, 200)
        self._delay_samp_win = RangeWidget(self._delay_samp_range, self.set_delay_samp, 'Number delay samples', "counter_slider", float)
        self.top_layout.addWidget(self._delay_samp_win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_fac,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_fac,
                taps=None,
                fractional_bw=None,
        )
        self.radar_usrp_echotimer_cc_0 = radar.usrp_echotimer_cc(samp_rate, center_freq, int(delay_samp), 'serial=30F4146', '', 'internal', 'none', 'TX/RX', gain_tx, 0.1, wait_to_start, 0, 'serial=30F4146', '', 'internal', 'none', 'RX2', gain_rx, 0.1, wait_to_start, 0, "packet_len")
        (self.radar_usrp_echotimer_cc_0).set_min_output_buffer(8388608)
        self.radar_ts_fft_cc_0_0 = radar.ts_fft_cc(packet_len_red,  "packet_len")
        self.radar_ts_fft_cc_0 = radar.ts_fft_cc(packet_len_red,  "packet_len")
        self.radar_tracking_singletarget_0 = radar.tracking_singletarget(500, range_res/100, vel_res, 2, 0.001, 1, "particle")
        self.radar_split_fsk_cc_0 = radar.split_fsk_cc(samp_per_freq, samp_per_freq-1, "packet_len")
        (self.radar_split_fsk_cc_0).set_min_output_buffer(4194304)
        self.radar_signal_generator_fsk_c_0 = radar.signal_generator_fsk_c(samp_rate, samp_per_freq, block_per_tag, -delta_freq/2, delta_freq/2, 0.5, "packet_len")
        (self.radar_signal_generator_fsk_c_0).set_min_output_buffer(8388608)
        self.radar_qtgui_time_plot_0_1 = radar.qtgui_time_plot(100, 'velocity', (-3,3), range_time, "TRACKING")
        self.radar_qtgui_time_plot_0_0_1 = radar.qtgui_time_plot(100, 'range', (0,15), range_time, "TRACKING")
        self.radar_qtgui_time_plot_0_0 = radar.qtgui_time_plot(100, 'range', (0,15), range_time, '')
        self.radar_qtgui_time_plot_0 = radar.qtgui_time_plot(100, 'velocity', (-3,3), range_time, '')
        self.radar_print_results_1 = radar.print_results(False, "store_msgs.txt")
        self.radar_find_max_peak_c_0 = radar.find_max_peak_c(samp_rate_red, threshold, int(samp_protect), (), False, "packet_len")
        self.radar_estimator_fsk_0 = radar.estimator_fsk(center_freq, delta_freq/fac_corr, False)
        self.blocks_tagged_stream_multiply_length_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 1/float(decim_fac))
        (self.blocks_tagged_stream_multiply_length_0_0).set_min_output_buffer(512)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 1/float(decim_fac))
        (self.blocks_tagged_stream_multiply_length_0).set_min_output_buffer(512)
        self.blocks_multiply_conjugate_cc_1 = blocks.multiply_conjugate_cc(1)
        (self.blocks_multiply_conjugate_cc_1).set_min_output_buffer(512)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        (self.blocks_multiply_conjugate_cc_0).set_min_output_buffer(8388608)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_fsk_0, 'Msg out'), (self.radar_print_results_1, 'Msg in'))
        self.msg_connect((self.radar_estimator_fsk_0, 'Msg out'), (self.radar_qtgui_time_plot_0, 'Msg in'))
        self.msg_connect((self.radar_estimator_fsk_0, 'Msg out'), (self.radar_qtgui_time_plot_0_0, 'Msg in'))
        self.msg_connect((self.radar_estimator_fsk_0, 'Msg out'), (self.radar_tracking_singletarget_0, 'Msg in'))
        self.msg_connect((self.radar_find_max_peak_c_0, 'Msg out'), (self.radar_estimator_fsk_0, 'Msg in'))
        self.msg_connect((self.radar_tracking_singletarget_0, 'Msg out'), (self.radar_qtgui_time_plot_0_0_1, 'Msg in'))
        self.msg_connect((self.radar_tracking_singletarget_0, 'Msg out'), (self.radar_qtgui_time_plot_0_1, 'Msg in'))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.radar_split_fsk_cc_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_1, 0), (self.radar_find_max_peak_c_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_ts_fft_cc_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0, 0), (self.radar_ts_fft_cc_0, 0))
        self.connect((self.radar_signal_generator_fsk_c_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.radar_signal_generator_fsk_c_0, 0), (self.radar_usrp_echotimer_cc_0, 0))
        self.connect((self.radar_split_fsk_cc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.radar_split_fsk_cc_0, 1), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.radar_ts_fft_cc_0, 0), (self.blocks_multiply_conjugate_cc_1, 1))
        self.connect((self.radar_ts_fft_cc_0_0, 0), (self.blocks_multiply_conjugate_cc_1, 0))
        self.connect((self.radar_usrp_echotimer_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_tagged_stream_multiply_length_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_fsk_tracking_singletarget")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_red(self.samp_rate/2/self.samp_per_freq/self.decim_fac)
        self.set_measure_time((self.block_per_tag*self.samp_per_freq*2)/float(self.samp_rate))

    def get_samp_per_freq(self):
        return self.samp_per_freq

    def set_samp_per_freq(self, samp_per_freq):
        self.samp_per_freq = samp_per_freq
        self.set_samp_rate_red(self.samp_rate/2/self.samp_per_freq/self.decim_fac)
        self.set_min_output_buffer(2*self.samp_per_freq*self.block_per_tag*2)
        self.set_measure_time((self.block_per_tag*self.samp_per_freq*2)/float(self.samp_rate))

    def get_decim_fac(self):
        return self.decim_fac

    def set_decim_fac(self, decim_fac):
        self.decim_fac = decim_fac
        self.set_samp_rate_red(self.samp_rate/2/self.samp_per_freq/self.decim_fac)
        self.set_packet_len_red(self.block_per_tag/self.decim_fac)
        self.blocks_tagged_stream_multiply_length_0_0.set_scalar(1/float(self.decim_fac))
        self.blocks_tagged_stream_multiply_length_0.set_scalar(1/float(self.decim_fac))

    def get_block_per_tag(self):
        return self.block_per_tag

    def set_block_per_tag(self, block_per_tag):
        self.block_per_tag = block_per_tag
        self.set_packet_len_red(self.block_per_tag/self.decim_fac)
        self.set_min_output_buffer(2*self.samp_per_freq*self.block_per_tag*2)
        self.set_measure_time((self.block_per_tag*self.samp_per_freq*2)/float(self.samp_rate))

    def get_samp_rate_red(self):
        return self.samp_rate_red

    def set_samp_rate_red(self, samp_rate_red):
        self.samp_rate_red = samp_rate_red
        self.set_freq_res(self.samp_rate_red/float(self.packet_len_red))

    def get_packet_len_red(self):
        return self.packet_len_red

    def set_packet_len_red(self, packet_len_red):
        self.packet_len_red = packet_len_red
        self.set_freq_res(self.samp_rate_red/float(self.packet_len_red))

    def get_freq_res(self):
        return self.freq_res

    def set_freq_res(self, freq_res):
        self.freq_res = freq_res
        self.set_vel_res(self.freq_res/2.0/self.center_freq*3e8)

    def get_fac_corr(self):
        return self.fac_corr

    def set_fac_corr(self, fac_corr):
        self.fac_corr = fac_corr
        self.set_range_res(3e8/2/self.delta_freq*self.fac_corr)

    def get_delta_freq(self):
        return self.delta_freq

    def set_delta_freq(self, delta_freq):
        self.delta_freq = delta_freq
        self.set_range_res(3e8/2/self.delta_freq*self.fac_corr)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_vel_res(self.freq_res/2.0/self.center_freq*3e8)

    def get_wait_to_start(self):
        return self.wait_to_start

    def set_wait_to_start(self, wait_to_start):
        self.wait_to_start = wait_to_start

    def get_vel_res(self):
        return self.vel_res

    def set_vel_res(self, vel_res):
        self.vel_res = vel_res

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.radar_find_max_peak_c_0.set_threshold(self.threshold)

    def get_samp_protect(self):
        return self.samp_protect

    def set_samp_protect(self, samp_protect):
        self.samp_protect = samp_protect
        self.radar_find_max_peak_c_0.set_samp_protect(int(self.samp_protect))

    def get_range_time(self):
        return self.range_time

    def set_range_time(self, range_time):
        self.range_time = range_time

    def get_range_res(self):
        return self.range_res

    def set_range_res(self, range_res):
        self.range_res = range_res

    def get_min_output_buffer(self):
        return self.min_output_buffer

    def set_min_output_buffer(self, min_output_buffer):
        self.min_output_buffer = min_output_buffer

    def get_measure_time(self):
        return self.measure_time

    def set_measure_time(self, measure_time):
        self.measure_time = measure_time

    def get_gain_tx(self):
        return self.gain_tx

    def set_gain_tx(self, gain_tx):
        self.gain_tx = gain_tx
        self.radar_usrp_echotimer_cc_0.set_tx_gain(self.gain_tx)

    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.radar_usrp_echotimer_cc_0.set_rx_gain(self.gain_rx)

    def get_delay_samp(self):
        return self.delay_samp

    def set_delay_samp(self, delay_samp):
        self.delay_samp = delay_samp
        self.radar_usrp_echotimer_cc_0.set_num_delay_samps(int(self.delay_samp))


def main(top_block_cls=usrp_echotimer_fsk_tracking_singletarget, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
