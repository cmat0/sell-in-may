import yfinance as yf
import pandas as pd
import calendar
from datetime import date
import re
from matplotlib import pyplot as plt
from textwrap import wrap


'''MAIN FUNCTIONS'''

#MAKE A SCATTER PLOT OF RAW PRICE PER SHARE
def raw_scatter(t,p):

    plt.close()

    monthly_df,monthly_dict = monthly_price_by_year_data(t,p)

    #SCALING THE LABEL TEXT
    label_size = max(5,10-len(monthly_dict)//5) #MINIMUM 5, DECREASING WITH NUMBER OF YEARS

    #PRINTING THE DATA!
    for year,data in monthly_dict.items(): # FOR EACH KEY(YEAR): DEFINE THE KEY AND ENTRY (YEAR = YEAR, DATA=DF FOR THAT YEAR)
        line, = plt.plot(data.index.month, data["Close"]) #PLOT THE DATA FOR EACH YEAR WITH EACH MONTH
        
        last_x = data.index.month[-1] #FIND THE LOCATION OF THE LAST DATA POINT 
        last_y = data["Close"].iloc[-1]
        plt.text(last_x, last_y, f" {year}", fontsize=label_size, #PRINT THE TEXT AT THE END OF THE LINE (SPACE NUDGES IT A BIT OVER)
                va='center', color=line.get_color()) #PRINT IN THE COLOUR OF THE LINE

    plt.xticks(range(1,13),list(calendar.month_abbr[1:])) #REPLACES THE MONTH NUMBERS FROM LN24 WITH THE ABBREVIATED NAMES
    plt.xlabel("Months")
    plt.ylabel("Share Price")
    plt.title(f"Monthly Share Price Over The Last {title_period(p)}")
    plt.show()



#MAKE A BAR CHART OF PERCENTAGE DIFFERENCE BETWEEN ANNUAL AVG AND MONTHLY AVG
def perc_diff_bar(t,p):

    monthly_df,monthly_dict = monthly_price_by_year_data(t,p)

    yearly_avg_dict = {}

    for year in monthly_dict:
        yearly_avg_dict[year] = monthly_dict[year]["Close"].mean() #CREATING A DICTIONARY OF THE YEARLY AVERAGES OF SHARE PRICE

    monthly_df["Year"] = monthly_df.index.year
    monthly_df["Year Avg"] = monthly_df["Year"].map(yearly_avg_dict)
    monthly_df["Percentage Difference"] = find_perc_diff(monthly_df["Close"],monthly_df["Year Avg"])

    month_avg_across_years = monthly_df.groupby(monthly_df.index.month)["Percentage Difference"].mean()

    colours = ["green" if v > 0 else "red" for v in month_avg_across_years]
    plt.bar(month_avg_across_years.index, month_avg_across_years.values,color=colours)
    plt.xticks(range(1,13),list(calendar.month_abbr[1:]))
    plt.xlabel("Months")
    plt.ylabel("Average Percentage Difference from Annual Average")
    plt.title("\n".join(wrap(f"Average Monthly Percentage Difference From Annual Averages Accross {title_period(p)}",60)))
    plt.show()



def monthly_diff(t,p):
    
    monthly_df,monthly_dict = monthly_price_by_year_data(t,p)


    #FIND THE AVERAGE ACROSS SEASONS

    #DEFINE MONTHS AND YEARS
    monthly_df["Month"] = monthly_df.index.month
    monthly_df["Year"] = monthly_df.index.year

    #CATAGORISE MONTHS BY WINTER + SUMMER
    monthly_df["Season"] = monthly_df["Month"].apply(lambda m: "Nov-Apr" if m in [11,12,1,2,3,4] else "May-Oct")

    #MAKE IT SO NOV-OCT IS ONE YEAR TO MAKE THE AVERAGES BETTER
    monthly_df.loc[monthly_df["Month"].isin([11,12]),"Year"] = monthly_df["Year"] + 1
    
    seasonal_df = monthly_df.groupby(["Year","Season"])[["Close"]].mean() #RESAMPLE BY THE NEW YEAR SYSTEM ABOVE
    seasonal_df = seasonal_df.reset_index()

    seasonal_df["Year Range"] = [f"{y} - {y+1}" if s == "Nov-Apr" else str(y) for y, s in zip(seasonal_df["Year"],seasonal_df["Season"])]
    #print(seasonal_avg_df[["Year Range","Close"]])

    #FIND THE YEARLY AVG (AGAIN)
    yr_avg_df = monthly_df.groupby("Year")["Close"].mean()

    seasonal_df["Percentage Difference"] = find_perc_diff(seasonal_df["Close"],seasonal_df["Year"].map(yr_avg_df))

    #FIND MEAN OF EACH SEASON
    avg_seasonal_df = seasonal_df.groupby(["Season"])["Percentage Difference"].mean()
    print(avg_seasonal_df)

    #MAKING WINTER COME BEFORE SUMMER
    avg_seasonal_df = avg_seasonal_df.sort_index(ascending=False)

    colours = ["green" if v > 0 else "red" for v in avg_seasonal_df.values]
    plt.bar(avg_seasonal_df.index, avg_seasonal_df.values,color=colours)
    plt.axhline(0, color='black', linewidth=0.8,linestyle="--")
    plt.xlabel("Season")
    plt.ylabel("Average Percentage Difference from Annual Average")
    plt.title("\n".join(wrap(f"{yf.Ticker(t).info.get("longName")} — Seasonal Stock Price: Winter (Nov–Apr) vs Summer (May–Oct) Accross {title_period(p)}.",60)))
    plt.show()




'''BG FUNCTIONS'''

#FINDING THE AVERAGE STOCK PRICE OF ANY TICKER PER A NUMBER OF YEARS (MIGHT BE ABLE TO DO MONTHS AS WELL)
def monthly_price_by_year_data(t,p): #T FOR TICKER, P FOR PERIOD
   
    dat = yf.Ticker(t) 

    df = pd.DataFrame(dat.history(period=p)) #MAKE A DATAFRAME OF THE TICKER HISTORY FOR THE LAST TIME PERIOD P, STARTING FROM 1 JAN 2026

    check_data_start(t,p,df)

    #MAKE YR_AVG_DF WHICH HAS THE AVG FROM EACH MONTH
    monthly_avg_df = df.resample("ME")["Close"].mean().to_frame() #FIND THE MEAN OF EACH MONTH IN EACH YEAR

    years = monthly_avg_df.index.year.unique() #ADD UNIQUE YEARS AS AN INDEX
    yearly_dict = {year: monthly_avg_df[monthly_avg_df.index.year == year] for year in years} #MAKES A DICTIONARY WITH YEAR AS KEY AND ENTRY AS VALUES FROM THAT YEAR
    
    return monthly_avg_df,yearly_dict #RETURNING THE YEARLY_DFS FOR THE NEXT FUNCTION



#CHANGE THE ABBREVIATION FOR THE PERIOD TO THE FULL NAME
def parse_period(p):
    period_map = {"y":"Years","mo":"Months","d":"Days"} #MAKE A DICTIONARY WITH THE FULL NAMES OF TIMES PERIODS
    for key,value in period_map.items(): #FOR EACH ENTRY IN THE DICT, SPLITTING THEM INTO KEYS AND VALUES
        if p.endswith(key): #IF THE PERIOD ENDS WITH THE ABBREVIATED PERIOD
            num,unit = re.search(r"(\d+)(\w+)",p).groups()
            return num,value
        


def find_perc_diff(new,avg):

    decimal = (new-avg)/avg
    perc = decimal*100
    return perc



def check_data_start(t,p,df):
    num, unit = re.search(r"(\d+)(\w+)", p).groups()
    
    #CHECK THAT DF EXISTS
    if df.empty:
        raise ValueError("There is an error in the database for this ticker.")

    #SET THE OFFSET
    unit_map = {"y":"years","mo":"months","d":"days"}
    kwargs = unit_map.get(unit)

    expected_start = pd.Timestamp(date.today(), tz=df.index.tz) - pd.DateOffset(**{kwargs: int(num)})
    actual_start = df.index.min()
    if actual_start > expected_start + pd.DateOffset(days=30):
        raise ValueError(
            f"Requested {p} of data for '{t}', but data only goes back to {actual_start.date()}. "
            f"The ticker may not have existed that far back."
            )
        


def start_date(p):
    num,value = parse_period(p)
    today = date.today()
    #MAKE ARGUMENT MAP
    kwarg = value.lower()
    
    offset = pd.DateOffset(**{kwarg: int(num)})
    new_date = pd.to_datetime(today) - offset
    return new_date



def title_period(p):
    if p == "ytd":
        title_period = "All Time"
    else:
        num,unit = parse_period(p)
        title_period = f"{num} {unit}"
    return title_period


#raw_scatter("^FTSE","10y") #FIRST VAR IS TICKER, SECOND IS PERIOD, THIS ONLY WORKS FROM 1YR BACK TO 2010
#perc_diff_bar("^FTSE","15y") #MAX 40 YEARS DUE TO LIBRARY LIMITATIONS
monthly_diff("^FTSE","15y")
