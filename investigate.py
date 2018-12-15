"""Script to ease ivestigation on a huge list of hosts
Author : JSIjerry
Operating Systems Supported : Linux/Unix based systems and Windows
"""


import os,subprocess,re,itertools,platform,sys,socket,xlsxwriter
# all_output=sys.stdout
# f=open('ping_script_log.txt','w')
# sys.stdout=f

def find_os():
    global operating_system
    current_platform=platform.platform()
    if current_platform.startswith("Linux"):
        operating_system= "linux"
    elif current_platform.startswith("Windows"):
        operating_system= "windows"
    else:
        print("The support for {} has not yet been added. If you'd like this feature, please contact Jerry".format(current_platform))
        exit
    print("Python is running on {} ".format(current_platform))
    print("The {} command set will be used".format(operating_system))
    return operating_system

def ping_servers():
    try:
        input_file = open((os.path.join(os.getcwd(), 'ping_list_test.txt')),'r');
        workbook = xlsxwriter.Workbook('investigation_results.xlsx')
        script_logs = workbook.add_worksheet('logs')
        results = workbook.add_worksheet('results')
        row = 0
        col = 0
        list = []
        servers=input_file.readlines()
        input_file.close()
        print("The file being used is {} ".format(input_file))
        print('\n', "Running Ping on the servers" , '\n')
        print("The {} command set will be used".format(operating_system))
        number_of_servers = file_len('ping_list_test.txt')
        #code for table
        formatted_results = workbook.add_worksheet('result_table')

        #
        for each_host in servers:
                if str(each_host):
                    with open('ping_script_result.txt','a') as result:
                        print('====================================================================================',file=result)
                        perform_ping(each_host)
                        ip_address=find_the_ip(each_host)
                        fqdn=find_fqdn(each_host)
                        #data = [[str.strip(str(each_host))],[str.strip(str(ip_address))],[str.strip(str(response))],[str.strip(fqdn)]]
                        data = [str.strip(str(each_host)),str.strip(str(ip_address)),str.strip(str(response)),str.strip(fqdn)]
                        print(data)
                        list.append(data)
                        with open('ping_script_log.txt','a') as log:	
                            print("The Response from {} was {} ".format(each_host,response),file=log)
                            print("The Response from {} was {} . Its IP addess is {} . Its FQDN is {} ".format(each_host,response,ip_address,fqdn),file=log)
                            script_logs.write(row,col,each_host)
                            script_logs.write(row,col+1,response)
                            script_logs.write(row,col+2,ip_address)
                            script_logs.write(row,col+3,fqdn)
                        if response==0:	
                            print("The server {} is online. Its IP addess is {} . Its FQDN is {} ".format(each_host,ip_address,fqdn),file=result)
                            results.write(row,col,each_host)
                            results.write(row,col+1,"The Server is pinging")
                            results.write(row,col+2,ip_address)
                            results.write(row,col+3,fqdn)                    
                            row += 1
                        else:
                            print("The server {} seems to be offline. Its IP addess is {} . Its FQDN is {} ".format(each_host,ip_address,fqdn),file=result)
                            results.write(row,col,each_host)
                            results.write(row,col+1,"The Server is not pinging")
                            results.write(row,col+2,ip_address)
                            results.write(row,col+3,fqdn)
                            row += 1
        formatted_results.add_table('A1:D{}'.format(number_of_servers+1),{'data': list,'columns': [{'header': 'Value from Input file'},{'header': 'IP Address'},{'header': 'Response Received'},{'header': 'FQDN'}]})
        workbook.close()

    except FileNotFoundError:
        print("The input file does exist. Please place the file in the same directory as the script.")

def find_the_ip(ip):
    if(len(str(re.search('[a-zA-Z]',ip))))==4:
        return ip
    else:
        try:
            print('\n')
            print('Trying to find the IP address of {}'.format(ip))
            return socket.gethostbyname(ip)
        except socket.error:
            pass

def find_fqdn(host):
    print('Trying to find the FQDN of {}'.format(host))
    return socket.getfqdn(host)



def perform_ping(a_host):
    global response
    if operating_system=="windows":
        #response=os.system('ping -a -n 2 {}'.format(a_host))
        # The command below suppresses the command prompt from popping up with every execution
        response=subprocess.call('ping -a -n 2 {}'.format(a_host), shell=True)
    elif operating_system=="linux":
        response=os.system('ping -c 2 {}'.format(a_host))
        return response


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    #print('The file has {} servers'.format(i+1))
    return i + 1

# ~ sys.stdout=all_output
# ~ f.close()
find_os()
ping_servers()
#file_len('ping_list_test.txt')
#print(find_the_ip("www.sante-sports.gouv.fr"))
#print(find_fqdn("8.8.8.8"))
