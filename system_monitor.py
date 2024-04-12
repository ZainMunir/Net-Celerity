    #!/home/user/miniconda3/bin/python3
    import os
    import sys
    import time
    import glob
    import psutil

    # Function to read disk I/O stats from /proc/diskstats
    def read_diskstats():
        diskstats = {}
        with open('/proc/diskstats', 'r') as f:
            for line in f:
                fields = line.split()
                if len(fields) >= 14:
                    device = fields[2]
                    reads_completed = int(fields[3])
                    reads_merged = int(fields[4])
                    sectors_read = int(fields[5])
                    read_time = int(fields[6])
                    writes_completed = int(fields[7])
                    writes_merged = int(fields[8])
                    sectors_written = int(fields[9])
                    write_time = int(fields[10])
                    io_in_progress = int(fields[11])
                    io_time = int(fields[12])
                    weighted_io_time = int(fields[13])
                    diskstats[device] = {
                        'reads_completed': reads_completed,
                        'reads_merged': reads_merged,
                        'sectors_read': sectors_read,
                        'read_time': read_time,
                        'writes_completed': writes_completed,
                        'writes_merged': writes_merged,
                        'sectors_written': sectors_written,
                        'write_time': write_time,
                        'io_in_progress': io_in_progress,
                        'io_time': io_time,
                        'weighted_io_time': weighted_io_time
                    }
        return diskstats

    # Function to calculate disk I/O statistics
    def calculate_disk_io_counters(prev_stats, curr_stats):
        disk_counters = {}
        for device, curr_data in curr_stats.items():
            prev_data = prev_stats.get(device, {})
            if prev_data:
                reads_completed = curr_data['reads_completed'] - prev_data.get('reads_completed', 0)
                writes_completed = curr_data['writes_completed'] - prev_data.get('writes_completed', 0)
                disk_counters[device] = {
                    'reads_completed': reads_completed,
                    'writes_completed': writes_completed
                }
        return disk_counters

    # Function to collect system statistics
    def collect_system_stats(pid):
        p = psutil.Process(pid)
        sys_counters = {}
        
        sys_counters['timestamp'] = time.time() * 1000
        
        # Get process CPU times
        cpu_times = p.cpu_times()
        for name, value in cpu_times._asdict().items():
            sys_counters[f'proc.cpu.{name}'] = value
        
        # Get process memory info
        mem_info = p.memory_info()
        sys_counters['proc.memory.rss'] = mem_info.rss
        sys_counters['proc.memory.vms'] = mem_info.vms
        
        # Get process memory percent
        sys_counters['proc.memory.percent'] = p.memory_percent()
        
        # Get process disk I/O counters
        diskstats_prev = read_diskstats()
        time.sleep(1)
        diskstats_curr = read_diskstats()
        disk_io_counters = calculate_disk_io_counters(diskstats_prev, diskstats_curr)
        for device, counters in disk_io_counters.items():
            for name, value in counters.items():
                sys_counters[f'proc.disk.{device}.{name}'] = value
        
        return sys_counters

    # Function to write system stats to a log file
    def write_to_logfile(logfile, stats):
        with open(logfile, 'a') as f:
            timestamp = stats['timestamp']
            del stats['timestamp']
            stats_list = [f"{key}={value}" for key, value in stats.items()]
            log_entry = f"{int(timestamp)}\t" + '\t'.join(stats_list) + os.linesep
            f.write(log_entry)

    def get_next_logfile_number(folder_path):
        files = glob.glob(os.path.join(folder_path, 'system_log_*.log'))
        if not files:
            return 1
        else:
            latest_logfile = max(files, key=os.path.getctime)
            latest_number = int(latest_logfile.split('_')[-1].split('.')[0])
            return latest_number + 1

    if __name__ == "__main__":
        if len(sys.argv) < 2:
            print("Usage: python3 system_monitor.py <pid>")
            sys.exit(1)

        pid = int(sys.argv[1])

        system_logs_folder = "./benchmark/system_logs"
        if not os.path.exists(system_logs_folder):
            os.makedirs(system_logs_folder)

        next_logfile_number = get_next_logfile_number(system_logs_folder)
        logfile = os.path.join(system_logs_folder, f"system_log_{next_logfile_number}.log")

        with open(logfile, 'w') as f:
            f.write("timestamp\t")  # Writing header
        
        while True:
            sys_stats = collect_system_stats(pid)
            write_to_logfile(logfile, sys_stats)
            time.sleep(1)
