import re
from datetime import datetime


def getLogsFromFile(file_name):
    with open(file_name,"r") as log_file:
        list =[]
        for line in log_file:           
            list.append(line)
    return list


def logFilter(from_date,to_date,logListWidget):
    if from_date<to_date:
        filtered_logs = []

        date_pattern = r'(\w{3}\s\d{1,2})'  # pattern dla daty 'Dec 21'
        logs =[]
        
        for index in range(logListWidget.count()):
            logs.append(logListWidget.item(index).text())
        
        for log in logs:
            result_date = re.search(date_pattern, log)           
            log_date = datetime.strptime(result_date.group(0), '%b %d').date().replace(year=datetime.now().year)          
            if from_date <= log_date <= to_date:
                filtered_logs.append(log)
        return filtered_logs
    else:
        return -1

def getDetails(currRow):
    currLog = currRow.text()

    host_pattern = r'([A-Z])\w\w([A-Z])+'
    date_pattern = r'\b\w{3}\s\d{1,2}\b'  # pattern dla daty np 'Dec 21'
    time_pattern = r'\b\d{2}:\d{2}:\d{2}\b'  # pattern dla czasu np '23:45:28'
    pattern_ip = r'(?<=from\s)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' 
    result_ip = re.search(pattern_ip, currLog)
    
    PID_pattern = r'\s[a-z].+?]'
    result_date = re.match(date_pattern,currLog)
    result_time = re.search(time_pattern,currLog)
    result_host = re.search(host_pattern,currLog)
    result_PID = re.search(PID_pattern,currLog)
    
    if result_ip:     
        return result_date.group(0),result_time.group(0),result_host.group(0),result_PID.group(0)[1:],result_ip.group(0)
    
    else:      
        return result_date.group(0),result_time.group(0),result_host.group(0),result_PID.group(0)[1:],"Brak adresu ip"
    