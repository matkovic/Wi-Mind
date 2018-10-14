#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrp Echotimer Fmcw Edited
# Generated: Tue Aug 14 18:34:43 2018
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
import epy_block_0
import radar
import sip
import sys
from gnuradio import qtgui


class usrp_echotimer_fmcw_edited(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Usrp Echotimer Fmcw Edited")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Usrp Echotimer Fmcw Edited")
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

        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_fmcw_edited")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 40000000
        self.sweep_freq = sweep_freq = samp_rate/2
        self.samp_up = samp_up = 2**15
        self.wait_to_start = wait_to_start = 0.02
        self.tx_gain = tx_gain = 40
        self.threshold = threshold = -150
        self.rx_gain = rx_gain = 60
        self.range_time = range_time = 30
        self.range_res = range_res = 3e8/2/sweep_freq
        self.protect_samp = protect_samp = 0
        self.min_output_buffer = min_output_buffer = int((samp_up)*2)
        self.max_output_buffer = max_output_buffer = 0
        self.freq_res_up = freq_res_up = samp_rate/samp_up
        self.delay_samp = delay_samp = 79
        self.decim_fac = decim_fac = 2**3
        self.center_freq = center_freq = 5.2e9

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 100, 1, 40, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 0,0)
        self._threshold_range = Range(-150, 0, 1, -150, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, "threshold", "counter_slider", float)
        self.top_grid_layout.addWidget(self._threshold_win, 1,0)
        self._rx_gain_range = Range(0, 100, 1, 60, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 0,1)
        self._protect_samp_range = Range(0, 100, 1, 0, 200)
        self._protect_samp_win = RangeWidget(self._protect_samp_range, self.set_protect_samp, "protect_samp", "counter_slider", float)
        self.top_grid_layout.addWidget(self._protect_samp_win, 1,1)
        self._delay_samp_range = Range(0, 100, 1, 79, 200)
        self._delay_samp_win = RangeWidget(self._delay_samp_range, self.set_delay_samp, 'Number delay samples', "counter_slider", float)
        self.top_layout.addWidget(self._delay_samp_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_fac,
                taps=None,
                fractional_bw=None,
        )
        self.radar_usrp_echotimer_cc_0 = radar.usrp_echotimer_cc(samp_rate, center_freq, int(delay_samp), '', '', 'internal', 'none', 'TX/RX', tx_gain, 0.1, wait_to_start, 0, '', '', 'internal', 'none', 'RX2', rx_gain, 0.1, wait_to_start, 0, "packet_len")
        (self.radar_usrp_echotimer_cc_0).set_min_output_buffer(65536)
        self.radar_ts_fft_cc_1 = radar.ts_fft_cc(samp_up/decim_fac,  "packet_len")
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(samp_rate, samp_up, 0, 0, -sweep_freq/2, sweep_freq, 1, "packet_len")
        (self.radar_signal_generator_fmcw_c_0).set_min_output_buffer(65536)
        self.radar_my_find_max_peak_c_0 = radar.my_find_max_peak_c(samp_rate/decim_fac, threshold, int(protect_samp), (), False, 44, "packet_len")
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	300, #size
        	samp_rate/decim_fac, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-4, 4)

        self.qtgui_time_sink_x_1.set_y_label('power', "")

        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_1.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 1.0/decim_fac)
        (self.blocks_tagged_stream_multiply_length_0).set_min_output_buffer(65536)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        (self.blocks_multiply_conjugate_cc_0).set_min_output_buffer(65536)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*1, '/home/tmatko/Desktop/grstuff/acquired-signals/time13.dat', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, '/home/tmatko/Desktop/grstuff/acquired-signals/phase13.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_my_find_max_peak_c_0, 'Msg out'), (self.epy_block_0, 'msg_in'))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_ts_fft_cc_1, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.epy_block_0, 1), (self.blocks_file_sink_0_0, 0))
        self.connect((self.epy_block_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.radar_usrp_echotimer_cc_0, 0))
        self.connect((self.radar_ts_fft_cc_1, 0), (self.radar_my_find_max_peak_c_0, 0))
        self.connect((self.radar_usrp_echotimer_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_fmcw_edited")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sweep_freq(self.samp_rate/2)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/self.decim_fac)
        self.set_freq_res_up(self.samp_rate/self.samp_up)

    def get_sweep_freq(self):
        return self.sweep_freq

    def set_sweep_freq(self, sweep_freq):
        self.sweep_freq = sweep_freq
        self.set_range_res(3e8/2/self.sweep_freq)

    def get_samp_up(self):
        return self.samp_up

    def set_samp_up(self, samp_up):
        self.samp_up = samp_up
        self.set_min_output_buffer(int((self.samp_up)*2))
        self.set_freq_res_up(self.samp_rate/self.samp_up)

    def get_wait_to_start(self):
        return self.wait_to_start

    def set_wait_to_start(self, wait_to_start):
        self.wait_to_start = wait_to_start

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.radar_usrp_echotimer_cc_0.set_tx_gain(self.tx_gain)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.radar_my_find_max_peak_c_0.set_threshold(self.threshold)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.radar_usrp_echotimer_cc_0.set_rx_gain(self.rx_gain)

    def get_range_time(self):
        return self.range_time

    def set_range_time(self, range_time):
        self.range_time = range_time

    def get_range_res(self):
        return self.range_res

    def set_range_res(self, range_res):
        self.range_res = range_res

    def get_protect_samp(self):
        return self.protect_samp

    def set_protect_samp(self, protect_samp):
        self.protect_samp = protect_samp
        self.radar_my_find_max_peak_c_0.set_samp_protect(int(self.protect_samp))

    def get_min_output_buffer(self):
        return self.min_output_buffer

    def set_min_output_buffer(self, min_output_buffer):
        self.min_output_buffer = min_output_buffer

    def get_max_output_buffer(self):
        return self.max_output_buffer

    def set_max_output_buffer(self, max_output_buffer):
        self.max_output_buffer = max_output_buffer

    def get_freq_res_up(self):
        return self.freq_res_up

    def set_freq_res_up(self, freq_res_up):
        self.freq_res_up = freq_res_up

    def get_delay_samp(self):
        return self.delay_samp

    def set_delay_samp(self, delay_samp):
        self.delay_samp = delay_samp
        self.radar_usrp_echotimer_cc_0.set_num_delay_samps(int(self.delay_samp))

    def get_decim_fac(self):
        return self.decim_fac

    def set_decim_fac(self, decim_fac):
        self.decim_fac = decim_fac
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/self.decim_fac)
        self.blocks_tagged_stream_multiply_length_0.set_scalar(1.0/self.decim_fac)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.radar_usrp_echotimer_cc_0.set_frequency(self.center_freq)


def main(top_block_cls=usrp_echotimer_fmcw_edited, options=None):

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
