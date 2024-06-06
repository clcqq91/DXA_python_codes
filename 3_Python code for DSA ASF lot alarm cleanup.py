# Phython code for DSA alarm cleanup
# Author: Longchao
# Date: 3/1/2023

if __name__ == "__main__":
    
    # File_path = r"\\cdATSHFS.intel.com\CDATAnalysis$\MAOATM\Longchao\DSA Full Log"
    File_path = r"\\t7filer04\ToolLog\Logs\A48\DSA"
    # File_path = r"C:\Users\longchao\OneDrive - Intel Corporation\Desktop\DSA_Script\DSA Log\TGB"#Logfile location
    # Output_CSV_path=r"C:\Users\longchao\OneDrive - Intel Corporation\Desktop\DSA_Script\DSA_Log.csv" #Output file location
    Output_CSV_path=r"\\cdATSHFS.intel.com\CDATAnalysis$\MAOATM\Longchao\DIA_clean_PBI_report\DSA_ASF_alarmclean_log.csv"
    import os
    from datetime import datetime, timedelta
    all_toolentity = []
    all_logfiles = []
    for ( roots, dirs, files ) in os.walk (File_path):
        for file in files:
            if file.endswith('.xml'):
                continue
            if os.path.basename(roots)[0:3] == 'ASF':
                all_toolentity.append(os.path.basename(roots))
                all_logfiles.append(os.path.join(roots,file))
   
    import re
    DSA_dooropen_close_loglist = []
    for i,file in enumerate(all_logfiles):
        with open(file,'r') as f:
            # if (datetime.now() - datetime.fromtimestamp(os.stat(file).st_ctime)).days > 3: if file date over 3 then ignore.
            #     continue
            lines=f.readlines()
            for line in lines: # Get aligned door open and close log with key word and date.
                if re.match('\d{2}:\d{2}:\d{2}.\d{4} ACLConveyor.cpp\(\d{5}\) ClearErr called.',line):#ASF alarm
                    # print(line)
                    LogDate=datetime.strftime(datetime.fromtimestamp(os.stat(file).st_ctime).replace(hour=int(line[line.find('[')+1:line.find('[')+3]),minute=int(line[line.find('[')+4:line.find('[')+6]),second=int(line[line.find('[')+7:line.find('[')+9]),microsecond=0),'%Y-%m-%d %H:%M:%S')
                    DSA_dooropen_close_loglist.append([all_toolentity[i],LogDate,line[line.find('ClearErr called'):].strip()])
                if re.match('\d{2}:\d{2}:\d{2}.\d{4} AclPlusDrv.cpp\(\d{5}\) Door',line):#ASF door open and close
                    # print(line)
                    LogDate=datetime.strftime(datetime.fromtimestamp(os.stat(file).st_ctime).replace(hour=int(line[line.find('[')+1:line.find('[')+3]),minute=int(line[line.find('[')+4:line.find('[')+6]),second=int(line[line.find('[')+7:line.find('[')+9]),microsecond=0),'%Y-%m-%d %H:%M:%S')
                    DSA_dooropen_close_loglist.append([all_toolentity[i],LogDate,line[line.find('Door'):].strip()])                                                                                             
                                                                                                                                        
    column_name = ('entity','logdate','log_event') #Give output CSV file.
    with open(Output_CSV_path,'w') as f:
        f.writelines(','.join(column_name))
        for i in DSA_dooropen_close_loglist:
            f.writelines('\n')
            f.writelines(','.join(i))