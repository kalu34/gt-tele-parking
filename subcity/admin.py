from django.contrib import admin

# Register your models here.

def sjf_scheduling(processes):
    processes.sort(key=lambda x: x[1])  # Sort by burst time
    completion_time = 0
    for process in processes:
        completion_time += process[1]
        print(f"Process {process[0]} completes at {completion_time}")

def srtf_scheduling(processes):
    remaining_time = {p[0]: p[1] for p in processes} #Dictionary to store the time remaining for each process
    completed = {}
    time = 0
    while any(remaining_time.values()):
      available_processes = [p for p in processes if p[1] <= time and p[0] not in completed]
      if available_processes:
        current_process = min(available_processes, key = lambda x: remaining_time[x[0]]) #Selecting the shortest remaining time process
        remaining_time[current_process[0]] -= 1
        time += 1
        if remaining_time[current_process[0]] == 0:
          completed[current_process[0]] = time
          print(f"Process {current_process[0]} completes at {time}")
      else:
        time += 1

# Example usage: (Process ID, Burst Time)
processes = [("P1", 6), ("P2", 8), ("P3", 7), ("P4", 3)]
print("SJF Scheduling:")
sjf_scheduling(processes.copy()) #Copy to avoid modifying original list for SRTF
print("\nSRTF Scheduling:")
srtf_scheduling(processes)
