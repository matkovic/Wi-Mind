import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
    plt.show()


def boxplot_br_task_complexities_users(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index_down'] < 10]
    df2 = df2.loc[all_data['br_ok'] == True]
    df2 = df2[['person_id', 'task_complexity', 'br_rate']]
    grouped_task = df2.groupby(['person_id'])
    df2_sort = pd.DataFrame({col: vals['br_rate'] for col, vals in grouped_task})
    meds = df2_sort.median()
    meds = meds.sort_values(ascending=True)
    ax = sns.boxplot(x='task_complexity', y='br_rate', hue='person_id', data=df2, order=['low', 'medium', 'high'],
                     hue_order=meds.index, palette='Set2', showfliers=False)
    plt.legend(title='person_id', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.xlabel('task complexity', fontsize=12)
    plt.ylabel('breathing rate', fontsize=12)
    plt.show()


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
    plt.show()


def histogram_TLX(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2['task_load_index']
    df2.hist(grid=False, bins=25, facecolor='green', edgecolor='black', linewidth=1.2)
    plt.title('')
    plt.xlabel('task load index', fontsize=12)
    plt.ylabel('frequency', fontsize=12)
    plt.show()


def barplot_mistakes_by_task(all_data):
    ###
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2[['task_label', 'num_incorrect']]
    ax = sns.barplot(x='task_label', y='num_incorrect', data=df2, palette='Set2', edgecolor='.2')
    plt.title('')
    plt.xlabel('task label', fontsize=12)
    plt.ylabel('number of incorrect answers', fontsize=12)
    plt.show()


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
    plt.show()


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
    plt.show()


def barplot_timeontask_by_task_and_complexity(all_data):
    df2 = all_data.loc[all_data['on_task'] == True]
    df2 = df2.loc[all_data['on_task_or_break_index'] == 1]
    df2 = df2[['task_label', 'task_complexity', 'time_on_task']]
    df2['time_on_task'] = df2['time_on_task'] / 1000
    ax = sns.barplot(x='task_label', y='time_on_task', hue='task_complexity', data=df2,
                     hue_order=['low', 'medium', 'high'], palette='Set2', edgecolor='.2')
    plt.legend(title='task complexity', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('')
    plt.xlabel('task label', fontsize=12)
    plt.ylabel('time on task (s)', fontsize=12)
    plt.show()
