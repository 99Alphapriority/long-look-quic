
import sys, os, random, time

def bandwitdh_oscillator(pipe1, pipe2, delay, baseBW, varBW, sleep):

    while True:
        # build command
        dummyCmd1 = 'sudo ipfw pipe {} config '.format(pipe1)
        dummyCmd2 = 'sudo ipfw pipe {} config '.format(pipe2)

        if delay:
            dummyCmd1 += 'delay {}ms '.format(delay)
            dummyCmd2 += 'delay {}ms '.format(delay)


        bw = random.randrange(baseBW, varBW)

        if bw:
            dummyCmd1 += 'bw {}Mbit/s '.format(bw)
            dummyCmd2 += 'bw {}Mbit/s '.format(bw) 

        print("{} && {}".format(dummyCmd1, dummyCmd2))  
        os.system("{} && {}".format(dummyCmd1, dummyCmd2))  
        time.sleep(sleep)

if __name__ == '__main__':

    if len(sys.argv) != 7:
        print("Usage: ", sys.argv[0], " <pipe1> <pipe2> <delay> <baseBW> <varBW> <sleep>")
        exit(1)
    else:
        pipe1, pipe2 = sys.argv[1], sys.argv[2]
        delay = int(sys.argv[3])
        baseBW, varBW = int(sys.argv[4]), int(sys.argv[5])
        sleep = int(sys.argv[6])

    bandwitdh_oscillator(pipe1, pipe2, delay, baseBW, varBW, sleep)
    
