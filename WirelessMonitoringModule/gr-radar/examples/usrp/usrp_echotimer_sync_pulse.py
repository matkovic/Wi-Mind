#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrp Echotimer Sync Pulse
# Generated: Sun Feb 11 12:05:57 2018
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


class usrp_echotimer_sync_pulse(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Usrp Echotimer Sync Pulse")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Usrp Echotimer Sync Pulse")
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

        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_sync_pulse")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.wait_samp = wait_samp = 100,100,100,100
        self.send_samp = send_samp = 100,400,300
        self.packet_len = packet_len = sum(wait_samp)+sum(send_samp)
        self.wait_to_start = wait_to_start = 0.03
        self.tx_gain = tx_gain = 20
        self.samp_rate = samp_rate = 15000000
        self.rx_gain = rx_gain = 40
        self.num_delay_samp = num_delay_samp = 0
        self.num_corr = num_corr = packet_len
        self.min_output_buffer = min_output_buffer = packet_len*2
        self.center_freq = center_freq = 2400000000

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 100, 1, 20, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX Gain', "counter_slider", float)
        self.top_layout.addWidget(self._tx_gain_win)
        self._rx_gain_range = Range(0, 100, 1, 40, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float)
        self.top_layout.addWidget(self._rx_gain_win)
        self._num_delay_samp_range = Range(0, packet_len, 1, 0, 200)
        self._num_delay_samp_win = RangeWidget(self._num_delay_samp_range, self.set_num_delay_samp, 'Number of delayed samples', "counter_slider", float)
        self.top_layout.addWidget(self._num_delay_samp_win)
        self._num_corr_range = Range(0, packet_len, 1, packet_len, 200)
        self._num_corr_win = RangeWidget(self._num_corr_range, self.set_num_corr, 'Number of cross correlations', "counter_slider", float)
        self.top_layout.addWidget(self._num_corr_win)
        self.radar_usrp_echotimer_cc_0 = radar.usrp_echotimer_cc(samp_rate, center_freq, int(num_delay_samp), '', '', 'internal', 'none', 'TX/RX', tx_gain, 0.2, wait_to_start, 0, '', '', 'internal', 'none', 'RX2', rx_gain, 0.2, wait_to_start, 0, "packet_len")
        (self.radar_usrp_echotimer_cc_0).set_min_output_buffer(2400)
        self.radar_signal_generator_sync_pulse_c_0 = radar.signal_generator_sync_pulse_c(packet_len, (send_samp), (wait_samp), 0.5, "packet_len")
        (self.radar_signal_generator_sync_pulse_c_0).set_min_output_buffer(2400)
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_estimator_sync_pulse_c_0 = radar.estimator_sync_pulse_c(int(num_corr), "packet_len")
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	packet_len, #size
        	samp_rate, #samp_rate
        	'QT GUI Plot', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

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

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_sync_pulse_c_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.radar_signal_generator_sync_pulse_c_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.radar_signal_generator_sync_pulse_c_0, 0), (self.radar_estimator_sync_pulse_c_0, 0))
        self.connect((self.radar_signal_generator_sync_pulse_c_0, 0), (self.radar_usrp_echotimer_cc_0, 0))
        self.connect((self.radar_usrp_echotimer_cc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.radar_usrp_echotimer_cc_0, 0), (self.radar_estimator_sync_pulse_c_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_echotimer_sync_pulse")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_wait_samp(self):
        return self.wait_samp

    def set_wait_samp(self, wait_samp):
        self.wait_samp = wait_samp
        self.set_packet_len(sum(self.wait_samp)+sum(self.send_samp))

    def get_send_samp(self):
        return self.send_samp

    def set_send_samp(self, send_samp):
        self.send_samp = send_samp
        self.set_packet_len(sum(self.wait_samp)+sum(self.send_samp))

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.set_num_corr(self.packet_len)
        self.set_min_output_buffer(self.packet_len*2)

    def get_wait_to_start(self):
        return self.wait_to_start

    def set_wait_to_start(self, wait_to_start):
        self.wait_to_start = wait_to_start

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.radar_usrp_echotimer_cc_0.set_tx_gain(self.tx_gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.radar_usrp_echotimer_cc_0.set_rx_gain(self.rx_gain)

    def get_num_delay_samp(self):
        return self.num_delay_samp

    def set_num_delay_samp(self, num_delay_samp):
        self.num_delay_samp = num_delay_samp
        self.radar_usrp_echotimer_cc_0.set_num_delay_samps(int(self.num_delay_samp))

    def get_num_corr(self):
        return self.num_corr

    def set_num_corr(self, num_corr):
        self.num_corr = num_corr
        self.radar_estimator_sync_pulse_c_0.set_num_xcorr(int(self.num_corr))

    def get_min_output_buffer(self):
        return self.min_output_buffer

    def set_min_output_buffer(self, min_output_buffer):
        self.min_output_buffer = min_output_buffer

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq


def main(top_block_cls=usrp_echotimer_sync_pulse, options=None):

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
