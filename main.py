
# You should not modify this part.
from datetime import datetime
import pandas as pd
from datetime import timedelta


def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()



def Calculation(path,parameter1,parameter2):
    df = pd.read_csv(path)
    time_dictionary = {}    #時間字典
    date_dictionary = {}    #日期字典
    for index,data in df.iterrows():
        min_datetime = pd.to_datetime(data[parameter1])
        time = datetime.time(min_datetime).strftime("%H:%M:%S")
        date = datetime.date(min_datetime).strftime("%Y-%m-%d")
        if time not in time_dictionary:
            time_dictionary[time] = float(data[parameter2])
        else:
            time_dictionary[time] += float(data[parameter2])
            time_dictionary[time] = round(time_dictionary[time],3)
        if date not in date_dictionary:
            date_dictionary[date] = 0
            
    for key in time_dictionary:
        time_dictionary[key] /=len(date_dictionary)
    return list(date_dictionary)[-1],time_dictionary

def demand(consumption,generation):
    for i in consumption:
        consumption[i]-=generation[i]
        consumption[i] = round(consumption[i],2)
    
    return consumption

def output_data(date,dict):
    date = (pd.to_datetime(date) +timedelta(days=1)).strftime("%Y-%m-%d")
    data = []
    for element in dict:
        if dict[element]>0:
            data.append([date+" "+element,"sell", 3, 1])
    return data 
            
def output(path, data):
    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    args = config()
    last_date,generation_dict = Calculation(args.generation,"time","generation")
    last_date,consumption_dict = Calculation(args.consumption,"time","consumption")
    demand_dict = demand(consumption_dict,generation_dict)

    data = output_data(last_date,demand_dict)
    output(args.output, data)
