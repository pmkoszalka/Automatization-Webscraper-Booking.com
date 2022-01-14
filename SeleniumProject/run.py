from Selenium.SeleniumProject.booking_folder.booking import Booking

# def example_run():
#     with Booking() as bot:
#         bot.land_first_page()  # once it reaches the bot of this method it will instantiate exit method
#         bot.change_currency('PLN')
#         bot.input_travel_location('Barcelona')
#         bot.select_date('2022-02-14', '2022-02-20')
#         bot.select_adults_number(2)
#         bot.search()
#         bot.apply_filtration()
#         stats = bot.report_hotel_names(10)
#         print(stats)
#         print(bot.show_basic_stats(stats))

if __name__ == '__main__':
    # context manager
    # try:
    with Booking() as bot:
        bot.land_first_page()  # once it reaches the bot of this method it will instantiate exit method
        bot.close_pop_up()
        bot.change_language_to_english()
        bot.change_currency('PLN')
        bot.input_travel_location('Barcelona')
        bot.select_date('2022-02-14', '2022-02-20')
        bot.select_adults_number(2)
        bot.search()
        bot.apply_filtration()
        bot.stops()
        stats = bot.report_hotel_names()
        # print(stats)
        # #print(bot.data_cleaning(stats))
        # print(bot.show_basic_stats(stats))

