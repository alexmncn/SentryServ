"""System funct."""
import subprocess


# Execute script/command
def execute_command(command, use_shell=True):
    try:
        output = subprocess.run(command, shell=use_shell, text=True, capture_output=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output


def get_ram_usage():
    command = ['free', '-m']
    
    # Execute the 'free -m' command and capture the output
    output = execute_command(command)

    # Get output lines
    lines = output.stdout.split('\n')

    # Iterate through lines and extract CPU usage percentages
    for line in lines:
        # Split the line into columns
        columns = line.split()
        # Check if there are columns and if the first column is 'Mem:'
        if len(columns) > 0 and columns[0] == 'Mem:':
            ram_usage = int(columns[1]) - int(columns[6])

    return ram_usage


# Execute the command and get the total CPU usage
def get_cpu_usage():
    # Execute the 'sar -u' command and capture the output
    command = ['sar', '-u', '1', '1']
    output = execute_command(command, shell=False)

    # Get the output lines
    lines = output.stdout.split('\n')

    # Initialize a list to store CPU usage percentages
    cpu_percentages = []

    # Iterate through the lines and extract CPU usage percentages
    for line in lines:
        # Split the line into columns
        columns = line.split()
        # Check if there are columns and if the first column is 'all'
        if len(columns) > 0 and columns[1] == 'all':
            
            for column in columns[2:7]:
                # Get the CPU usage percentage and convert it to float
                cpu_percentage = float(column)
                # Append the percentage to the list
                cpu_percentages.append(cpu_percentage)

    # Sum up the CPU usage percentages
    total_cpu_usage = sum(cpu_percentages)

    # Return the total CPU usage1
    return total_cpu_usage

# Execute the command and get the cpu temp
def get_cpu_temp():
    command = 'cat /sys/class/thermal/thermal_zone0/temp'
    result = execute_command(command)
    temp = int(float(result.stdout)/1000)
    return temp
