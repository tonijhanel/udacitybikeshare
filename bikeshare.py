import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city =input("Please enter one of the following cities you want to see data for:\n Chicago, New York,or Washington\n").lower()
        print('City ', city)
        if city in cities:
            break
        else:
            print('Please enter valid city.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        choice = input("Would you like to filter the data by month, day, or none?\n").lower()
        if choice == 'month':
            month = input("Please enter the month you want to explore. If you do not want a month filter enter 'all'. \nChoices: All, January, February, March, April, May, June\n").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Please enter a valid month.')
        elif choice == 'day':
            day = input("Please enter the day of the week you want to explore. If you do not want to apply a month filter enter 'all'. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()
    
            month = 'all'
            if day in days:
                break
            else:
                print('Please enter a valid day')
        elif choice == 'none':
            month = 'all'
            day = 'all'
            break
   

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)


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
    #load city data csv file
    #format Start Time columne to date time
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
  
    #filter months
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

 
    if day != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'sunday']
        #day = days.index(day.capitalize()) 
        
        df = df[df['Day_of_Week'] == day.capitalize()]
   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Month'].mode()[0]
    common_month = months[common_month-1].capitalize()
    print("The most common month is:",common_month, "\n")

    # TO DO: display the most common day of week
    popular_day = df['Day_of_Week'].mode()[0]
    print("The most common day is:",popular_day, "\n")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is:", df['hour'].mode()[0], "\n")
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0], "\n")

    # TO DO: display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0], "\n")

    # TO DO: display most frequent combination of start station and end station trip
    #created combined column for start and end stations
    df['Station Combo'] = df['Start Station'] + " : " + df['End Station']
 
    #get the most occurring combo using mode() method
    print("The most frequent combination of start station and end station trip is: ", df['Station Combo'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total Trip Duration = ", seconds_to_datestring(total_duration))

    # TO DO: display mean travel time
    total_mean = df['Trip Duration'].mean()
    

    #print("Average Trip duration = ", total_mean)
    print("Average Trip duration = ", seconds_to_datestring(total_mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print()
    print(user_types)

    # TO DO: Display counts of gender
    # only is data set city is not washington
    if city != 'washington':
        # Display counts of gender
        gen = df.groupby(['Gender'])['Gender'].count()
        print()
        print(gen)
        print()

        # TO DO: Display earliest, most recent, and most common year of birth
        
        #Get and print oldest year of birth
        earliest = df['Birth Year'].min() 
        print('The earliest year of birth is= ', earliest)

        #Get and print youngest year of birth
        recent = df['Birth Year'].max() 
        print('The youngest year of birth = ', recent)

        #Get and print most common year of birth 
        common = df['Birth Year'].mode()[0] #This gives the Common Birth Year 
        print('The most common year of birth year =', common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    # Ask user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to see  5 lines of raw data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break

#method that takes seconds as input parameter and returns hours, minutes and seconds in string format
def seconds_to_datestring(seconds):
    datestring = ''
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    datestring = "Hours: {}, Minutes: {}, Seconds: {}".format(hours, minutes, seconds)
    return datestring

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
