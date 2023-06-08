import time
import pandas as pd
import numpy as np
import calendar

# Dictionary to store city names as keys and the csv files as values
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Get specific input for particular cities 
    while(True):
        city = input("Which bikeshare's system would you like to analyze? Washington, New York City or Chicago\n").lower()

        print()
        
        # if the city entered by the user is in the dictionary
        if city in CITY_DATA.keys():
            print(f"Great you selected {city.title()}. To change the city please restart the program.")
            break
        else:
            print("You selected an incorrect city. Please select from the given list.")

    # get user input for month (all, january, february, ... , june)
    while True:
        filter = input("How would you like to filer the data?\nFor daily type 'day', for monthly type 'month', and to apply no filters type 'none'. \n").lower()
        # none in filters means that the user wants stats of the whole dataset
        filters = ["month", "day", "none"]
        if filter in filters:
            if filter == "month":
                month = input(f"""Select a month ---- {[i for i in months]}?
                            Type 'all' to apply no filter\n""").lower()
                """
                if the user selects the month as filters and that month is in the months list then we will assign
                "all" value to the day implying that all days of that month
                """
                if month in months:
                    day = "all"
                    break
                elif month == "all":
                    day = "all"
                    month = "all"
                    break
                else:
                    print("\nThe month name you typed doesn't match the available months list. Let's restart the process.")
        # get user input for day of week (all, monday, tuesday, ... sunday)
            elif filter == "day":
                day = input(f"""Select a day - {[i for i in days]}?
                        Type 'all' to apply no filter\n""").lower()
                if day in days:
                    month = "all"
                    break
                elif day == "all":
                    day = "all"
                    month = "all"
                    break
                else:
                    print()
                    print("Please input day full name correctly! Let's start over.")
            elif filter == "none":
                print("You have selected 'none'. \n")
                day = "all"
                month = "all"
                break
        elif filter not in filters:
            print("Select from the given filters!")

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

    # reading the dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converting start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # after converting start time to datetime extracting month and day of the week from it and creating two new columns # in the dataframe
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filtering the dataframe on the basis of month first.
    if month != 'all':
        
        # use the index of the months list to get the corresponding int
        print(f"\n You have selected the month {month.title()}")
        # index() returns the index of the particular entry from the list
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "all" and day != "all":
        """
        value_counts() function return the count of all the unique values and idxmax() chooses
        the maximum of them all
        """
        common_month = df['month'].value_counts().idxmax()
        print(f'Most Common Month: {calendar.month_name[common_month]}')

    # display the most common day of week
    elif month != "all" and day == "all":
        common_day = df['day_of_week'].value_counts().idxmax()
        print(f"Most common day of week: {common_day}")

    elif (month != "all" and day != "all") or (month == "all" and day == "all"):
        common_month = df['month'].value_counts().idxmax()
        common_day = df['day_of_week'].value_counts().idxmax()
        print(f'Most Common Month: {calendar.month_name[common_month]}')
        print(f"Most common day of week: {common_day}\n")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    """
    mode() return that value from the column which occurs the most
    """
    common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {common_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print(f"Most common start station: {common_start_station} \n")

    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print(f"Most common end station: {common_end_station} \n")

    # display most frequent combination of start station and end station trip
    df['Freq Start End'] = df['Start Station'] + " => " + df['End Station']
    freq_start_end = df['Freq Start End'].mode()[0]
    print(f"Most frequent combination of start station and end station trip: {freq_start_end} \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # displaying total travel time in hours to increase readability
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} hours \n")

    # display mean travel time
    # displaying mean travel time in minutes
    mean_travel = df['Trip Duration'].mean()
    mean_travel = mean_travel/60
    print(f"Average Travel Time: {mean_travel} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_type = df['User Type'].value_counts()
    print(counts_user_type)

    # Display counts of gender
    # Since the washington.csv doesn't include the gender column so we won't display counts of gender for washington
    # aso birth year isn't given in washingto.csv file
    if city != "washington":
        gender_count = df['Gender'].value_counts(dropna=False)
        print(f"Gender Count: \n{gender_count}\n")
        
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df["Birth Year"].sort_values(ascending = True)
        latest_birth = df["Birth Year"].sort_values(ascending = False)
        common_birth = df["Birth Year"].mode()[0]

        print(f"Earliest Year of Birth: \n{earliest_birth.iloc[0]}")
        print(f"Most Recent Year of Birth: \n{latest_birth.iloc[0]}")
        print(f"Common Year of Birth: \n{common_birth}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
