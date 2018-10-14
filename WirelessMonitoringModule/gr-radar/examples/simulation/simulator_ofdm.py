#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Simulator Ofdm
# Generated: Sat Jan 20 16:00:36 2018
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
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy
import numpy as np
import radar
import sys
from gnuradio import qtgui


class simulator_ofdm(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Simulator Ofdm")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Simulator Ofdm")
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

        self.settings = Qt.QSettings("GNU Radio", "simulator_ofdm")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5000000
        self.packet_len = packet_len = 2**9
        self.occupied_carriers_all = occupied_carriers_all = (range(-26,27),)
        self.fft_len = fft_len = 2**6
        self.zeropadding_fac = zeropadding_fac = 2
        self.velocity = velocity = 500
        self.value_range = value_range = 100
        self.v_max = v_max = 2000
        self.transpose_len = transpose_len = int(np.ceil(packet_len*4.0/len(occupied_carriers_all[0])))
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.payload_mod = payload_mod = digital.constellation_qpsk()
        self.occupied_carriers = occupied_carriers = (range(-26, -21) + range(-20, -7) + range(-6, 0) + range(1, 7) + range(8, 21) + range(22, 27),)
        self.length_tag_key = length_tag_key = "packet_len"
        self.discarded_carriers = discarded_carriers = []
        self.center_freq = center_freq = 2.45e9
        self.R_max = R_max = 3e8/2/samp_rate*fft_len

        ##################################################
        # Blocks
        ##################################################
        self._velocity_range = Range(-v_max, v_max, 1, 500, 200)
        self._velocity_win = RangeWidget(self._velocity_range, self.set_velocity, 'Velocity', "counter_slider", float)
        self.top_grid_layout.addWidget(self._velocity_win, 0,1)
        self._value_range_range = Range(0.1, R_max, 1, 100, 200)
        self._value_range_win = RangeWidget(self._value_range_range, self.set_value_range, 'range', "counter_slider", float)
        self.top_grid_layout.addWidget(self._value_range_win, 0,0)
        self.radar_transpose_matrix_vcvc_0_0 = radar.transpose_matrix_vcvc(transpose_len, fft_len*zeropadding_fac, "packet_len")
        (self.radar_transpose_matrix_vcvc_0_0).set_min_output_buffer(78)
        self.radar_transpose_matrix_vcvc_0 = radar.transpose_matrix_vcvc(fft_len*zeropadding_fac, transpose_len, "packet_len")
        (self.radar_transpose_matrix_vcvc_0).set_min_output_buffer(256)
        self.radar_static_target_simulator_cc_0 = radar.static_target_simulator_cc((value_range, ), (velocity, ), (1e25, ), (0, ), (0,), samp_rate, center_freq, -10, True, True, "packet_len")
        (self.radar_static_target_simulator_cc_0).set_min_output_buffer(6240)
        self.radar_qtgui_spectrogram_plot_0 = radar.qtgui_spectrogram_plot(fft_len*zeropadding_fac, 500, 'value_range', 'Velocity', 'OFDM Radar', (0,R_max), (0,v_max), (-15,-12), True, "packet_len")
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_os_cfar_2d_vc_0 = radar.os_cfar_2d_vc(fft_len*zeropadding_fac, (10,10), (0,0), 0.78, 30, "packet_len")
        self.radar_ofdm_divide_vcvc_0 = radar.ofdm_divide_vcvc(fft_len, (fft_len-len(discarded_carriers))*zeropadding_fac, (()), 0, "packet_len")
        (self.radar_ofdm_divide_vcvc_0).set_min_output_buffer(78)
        self.radar_ofdm_cyclic_prefix_remover_cvc_0 = radar.ofdm_cyclic_prefix_remover_cvc(fft_len, fft_len/4, "packet_len")
        (self.radar_ofdm_cyclic_prefix_remover_cvc_0).set_min_output_buffer(78)
        self.radar_estimator_ofdm_0 = radar.estimator_ofdm('range', fft_len*zeropadding_fac, (0,R_max), 'velocity', transpose_len, (0,v_max,-v_max,0), True)
        self.fft_vxx_0_1_0 = fft.fft_vcc(transpose_len, False, (window.blackmanharris(transpose_len)), False, 1)
        self.fft_vxx_0_1 = fft.fft_vcc(fft_len*zeropadding_fac, True, (window.blackmanharris(fft_len*zeropadding_fac)), False, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(fft_len, True, (()), True, 1)
        (self.fft_vxx_0_0).set_min_output_buffer(78)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (()), True, 1)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len+fft_len/4, 0, length_tag_key)
        (self.digital_ofdm_cyclic_prefixer_0).set_min_output_buffer(6240)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc(fft_len, occupied_carriers_all, ((),), ((),), (), length_tag_key)
        (self.digital_ofdm_carrier_allocator_cvc_0).set_min_output_buffer(78)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((payload_mod.points()), 1)
        (self.digital_chunks_to_symbols_xx_0_0).set_min_output_buffer(4096)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, length_tag_key)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*fft_len*zeropadding_fac)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, fft_len*zeropadding_fac, 0)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_len*zeropadding_fac)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 255, 1000)), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_ofdm_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.msg_connect((self.radar_os_cfar_2d_vc_0, 'Msg out'), (self.radar_estimator_ofdm_0, 'Msg in'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.radar_ofdm_cyclic_prefix_remover_cvc_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.radar_qtgui_spectrogram_plot_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.radar_ofdm_divide_vcvc_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.radar_static_target_simulator_cc_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.radar_ofdm_divide_vcvc_0, 1))
        self.connect((self.fft_vxx_0_1, 0), (self.radar_transpose_matrix_vcvc_0, 0))
        self.connect((self.fft_vxx_0_1_0, 0), (self.radar_transpose_matrix_vcvc_0_0, 0))
        self.connect((self.radar_ofdm_cyclic_prefix_remover_cvc_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.radar_ofdm_divide_vcvc_0, 0), (self.fft_vxx_0_1, 0))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.radar_transpose_matrix_vcvc_0, 0), (self.fft_vxx_0_1_0, 0))
        self.connect((self.radar_transpose_matrix_vcvc_0_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.radar_transpose_matrix_vcvc_0_0, 0), (self.radar_os_cfar_2d_vc_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "simulator_ofdm")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_R_max(3e8/2/self.samp_rate*self.fft_len)
        self.radar_static_target_simulator_cc_0.setup_targets((self.value_range, ), (self.velocity, ), (1e25, ), (0, ), (0,), self.samp_rate, self.center_freq, -10, True, True)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.set_transpose_len(int(np.ceil(self.packet_len*4.0/len(self.occupied_carriers_all[0]))))
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_occupied_carriers_all(self):
        return self.occupied_carriers_all

    def set_occupied_carriers_all(self, occupied_carriers_all):
        self.occupied_carriers_all = occupied_carriers_all
        self.set_transpose_len(int(np.ceil(self.packet_len*4.0/len(self.occupied_carriers_all[0]))))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_R_max(3e8/2/self.samp_rate*self.fft_len)

    def get_zeropadding_fac(self):
        return self.zeropadding_fac

    def set_zeropadding_fac(self, zeropadding_fac):
        self.zeropadding_fac = zeropadding_fac

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        self.radar_static_target_simulator_cc_0.setup_targets((self.value_range, ), (self.velocity, ), (1e25, ), (0, ), (0,), self.samp_rate, self.center_freq, -10, True, True)

    def get_value_range(self):
        return self.value_range

    def set_value_range(self, value_range):
        self.value_range = value_range
        self.radar_static_target_simulator_cc_0.setup_targets((self.value_range, ), (self.velocity, ), (1e25, ), (0, ), (0,), self.samp_rate, self.center_freq, -10, True, True)

    def get_v_max(self):
        return self.v_max

    def set_v_max(self, v_max):
        self.v_max = v_max

    def get_transpose_len(self):
        return self.transpose_len

    def set_transpose_len(self, transpose_len):
        self.transpose_len = transpose_len

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key

    def get_discarded_carriers(self):
        return self.discarded_carriers

    def set_discarded_carriers(self, discarded_carriers):
        self.discarded_carriers = discarded_carriers

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.radar_static_target_simulator_cc_0.setup_targets((self.value_range, ), (self.velocity, ), (1e25, ), (0, ), (0,), self.samp_rate, self.center_freq, -10, True, True)

    def get_R_max(self):
        return self.R_max

    def set_R_max(self, R_max):
        self.R_max = R_max


def main(top_block_cls=simulator_ofdm, options=None):

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
