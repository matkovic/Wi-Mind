#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Simulator Sync Pulse
# Generated: Sat Jan 20 16:01:11 2018
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
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import radar
import sys
from gnuradio import qtgui


class simulator_sync_pulse(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Simulator Sync Pulse")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Simulator Sync Pulse")
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

        self.settings = Qt.QSettings("GNU Radio", "simulator_sync_pulse")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 250000
        self.num_skip = num_skip = 50
        self.num_corr = num_corr = 75

        ##################################################
        # Blocks
        ##################################################
        self._num_corr_range = Range(0, 100, 1, 75, 200)
        self._num_corr_win = RangeWidget(self._num_corr_range, self.set_num_corr, "num_corr", "counter_slider", float)
        self.top_layout.addWidget(self._num_corr_win)
        self.radar_signal_generator_sync_pulse_c_0 = radar.signal_generator_sync_pulse_c(2**12, ((300,50,200)), ((100,200,50)), 0.5, "packet_len")
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_estimator_sync_pulse_c_0 = radar.estimator_sync_pulse_c(int(num_corr), "packet_len")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, num_skip)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_sync_pulse_c_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.connect((self.blocks_skiphead_0, 0), (self.radar_estimator_sync_pulse_c_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.radar_estimator_sync_pulse_c_0, 1))
        self.connect((self.radar_signal_generator_sync_pulse_c_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.radar_signal_generator_sync_pulse_c_0, 0), (self.blocks_throttle_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "simulator_sync_pulse")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_num_skip(self):
        return self.num_skip

    def set_num_skip(self, num_skip):
        self.num_skip = num_skip

    def get_num_corr(self):
        return self.num_corr

    def set_num_corr(self, num_corr):
        self.num_corr = num_corr
        self.radar_estimator_sync_pulse_c_0.set_num_xcorr(int(self.num_corr))


def main(top_block_cls=simulator_sync_pulse, options=None):

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
