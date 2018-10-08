import datareader
import dataextractor
import bandreader
import numpy as np
from _bisect import bisect
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import pandas as pd
from scipy import stats
from sklearn import metrics
import seaborn as sns


def full_signal_extract(path, ident):
    """Extract breathing and heartbeat features from one user and save features to file.

    :param path: (str) main path to data, where user data is located in specific folders
    :param ident: (str) user identifier
    :return: Nothing. It saves features (dataframe) to a .csv file
    """

    dataread = datareader.DataReader(path, ident)  # initialize path to data
    data = dataread.read_grc_data()  # read from files

    data = dataread.unwrap_grc_data()  # unwrap phase. returns time and y values

    samp_rate = round(len(data[1]) / max(data[0]))

    dataextract = dataextractor.DataExtractor(data[0], data[1], samp_rate)

    cog_res = dataread.read_cognitive_load_study(ident + '-primary-extract.txt')
    end_epoch_time = dataread.get_end_time_cognitive_load_study()  # end t

    extracted_br_features = dataextract.raw_windowing_breathing(30, 1)
    extracted_br_features['br_rate'] = np.array(extracted_br_features['br_rate'].rolling(6).mean())
    extracted_br_features_roll_avg = extracted_br_features.loc[:, extracted_br_features.columns != 'times'].rolling(
        6).mean()
    extracted_br_features_roll_avg['times'] = extracted_br_features['times']
    extracted_br_features_roll_avg['br_ok'] = extracted_br_features['br_ok']

    extracted_hr_features = dataextract.raw_windowing_heartrate(10, 1)
    extracted_hr_features = extracted_hr_features.drop(['hr_HRV_lf', 'hr_HRV_hf', 'hr_HRV_lf_hf'], axis=1)
    extracted_hr_features_roll_avg = extracted_hr_features.loc[:, extracted_hr_features.columns != 'times'].rolling(
        10).mean()
    extracted_hr_features_roll_avg['times'] = extracted_hr_features['times']
    extracted_hr_features_roll_avg['hr_ok'] = extracted_hr_features['hr_ok']
    extracted_hr_features2 = dataextract.raw_windowing_heartrate(100, 1)  # longer time to extract HRV frequency feat.
    extracted_hr_features2 = extracted_hr_features2[['hr_HRV_lf', 'hr_HRV_hf', 'hr_HRV_lf_hf', 'times']]
    extracted_hr_features2_roll_avg = extracted_hr_features2.loc[:, extracted_hr_features2.columns != 'times'].rolling(
        10).mean()
    extracted_hr_features2_roll_avg['times'] = extracted_hr_features2['times']

    all_features = extracted_br_features_roll_avg
    all_features = pd.merge(all_features, extracted_hr_features_roll_avg, on='times')
    all_features = pd.merge(all_features, extracted_hr_features2_roll_avg, on='times')

    task_timestamps = dataread.get_data_task_timestamps()
    relax_timestamps = dataread.get_relax_timestamps()

    bandread = bandreader.HeartRateBand(path + '_Hrates/', ident)
    band_data = bandread.load()
    band_data_time_start = bisect(band_data[0][:], end_epoch_time - data[0][-1] * 1000)
    band_data_time_stop = bisect(band_data[0][:], end_epoch_time)
    band_data = [band_data[0][band_data_time_start:band_data_time_stop],
                 band_data[1][band_data_time_start:band_data_time_stop]]
    band_data_new__data = [(band_data[0] - band_data[0][0]) / 1000, band_data[1]]

    hr_data = extracted_hr_features_roll_avg[['times', 'hr_rate']]
    hr_data['times'] = hr_data['times'].astype(int)
    band_data = pd.DataFrame()
    band_data['times'] = band_data_new__data[0]
    band_data['times'] = band_data['times'].astype(int)
    band_data['band_rate'] = band_data_new__data[1]
    band_data = band_data.drop_duplicates(subset=['times'])
    together_data = pd.merge(hr_data, band_data, on='times')
    together_data = together_data.dropna()

    for i in range(len(all_features['times'])):
        find_in_hr_data = bisect(together_data['times'], all_features['times'][i])
        all_features.ix[i, 'band_rate'] = together_data['band_rate'][find_in_hr_data]

    for i in range(len(cog_res)):
        all_feat_ind_task_start = bisect(all_features['times'], task_timestamps[i][0])
        all_feat_ind_task_end = bisect(all_features['times'], task_timestamps[i][1])
        for j in cog_res.columns:
            all_features.ix[all_feat_ind_task_start:all_feat_ind_task_end, j] = cog_res.iloc[i][j]
            if cog_res.iloc[i][j] == 'GC' or cog_res.iloc[i][j] == 'PT':
                all_features.ix[all_feat_ind_task_start:all_feat_ind_task_end, 'keyboard_task'] = True
            elif cog_res.iloc[i][j] == 'HP' or cog_res.iloc[i][j] == 'FA' or cog_res.iloc[i][j] == 'NC' or \
                    cog_res.iloc[i][j] == 'SX':
                all_features.ix[all_feat_ind_task_start:all_feat_ind_task_end, 'keyboard_task'] = False
        for k in range(all_feat_ind_task_end - all_feat_ind_task_start + 1):
            all_features.ix[k + all_feat_ind_task_start, 'on_task_or_break_index'] = k
        for k in range(all_feat_ind_task_end - all_feat_ind_task_start, -1, -1):
            all_features.ix[all_feat_ind_task_end - k, 'on_task_or_break_index_down'] = k
        all_features.ix[all_feat_ind_task_start:all_feat_ind_task_end, 'on_task'] = True

    for i in range(len(relax_timestamps)):
        all_feat_ind_task_start = bisect(all_features['times'], relax_timestamps[i][0])
        all_feat_ind_task_end = bisect(all_features['times'], relax_timestamps[i][1])
        new_end = all_feat_ind_task_end + 30
        # if i==0:
        #     continue
        for k in range(all_feat_ind_task_end - all_feat_ind_task_start + 1):
            all_features.ix[k + all_feat_ind_task_start, 'on_task_or_break_index'] = k
            all_features.ix[k + all_feat_ind_task_start, 'consecutive_break'] = i
        for k in range(new_end - all_feat_ind_task_start + 1):
            all_features.ix[k + all_feat_ind_task_start, 'on_break_and_after_index'] = k
            if k <= 15:
                all_features.ix[k + all_feat_ind_task_start, 'engagement_increase'] = False
            elif k <= 30:
                all_features.ix[k + all_feat_ind_task_start, 'engagement_increase'] = np.nan
            else:
                all_features.ix[k + all_feat_ind_task_start, 'engagement_increase'] = True
        for k in range(all_feat_ind_task_end - all_feat_ind_task_start, -1, -1):
            all_features.ix[all_feat_ind_task_end - k, 'on_task_or_break_index_down'] = k
        all_features.ix[all_feat_ind_task_start:all_feat_ind_task_end, 'on_task'] = False

    all_features['person_id'] = cog_res['person_id'][0]
    all_features.to_csv(path_or_buf=path + ident + '/' + ident + '-data.csv', index=False)


def extract_for_all_users_and_combine(path, idents, outfile):
    for i in idents:
        print(i)
        # plot_whole_signal_and_tasks_times(path, i)
        full_signal_extract(path, i)
    # outfile = 'full-data_1.csv'  # uncomment if combining multiple files
    append_csv_files(path, idents, outfile)


def compare_extracted_hr_and_band(path, ident):
    """Compater heart rates acquired wirelessly and with Microfost Band.

    :param path: (str) main path to data, where user data is located in specific folders
    :param ident: (str) user identifier
    :return: MAE, MSE, CORRelation values of the aligned HR time series
    """

    dataread = datareader.DataReader(path, ident)  # initialize path to data
    data = dataread.read_grc_data()  # read from files
    data = dataread.unwrap_grc_data()  # unwrap phase. returns time and y values

    samp_rate = round(len(data[1]) / max(data[0]))

    dataextract = dataextractor.DataExtractor(data[0], data[1], samp_rate)

    cog_res = dataread.read_cognitive_load_study(ident + '-primary-extract.txt')
    end_epoch_time = dataread.get_end_time_cognitive_load_study()  # end t

    extracted_br_features = dataextract.raw_windowing_breathing(30, 1)
    extracted_br_features['br_rate'] = np.array(extracted_br_features['br_rate'].rolling(6).mean())
    extracted_br_features_roll_avg = extracted_br_features.loc[:, extracted_br_features.columns != 'times'].rolling(
        6).mean()
    extracted_br_features_roll_avg['times'] = extracted_br_features['times']
    extracted_br_features_roll_avg['br_ok'] = extracted_br_features['br_ok']

    extracted_hr_features = dataextract.raw_windowing_heartrate(10, 1)
    extracted_hr_features = extracted_hr_features.drop(['hr_HRV_lf', 'hr_HRV_hf', 'hr_HRV_lf_hf'], axis=1)
    extracted_hr_features_roll_avg = extracted_hr_features.loc[:, extracted_hr_features.columns != 'times'].rolling(
        10).mean()
    extracted_hr_features_roll_avg['times'] = extracted_hr_features['times']
    extracted_hr_features_roll_avg['hr_ok1'] = extracted_hr_features['hr_ok']

    bandread = bandreader.HeartRateBand(path + '_Hrates/', ident)
    band_data = bandread.load()
    band_data_time_start = bisect(band_data[0][:], end_epoch_time - data[0][-1] * 1000)
    band_data_time_stop = bisect(band_data[0][:], end_epoch_time)
    band_data = [band_data[0][band_data_time_start:band_data_time_stop],
                 band_data[1][band_data_time_start:band_data_time_stop]]
    band_data_new_data = [(band_data[0] - band_data[0][0]) / 1000, band_data[1]]

    plt.figure(1)
    plt.clf()
    plt.plot(extracted_hr_features_roll_avg['times'], extracted_hr_features_roll_avg['hr_rate'], color='orange',
             label='Wi-Mind heart rate')

    plt.plot(band_data_new_data[0], band_data_new_data[1], color='green', label='Microsoft Band heart rate')
    plt.xlabel('time (s)')
    plt.ylabel('heart rate')
    plt.legend()
    plt.show()

    hr_data = extracted_hr_features_roll_avg[['times', 'hr_rate']]
    hr_data['times'] = hr_data['times'].astype(int)
    band_data = pd.DataFrame()
    band_data['times'] = band_data_new_data[0]
    band_data['times'] = band_data['times'].astype(int)
    band_data['rate'] = band_data_new_data[1]
    band_data = band_data.drop_duplicates(subset=['times'])

    together_data = pd.merge(hr_data, band_data, on='times')
    together_data = together_data.dropna()

    # new_hr = res_ind[intersect]
    # new_band = band_data_new__data[1][intersect]
    mae = metrics.mean_absolute_error(together_data['rate'], together_data['hr_rate'])
    mse = metrics.mean_squared_error(together_data['rate'], together_data['hr_rate'])
    corr = stats.pearsonr(together_data['rate'], together_data['hr_rate'])
    # print('mae amd mse: ', mae, mse)

    return mae, mse, corr


def compare_hr_for_all_idents(path, idents):
    compare_metrics = pd.DataFrame()
    for i in idents:
        print(i)
        mae, mse, cor = compare_extracted_hr_and_band(path, i)  # uncomment if comparing errors
        df = pd.DataFrame([[i, mae, mse, cor[0]]], columns=['ID', 'MAE', 'MSE', 'COR'])
        compare_metrics = compare_metrics.append(df, ignore_index=True)
    print(compare_metrics)


# # # plotting functions


def boxplot_br_busy_relax(all_data):
    df2 = all_data.loc[all_data['on_task_or_break_index_down'] < 10]
    df2 = df2.loc[all_data['br_ok'] == True]
    df2 = df2[['person_id', 'on_task', 'br_rate']]
    # person_ids = np.unique(df2['person_id'])
    #
    grouped_task = df2.loc[df2['on_task'] == True].groupby(['person_id'])
    df2_sort = pd.DataFrame({col: vals['br_rate'] for col, vals in grouped_task})
    meds_task = df2_sort.median()
    #
    grouped_no_task = df2.loc[df2['on_task'] == False].groupby(['person_id'])
    df2_sort = pd.DataFrame({col: vals['br_rate'] for col, vals in grouped_no_task})
    meds_no_task = df2_sort.median()
    meds_no_task = meds_no_task.sort_values(ascending=True)
    #
    ax = sns.boxplot(x='on_task', y='br_rate', hue='person_id', data=df2, hue_order=meds_no_task.index, palette='Set2',
                     showfliers=False)
    plt.legend(title='person_id', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax.legend_.remove()
    plt.title('')
    plt.xlabel('on task', fontsize=12)
    plt.ylabel('breathing rate', fontsize=12)
    #
    plt.axhline(np.median(meds_task), xmin=0.5, xmax=1, color='red')
    plt.axhline(np.median(meds_no_task), xmin=0, xmax=0.5, color='blue')

    changes = {}
    for ind in meds_no_task.index.values:
        no_ind_val = meds_no_task.loc[ind]
        ind_val = meds_task.loc[ind]
        changes[ind] = ind_val - no_ind_val

    changes = pd.DataFrame.from_dict(changes, orient='index').sort_values(by=0)


def boxplot_br_task_complexities_users(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index_down'] < 10]
    df2 = df2.loc[all_data['br_ok'] == True]
    df2 = df2[['person_id', 'task_complexity', 'br_rate']]
    grouped_task = df2.groupby(['person_id'])
    df2_sort = pd.DataFrame({col: vals['br_rate'] for col, vals in grouped_task})
    meds = df2_sort.median()
    meds = meds.sort_values(ascending=True)
    ax = sns.boxplot(x='task_complexity', y='br_rate', hue='person_id', data=df2, order=['low', 'medium', 'high'], hue_order=meds.index, palette='Set2', showfliers=False)
    plt.legend(title='person_id', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.xlabel('task complexity', fontsize=12)
    plt.ylabel('breathing rate', fontsize=12)


def boxplot_hr_compare_extracted_vs_band(all_data):
    ###
    plt.subplot(121)
    df2 = all_data[['on_task', 'person_id', 'band_rate', 'on_task_or_break_index_down']]
    df2 = df2.loc[all_data['on_task_or_break_index_down'] < 15]
    person_ids = np.unique(df2['person_id'])
    grouped = df2.groupby(['person_id'])
    df2_sort = pd.DataFrame({col: vals['band_rate'] for col, vals in grouped})
    meds = df2_sort.median()
    meds = meds.sort_values(ascending=True)
    ax = sns.boxplot(x='person_id', y='band_rate', data=df2,
                     order=meds.index, palette='Set2', showfliers=False)
    # plt.legend(title='person_id', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.ylim(40, 120)
    ax.get_xaxis().set_ticklabels([])
    plt.xlabel('users', fontsize=12)
    plt.ylabel('band heart rate', fontsize=12)

    # plt.figure(2)
    plt.subplot(122)
    df2 = all_data[['on_task', 'person_id', 'hr_rate', 'on_task_or_break_index_down']]
    df2 = df2.loc[all_data['on_task_or_break_index_down'] < 15]
    person_ids = np.unique(df2['person_id'])
    ax = sns.boxplot(x='person_id', y='hr_rate', data=df2,
                     order=meds.index, palette='Set2', showfliers=False)
    # plt.legend(title='person_id', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.ylim(40, 120)
    ax.get_xaxis().set_ticklabels([])
    plt.xlabel('users', fontsize=12)
    plt.ylabel('wi-mind heart rate', fontsize=12)


def histogram_TLX(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2['task_load_index']
    df2.hist(grid=False, bins=25, facecolor='green', edgecolor='black', linewidth=1.2)
    plt.title('')
    plt.xlabel('task load index', fontsize=12)
    plt.ylabel('frequency', fontsize=12)


def barplot_mistakes_by_task(all_data):
    ###
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2[['task_label', 'num_incorrect']]
    ax = sns.barplot(x='task_label', y='num_incorrect', data=df2, palette='Set2', edgecolor='.2')
    plt.title('')
    plt.xlabel('task label', fontsize=12)
    plt.ylabel('number of incorrect answers', fontsize=12)


def boxplot_TLX_by_task_and_complexity(all_data):
    ###
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2[['task_label', 'task_complexity', 'task_load_index']]
    ax = sns.boxplot(x='task_label', y='task_load_index', hue='task_complexity', data=df2,
                     hue_order=['low', 'medium', 'high'], palette='Set2', showfliers=False)
    plt.legend(title='task complexity', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.xlabel('task label', fontsize=12)
    plt.ylabel('task load index', fontsize=12)


def boxplot_TLI_by_users(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2[['person_id', 'task_load_index']]
    grouped = df2.groupby(['person_id'])
    df2_sort = pd.DataFrame({col: vals['task_load_index'] for col, vals in grouped})
    meds = df2_sort.median()
    meds = meds.sort_values(ascending=True)
    ax = sns.boxplot(x='person_id', y='task_load_index', data=df2, palette='Set2', order=meds.index)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    # plt.legend(title='task complexity', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.xlabel('user id', fontsize=12)
    plt.ylabel('task load index', fontsize=12)


def barplot_timeontask_by_task_and_complexity(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2[['task_label', 'task_complexity', 'time_on_task']]
    df2['time_on_task'] = df2['time_on_task']/1000
    ax = sns.barplot(x='task_label', y='time_on_task', hue='task_complexity', data=df2, hue_order=['low', 'medium', 'high'], palette='Set2', edgecolor='.2')
    plt.legend(title='task complexity', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.xlabel('task label', fontsize=12)
    plt.ylabel('time on task (s)', fontsize=12)

# # #


def append_csv_files(path, idents, out_file_name_csv):
    """Goes through .csv files (all 'idents'), where all features are stored and combines them to one file."""
    full_appended_frame = pd.DataFrame()
    list_ = []
    for i in idents:
        df = pd.read_csv(path + i + '/' + i + '-data.csv')
        list_.append(df)
    full_appended_frame = pd.concat(list_)
    full_appended_frame.to_csv(path_or_buf=path + out_file_name_csv, index=False)


def plot_whole_signal_and_tasks_times(path, ident):
    """Plots signal, which was acquired wirelessly with GNU Radio, along with colored task timeframes."""
    dataread = datareader.DataReader(path, ident)  # initialize path to data
    data = dataread.read_grc_data()  # read from files
    data = dataread.unwrap_grc_data()  # unwrap phase. returns time and y values

    task_timestamps = dataread.get_data_task_timestamps()
    relax_timestamps = dataread.get_relax_timestamps()

    plt.figure(2)
    plt.clf()
    plt.plot(data[0], data[1])
    plt.xlabel('time (s)', fontsize=12)
    plt.ylabel('distance', fontsize=12)

    loc = plticker.MultipleLocator(base=50.0)
    for (start, stop) in task_timestamps:
        plt.axvspan(start, stop, alpha=0.4, color='r')

    for (start, stop) in relax_timestamps:
        plt.axvspan(start, stop, alpha=0.4, color='b')

    tasks = ['HP\nhigh', 'HP\nlow', 'HP\nmedium',
             'FA\nhigh', 'FA\nmedium', 'FA\nlow',
             'GC\nmedium', 'GC\nhigh', 'GC\nlow',
             'NC\nlow', 'NC\nhigh', 'NC\nmedium',
             'SX\nlow', 'SX\nmedium', 'SX\nhigh',
             'PT\nmedium', 'PT\nlow', 'PT\nhigh']

    task_i = 0
    for (start, stop) in task_timestamps:
        plt.text((start + stop) / 2, 0, tasks[task_i], horizontalalignment='center', fontsize=12, clip_on=True)
        task_i += 1

    plt.show()


def update_extraction_files(path, ident):
    dataread = datareader.DataReader(path, ident)  # initialize path to data
    dataread.extract_cognitive_load_study(save_path=path + '/' + str(ident) + '/' + str(ident) + '-primary-extract.txt')

    dataread.read_grc_data()
    dataread.fix_grc_data_and_save()


def normalize_breathing_rate(all_data, path, out_file):
    """'Normalize' breathing rates, so all breathing rates (from all users) are approximately the same."""
    # first_break_data = all_data.loc[all_data['consecutive_break'] == 0]
    first_break_data = all_data.loc[all_data['on_task'] == False]
    first_break_br = first_break_data[['br_rate', 'person_id']]
    user_ids = np.unique(first_break_br['person_id'])

    grouped = first_break_br.groupby(['person_id'])
    grouped_sort = pd.DataFrame({col: vals['br_rate'] for col, vals in grouped})
    meds = grouped_sort.median()
    min_med_val = min(meds)
    # min_med_val = min(np.min(grouped_sort))
    # min_med_val = 0

    diffs = meds - min_med_val

    meds_new_vals = meds - diffs

    new_all_data = all_data
    for user_id in user_ids:
        # (diffs.get(user_id))
        user_data = new_all_data[new_all_data['person_id'] == user_id]
        user_data['br_rate'] -= diffs.get(user_id)
        new_all_data[new_all_data['person_id'] == user_id] = user_data

    new_all_data.to_csv(path_or_buf=path + out_file, index=False)


def __main__():
    path = 'E:/signal_acquiring/'
    path_hrates = path + '_Hrates/'

    idents = ['2gu87', 'iz2ps', '1mpau', '7dwjy', '7swyk', '94mnx', 'bd47a', 'c24ur', 'ctsax', 'dkhty', 'e4gay',
              'ef5rq', 'f1gjp', 'hpbxa', 'pmyfl', 'r89k1', 'tn4vl', 'td5pr', 'gyqu9', 'fzchw', 'l53hg', '3n2f9',
              '62i9y']

    outfile = 'full_data_1.csv'
    extract_for_all_users_and_combine(path, idents, outfile)
    # compare_hr_for_all_idents(path, idents)
    # normalize_breathing_rate(pd.read_csv(path+outfile), path, 'full-data_1_norm.csv')


__main__()
