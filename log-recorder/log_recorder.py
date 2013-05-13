#!/usr/bin/python

import sys, os, signal, time, re

def flush_output_buffer():
    urls = None
    try:
        urls = open(working_dir + 'urls.txt','r')
    except IOError, e:
        lines_processed = 0
        os.rename(working_dir + 'out.tmp',working_dir + 'urls.txt')
    if urls is not None:
        urls.close()


def process_log_inner(line,wrk_fd,lines_processed):
    try :
        url = line.split('"')[1].split(' ')[1]
        wrk_fd.write(url_prefix + url + '\n')
    except:
        pass
    lines_processed += 1
    if lines_processed > 1000:
        wrk_fd.close()
        flush_output_buffer()
        wrk_fd = open(working_dir + 'out.tmp','a')


def process_lines(log_file,seek):
    wrk_fd = open(working_dir + 'out.tmp','a')
    try:
        log_fd = open(log_file,'r')
    except IOError, e:
        return
    log_fd.seek(seek)
    lines_processed = 0
    [process_log_inner(line,wrk_fd,lines_processed) for line in log_fd.readlines()]
    wrk_fd.close()


def perform_log_processing():
    files = []
    for entry in os.listdir(log_dir):
        if('access' in entry and 'log' in entry and 'swp' not in entry):
            files.append((entry, os.path.getmtime(log_dir + entry), \
                os.path.getsize(log_dir + entry)))
    files.sort(key=lambda tup: tup[1])
    try:
        cur_log = open(working_dir + 'current_log.txt','r+')
    except:
        process_lines(log_dir + files[-1][0],0)
        cur_log = open(working_dir + 'current_log.txt','w')
        cur_log.write(files[-1][0] + '|' + str(files[-1][2]))
        return
    cur_file = cur_log.readline().split('|')
    process_lines(log_dir + cur_file[0],int(cur_file[1]))
    cur_log.seek(0)
    cur_log.truncate()
    if cur_file[0] != files[-1][0]:
        process_lines(log_dir + files[-1][0],0)
        cur_log.write(files[-1][0] + '|' + str(files[-1][2]))
    else:
        cur_log.write(cur_file[0] + '|' + str(os.path.getsize(log_dir + cur_file[0])))
    cur_log.close()


def main():
    global working_dir
    global log_dir
    global url_prefix
    working_dir = '/tmp/'
    if (len(sys.argv) > 1 and sys.argv[1] is not None):
        working_dir = sys.argv[1]
    log_dir = '/local/apache-logs/'
    if (len(sys.argv) > 2 and sys.argv[2] is not None):
        log_dir = sys.argv[2]
    url_prefix = 'http://www.default.com'
    if (len(sys.argv) > 3 and sys.argv[3] is not None):
        url_prefix = sys.argv[3]
    f = None
    try:
        f = open(working_dir + 'log_recorder.lock','r+')
        if len(f.readline()) > 0:
            sys.exit("Log Recorder is Already Running.. Exiting..")
    except IOError, e:
        pass
    if f is None:
        f = open(working_dir + 'log_recorder.lock','w')
    f.write(str(os.getpid()))
    f.close()
    while True:
        perform_log_processing()
        flush_output_buffer()
        time.sleep(10)


def kill_handler(signal, frame):
    os.remove(working_dir + 'log_recorder.lock')
    print("Exiting Cleanly..")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, kill_handler)
    signal.signal(signal.SIGINT, kill_handler)
    main()
