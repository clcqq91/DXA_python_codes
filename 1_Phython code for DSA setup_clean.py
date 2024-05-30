# Phython code for DSA log files 
# Author: Longchao
# Date: 12/26/2023

if __name__ == "__main__":
    
    # File_path = r"\\cdATSHFS.intel.com\CDATAnalysis$\MAOATM\Longchao\DSA Full Log"
    # File_path = r"\\cdATSHFS.intel.com\CDATAnalysis$\MAOATM\Longchao\ASF Log"
    File_path = r"\\t7filer04\ToolLog\Logs\A48\DSA"
    # File_path = r"C:\Users\longchao\OneDrive - Intel Corporation\Desktop\DSA_Script\DSA Log\TGB"#Logfile location
    # Output_CSV_path=r"C:\Users\longchao\OneDrive - Intel Corporation\Desktop\DSA_Script\DSA_Log.csv" #Output file location
    ASF_CSV_path=r"\\cdATSHFS.intel.com\CDATAnalysis$\MAOATM\Longchao\DSA_Clean_compliance\ASF_LogWindow.csv"
    Clean_record_CSV_path=r"\\cdATSHFS.intel.com\CDATAnalysis$\MAOATM\Longchao\DSA_Clean_compliance\DSA_cleanLog.csv"
    import os
    from datetime import datetime, timedelta
    ASF_toolentity = [] 
    ASF_logfiles = []
    all_toolentity = []
    all_logfiles = []
    recordday = 7 
    for (roots, dirs, files ) in os.walk (File_path):
        for file in files:
            if os.path.basename(roots)[0:3] == 'ASF': # Get ASF window
                if file.endswith('.log'):
                    ASF_toolentity.append(os.path.basename(roots))
                    ASF_logfiles.append(os.path.join(roots,file))
            if file.endswith('.xml'):
                continue
            if os.path.basename(roots)[0:3] == 'ASF' or os.path.basename(roots)[0:3] == 'LPP' or os.path.basename(roots)[0:3] == 'TGB':
                all_toolentity.append(os.path.basename(roots))
                all_logfiles.append(os.path.join(roots,file))
    import re
    ASF_SetupWindow = []
    for i,file in enumerate(ASF_logfiles): # RE for ASF setup window
        with open(file,'r') as f:
            if (datetime.now() - datetime.fromtimestamp(os.stat(file).st_mtime)).days > recordday:
                continue
            lines=f.readlines()
            for line in lines: # Get aligned ASF setup log with key word and date.
                if re.match('\d{4}-\d{2}-\d{2},\d{2}:\d{2}:\d{2}.\d{3},Prompted Setup \(Script\) Started',line) or re.match('\d{4}-\d{2}-\d{2},\d{2}:\d{2}:\d{2}.\d{3},Prompted Setup Finished',line):#ASF              
                    ASF_SetupWindow.append([ASF_toolentity[i],line[0:10]+' '+line[11:19],line[line.find('Prompted Setup'):].strip()])

    DSA_dooropen_close_loglist = []
    for i,file in enumerate(all_logfiles): # RE for open close door
        with open(file,'r',encoding='UTF-8',errors='ignore') as f:
            if (datetime.now() - datetime.fromtimestamp(os.stat(file).st_mtime)).days > recordday:
                continue
            lines=f.readlines()
            for line in lines: # Get aligned door open and close log with key word and date.
                if re.match('\d{2}:\d{2}:\d{2}.\d{4} AclPlusDrv.cpp\(\d{5}\) Door',line):#ASF 
                    LogDate=datetime.strftime(datetime.fromtimestamp(os.stat(file).st_mtime).replace(hour=int(line[line.find('[')+1:line.find('[')+3]),minute=int(line[line.find('[')+4:line.find('[')+6]),second=int(line[line.find('[')+7:line.find('[')+9]),microsecond=0),'%Y-%m-%d %H:%M:%S')
                    DSA_dooropen_close_loglist.append([all_toolentity[i],LogDate,line[line.find('Door'):].strip()])
                if re.match('ActionServer\d{1} \[\d{2}:\d{2}:\d{2},\d{3}\]:  start function for cover',line): #LPP
                    LogDate=datetime.strftime(datetime.fromtimestamp(os.stat(file).st_mtime).replace(hour=int(line[line.find('[')+1:line.find('[')+3]),minute=int(line[line.find('[')+4:line.find('[')+6]),second=int(line[line.find('[')+7:line.find('[')+9]),microsecond=0),'%Y-%m-%d %H:%M:%S')
                    DSA_dooropen_close_loglist.append([all_toolentity[i],LogDate,line[line.find('cover'):].strip()])
                if re.match('tUnlockCover \[\d{2}:\d{2}:\d{2},\d{3}\]: mcbase.cpp:\d{4} \( \) Psu: Unlock door-switch',line) or re.match('tLockCover \[\d{2}:\d{2}:\d{2},\d{3}\]: mcbase.cpp:\d{4} \( \) Psu: Lock door-switch',line): #TGB
                    LogDate=datetime.strftime(datetime.fromtimestamp(os.stat(file).st_mtime).replace(hour=int(line[line.find('[')+1:line.find('[')+3]),minute=int(line[line.find('[')+4:line.find('[')+6]),second=int(line[line.find('[')+7:line.find('[')+9]),microsecond=0),'%Y-%m-%d %H:%M:%S')
                    DSA_dooropen_close_loglist.append([all_toolentity[i],LogDate,line[line.find('Psu:'):].strip()])    
    
    column_name = ('entity','logdate','log_event') #Give ASF CSV file.
    with open(ASF_CSV_path,'w') as f:
        f.writelines(','.join(column_name))
        for i in ASF_SetupWindow:
            f.writelines('\n')
            f.writelines(','.join(i))

    column_name = ('entity','logdate','log_event') #Give output CSV file.
    with open(Clean_record_CSV_path,'w') as f:
        f.writelines(','.join(column_name))
        for i in DSA_dooropen_close_loglist:
            f.writelines('\n')
            f.writelines(','.join(i))

#add comments for GIT test