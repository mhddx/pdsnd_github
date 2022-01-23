import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all' ]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    print("\nChoose a city: New York City, Chicago or Washington?")
    while True:
       city = input('Enter city: ').lower()
       if city in CITIES:
           break


    # get user input for month.
    print("\nChoose a Month: January, February, March, April, May, June or  all")
    while True:
        month = input('Enter a month: ').lower()
        if month in MONTHS:
            break

    # get user input for day of week.
    print("\nChoose any day of the following days like: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all")
    while True:
        day = input('Please enter the day: ').lower()
        if day in DAYS:
            break
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load selected file from the user into data frame
    df = pd.read_csv('{}.csv'.format(city))

    #convert Start Time and End Time columns to date
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day
    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculator the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month is: ", df['month'].value_counts().idxmax())

    # display the most common day of week
    print("Most common day is: ", df['day_of_week'].value_counts().idxmax())

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("Most common hour is: ", df['hour'].value_counts().idxmax())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculator the most popular station and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station is: ", df ['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("Most common end station is: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("Most frequent combination of start station and end station trip are {}, {}".format(most_common_start_end_station[0],most_common_start_end_station[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculator trip duration...\n')
    start_time = time.time()

    # display total travel time in hours
    total_duration = df['Trip Duration'].sum() / 3600
    print("Total travel time {} hours".format(int(total_duration)))

    # display mean travel time in minutes
    mean_duration = df['Trip Duration'].mean() / 60
    print("Mean travel time {} minutes".format(int(mean_duration)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculator user stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())

    # Display counts of gender
    try:
        print("\nCounts of gender:")
        user_gender = df['Gender'].value_counts()
        print(user_gender.to_string())
    except KeyError: print("US Bikeshare does not provide information on genders in 'Washington'.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].value_counts().idxmax())

        print("\nEarliest year of birth is: {} \n"
          "Most recent year of birth is: {} \n"
          "Most common year of birth is: {}".format(earliest_yob,most_recent_yob,most_common_yob))
    except KeyError: print("US Bikeshare does not provide information on years of birth in 'Washington'.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data (df):
    """Displays the 5 rows will added in each time"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter ( Yes or No ).\n')
    start_loc = 5
    while (view_data != 'no'):
        print(df.head(start_loc))
        start_loc += 5
        view_data = input("Do you want to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter ( Yes or No ).\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()