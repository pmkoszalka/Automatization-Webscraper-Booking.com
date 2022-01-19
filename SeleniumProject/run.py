from Selenium.SeleniumProject.booking_folder.booking import Booking

if __name__ == '__main__':
    with Booking() as bot:  # context manager
        bot.land_first_page()  # lands the opening page
        bot.close_pop_up()  # clears the cookies pop-up
        bot.change_language_to_english()  # changes the language to english for the script to be in english
        bot.change_currency('PLN')  # changes to the desired currency
        bot.input_travel_location('Bilbao')  # searches for the desired location
        bot.select_date('2022-02-11', '2022-02-14')  # searches for the desired dates of the vacations
        bot.select_adults_number(2)  # selects desired number of adults in the party
        bot.search()  # searches for results
        bot.apply_filtration()  # applies the filtration, they can be set up in the booking.py
        stats = bot.report(26)  # reports the desired number of entries
        data_cleaned = bot.data_cleaning(stats)  # cleans the data
        data_cleaned_with_columns = bot.add_ratio_columns(data_cleaned)
        print('-----------------------------------------------------------')
        print(data_cleaned_with_columns.sort_values(by=data_cleaned_with_columns.columns[-1])) # the lowest KPI the better
        print('-----------------------------------------------------------')
        data_cleaned_with_columns_described = bot.show_basic_stats(data_cleaned_with_columns)  # describes the data
        print(data_cleaned_with_columns_described)
