#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrp Echotimer Cw
# Generated: Fri Jan 26 19:15:02 2018
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
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import radar
import sip
import sys
from gnuradio import qtgui


class usrp_echotimer_cw(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Usrp Echotimer Cw")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Usrp Echotimer Cw")
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

        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_cw")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 250000
        self.packet_len = packet_len = 2**16
        self.decim_fac = decim_fac = 2**9
        self.wait_to_start = wait_to_start = 0.02
        self.threshold = threshold = -200
        self.t_measure = t_measure = packet_len/float(samp_rate)
        self.samp_protect = samp_protect = 0
        self.packet_len_red = packet_len_red = packet_len/decim_fac
        self.min_output_buffer = min_output_buffer = packet_len*2
        self.gain_tx = gain_tx = 0
        self.gain_rx = gain_rx = 0
        self.freq_res = freq_res = samp_rate/float(packet_len)
        self.center_freq = center_freq = 2400000000

        ##################################################
        # Blocks
        ##################################################
        self._threshold_range = Range(-200, 100, 1, -200, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, 'Find peak treshold', "counter_slider", float)
        self.top_grid_layout.addWidget(self._threshold_win, 1,1)
        self._samp_protect_range = Range(0, 100, 1, 0, 200)
        self._samp_protect_win = RangeWidget(self._samp_protect_range, self.set_samp_protect, 'Number protected samples', "counter_slider", float)
        self.top_grid_layout.addWidget(self._samp_protect_win, 1,0)
        self._gain_tx_range = Range(0, 100, 1, 0, 200)
        self._gain_tx_win = RangeWidget(self._gain_tx_range, self.set_gain_tx, 'TX gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_tx_win, 0,0)
        self._gain_rx_range = Range(0, 100, 1, 0, 200)
        self._gain_rx_win = RangeWidget(self._gain_rx_range, self.set_gain_rx, 'RX gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_rx_win, 0,1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_fac,
                taps=None,
                fractional_bw=None,
        )
        self.radar_usrp_echotimer_cc_0 = radar.usrp_echotimer_cc(samp_rate, center_freq, 24, '', '', 'internal', 'none', 'TX/RX', gain_tx, 0.1, wait_to_start, 0, '', '', 'internal', 'none', 'RX2', gain_rx, 0.1, wait_to_start, 0, "packet_len")
        (self.radar_usrp_echotimer_cc_0).set_min_output_buffer(131072)
        self.radar_ts_fft_cc_0 = radar.ts_fft_cc(packet_len/decim_fac,  "packet_len")
        self.radar_signal_generator_cw_c_0 = radar.signal_generator_cw_c(packet_len, samp_rate, (0, ), 0.5, "packet_len")
        (self.radar_signal_generator_cw_c_0).set_min_output_buffer(131072)
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_find_max_peak_c_0 = radar.find_max_peak_c(samp_rate/decim_fac, threshold, int(samp_protect), (), False, "packet_len")
        self.radar_estimator_cw_0 = radar.estimator_cw(center_freq)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	packet_len/decim_fac, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/decim_fac, #bw
        	'QT GUI Plot', #name
        	True, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 1.0/decim_fac)
        (self.blocks_tagged_stream_multiply_length_0).set_min_output_buffer(131072)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        (self.blocks_multiply_conjugate_cc_0).set_min_output_buffer(131072)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_cw_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.msg_connect((self.radar_find_max_peak_c_0, 'Msg out'), (self.radar_estimator_cw_0, 'Msg in'))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_ts_fft_cc_0, 0))
        self.connect((self.radar_signal_generator_cw_c_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.radar_signal_generator_cw_c_0, 0), (self.radar_usrp_echotimer_cc_0, 0))
        self.connect((self.radar_ts_fft_cc_0, 0), (self.radar_find_max_peak_c_0, 0))
        self.connect((self.radar_usrp_echotimer_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_cw")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_t_measure(self.packet_len/float(self.samp_rate))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate/self.decim_fac)
        self.set_freq_res(self.samp_rate/float(self.packet_len))

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.set_t_measure(self.packet_len/float(self.samp_rate))
        self.set_packet_len_red(self.packet_len/self.decim_fac)
        self.set_min_output_buffer(self.packet_len*2)
        self.set_freq_res(self.samp_rate/float(self.packet_len))

    def get_decim_fac(self):
        return self.decim_fac

    def set_decim_fac(self, decim_fac):
        self.decim_fac = decim_fac
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate/self.decim_fac)
        self.set_packet_len_red(self.packet_len/self.decim_fac)
        self.blocks_tagged_stream_multiply_length_0.set_scalar(1.0/self.decim_fac)

    def get_wait_to_start(self):
        return self.wait_to_start

    def set_wait_to_start(self, wait_to_start):
        self.wait_to_start = wait_to_start

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.radar_find_max_peak_c_0.set_threshold(self.threshold)

    def get_t_measure(self):
        return self.t_measure

    def set_t_measure(self, t_measure):
        self.t_measure = t_measure

    def get_samp_protect(self):
        return self.samp_protect

    def set_samp_protect(self, samp_protect):
        self.samp_protect = samp_protect
        self.radar_find_max_peak_c_0.set_samp_protect(int(self.samp_protect))

    def get_packet_len_red(self):
        return self.packet_len_red

    def set_packet_len_red(self, packet_len_red):
        self.packet_len_red = packet_len_red

    def get_min_output_buffer(self):
        return self.min_output_buffer

    def set_min_output_buffer(self, min_output_buffer):
        self.min_output_buffer = min_output_buffer

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

    def get_freq_res(self):
        return self.freq_res

    def set_freq_res(self, freq_res):
        self.freq_res = freq_res

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq


def main(top_block_cls=usrp_echotimer_cw, options=None):

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
