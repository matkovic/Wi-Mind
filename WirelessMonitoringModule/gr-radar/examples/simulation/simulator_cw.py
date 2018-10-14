#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Simulator Cw
# Generated: Sun Jan 21 11:58:40 2018
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
from gnuradio import analog
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


class simulator_cw(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Simulator Cw")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Simulator Cw")
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

        self.settings = Qt.QSettings("GNU Radio", "simulator_cw")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 250000
        self.packet_len = packet_len = 2**15
        self.freq_res = freq_res = samp_rate/float(packet_len)
        self.center_freq = center_freq = 5.7e9
        self.vel = vel = 50
        self.v_res = v_res = freq_res*3e8/2/center_freq
        self.time_res = time_res = packet_len/float(samp_rate)
        self.range_value = range_value = 2000
        self.min_output_buffer = min_output_buffer = int(packet_len*2)
        self.max_output_buffer = max_output_buffer = 0
        self.freq = freq = (0,)
        self.decimator_fac = decimator_fac = 2**0

        ##################################################
        # Blocks
        ##################################################
        self._vel_range = Range(-50, 50, 0.1, 50, 200)
        self._vel_win = RangeWidget(self._vel_range, self.set_vel, "vel", "counter_slider", float)
        self.top_layout.addWidget(self._vel_win)
        self._range_value_range = Range(0, 10000, 100, 2000, 200)
        self._range_value_win = RangeWidget(self._range_value_range, self.set_range_value, 'range', "counter_slider", float)
        self.top_layout.addWidget(self._range_value_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decimator_fac,
                taps=None,
                fractional_bw=None,
        )
        self.radar_ts_fft_cc_0 = radar.ts_fft_cc(packet_len/decimator_fac,  "packet_len")
        (self.radar_ts_fft_cc_0).set_min_output_buffer(65536)
        self.radar_static_target_simulator_cc_0 = radar.static_target_simulator_cc((range_value,), (vel,), (1e22,), (0,), (0,), samp_rate, center_freq, -10, True, False, "packet_len")
        (self.radar_static_target_simulator_cc_0).set_min_output_buffer(65536)
        self.radar_signal_generator_cw_c_0 = radar.signal_generator_cw_c(packet_len, samp_rate, (freq), 1, "packet_len")
        (self.radar_signal_generator_cw_c_0).set_min_output_buffer(65536)
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_os_cfar_c_0 = radar.os_cfar_c(samp_rate, 10, 0, 0.78, 20, True, "packet_len")
        (self.radar_os_cfar_c_0).set_min_output_buffer(65536)
        self.radar_estimator_cw_0 = radar.estimator_cw(center_freq)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	packet_len/decimator_fac, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/decimator_fac, #bw
        	'QT GUI Plot', #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        (self.blocks_throttle_0).set_min_output_buffer(65536)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 1/float(decimator_fac))
        (self.blocks_tagged_stream_multiply_length_0).set_min_output_buffer(65536)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        (self.blocks_add_xx_0).set_min_output_buffer(65536)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.5, 0)
        (self.analog_noise_source_x_0).set_min_output_buffer(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_cw_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.msg_connect((self.radar_os_cfar_c_0, 'Msg out'), (self.radar_estimator_cw_0, 'Msg in'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_ts_fft_cc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.radar_static_target_simulator_cc_0, 0))
        self.connect((self.radar_signal_generator_cw_c_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.radar_ts_fft_cc_0, 0), (self.radar_os_cfar_c_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "simulator_cw")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_time_res(self.packet_len/float(self.samp_rate))
        self.radar_static_target_simulator_cc_0.setup_targets((self.range_value,), (self.vel,), (1e22,), (0,), (0,), self.samp_rate, self.center_freq, -10, True, False)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate/self.decimator_fac)
        self.set_freq_res(self.samp_rate/float(self.packet_len))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.set_time_res(self.packet_len/float(self.samp_rate))
        self.set_min_output_buffer(int(self.packet_len*2))
        self.set_freq_res(self.samp_rate/float(self.packet_len))

    def get_freq_res(self):
        return self.freq_res

    def set_freq_res(self, freq_res):
        self.freq_res = freq_res
        self.set_v_res(self.freq_res*3e8/2/self.center_freq)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_v_res(self.freq_res*3e8/2/self.center_freq)
        self.radar_static_target_simulator_cc_0.setup_targets((self.range_value,), (self.vel,), (1e22,), (0,), (0,), self.samp_rate, self.center_freq, -10, True, False)

    def get_vel(self):
        return self.vel

    def set_vel(self, vel):
        self.vel = vel
        self.radar_static_target_simulator_cc_0.setup_targets((self.range_value,), (self.vel,), (1e22,), (0,), (0,), self.samp_rate, self.center_freq, -10, True, False)

    def get_v_res(self):
        return self.v_res

    def set_v_res(self, v_res):
        self.v_res = v_res

    def get_time_res(self):
        return self.time_res

    def set_time_res(self, time_res):
        self.time_res = time_res

    def get_range_value(self):
        return self.range_value

    def set_range_value(self, range_value):
        self.range_value = range_value
        self.radar_static_target_simulator_cc_0.setup_targets((self.range_value,), (self.vel,), (1e22,), (0,), (0,), self.samp_rate, self.center_freq, -10, True, False)

    def get_min_output_buffer(self):
        return self.min_output_buffer

    def set_min_output_buffer(self, min_output_buffer):
        self.min_output_buffer = min_output_buffer

    def get_max_output_buffer(self):
        return self.max_output_buffer

    def set_max_output_buffer(self, max_output_buffer):
        self.max_output_buffer = max_output_buffer

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_decimator_fac(self):
        return self.decimator_fac

    def set_decimator_fac(self, decimator_fac):
        self.decimator_fac = decimator_fac
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate/self.decimator_fac)
        self.blocks_tagged_stream_multiply_length_0.set_scalar(1/float(self.decimator_fac))


def main(top_block_cls=simulator_cw, options=None):

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
