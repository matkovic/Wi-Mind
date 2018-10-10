import numpy as np
from scipy import signal
import math
import matplotlib.pyplot as plt
import pandas as pd
from peakutils.peak import indexes


class DataExtractor:
    """Provides functions to extract relevant features (i.e. breathing or heartbeat features)
    from the wirelessly acuired data (from GNU Radio)."""

    def __init__(self, t, y, samp_rate):
        """
        :param t: (Array) Timestamps of phase values
        :param y: (Array) Phase values
        :param samp_rate: sampling rate
        """
        self.t = t
        self.y = y
        self.samp_rate = int(samp_rate)

    def raw_windowing_breathing(self, window_size, step, highpass_beat_f=5):
        """Return breathing features across the signal, according to the given window size, step and cutoff freq

        :param window_size: (int) Sliding time window length (in seconds)
        :param step: (int) Sliding time window step (in seconds)
        :param highpass_beat_f: Cutoff frequency to remove slow drift noise.
        :return: Dataframe of features for each time window.
        """

        pd_df = pd.DataFrame()
        times = []

        for i in range(min(window_size*self.samp_rate, len(self.t)-1), len(self.t), step*self.samp_rate):
            end_ind = min(len(self.t)-1, window_size*self.samp_rate)
            win_t = self.t[i-end_ind:i]
            win_y = self.y[i-end_ind:i]

            curr_df = self.extract_from_breathing_time(win_t, win_y)

            times = np.append(times, win_t[-1])
            pd_df = pd_df.append(curr_df, ignore_index=True)

        pd_df['times'] = times
        return pd_df

    def raw_windowing_heartrate(self, window_size, step, bandpass_beat_fs=[60, 150]):
        """Return heartbeat features across the signal, according to the given window size, step and cutoff freq

        :param window_size: (int) Sliding time window length (in seconds)
        :param step: (int) Sliding time window step (in seconds)
        :param bandpass_beat_fs: Array with two values. Bandpass frequency values (low and high).
        :return: Dataframe of features for each time window.
        """

        pd_df = pd.DataFrame()
        times = []

        for i in range(min(window_size*self.samp_rate, len(self.t)-1), len(self.t), step*self.samp_rate):
            end_ind = min(len(self.t)-1, window_size*self.samp_rate)
            win_t = self.t[i-end_ind:i]
            win_y = self.y[i-end_ind:i]

            curr_df = self.extract_from_heartbeat_time(win_t, win_y)

            times = np.append(times, win_t[-1])
            pd_df = pd_df.append(curr_df, ignore_index=True)

        pd_df['times'] = times
        return pd_df

    def extract_from_breathing_time(self, win_t, win_y, highpass_beat_f=5):
        """Return breathing features from one time frame.

        :param win_t: (array) input time stamps of phase values
        :param win_y: (array) input phase values
        :param highpass_beat_f: highpass frequency filter value
        :return: breathing features for this time frame
        """

        fltrd_hp = filtering_hp(win_y, highpass_beat_f / 60, self.samp_rate)
        fltrd_hp = filtering_lp(fltrd_hp, 1, self.samp_rate)  # remove noise above 1 Hz

        fft_fltrd_hp_norm = fft_1ss(fltrd_hp, self.samp_rate, 100)
        fft_fltrd_hp_norm[1] = fft_fltrd_hp_norm[1] / max(fft_fltrd_hp_norm[1]) # normalize FFT

        # plot_time_and_frequency(win_t, win_y, fltrd_hp,
        #                         self.samp_rate, fft_fltrd_hp_norm, xlabel='frequency (breaths per minute')

        average_power = np.average(fft_fltrd_hp_norm[1])
        fft_valid = True
        if average_power >= 0.2:
            fft_valid = False

        max_respiratory_rate = fft_fltrd_hp_norm[0][fft_fltrd_hp_norm[1].tolist().index(max(fft_fltrd_hp_norm[1]))]

        fft_beginning = fft_1ss(fltrd_hp[:int(len(fltrd_hp)/2)], self.samp_rate, 100)
        fft_ending = fft_1ss(fltrd_hp[int(len(fltrd_hp)/2):], self.samp_rate, 100)
        max_rate_begining = fft_beginning[0][fft_beginning[1].tolist().index(max(fft_beginning[1]))]
        max_rate_ending = fft_ending[0][fft_ending[1].tolist().index(max(fft_ending[1]))]

        # freq_to_6 = np.trapz(abs(fft_fltrd_hp_norm[1][(fft_fltrd_hp_norm[0] <= 6)]))
        freq_6_12 = np.trapz(abs(fft_fltrd_hp_norm[1][(fft_fltrd_hp_norm[0] >= 6) & (fft_fltrd_hp_norm[0] <= 12)]))
        freq_12_18 = np.trapz(
            abs(fft_fltrd_hp_norm[1][(fft_fltrd_hp_norm[0] >= 12) & (fft_fltrd_hp_norm[0] <= 18)]))
        freq_18_24 = np.trapz(
            abs(fft_fltrd_hp_norm[1][(fft_fltrd_hp_norm[0] >= 18) & (fft_fltrd_hp_norm[0] <= 24)]))
        freq_24_30 = np.trapz(
            abs(fft_fltrd_hp_norm[1][(fft_fltrd_hp_norm[0] >= 24) & (fft_fltrd_hp_norm[0] <= 30)]))

        BB_intervals = self.breathing_intervals(win_t, fltrd_hp)

        curr_df = pd.DataFrame([[max_respiratory_rate,
                                 max_rate_ending - max_rate_begining,
                                 freq_6_12, freq_12_18, freq_18_24, freq_24_30,
                                 np.mean(BB_intervals), np.std(BB_intervals),
                                 np.mean(fltrd_hp), np.median(fltrd_hp), np.std(fltrd_hp), np.sqrt(np.mean(fltrd_hp**2)),
                                 fft_valid
                                 ]],
                               columns=['br_rate',
                                        'br_change_in_rate_start_end',
                                        'br_freq_6_12', 'br_freq_12_18', 'br_freq_18_24', 'br_freq_24_30',
                                        'br_IBI_mean', 'br_IBI_std',
                                        'br_raw_mean', 'br_raw_median', 'br_raw_std', 'br_raw_rms',
                                        'br_ok'
                                        ])
        return curr_df

    def extract_from_heartbeat_time(self, win_t, win_y, bandpass_beat_fs=[50, 150]):
        """Return heartbeat features from one time frame.

        :param win_t: (array) input time stamps of phase values
        :param win_y: (array) input phase values
        :param bandpass_beat_fs: (array of 2 values / tuple) bandpass cutoff frequencies
        :return: heartbeat features for this time frame
        """

        fltrd_bp = filtering_bp(win_y, bandpass_beat_fs[0] / 60, bandpass_beat_fs[1] / 60, self.samp_rate)

        win_y_hann = fltrd_bp * np.hanning(len(fltrd_bp))

        fft_fltrd_bp = fft_1ss(win_y_hann, self.samp_rate, 150)
        fft_fltrd_bp[1] = fft_fltrd_bp[1] / max(fft_fltrd_bp[1])

        max_heart_rate = fft_fltrd_bp[0][fft_fltrd_bp[1].tolist().index(max(fft_fltrd_bp[1]))]

        fft_beginning = fft_1ss(fltrd_bp[:int(len(fltrd_bp)/2)], self.samp_rate, 150)
        fft_ending = fft_1ss(fltrd_bp[int(len(fltrd_bp)/2):], self.samp_rate, 150)
        max_rate_begining = fft_beginning[0][fft_beginning[1].tolist().index(max(fft_beginning[1]))]
        max_rate_ending = fft_ending[0][fft_ending[1].tolist().index(max(fft_ending[1]))]

        RR_intervals = self.time_rr_intervals(win_t, fltrd_bp)

        RR_rms = np.sqrt(np.mean(RR_intervals**2))
        RR_percentage_high_50ms = sum(i > 0.5 for i in RR_intervals) / len(RR_intervals)
        RR_percentage_high_70ms = sum(i > 0.7 for i in RR_intervals) / len(RR_intervals)

        Y, frq = self.freq_hrv_ls(win_t, fltrd_bp)
        ulf = np.trapz(abs(Y[(frq <= 0.04)]))
        vlf = np.trapz(abs(Y[(frq >= 0.003) & (
                    frq <= 0.04)]))  # Slice frequency spectrum where x is between 0.003 and 0.04Hz (LF),
        # and use NumPy's trapezoidal integration function to find the area
        lf = np.trapz(abs(Y[(frq >= 0.04) & (
                    frq <= 0.15)]))  # Slice frequency spectrum where x is between 0.04 and 0.15Hz (LF),
        hf = np.trapz(abs(Y[(frq >= 0.16) & (frq <= 0.5)]))  # Do the same for 0.16-0.5Hz (HF)

        # plot_time_and_frequency(win_t, win_y, fltrd_bp, self.samp_rate,
        #                         fft_fltrd_bp, xlabel='frequency (beats per minute)')

        average_power = np.average(fft_fltrd_bp[1])
        fft_valid = True
        if average_power >= 0.25:
            fft_valid = False

        curr_df = pd.DataFrame([[max_heart_rate,
                                 max_rate_begining - max_rate_ending,
                                 np.mean(RR_intervals), np.std(RR_intervals), RR_rms,
                                 RR_percentage_high_50ms, RR_percentage_high_70ms,
                                 lf, hf, lf/hf,
                                 fft_valid
                                ]],
                               columns=['hr_rate',
                                        'hr_change_in_rate_start_end',
                                        'hr_RR_mean', 'hr_SDNN', 'hr_RMSSD',
                                        'hr_pNN50', 'hr_pNN70',
                                        'hr_HRV_lf', 'hr_HRV_hf', 'hr_HRV_lf_hf',
                                        'hr_ok'
                                        ])
        return curr_df

    def time_rr_intervals(self, t, y):
        """Returns heartbeat RR / NN intervals on a filtered input signal
        Note - it may contain noise values.

        :param t: (array) input time stamps of phase values
        :param y: (array) input phase values
        :return: (array) filtered heartbeat NN intervals
        """
        # HRV time
        indexes_peaks = indexes(y, min_dist=self.samp_rate / 2)
        RR_times = t[indexes_peaks]
        RR_intervals = np.diff(RR_times)

        RR_new = []
        for i in range(1, len(RR_intervals), 1):
            orig = RR_intervals[i-1]
            new = RR_intervals[i]
            inc_dec = abs(((new-orig)/orig)*100)
            if inc_dec > 25:
                continue
            else:
                RR_new.append(new)

        if len(RR_new) == 0:  # to deal with noisy data
            RR_new = [0]

        return np.array(RR_new)

    def breathing_intervals(self, t, y):
        """Returns intervals between each breaths. (sometimes called respiratory rate (RR) intervals)
        Note - it may contain noise.

        :param t: (array) input time stamps of phase values
        :param y: (array) input phase values
        :return: array of RR intervals
        """
        y=pd.DataFrame(y)
        # t=pd.DataFrame(t)
        y_ma = np.array(y.rolling(int(self.samp_rate*1), center=True).mean())
        y_not_nans = np.logical_not(np.isnan(y_ma))
        y_not_nans = y_not_nans[:, 0]
        y_ma = y_ma[y_not_nans, 0]
        t_ma = t[y_not_nans]
        indexes_peaks = indexes(y_ma, min_dist=self.samp_rate*1.4)

        BB_times = t_ma[indexes_peaks]
        BB_intervals_diffs = np.diff(BB_times)

        return BB_intervals_diffs

    def freq_hrv_ls(self, t, y):
        """Returns HRV (heart rate variability) in frequency domain using Lomb-Scargle periodogram.
        Note - it may contain noise.

        :param t: (array) input time stamps of phase values
        :param y: (array) input phase values
        :return: periodogram value amplitudes with corresponding frequencies
        """
        indexes_peaks = indexes(y, min_dist=self.samp_rate / 2)

        if len(indexes_peaks) < 2:
            return np.array([0]), np.array([0])

        peaklist = indexes_peaks
        RR_list = np.diff(t[indexes_peaks])*1000

        RR_x = peaklist[1:]
        RR_y = RR_list

        f = np.linspace(0.01, 0.5, 100)

        try:
            pgram = signal.lombscargle(RR_x, RR_y, f, normalize=True)
        except ValueError:
            return np.array([0]), np.array([0])

        return pgram, f


def plot_time_and_frequency(win_t, win_y, fltrd_hp, samp_rate, fltrd, xlabel='frequency (breaths per minute)'):
    """Signal plotting"""
    plt.figure(1)
    plt.clf()
    plt.subplot(121)
    plt.xlabel('time (s)', fontsize=12)
    plt.ylabel('distance', fontsize=12)
    plt.plot(win_t, win_y, label='Signal')
    plt.plot(win_t, fltrd_hp, 'orange', label='Filtered signal')
    indexes_peaks = indexes(fltrd_hp, min_dist=samp_rate / 2)
    plt.plot(win_t[indexes_peaks], fltrd_hp[indexes_peaks], 'ro')
    plt.legend()
    plt.subplot(122)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel('amplitude', fontsize=12)
    plt.plot(fltrd[0], fltrd[1], 'orange')


def fft_1ss(y, samp_rate, upper_limit_f):
    """Returns one side FFT"""
    ffted = np.fft.fft(y, ceilpow2(len(y)))  # pow of 2 works faster; also can change FFT granularity is bigger values
    # ffted = np.fft.fft(y)
    ffted_abs = np.abs(ffted)
    ffted_1ss = ffted_abs[:int(len(ffted)/2)]
    xf = np.linspace(0, (samp_rate)*60, len(ffted))
    to_bin = math.floor(upper_limit_f*(len(ffted))/max(xf))
    return [xf[:to_bin], ffted_1ss[:to_bin]]


def filtering_lp(y_sig, cut, fs):
    """Returns a filtered signal, using lowpass filter"""
    nyq = 0.5 * fs
    low = cut / nyq
    b, a = signal.butter(2, low, 'low')
    y = signal.filtfilt(b, a, y_sig)
    return y


def filtering_hp(y_sig, cut, fs):
    """Returns a filtered signal, using highpass filter"""
    nyq = 0.5 * fs
    high = cut / nyq
    b, a = signal.butter(2, high, 'high')
    y = signal.filtfilt(b, a, y_sig)
    return y


def filtering_bp(y_sig, lowcut, highcut, fs):
    """Returns a filtered signal, using bandpass filter"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(2, [low, high], btype='band')
    y = signal.filtfilt(b, a, y_sig)
    return y


def ceilpow2(N):
    '''Returns the closest higher 2^x value'''
    # Example -
    #     ceilpow2(15) = 16
    #     ceilpow2(16) = 16
    p = 1
    while p < N:
        p *= 2
    return p
