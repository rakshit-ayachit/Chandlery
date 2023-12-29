import plotly.graph_objs as go
import streamlit as st
import datetime as dt
from kiteapp import *
import pandas as pd
import numpy as np
import time

with open("enctoken.txt") as f1:
	enctoken = f1.read()

kite = KiteApp("s1", "U#####", enctoken)
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
# instrument_dump = kite.instruments("BSE")
# instrument_df = pd.DataFrame(instrument_dump)

def instrumentLookup(instrument_df,symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1

def fetch_data(ticker, interval, duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data

def doji(ohlc_df):    
    """returns dataframe with doji candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["doji"] = abs(df["close"] - df["open"]) <=  (0.05 * avg_candle_size)
    return df

def maru_bozu(ohlc_df):    
    """returns dataframe with maru bozu candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["h-c"] = df["high"]-df["close"]
    df["l-o"] = df["low"]-df["open"]
    df["h-o"] = df["high"]-df["open"]
    df["l-c"] = df["low"]-df["close"]
    df["maru_bozu"] = np.where((df["close"] - df["open"] > 2*avg_candle_size) & \
                               (df[["h-c","l-o"]].max(axis=1) < 0.005*avg_candle_size),"maru_bozu_green",
                               np.where((df["open"] - df["close"] > 2*avg_candle_size) & \
                               (abs(df[["h-o","l-c"]]).max(axis=1) < 0.005*avg_candle_size),"maru_bozu_red",False))
    df.drop(["h-c","l-o","h-o","l-c"],axis=1,inplace=True)
    return df

def hammer(ohlc_df):    
    """returns dataframe with hammer candle column"""
    df = ohlc_df.copy()
    df["hammer"] = (((df["high"] - df["low"])>3*(df["open"] - df["close"])) & \
                   ((df["close"] - df["low"])/(.001 + df["high"] - df["low"]) > 0.6) & \
                   ((df["open"] - df["low"])/(.001 + df["high"] - df["low"]) > 0.6)) & \
                   (abs(df["close"] - df["open"]) > 0.1* (df["high"] - df["low"]))
    return df


def shooting_star(ohlc_df):    
    """returns dataframe with shooting star candle column"""
    df = ohlc_df.copy()
    df["sstar"] = (((df["high"] - df["low"])>3*(df["open"] - df["close"])) & \
                   ((df["high"] - df["close"])/(.001 + df["high"] - df["low"]) > 0.6) & \
                   ((df["high"] - df["open"])/(.001 + df["high"] - df["low"]) > 0.6)) & \
                   (abs(df["close"] - df["open"]) > 0.1* (df["high"] - df["low"]))
    return df

def long_legged_doji(ohlc_df):    
    """returns dataframe with Long-Legged Doji candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["long_legged_doji"] = (abs(df["high"] - df["low"]) > 2 * avg_candle_size) & \
                              (abs(df["close"] - df["open"]) <= 0.3 * (df["high"] - df["low"]))
    return df

def dragonfly_doji(ohlc_df):    
    """returns dataframe with Dragonfly Doji candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["dragonfly_doji"] = (abs(df["high"] - df["low"]) <= 0.1 * avg_candle_size) & \
                            (df["open"] == df["low"]) & \
                            (abs(df["close"] - df["open"]) <= 0.1 * (df["high"] - df["low"]))
    return df

def gravestone_doji(ohlc_df):    
    """returns dataframe with Gravestone Doji candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["gravestone_doji"] = (abs(df["high"] - df["low"]) <= 0.1 * avg_candle_size) & \
                              (df["close"] == df["low"]) & \
                              (abs(df["close"] - df["open"]) <= 0.1 * (df["high"] - df["low"]))
    return df

def rickshaw_man(ohlc_df):    
    """returns dataframe with Rickshaw Man candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    body_size = abs(df["close"] - df["open"])
    wick_size = df["high"] - df["low"]
    df["rickshaw_man"] = (body_size <= 0.1 * avg_candle_size) & (wick_size >= 2 * body_size)
    return df

def levels(ohlc_day):    
    """returns pivot point and support/resistance levels"""
    high = round(ohlc_day["high"][-1],2)
    low = round(ohlc_day["low"][-1],2)
    close = round(ohlc_day["close"][-1],2)
    pivot = round((high + low + close)/3,2)
    r1 = round((2*pivot - low),2)
    r2 = round((pivot + (high - low)),2)
    r3 = round((high + 2*(pivot - low)),2)
    s1 = round((2*pivot - high),2)
    s2 = round((pivot - (high - low)),2)
    s3 = round((low - 2*(high - pivot)),2)
    return (pivot,r1,r2,r3,s1,s2,s3)

def trend(ohlc_df,n):
    "function to assess the trend by analyzing each candle"
    df = ohlc_df.copy()
    df["up"] = np.where(df["low"]>=df["low"].shift(1),1,0)
    df["dn"] = np.where(df["high"]<=df["high"].shift(1),1,0)
    if df["close"][-1] > df["open"][-1]:
        if df["up"][-1*n:].sum() >= 0.7*n:
            return "uptrend"
    elif df["open"][-1] > df["close"][-1]:
        if df["dn"][-1*n:].sum() >= 0.7*n:
            return "downtrend"
    else:
        return None
   
def res_sup(ohlc_df,ohlc_day):
    """calculates closest resistance and support levels for a given candle"""
    level = ((ohlc_df["close"][-1] + ohlc_df["open"][-1])/2 + (ohlc_df["high"][-1] + ohlc_df["low"][-1])/2)/2
    p,r1,r2,r3,s1,s2,s3 = levels(ohlc_day)
    l_r1=level-r1
    l_r2=level-r2
    l_r3=level-r3
    l_p=level-p
    l_s1=level-s1
    l_s2=level-s2
    l_s3=level-s3
    lev_ser = pd.Series([l_p,l_r1,l_r2,l_r3,l_s1,l_s2,l_s3],index=["p","r1","r2","r3","s1","s2","s3"])
    sup = lev_ser[lev_ser>0].idxmin()
    res = lev_ser[lev_ser<0].idxmax()
    return (eval('{}'.format(res)), eval('{}'.format(sup)))

def candle_type(ohlc_df):    
    """returns the candle type of the last candle of an OHLC DF"""
    candle = None
    if doji(ohlc_df)["doji"][-1] == True:
        candle = "doji"    
    if maru_bozu(ohlc_df)["maru_bozu"][-1] == "maru_bozu_green":
        candle = "maru_bozu_green"       
    if maru_bozu(ohlc_df)["maru_bozu"][-1] == "maru_bozu_red":
        candle = "maru_bozu_red"        
    if shooting_star(ohlc_df)["sstar"][-1] == True:
        candle = "shooting_star"        
    if hammer(ohlc_df)["hammer"][-1] == True:
        candle = "hammer"
    if long_legged_doji(ohlc_df)["long_legged_doji"][-1] == True:
        candle = "long_legged_doji"
    if dragonfly_doji(ohlc_df)["dragonfly_doji"][-1] == True:
        candle = "dragonfly_doji"
    if gravestone_doji(ohlc_df)["gravestone_doji"][-1] == True:
        candle = "gravestone_doji"
    if rickshaw_man(ohlc_df)["rickshaw_man"][-1] == True:
        candle = "rickshaw_man"
    return candle

def candle_pattern(ohlc_df, ohlc_day):    
    """returns the candle pattern identified"""
    pattern = None
    description = None
    recommendation = None

    signi = "low"
    avg_candle_size = abs(ohlc_df["close"] - ohlc_df["open"]).median()
    sup, res = res_sup(ohlc_df, ohlc_day)
    
    if (sup - 1.5 * avg_candle_size) < ohlc_df["close"][-1] < (sup + 1.5 * avg_candle_size):
        signi = "HIGH"
        
    if (res - 1.5 * avg_candle_size) < ohlc_df["close"][-1] < (res + 1.5 * avg_candle_size):
        signi = "HIGH"
    
    if candle_type(ohlc_df) == 'doji' \
            and ohlc_df["close"][-1] > ohlc_df["close"][-2] \
            and ohlc_df["close"][-1] > ohlc_df["open"][-1]:
        pattern = "doji_bullish"
        description = "A doji candle indicating market indecision. Occurs when opening and closing prices are nearly equal."
        recommendation = "Consider potential reversal or trend continuation based on confirmation from subsequent candles."

    
    if candle_type(ohlc_df) == 'doji' \
            and ohlc_df["close"][-1] < ohlc_df["close"][-2] \
            and ohlc_df["close"][-1] < ohlc_df["open"][-1]:
        pattern = "doji_bearish"
        description= "A doji candle indicating market indecision. Occurs when opening and closing prices are nearly equal."
        recommendation= "Consider potential reversal or trend continuation based on confirmation from subsequent candles."

            
    if candle_type(ohlc_df) == "maru_bozu_green":
        pattern = "maru_bozu_bullish"
        description = "A candlestick with no shadows, indicating strong bullish momentum."
        recommendation = "Consider potential continuation of the uptrend."
    
    if candle_type(ohlc_df) == "maru_bozu_red":
        pattern = "maru_bozu_bearish"
        description = "A candlestick with no shadows, indicating strong bearish momentum."
        recommendation ="Consider potential continuation of the downtrend."

        
    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" and candle_type(ohlc_df) == "hammer":
        pattern = "hanging_man_bearish"
        description ="A bearish reversal pattern, signaling a potential trend change."
        recommendation = "Consider selling or shorting positions, based on confirmation from subsequent candles."
    
        
    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" and candle_type(ohlc_df) == "hammer":
        pattern = "hammer_bullish"
        description = "A bullish reversal pattern, suggesting a potential trend change."
        recommendation = "A bullish reversal pattern, suggesting a potential trend change."

        
    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" and candle_type(ohlc_df) == "shooting_star":
        pattern = "shooting_star_bearish"
        description = "A bearish reversal pattern, indicating potential downward movement."
        recommendation = "Consider selling or shorting positions, based on confirmation from subsequent candles."
        
    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" \
            and candle_type(ohlc_df) == "doji" \
            and ohlc_df["high"][-1] < ohlc_df["close"][-2] \
            and ohlc_df["low"][-1] > ohlc_df["open"][-2]:
        pattern = "harami_cross_bearish"
        description = "A bearish reversal pattern, indicating a potential trend change."
        recommendation = "Consider selling or shorting positions, based on confirmation from subsequent candles."
    
    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" \
            and candle_type(ohlc_df) == "doji" \
            and ohlc_df["high"][-1] < ohlc_df["open"][-2] \
            and ohlc_df["low"][-1] > ohlc_df["close"][-2]:
        pattern = "harami_cross_bullish"
        description =  "A bullish reversal pattern, indicating a potential trend change."
        recommendation = "Consider buying or going long, based on confirmation from subsequent candles."
        
    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" \
            and candle_type(ohlc_df) != "doji" \
            and ohlc_df["open"][-1] > ohlc_df["high"][-2] \
            and ohlc_df["close"][-1] < ohlc_df["low"][-2]:
        pattern = "engulfing_bearish"
        description ="A bearish reversal pattern, suggesting a potential trend change."
        recommendation = "Consider selling or shorting positions, based on confirmation from subsequent candles."
            
    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" \
            and candle_type(ohlc_df) != "doji" \
            and ohlc_df["close"][-1] > ohlc_df["high"][-2] \
            and ohlc_df["open"][-1] < ohlc_df["low"][-2]:
        pattern = "engulfing_bullish"
        description =  "A bullish reversal pattern, suggesting a potential trend change."
        recommendation = "Consider buying or going long, based on confirmation from subsequent candles."
    
    if long_legged_doji(ohlc_df)["long_legged_doji"][-1] == True:
        if candle_type(ohlc_df) == 'doji':
            pattern = "long_legged_doji_neutral"
            description = "A doji candle with long upper and lower shadows, indicating market indecision."
            recommendation = "Wait for further confirmation before taking any trading decisions."

        elif ohlc_df["close"][-1] > ohlc_df["open"][-1]:
            pattern = "long_legged_doji_bullish"
            description = "A doji candle with long upper and lower shadows, indicating potential bullish reversal."
            recommendation = "Consider potential reversal to the upside based on confirmation from subsequent candles."

        else:
            pattern = "long_legged_doji_bearish"
            description = "A doji candle with long upper and lower shadows, indicating potential bearish reversal."
            recommendation = "Consider potential reversal to the downside based on confirmation from subsequent candles."
    
    if dragonfly_doji(ohlc_df)["dragonfly_doji"][-1] == True:
        if ohlc_df["close"][-1] > ohlc_df["open"][-1]:
            pattern = "dragonfly_doji_bullish"
            description = "A doji candle with a long lower shadow, indicating potential bullish reversal."
            recommendation = "Consider potential reversal to the upside based on confirmation from subsequent candles."
   
        else:
            pattern = "dragonfly_doji_bearish"
            description = "A doji candle with a long upper shadow, indicating potential bearish reversal."
            recommendation = "Consider potential reversal to the downside based on confirmation from subsequent candles."

    if gravestone_doji(ohlc_df)["gravestone_doji"][-1] == True:
        if ohlc_df["close"][-1] > ohlc_df["open"][-1]:
            pattern = "gravestone_doji_bullish"
            description =  "A doji candle with a long upper shadow, indicating potential bullish reversal."
            recommendation = "Consider potential reversal to the upside based on confirmation from subsequent candles."
        else:
            pattern = "gravestone_doji_bearish"
            description = "A doji candle with a long lower shadow, indicating potential bearish reversal."
            recommendation = "Consider potential reversal to the downside based on confirmation from subsequent candles."
    
    if rickshaw_man(ohlc_df)["rickshaw_man"][-1] == True:
        if ohlc_df["close"][-1] > ohlc_df["open"][-1]:
            pattern = "rickshaw_man_bullish"
            description ="A candlestick with a small body and long shadows, indicating market indecision."
            recommendation = "Wait for further confirmation before taking any trading decisions."

        else:
            pattern = "rickshaw_man_bearish"
            description = "A candlestick with a small body and long shadows, indicating market indecision."
            recommendation = "Wait for further confirmation before taking any trading decisions."
       
    return pattern, signi, description, recommendation

def main(ticker):
    try:
        ohlc = fetch_data(ticker, '5minute', 5)
        ohlc_day = fetch_data(ticker, 'day', 30)
        ohlc_day = ohlc_day.iloc[:-1, :]
        cp = candle_pattern(ohlc, ohlc_day)
        st.write(f"Analysis for {ticker}: {cp}")
    except:
        st.error(f"Skipping for {ticker}. Some error occurred.")

def display_interface():

    st.title('Chandlery: Illuminating Market Signals')
    st.header("A tool illuminating market signals through candlestick pattern analysis for informed trading decisions.")
    st.markdown("Select options from the sidebar to explore candlestick patterns in stock data.")

    ticker = st.sidebar.selectbox('Select Ticker', tickers)
    interval = st.sidebar.selectbox('Select Interval', ['5minute', '10minute', '30minute'])
    duration = st.sidebar.selectbox('Select Duration', [7, 30, 90, 180])

    if st.sidebar.button('Run Analysis'):
        try:
            ohlc = fetch_data(ticker, interval, duration)
            ohlc_day = fetch_data(ticker, 'day', 30)
            ohlc_day = ohlc_day.iloc[:-1, :]

            pattern, signi, description, recommendation = candle_pattern(ohlc, ohlc_day)
            
            st.subheader("Candlestick Patterns Identified")
            st.info(pattern)
            
            st.subheader("Significance")
            st.info(signi)
            
            st.subheader("Description")
            st.info(description)
            
            st.subheader("Recommendation")
            st.info(recommendation)
            
            fig = go.Figure(data=[go.Candlestick(x=ohlc.index,
                                                 open=ohlc['open'],
                                                 high=ohlc['high'],
                                                 low=ohlc['low'],
                                                 close=ohlc['close'])])
            st.plotly_chart(fig)
            
        except:
            st.error(f"Skipping for {ticker}. Some error occurred.")
    st.markdown("---")
    st.markdown("**Disclaimer**")
    st.warning(
        "Please note, Chandlery is currently under development and may not fully function for all market scenarios, particularly for sideways trends. It is intended for personal use only and should not be considered as a professional trading strategy or financial advice. Users are encouraged to seek guidance from financial experts before executing any trades based on the information provided by this application. The developer cannot be held responsible for any financial losses incurred by using this app."
    )

    if st.sidebar.button('Stop Analysis'):
        st.warning('Stopping the analysis...')
        time.sleep(5)
        st.experimental_rerun()
    pass

tickers = ["ZEEL","WIPRO","VEDL","ULTRACEMCO","UPL","TITAN","TECHM","TATASTEEL",
            "TATAMOTORS","TCS","SUNPHARMA","SBIN","SHREECEM","RELIANCE","POWERGRID",
            "ONGC","NESTLEIND","NTPC","MARUTI","M&M","LT","KOTAKBANK","JSWSTEEL","INFY",
            "INDUSINDBK","IOC","ITC","ICICIBANK","HDFC","HINDUNILVR","HINDALCO",
            "HEROMOTOCO","HDFCBANK","HCLTECH","GRASIM","GAIL","EICHERMOT","DRREDDY",
            "COALINDIA","CIPLA","BRITANNIA","INFRATEL","BHARTIARTL","BPCL","BAJAJFINSV",
            "BAJFINANCE","BAJAJ-AUTO","AXISBANK","ASIANPAINT","ADANIPORTS","IDEA",
            "MCDOWELL-N","UBL","NIACL","SIEMENS","SRTRANSFIN","SBILIFE","PNB",
            "PGHH","PFC","PEL","PIDILITIND","PETRONET","PAGEIND","OFSS","NMDC","NHPC",
            "MOTHERSUMI","MARICO","LUPIN","L&TFH","INDIGO","IBULHSGFIN","ICICIPRULI",
            "ICICIGI","HINDZINC","HINDPETRO","HAVELLS","HDFCLIFE","HDFCAMC","GODREJCP",
            "GICRE","DIVISLAB","DABUR","DLF","CONCOR","COLPAL","CADILAHC","BOSCHLTD",
            "BIOCON","BERGEPAINT","BANKBARODA","BANDHANBNK","BAJAJHLDNG","DMART",
            "AUROPHARMA","ASHOKLEY","AMBUJACEM","ADANITRANS","ACC",
            "WHIRLPOOL","WABCOINDIA","VOLTAS","VINATIORGA","VBL","VARROC","VGUARD",
            "UNIONBANK","UCOBANK","TRENT","TORNTPOWER","TORNTPHARM","THERMAX","RAMCOCEM",
            "TATAPOWER","TATACONSUM","TVSMOTOR","TTKPRESTIG","SYNGENE","SYMPHONY",
            "SUPREMEIND","SUNDRMFAST","SUNDARMFIN","SUNTV","STRTECH","SAIL","SOLARINDS",
            "SHRIRAMCIT","SCHAEFFLER","SANOFI","SRF","SKFINDIA","SJVN","RELAXO",
           "RAJESHEXPO","RECLTD","RBLBANK","QUESS","PRESTIGE","POLYCAB","PHOENIXLTD",
           "PFIZER","PNBHOUSING","PIIND","OIL","OBEROIRLTY","NAM-INDIA","NATIONALUM",
           "NLCINDIA","NBCC","NATCOPHARM","MUTHOOTFIN","MPHASIS","MOTILALOFS","MINDTREE",
           "MFSL","MRPL","MANAPPURAM","MAHINDCIE","M&MFIN","MGL","MRF","LTI","LICHSGFIN",
           "LTTS","KANSAINER","KRBL","JUBILANT","JUBLFOOD","JINDALSTEL","JSWENERGY",
           "IPCALAB","NAUKRI","IGL","IOB","INDHOTEL","INDIANB","IBVENTURES","IDFCFIRSTB",
           "IDBI","ISEC","HUDCO","HONAUT","HAL","HEXAWARE","HATSUN","HEG","GSPL",
           "GUJGASLTD","GRAPHITE","GODREJPROP","GODREJIND","GODREJAGRO","GLENMARK",
           "GLAXO","GILLETTE","GMRINFRA","FRETAIL","FCONSUMER","FORTIS","FEDERALBNK",
           "EXIDEIND","ESCORTS","ERIS","ENGINERSIN","ENDURANCE","EMAMILTD","EDELWEISS",
           "EIHOTEL","LALPATHLAB","DALBHARAT","CUMMINSIND","CROMPTON","COROMANDEL","CUB",
           "CHOLAFIN","CHOLAHLDNG","CENTRALBK","CASTROLIND","CANBK","CRISIL","CESC",
           "BBTC","BLUEDART","BHEL","BHARATFORG","BEL","BAYERCROP","BATAINDIA",
           "BANKINDIA","BALKRISIND","ATUL","ASTRAL","APOLLOTYRE","APOLLOHOSP",
           "AMARAJABAT","ALKEM","APLLTD","AJANTPHARM","ABFRL","ABCAPITAL","ADANIPOWER",
           "ADANIGREEN","ADANIGAS","ABBOTINDIA","AAVAS","AARTIIND","AUBANK","AIAENG","3MINDIA"]

if __name__ == '__main__':
    display_interface()
