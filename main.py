import datetime
import Server.Server as Server

logfile = "logs/Commands/" + datetime.datetime.now().strftime("%d.%m.%Y") + ".log"
log = open(logfile, "a")

def main():
    log.write(datetime.datetime.now().strftime("%H:%M:%S") + ": Starting ...\n")
    log.flush()
    Server.start()
    log.write(datetime.datetime.now().strftime("%H:%M:%S") + ": Server started.\n")
    log.flush()



main()