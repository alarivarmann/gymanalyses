import pandas as pd
import pytest
import pytz
from datetime import datetime
import os

@pytest.fixture
def df():
    # Load DataFrame from CSV file
    full_path = os.path.join("data","hietaniemi-gym-data.csv")
    print(full_path)
    df = pd.read_csv(full_path)
    #tz = pytz.UTC
    df['time'] = pd.to_datetime(df['time'])
    return df


def test_check_number_of_rows(df):
    # Check number of rows
    assert len(df) > 50000, "Number of rows is not greater than 50,000"



def test_check_time_range_with_index(df):

    # Define the start and end datetimes with timezone information
    start_datetime = pytz.datetime.datetime(2020, 4, 24, tzinfo=pytz.UTC)
    end_datetime = pytz.datetime.datetime(2021, 5, 12, tzinfo=pytz.UTC)

    # Check if 'time' values fall within the specified time range
    assert (df['time'] >= start_datetime).all() and (df['time'] <= end_datetime).all(), \
        "Values in the 'time' column are not within the specified time range (2020-04-24 to 2021-05-11)"


def test_check_time_range_with_index_2(df):
    start_date = '2020-04-24'
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = '2021-05-11'
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    df['time'] = pd.to_datetime(df['time'])
    # check whether all dates in the DataFrame fall within the specified date range
    df['date'] = df['time'].apply(lambda x: x.date())
    records_in_range = df.date.between(start_date, end_date).all()
    assert records_in_range


def test_check_numerical_values_positive(df):
    # Set 'time' column as index
    df.set_index('time', inplace=True)
    # Check if all values in remaining columns are positive
    assert (df > 0).all().all(), "There are non-positive values in the DataFrame"
