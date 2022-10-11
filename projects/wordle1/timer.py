import sys
import datetime as dt
import time as t
def start_timer():
    start = t.time()
    while True:
        sys.stdout.write("\r")
        stop = t.time()-start
        sys.stdout.write('total time: '+t.strftime('%H:%M:%S', t.gmtime(stop))+'.'+str(round(stop, 3)).split('.')[1]+15*' ') 
        sys.stdout.flush()
        
        with open('times.txt', 'r') as file:
            if stop<5:
                continue
            if file.read()[-2]=='-':
                input('\nrun completed')
                #f.close()
                #print('\ntotal time:', t.strftime('%H:%M:%S', t.gmtime(stop))+'.'+str(round(stop, 3)).split('.')[1])
                exit()
    return None
if __name__ == "__main__":
    start_timer()
    
else:
    start_timer()

