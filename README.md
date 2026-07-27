# sell-in-may
Sell in May and Go Away — Testing a Stock Market Seasonality Myth with Python

Overview -

"Sell in May is an investment strategy for stocks based on a theory that the period from November to April inclusive has a significantly stronger stock market growth on average than the other months." (Wikipedia)

I am testing whether this "Sell in May" theory holds up against historical stock market data using the FTSE 100 and a time period of 25 years. I believe the FTSE 100 is broad enough to represent the stock market as a whole, and 25 years is enough time to smooth out anomalous years while maintaining quality data. I tested the hypothesis by calculating the percentage difference in the price of stock from the annual average and comparing the two time periods.

So does the November-April period actually outperform May-October, and by how much?

Methods - 

Data Source: yFinance
Season Periods: November-April, May-October. A year is defined from November-October to maintain consistency across the Christmas period
Metric: Seasonal Average Close Price, % Difference from Yearly Average

Functions - 
There are three primary functions in the code, which all take the ticker (t) and the period (p) as arguments:

raw_scatter: this shows, using a scatter diagram, the stock price of a ticker across multiple years. I did not find this function very useful as it is difficult to determine whether there is consistency across the years using this graph.

monthly_diff_bar: this shows, using a bar chart, the monthly percentage difference from the annual average across multiple years. This was useful to examine the monthly affect on the stock price but wasn't concrete evidence of the seasonal trend being examined.

seasonal_diff_bar: this shows, using bar chart, the seasonal percentage difference from the annual average across multiple years. This was the most useful in observing the seasonal change in stock price and whether the phrase had measurable evidence.

Results -
![Seasonal Percentage Difference Chart](images/seasonal_perc_diff.png)
As shown in the bar chart (using seasonal_diff), stock price increases in the May-October period and decrease in the November-April period, which is the opposite of the proposed "Sell in May" statement. The chart does not show that the May-October period has consistently little stock price growth, in fact the opposite is displayed.

Limitations-

However, this is only tested on one stock index, the FTSE 100, and the generalisation of the months makes it difficult to make concrete findings.

Resolving Limitations-

Limited data - I tested the hypothesis across 10 stocks and indexes and found the results to be consistent across 11/12 of them. The stocks and indexes tested were: FTSE 100, S&P 500, Dow Jones, Nasdaq, Russell 2000, Vix (not consistent), Nvidia, Apple, Amazon, Intel, Blackrock, and AMD.

Generalising Seasons - Below are some graphs (using monthly_diff_bar) showing the monthly percentage difference from annual averages for the FTSE 100. This shows slightly different results, revealing that the data for the Nov-Apr period may be skewed by the anomalous low in March. I hypothesised that this was due to two major events occurring in the last 25 years that happened in March: COVID-19, and the Trump Tariffs stock market crash (which primarily happened in April but still affected March). After removing these two years as anomalies, the March percentage difference is similar to that of January and February rather than much lower than either. These years are removed in the graph shown below.
![Monthly Percentage Difference Chart](images/monthly_perc_diff.png)

