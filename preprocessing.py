
import re
import pandas as pd
def preprocess(data):
    pattern=r'.*?-\s'
    messages=re.split(pattern, data)[1:]

    dates=re.findall(pattern, data)
    
    patternn='\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s\w+ -\s'

    parsed_dates=[]
    for string in dates:
        match = re.match(patternn, string)
        
        if match:
            datetime_message = match.group(0)
            parsed_dates.append(datetime_message)
        else:
            converted_string ='11/11/11, 11:11\u202fam - '
            parsed_dates.append( converted_string)

    df=pd.DataFrame({'user_message':messages, 'date_time':parsed_dates})
    
    # Remove non-breaking space characters from date strings
    cleaned_dates = [date.replace('\u202f', '') for date in df['date_time']]
    
    # Convert cleaned date strings to datetime objects
    datetime_objects = pd.to_datetime(cleaned_dates, format='%d/%m/%y, %I:%M%p - ')
    df['date_time']=datetime_objects
    
    users=[]
    messages=[]
    for message in df['user_message']:
      texts=re.split('([\w\W]+?):\s', message)
      if texts[1:]:
        users.append(texts[1])
        messages.append(texts[2])
      else:
        users.append('group_notification')
        messages.append(texts[0])
    
    df['user']=users
    df['message']=messages
    
    df.drop(columns=['user_message'], inplace=True)
    
    df['date']=df['date_time'].dt.date
    df['year']=df['date_time'].dt.year
    df['month_num']=df['date_time'].dt.month
    df['month']=df['date_time'].dt.month_name()
    df['day']=df['date_time'].dt.day
    df['day_name']=df['date_time'].dt.day_name()
    df['hour']=df['date_time'].dt.hour
    df['minute']=df['date_time'].dt.minute


    period=[]
    for hour in df[['day_name', 'hour']]['hour']:
      if hour==23:
        period.append(str(hour)+"-"+str("00"))
      elif hour==0:
        period.append(str('00')+"-"+str(hour+1))
      else:
        period.append(str(hour)+"-"+str(hour+1))

    df['period']=period
    
    to_remove = ['Give a brief overview of the idea approach and state your vision to tackle it.\nWorkflow diagram, Pictorial representation(optional)\n\n5) Solution of the problem', '🥇 *1st Prize', '🥈 *2nd Prize', '🥉 *3rd Prize']
    df = df.drop(df[df['user'].isin(to_remove)].index)

    return df