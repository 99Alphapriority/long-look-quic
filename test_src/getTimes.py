
import json

obj_names = [ '5k', '10k', '100k', '200k', '500k', '1mb' ]

setting = "100_112_0/"
cases = ["https", "quic"]

print("Setting :", setting)
for obj in obj_names:
    print("Object :", obj)
    for case in cases:
        time = 0
        for expNo in range(1,11):
            file_name = "../data/results/" + setting + obj + "/resultsDir/"+case+"_"+str(expNo)+".har"
            try:
                with open( file_name , 'r') as f:
                    j = json.load(f)
                    # print('\t\t', j['log']['entries'][0]['time'])
                    total_t = j['log']['entries'][0]['time']
                    dns_t = j['log']['entries'][0]['timings']['dns']
                    time += total_t - dns_t
            except:
                print("Failed ", )
        total = time / 10
        print(str(case), ": ", total)
    print("")
