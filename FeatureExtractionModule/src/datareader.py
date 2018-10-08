import scipy
import re
import os
from datetime import datetime
import numpy as np
import pandas as pd
from _bisect import bisect
from itertools import groupby


class DataReader:
    """Provides functions to read raw data acquired during the cognitive load study
    i.e. tasks information and wireless data)."""

    def __init__(self, path, ident):
        """
        :param path: (str) Path to a files
        :param ident: (str) User identifier
        """
        self.path = path
        self.ident = ident
        self.phase = None
        self.time = None
        self.extracted_cog_res = None

    def read_grc_data(self):
        """Loads data from given path (self.path) and identifier (self.ident)

        :returns: Array of [time and phase] values.
        """
        self.phase = scipy.fromfile(open(self.path+'/'+self.ident+'/'+self.ident+'-phase-new.dat'), dtype=scipy.float32)
        self.time = scipy.fromfile(open(self.path+'/'+self.ident+'/'+self.ident+'-time-new.dat'), dtype=scipy.float32)

        # fixes different lenghts of data phase and time, this does not significantly "destroy" data
        if len(self.phase) < len(self.time):
            self.time = self.time[:len(self.phase)]
        elif len(self.phase) > len(self.time):
            self.phase = self.phase[:len(self.time)]

        return [self.time, self.phase]

    def fix_grc_data_and_save(self):
        """Fix repetitive / "duplicate" values from the signal and save to files.
        This fixes data, acquired directly with GNU Radio. (can be done in GNU Radio, if possible)"""
        ph = [x[0] for x in groupby(self.phase)]
        ti = [x[0] for x in groupby(self.time)]
        np.array(ph).tofile(self.path+'/'+self.ident+'/'+self.ident+'-phase-new.dat')
        np.array(ti).tofile(self.path+'/'+self.ident+'/'+self.ident+'-time-new.dat')

    def unwrap_grc_data(self):
        """
        :returns: Array of [time and unwrapped phase] values.
        """
        return [self.time, np.unwrap(self.phase)]

    def extract_cognitive_load_study(self, save_path=None):
        """Reads relevant data from study files (task information) and saves to file.

        :param save_path: (str) Path to output file

        :returns: Output data (same as output file data)
        """

        global client_id
        reset_global()

        directory = self.path+self.ident+'/'
        mSF = re.compile(r"(\w+)-primary.txt")

        if save_path:
            try:
                os.remove(save_path)
            except OSError:
                pass

        for filename in os.listdir(directory):
            if mSF.search(filename):
                reset_user()
                reset_task()
                client_id = mSF.search(filename).group(1)
                f = open(os.path.join(directory, filename), "r", encoding="utf8")
                for line in f:
                    # print line
                    parse(line, save_path)
                continue
            else:
                continue

        results = []
        for filename in os.listdir(directory):
            if mSF.search(filename):
                f = open(os.path.join(save_path), "r", encoding="utf8")
                for line in f:
                    # print line
                    results.append([x.strip() if not x.isdigit() else int(x.strip()) for x in line.split(' ')])
                continue
            else:
                continue

        # also save to object var
        self.extracted_cog_res = results
        return results

    def read_cognitive_load_study(self, file):
        """Use if you already have the extracted file. This reads data from the extracted file.

        :param file: (str) Name of the file, that contains extracted data from the study (tasks information).
        :returns: Dataframe of extracted file.
        """
        filepath = self.path+self.ident+'/'+file
        readfile = pd.read_csv(filepath, sep=" ", header=None)
        readfile.columns = ['task_number', 'person_id', 'task_label',
                                                               'task_complexity', 'start_time', 'time_on_task',
                                                               'num_correct', 'num_incorrect', 'num_all_correct',
                                                               'task_load_index', 'finished']
        return readfile

    def get_data_task_timestamps(self, return_indexes=False):
        """Returns times of each task time frame start-end.

        :param return_indexes: True - return index in array; False - return actual time in array.
        :return: Array of tuples, where each tuple presents beginning and end of a task time frame.
        """
        data = [self.time, self.phase]
        end_time = self.get_end_time_cognitive_load_study()
        cognitive_study_results = self.read_cognitive_load_study(self.ident+'-primary-extract.txt')

        timestamps = []
        for i in range(len(cognitive_study_results)):
            task_1_start = cognitive_study_results['start_time'][i]
            task_1_length = cognitive_study_results['time_on_task'][i]

            difference = (end_time - task_1_start) / 1000

            start_on_data = data[0][-1] - difference
            end_on_data = start_on_data + task_1_length / 1000

            if return_indexes:
                start_on_data = bisect(data[0], start_on_data)
                end_on_data = bisect(data[0], end_on_data)

            timestamps.append((start_on_data, end_on_data))

        return timestamps

    def get_relax_timestamps(self, return_indexes=False):
        """Returns times of each relax time frame start-end.

        :param return_indexes: True - return index in array; False - return actual time in array.
        :return: Array of tuples, where each tuple presents beginning and end of a relax time frame.
        """
        dataread = self
        end_time = self.get_end_time_cognitive_load_study()
        relax_timestamps = dataread.get_relax_timestamps_from_file()
        data = [self.time, self.phase]

        timestamps = []
        for i in range(0, len(relax_timestamps) - 1, 2):
            relax_start = relax_timestamps[i]
            relax_stop = relax_timestamps[i + 1]

            difference1 = (end_time - relax_start) / 1000
            difference2 = (end_time - relax_stop) / 1000

            start_on_data = data[0][-1] - difference1
            stop_on_data = data[0][-1] - difference2

            if return_indexes:
                start_on_data = bisect(data[0], start_on_data)
                stop_on_data = bisect(data[0], stop_on_data)

            timestamps.append((start_on_data, stop_on_data))

        return timestamps

    def get_end_time_cognitive_load_study(self):
        """Returns the end time of the study (used to synchronize the data from GNU Radio).

        :return: Unix epoch time.
        """

        global client_id
        reset_global()

        directory = self.path+self.ident+'/'
        mSF = re.compile(r"(\w+)-primary.txt")

        for filename in os.listdir(directory):
            if mSF.search(filename):
                reset_user()
                reset_task()
                f = open(os.path.join(directory, filename), "r", encoding="utf8")
                linelist = f.readlines()
                f.close()
                return convert_to_epoch([x.strip() for x in linelist[-1].split(',')][0])
                continue
            else:
                continue
        return 0

    def get_relax_timestamps_from_file(self):
        """Read relax timestamps from file.

        :return: Array of times, where each value presents either beginning (i) or end (i+1) of a relax time frame.
        """

        global client_id
        reset_global()

        directory = self.path+self.ident+'/'
        mSF = re.compile(r"(\w+)-primary.txt")

        times = []
        for filename in os.listdir(directory):
            if mSF.search(filename):
                reset_user()
                reset_task()
                client_id = mSF.search(filename).group(1)
                f = open(os.path.join(directory, filename), "r", encoding="utf8")
                for line in f:
                    # print line
                    time = parse_relax_times(line)
                    if time!=None:
                        times.append(time)
                continue
            else:
                continue

        # also save to object var
        # self.extracted_cog_res = results
        return times


"""Code below is used to extract relevant data from the study."""

# Reset the whole process - taskIds start from zero
def reset_global():
    global SEED_TASK_ID
    global SEED_SEC_TASK_ID
    SEED_TASK_ID = 224
    SEED_SEC_TASK_ID = 1730


def reset_user():
    global client_id
    client_id = ""


# For each new Task - reset all task-related params
def reset_task():
    global start_time
    global end_time
    global state_prim
    global state_sec
    global task_type
    global label
    global finished
    global num_all_correct
    global num_correct
    global num_incorrect
    global curr_task_id
    global curr_sec_task_id
    global task_load_index

    start_time = 0
    end_time = 0
    num_correct = 0
    num_incorrect = 0
    num_all_correct = 0
    label = ""
    task_type = ""
    task_load_index = 0
    finished = True
    state_prim = 0
    state_sec = 0
    curr_task_id = -1
    curr_sec_task_id = -1


# This function is called when a primary task end is detected
def process_end(file_path):
    global state_prim
    global start_time
    global end_time
    global task_type
    global label
    global finished
    global num_all_correct
    global num_correct
    global num_incorrect
    global curr_task_id
    global client_id
    global task_load_index
    global cursor

    time_on_task = end_time - start_time

    if task_type == 'HP':
        num_all_correct = 21
    if task_type == 'FA':
        # We know that there are 2 groups, 5 A-words in evey group
        num_all_correct = 10
    if task_type == 'GC':
        num_all_correct = 5
    if task_type == 'NC':
        if label == "low":
            num_all_correct = 11
        elif label == "medium":
            num_all_correct = 14
        elif label == "high":
            num_all_correct = 4
    if task_type == 'SX':
        num_all_correct = 20
    if task_type == 'PT':
        num_all_correct = 10

    if curr_task_id > -1:
        if not file_path:
            print(curr_task_id, client_id, task_type, label, start_time, time_on_task, num_correct, num_incorrect,
                  num_all_correct, task_load_index, finished)
        else:
            with open(file_path, 'a') as save_file:
                save_file.write(str(curr_task_id)+' '+str(client_id)+' '+str(task_type)+' '+str(label)+' '+str(start_time)+' '+str(time_on_task)+' '+str(num_correct)+' '+str(num_incorrect)+' '+
                                                                                                                                                    str(num_all_correct)+' '+str(task_load_index)+' '+str(finished)+'\n')


def convert_to_epoch(value):
    datetime_object = datetime.strptime(value, '%Y:%m:%d:%H:%M:%S:%f')
    return int(datetime_object.timestamp()) * 1000 + int(datetime_object.microsecond / 1000)


def generate_task_ID():
    global SEED_TASK_ID
    SEED_TASK_ID += 1
    return SEED_TASK_ID


# Result checker for PT task
def PT_checker(num1, num2, task_type):
    low_map = {
        "1": "3",
        "2": "4",
        "3": "1",
        "4": "2",
        "5": "6",
        "6": "5",
        "7": "9",
        "8": "10",
        "9": "7",
        "10": "8",
    }

    medium_map = {
        "1": "5",
        "2": "6",
        "3": "2",
        "4": "8",
        "5": "10",
        "6": "1",
        "7": "3",
        "8": "9",
        "9": "4",
        "10": "6",
    }

    high_map = {
        "1": "9",
        "2": "8",
        "3": "10",
        "4": "7",
        "5": "6",
        "6": "5",
        "7": "4",
        "8": "3",
        "9": "1",
        "10": "2",
    }

    if task_type == "low":
        return num2 == low_map.get(num1)
    elif task_type == "medium":
        return num2 == medium_map.get(num1)
    elif task_type == "high":
        return num2 == high_map.get(num1)


# TLX string value to int mapping
def TLX(value, measure_type):
    M_map = {
        "Zelo nizko": 1,
        "Nizko": 2,
        "Srednje": 3,
        "Visoko": 4,
        "Zelo visoko": 5,
    }

    P_map = {
        "Zelo dobro": 1,
        "Dobro": 2,
        "Srednje": 3,
        "Slabo": 4,
        "Zelo slabo": 5,
    }

    E_map = {
        "Zelo malo": 1,
        "Malo": 2,
        "Srednje": 3,
        "Veliko": 4,
        "Zelo veliko": 5,
    }

    if measure_type == "Physical" or measure_type == "Mental" or measure_type == "Temporal" or measure_type == "Frustration":
        return M_map.get(value)
    if measure_type == "Performance":
        return P_map.get(value)
    if measure_type == "Effort":
        return E_map.get(value)


# Each line of text in the file should be processed, so that primary and secondary tasks are identified
def parse(line, file_path):
    global curr_task_id
    global curr_sec_task_id
    global num_correct
    global num_incorrect
    global label
    global finished
    global task_load_index
    global start_time
    global start_time_sec
    global end_time
    global state_prim
    global state_sec
    global task_type
    global cursor

    mHP = re.compile(r"(\S+), Hidden Pattern Question Slide, HiddenPattern(\d).txt, (\w+),")
    mHPres = mHP.search(line)
    if mHPres and state_prim == 0:
        task_type = 'HP'
        label = mHPres.group(3).lower()
        start_time = convert_to_epoch(mHPres.group(1))
        state_prim = 1
        curr_task_id = generate_task_ID()
        # print(start_time, task_type, label, curr_task_id)

    mFA = re.compile(r"(\S+), Finding A's Question Slide, FindingAs_(\d).txt, (\w+)")
    mFAres = mFA.search(line)
    if mFAres and state_prim == 0:
        task_type = 'FA'
        label = mFAres.group(3).lower()
        start_time = convert_to_epoch(mFAres.group(1))
        state_prim = 1
        curr_task_id = generate_task_ID()
        # print(start_time, task_type, label, curr_task_id)

    mGC = re.compile(r"(\S+), Gestalt Completion Question Slide, GestaltCompletion(\d).txt, (\w+)")
    mGCres = mGC.search(line)
    if mGCres and state_prim == 0:
        task_type = 'GC'
        label = mGCres.group(3).lower()
        start_time = convert_to_epoch(mGCres.group(1))
        state_prim = 1
        curr_task_id = generate_task_ID()
        # print(start_time, task_type, label, curr_task_id)

    mNC = re.compile(r"(\S+), Number Comparison Question Slide, NumberComparison_(\d).txt, (\w+)")
    mNCres = mNC.search(line)
    if mNCres and state_prim == 0:
        task_type = 'NC'
        label = mNCres.group(3).lower()
        start_time = convert_to_epoch(mNCres.group(1))
        state_prim = 1
        curr_task_id = generate_task_ID()
        # print(start_time, task_type, label, curr_task_id)

    mSX = re.compile(r"(\S+), Scattered X's Question Slide, ScatteredXs_(\d).txt, (\w+)")
    mSXres = mSX.search(line)
    if mSXres and state_prim == 0:
        task_type = 'SX'
        label = mSXres.group(3).lower()
        start_time = convert_to_epoch(mSXres.group(1))
        state_prim = 1
        curr_task_id = generate_task_ID()
        # print(start_time, task_type, label, curr_task_id)

    mPT = re.compile(r"(\S+), Pursuit Test Question Slide, Pursuit_(\d).txt, (\w+)")
    mPTres = mPT.search(line)
    if mPTres and state_prim == 0:
        task_type = 'PT'
        label = mPTres.group(3).lower()
        start_time = convert_to_epoch(mPTres.group(1))
        state_prim = 1
        curr_task_id = generate_task_ID()
        # print(start_time, task_type, label, curr_task_id)

    mHProw = re.compile(r"'image/HiddenPatterns/(\S+)_(\w+).jpg' selected")
    mHProwres = mHProw.search(line)
    if mHProwres:
        result = mHProwres.group(2)
        if result == "true":
            num_correct += 1
        elif result == "false":
            num_incorrect += 1

    mFArow = re.compile(r" '([a-zA-Z]+)' selected")
    mFArowres = mFArow.search(line)
    if mFArowres:
        result = mFArowres.group(1).lower()
        if 'a' in result:
            num_correct += 1
        else:
            num_incorrect += 1

    mNCrow = re.compile(r" '([0-9]+)-([0-9]+)' selected")
    mNCrowres = mNCrow.search(line)
    if mNCrowres:
        num1 = mNCrowres.group(1)
        num2 = mNCrowres.group(2)
        if num1 != num2:
            num_correct += 1
        else:
            num_incorrect += 1

    mSXrow = re.compile(" \(\d+,\d+\), \(\d+,\d+\)")
    mSXrowres = mSXrow.search(line)
    if mSXrowres:
        num_correct += 1

    mPTrow = re.compile(", (\d+), '(\d+)'")
    mPTrowres = mPTrow.search(line)
    if mPTrowres:
        num1 = mPTrowres.group(1)
        num2 = mPTrowres.group(2)
        if PT_checker(num1, num2, label):
            num_correct += 1
        else:
            num_incorrect += 1

    mTIU = re.compile(r"TimeIsUp Slide")
    mTIUres = mTIU.search(line)
    if mTIUres:
        finished = False

    mR = re.compile(r"(\S+), Rating Slide")
    mRres = mR.search(line)
    if mRres:
        end_time = convert_to_epoch(mRres.group(1))

    mRM = re.compile(r"(Mental|Physical|Temporal|Performance|Effort|Frustration), ([\s\w]+)")
    mRMres = mRM.search(line)
    if mRMres:
        task_load_index += TLX(mRMres.group(2).rstrip(), mRMres.group(1).rstrip())

    mB = re.compile(r"(Break|End) Slide")
    mBres = mB.search(line)
    if mBres and state_prim == 1:
        process_end(file_path)
        reset_task()


def parse_relax_times(line):
    mB = re.compile(r"(\S+), (Break|End) Slide")
    mBres = mB.search(line)
    if mBres:
        start_time = convert_to_epoch(mBres.group(1))
        return start_time

    mR = re.compile(r"(\S+), Test Continues Slide")
    mRres = mR.search(line)
    if mRres:
        end_time = convert_to_epoch(mRres.group(1))
        return end_time
