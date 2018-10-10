import helper_data_prepare as hp
import helper_descriptive_statistics as descr_stats


def __main__():
    path = 'E:/signal_acquiring/'
    path_hrates = path + '_Hrates/'

    idents = ['2gu87', 'iz2ps', '1mpau', '7dwjy', '7swyk', '94mnx', 'bd47a', 'c24ur', 'ctsax', 'dkhty', 'e4gay',
              'ef5rq', 'f1gjp', 'hpbxa', 'pmyfl', 'r89k1', 'tn4vl', 'td5pr', 'gyqu9', 'fzchw', 'l53hg', '3n2f9',
              '62i9y']

    # outfile = 'full-data21.csv'
    # hp.extract_for_all_users_and_combine(path, idents, outfile)
    # hp.compare_hr_for_all_idents(path, idents)
    # hp.normalize_breathing_rate(pd.read_csv(path+outfile), path, 'full-data_1_norm.csv')
    # descr_stats.barplot_mistakes_by_task(pd.read_csv(path+outfile))
    hp.plot_all_full_signals(path, idents)


__main__()
