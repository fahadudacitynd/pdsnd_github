import time 
import pandas as pd
import numpy as np
import datetime as dt
import click
# Preparing 

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
# Variables are set 

def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers."""

    while True:
        choice = input(prompt).lower().strip()
        # If the input is end 
        if choice == 'end':
            raise SystemExit
        # If the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # If the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break
        # If the input was wrong  
        prompt = ("\nSomething is wrong. Please ensure entering a valid option:\n>")

    return choice

# Selecting choices 
def get_filters():
    """ Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"          to apply no month filter
        (str) day - name of the day of week to filter by, or            "all" to apply no day filter
    """

    print("\n\nHello! Let's explore some US bikeshare data!\n")

    print("Type 'end' whenever you would like to exit the program.\n")

    while True:
        city = choice("\nChoose a city: New York City, Chicago or Washington."
                      " Use commas to list many choices.\n>", CITY_DATA.keys())
        month = choice("\nChoose a month from January to June."
                       " Use commas to list many choices.\n>",
                       months)
        day = choice("\nChoose a day from Sunday to Saturday."
                     " Use commas to list many choices.\n>", days)

        # Confirming the choice 
        confirmation = choice("\nPlease confirm that you would like to apply the following choices to the data."
                              "\n\n City: {}\n Month: {}\n Day"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's give it one more time!")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the choice of city, month and
       day.

    Args:
        (str) city - name of the city to filter 
        (str) month - name of the month to filter
        (str) day - name of the day to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nLoading the data.")
    start_time = time.time()

    # filter the data for the selected city 
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # Reorganizing
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # An additional column to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to the selected month and day 
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month) + 1)], month))
    else:
        df = df[df['Month'] == (months.index(month) + 1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Day'] == day.title()], day))
    else:
        df = df[df['Day'] == day.title()]

    print("\nIt took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df

# Popular Times of Travel 
def time_stats(df):
    """Display the popular times of travel."""

    print('\nDisplaying the popular times of travel...\n')
    start_time = time.time()

    # The most common month
    most_common_month = df['Month'].mode()[0]
    print('The most common traveling month is: ' +
          str(months[most_common_month-1]).title() + '.')

    # The most common weekday
    most_common_day = df['Day'].mode()[0]
    print('The most common weekday is: ' +
          str(most_common_day) + '.')

    # The most common hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common hour of the day is: ' +
          str(most_common_hour) + '.')

    print("\nIt took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

# Popular Stations and Trip 
def station_stats(df):
    """Display the popular stations and trip."""

    print('\nDisplaying the popular Stations and Trip...\n')
    start_time = time.time()

    # Most common start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " +
          most_common_start_station)

    # Most common end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common end station is: " +
          most_common_end_station)

    # Most common trip from start to end 
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("The most common trip from start to end is: " + most_common_start_end_combination)

    print("\nIt took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

# Trip duration 
def trip_duration_stats(df):
    """Display trip duration."""

    print('\nDisplaying trip duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time // 86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400) // 3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600) // 60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('The total travel time is : ' +
          total_travel_time + '.')

    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time // 60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("The mean travel time is : " +
          mean_travel_time + ".")

    print("\nIt took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

# User information 
def user_stats(df, city):
    """Display user information."""

    print('\nDisplaying user information...\n')
    start_time = time.time()

    # Counts of each user type
    user_types = df['User Type'].value_counts().to_string()
    print("Counts of each user type: ")
    print(user_types)

    # Counts of each user gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nCounts of each user gender:")
        print(gender_distribution)
    except KeyError:
        print("There is no data of user genders for {}."
              .format(city.title()))

    # Earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nThe earliest year of birth for a user is: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("\nThe most recent year of birth for a user is: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("The most common year of birth for a user is: " + most_common_birth_year)
    except:
        print("There is no data of birth year for {}."
              .format(city.title()))

    print("\nIt took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

# Raw data 
def raw_data(df, mark_place):
    """Display 5 lines of sorted raw data each time."""

    print("\nViewing raw data.")

    # User last stop 
    if mark_place > 0:
        last_place = choice("\nWould you like to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0

    # sort data by column
    if mark_place == 0:
        sort_df = choice("\nPress enter to view unsorted data.\n \n [st] Start Time\n [et] End Time\n "
                         "[td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>",
                         ('st', 'et', 'td', 'ss', 'es', ''))

        asc_or_desc = choice("\nSorting data ascending or "
                             "descending? \n [a] Ascending\n [d] Descending"
                             "\n\n>",
                             ('a', 'd'))

        if asc_or_desc == 'a':
            asc_or_desc = True
        elif asc_or_desc == 'd':
            asc_or_desc = False

        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_or_desc)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_or_desc)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_or_desc)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_or_desc)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_or_desc)
        elif sort_df == '':
            pass

    # 5 lines of data for each loop 
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if choice("Would you like to keep printing data?"
                      "\n\n[y] Yes\n[n] No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mark_place


def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        mark_place = 0
        while True:
            select_data = choice("\nPlease select the required information.\n\n [ts] Time Stats\n [ss] "
                                 "Station Information\n [tds] Trip Duration Information\n "
                                 "[us] User Information\n [rd] Display Raw Data\n "
                                 "[r] Restart\n\n>",
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                mark_place = raw_data(df, mark_place)
            elif select_data == 'r':
                break

        restart = choice("\nWould you like to restart?\n\n[y] Yes\n[n] No\n\n>")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
