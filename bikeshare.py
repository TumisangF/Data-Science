
import time
import pandas as pd
import numpy as np
from statistics import mean

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # TO DO: get user input for city (chicago, new york city, washington). 
    while True:
        cities = ['chicago','new york city','washington']
        city = input('Which city would you like to explore? Chicago, New York City, or Washington?\n').lower().strip()
        
        if city in cities:
            break
        else:
            print('Please enter a valid city')
            continue
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['All','January','February','March','April','May','June']
        invalid_months = ['July','August','September','October','November','December']
        month = input('Enter a month (e.g May) or "All" for all \n').title().strip()
        
        if month in months:
            break
        # Edge case 1. If input month is out of bounds, greater than June
        elif month in invalid_months:
            print('Please enter any month between January and June, Inclusive')
        else:
            print('Sorry, please try again')
            continue
    
    while True:
      day = input("Please enter any day of week. e.g 'Monday' or 'All' for no filter.\n").title().strip()
      weekdays = ['All','Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      
      if day not in weekdays:
        print("Sorry, Please Try again.")
        continue
      else:
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
    
    df = pd.read_csv(CITY_DATA[city])

    # convert the 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day and hour from 'Start Time' to create new columns
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'All':
        df = df[df['month'] == month]
    
    if day != 'All':
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    frequent_month = df['month'].mode()[0]
    print(f'The most common month is: {frequent_month}')
    
    # TO DO: display the most common day of week
    frequent_day = df['day_of_week'].mode()[0]
    print(f'The most frequent day of the week is: {frequent_day}')

    # TO DO: display the most common start hour
    frequent_hour = df['hour'].mode()[0]
    print(f'The most frequent hour is: {frequent_hour}')


    print(f'\nThis took {round(time.time() - start_time,3)} seconds')
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station =  df['Start Station'].mode()[0]
    print(f'The most common start station is: {common_start_station}')

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'The most common end station is: {common_end_station}')

    
    # TO DO: display most frequent combination of start station and end station trip
    
    df['Start End'] = df['Start Station'] + ' >>> ' + df['End Station']
    common_combination  = df['Start End'].mode()[0]
    print(f'The most common start end  stations is: {common_combination}')

    print(f'\nThis took {round(time.time() - start_time,3)} seconds')
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    seconds = round(df['Trip Duration'].sum(axis=0))
    
    # Converting time to days, hours, min and seconds
    day = seconds // (3600 * 24)
    hour = seconds // 3600 % 24
    min = seconds % 3600 // 60
    sec = seconds % 3600 % 60

    if day > 0:
        print(f'Total travel time is: {day} days, {hour} hours, {min} minutes and {sec} seconds')
    elif hour > 0:
        print(f'Total travel time is: {hour} hour, {min} minutes and {sec} seconds')
    elif min > 0:
        print(f'Total travel time is: {min} minutes and {sec} seconds')

    # TO DO: display mean travel time
    # TO DO: get rid of decimal numbers
    
    mean_travel_time = round((df['Trip Duration'].mean()))
    m = mean_travel_time // 60
    s = mean_travel_time % 60

    print(f'Mean travel time is {m} minutes and {s} seconds')
    
    print(f'\nThis took {round(time.time() - start_time,3)} seconds')
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    '''
    Edge case 1. Chicago has an outlier:
    Expected  user types >> Subscriber and Customer
    Output user types >> Subscriber, Customer & Dependant

    Solution:
    >> Replace the outliner with the most frequent value with the assumption that it was a mistake since there can only be two values
    >> Fixing outliers is the best option for algorithms like regression 
    '''

    df = df.replace('Dependent',df['User Type'].mode()[0])

    print(f"User type information:\n{df['User Type'].value_counts().to_string()} \n")

    # TO DO: Display counts of gender
    # Edge case: Gender information is not available for Washington city resulting in a KeyError
    try:
        
        print(f"Gender Information:\n{df['Gender'].value_counts().to_string()} \n")

    # TO DO: Display earliest, most recent, and most common year of birth
    # Edge case: Birth year is not available for the washington city resulting in a KeyError
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]

        print(f'The oldest user was born in: {int(earliest)}')
        print(f'The youngest user was born in: {int(recent)}')
        print(f'The most frequent age amongst all users is: {int(common)}')
    
    except KeyError:
        print("Sorry, No additional information is available for Washington city")


    print(f'\nThis took {round(time.time() - start_time,3)} seconds')
    print('-'*40)

def data(df):
    # TO DO: Display individual data
    df = df.drop('Unnamed: 0', axis =1)

    start,end = 0,5
    while True:
        answer = input('Would you like to see data? \n').lower()
 
        if answer == 'yes':
            print(df.iloc[start:end])
            start += 5
            end += 5
            continue
        elif answer == 'no':
            break
        else:
            print('Sorry. invalid input. Enter "yes" or "no"')


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()