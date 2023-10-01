import pandas as pd
import re



# the function of this function is take the data and covert in into desired data frame with desired column
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}\s-\s'
    message = re.split(pattern,data)[1:] # it will give the data from patten onward
    dates = re.findall(pattern,data) # to get the rest of pattern
    df =pd.DataFrame({'user_message':message,'dates':dates})

    # convert message_date types
    df['dates']=pd.to_datetime(df['dates'], format='%m/%d/%y, %H:%M - ')

    df.rename(columns={'dates':'date'},inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:  # user name
                users.append(entry[1])
                messages.append(" ".join(entry[2:]))
            else:
                users.append('group_notification')
                messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date']=df['date'].dt.date
    df['year']=df['date'].dt.year # making a new colunm name year
    df['month_num'] = df['date'].dt.month
    df['month']=df['date'].dt.month_name() # separate the month name

    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+'-'+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['period']=period
    return df
