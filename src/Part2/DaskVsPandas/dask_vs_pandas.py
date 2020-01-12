import os
import psutil
from hurry.filesize import size
import pandas as pd
import dask.dataframe as dd
import time


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def show_results(start_time, memory_before, task_name):
    elapsed_time = elapsed_since(start_time)
    memory_after = get_process_memory()
    print(task_name, ": memory before: {}, after: {}, consumed: {}; exec time: {}".format(
        size(memory_before), size(memory_after), size(memory_after - memory_before), elapsed_time))


def test_pandas_load():
    memory_before = get_process_memory()
    start_time = time.time()
    df1 = pd.read_csv('../../../DataSet/Hotel_Reviews.csv')
    pd_list = [df1, df1, df1, df1, df1]  # Concat 5 dfs
    df = pd.concat(pd_list)
    show_results(start_time, memory_before, 'Pandas Load')

    return df


def test_dask_load():
    memory_before = get_process_memory()
    start_time = time.time()
    ddf1 = dd.read_csv('../../../DataSet/Hotel_Reviews.csv')
    ddf_list = [ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1, ddf1]  # Concat 10 ddfs
    ddf = dd.concat(ddf_list, axis=0, interleave_partitions=True)
    show_results(start_time, memory_before, 'Dask Load')

    return ddf


def filter_dfs(df, ddf):
    memory_before = get_process_memory()
    start_time = time.time()
    df_filter = df[df['Total_Number_of_Reviews'] > 2000]
    show_results(start_time, memory_before, 'Pandas Filter')

    memory_after_pandas = get_process_memory()
    start_time = time.time()
    ddf_filter = ddf[ddf['Total_Number_of_Reviews'] > 2000]
    show_results(start_time, memory_after_pandas, 'Dask Filter')

    # garbage collection
    del df_filter
    del ddf_filter


def get_sums(df, ddf):
    # df, ddf = drop_duplicates(df, ddf)
    memory_before = get_process_memory()
    start_time = time.time()
    df_sum = df['Total_Number_of_Reviews'].sum()
    show_results(start_time, memory_before, 'Pandas Sum (' + str(df_sum) + ')')

    memory_after_pandas = get_process_memory()
    start_time = time.time()
    ddf_sum = ddf['Total_Number_of_Reviews'].sum()
    show_results(start_time, memory_after_pandas, 'Dask Sum (' + str(ddf_sum) + ')')


def drop_duplicates(df, ddf):
    memory_before = get_process_memory()
    start_time = time.time()
    df_dropped = df.drop_duplicates(subset='Hotel_Name')
    show_results(start_time, memory_before, 'Pandas Drop Duplicates')

    memory_after_pandas = get_process_memory()
    start_time = time.time()
    ddf_dropped = ddf.drop_duplicates(subset='Hotel_Name')
    show_results(start_time, memory_after_pandas, 'Dask Drop Duplicates')

    del df_dropped
    del ddf_dropped
    # return [df_dropped, ddf_dropped]


def test_performance():
    df = test_pandas_load()
    ddf = test_dask_load()

    filter_dfs(df, ddf)
    drop_duplicates(df, ddf)
    # get_sums(df, ddf)


def save_csv():
    memory_before = get_process_memory()
    start_time = time.time()
    ddf = pd.read_csv('../../../DataSet/Hotel_Reviews.csv')
    ddf_pos = ddf.filter(['Positive_Review'])
    ddf_neg = ddf.filter(['Negative_Review'])
    ddf_pos.to_csv('./csv/Review_pos.csv')
    ddf_neg.to_csv('./csv/Review_neg.csv')
    show_results(start_time, memory_before, 'Dask Read, Drop and save to CSV')


test_performance()
save_csv()