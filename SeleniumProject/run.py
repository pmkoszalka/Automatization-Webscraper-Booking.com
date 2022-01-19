from Selenium.SeleniumProject.booking_folder.booking import Booking

if __name__ == '__main__':
    # context manager
    with Booking() as bot:
        bot.land_first_page()  # once it reaches the bot of this method it will instantiate exit method
        bot.close_pop_up()
        bot.change_language_to_english()
        bot.change_currency('PLN')
        bot.input_travel_location('Madrid')
        bot.select_date('2022-02-11', '2022-02-14')
        bot.select_adults_number(2)
        bot.search()
        bot.apply_filtration()
        bot.stops()
        stats = bot.report(26)
        data_cleaned = bot.data_cleaning(stats)
        data_cleaned_with_columns = bot.add_ratio_column(data_cleaned)
        print('-----------------------------------------------------------')
        print(data_cleaned_with_columns)
        print('-----------------------------------------------------------')
        print(bot.show_basic_stats(data_cleaned_with_columns))

