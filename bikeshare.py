import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    /Asks user to specify a city, month, and day to analyze/.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to analyze? (Chicago, New York City, Washington)\n").lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            print("\nPlease enter a correct city")

    # TO DO: get user input for month (all,   ... , june)
    while True:
        months = ['January', 'February', 'March', 'April', 'June', 'May', 'None']
        month = input("\nWhich month would you like to consider? (January, February, March, April, May, June)? Type 'None' for no month filter\n").title()
        if month == 'None' or month in months[:-1]:
            break
        else:
            print("\nPlease enter a valid month")    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'None']
        day = input("\nWhich day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Choose 'None' if it is none of the days mentioned\n").title()
        if day in days:
            break
        else:
            print("\nPlease enter a valid day")

    print('-' * 40)
    return city, month
def load_data(city):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
     # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'None':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May']
        try:
            month = months.index(month) + 1
        except ValueError:
            print("\nPlease enter a valid month")

        # filter by month to create the new dataframe
        df = df.query('month == @month')

    # filter by day of week if applicable
    if day != 'None':
        # filter by day of week to create the new dataframe
        df = df.query('day_of_week == @day')

    return df
def time_stats(df, month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'None':
        com_month = df['month'].value_counts().idxmax()
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        com_month = months[com_month - 1]
        print("The most common month is", com_month)

    # TO DO: display the most common day of week
    if day == 'None':
        com_day = df['day_of_week'].value_counts().idxmax()
        print("The most common day is", com_day)

    # TO DO: display the most common start hour
    com_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print("The most popular start hour is {}:00 hrs".format(com_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    com_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used Start Station is", com_start_station)

    # TO DO: display most commonly used end station
    com_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used End Station is", com_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    com_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of Start Station and End Station trip is:", com_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = pd.to_timedelta(df['Trip Duration'], unit='s').sum()
    days = total_duration.days
    hours, remainder = divmod(total_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("The total trip duration: {} day(s) {} hour(s) {} minute(s) {} second(s)".format(days, hours, minutes, seconds))

    # TO DO: display mean travel time
    mean_duration = pd.to_timedelta(df['Trip Duration'], unit='s').mean()
    mean_minutes = mean_duration.total_seconds() / 60
    print("The average trip duration: {:.2f} minutes".format(mean_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].unique()

    print("The user types are:")
    for user_type in user_types:
        count = (df['User Type'] == user_type).sum()
        print(f"{user_type}: {count}")

    # TO DO: Display counts of gender
    if 'Gender' in df:
        genders = df['Gender'].unique()
        print("\nThe gender distribution is:")
        for gender in genders:
            count = (df['Gender'] == gender).sum()
            print(f"{gender}: {count}")
    else:
        print("\nGender information is not available for this dataset.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nBirth Year Statistics:")
        print(f"Earliest Birth Year: {earliest_birth_year}")
        print(f"Most Recent Birth Year: {most_recent_birth_year}")
        print(f"Most Common Birth Year: {most_common_birth_year}")
    else:
        print("\nBirth year information is not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)  # Call the display_data function here
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
