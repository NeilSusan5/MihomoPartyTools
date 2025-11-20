#!/bin/bash

# Function to display system information
display_system_info() {
    echo "--- System Information ---"
    uname -a
    echo "--------------------------"
}

# Function to display CPU information
display_cpu_info() {
    echo "--- CPU Information ---"
    lscpu | grep "Model name:" | sed "s/Model name: *//"
    echo "-----------------------"
}

# Function to display memory information
display_memory_info() {
    echo "--- Memory Information ---"
    free -h | grep "Mem:" | awk "{print \$2}"
    echo "--------------------------"
}

# Function to display disk usage
display_disk_usage() {
    echo "--- Disk Usage ---"
    df -h
    echo "------------------"
}

# Function to display Docker information (newly added)
display_docker_info() {
    echo "--- Docker Information ---"
    if command -v docker &> /dev/null
    then
        docker info
    else
        echo "Docker is not installed."
    fi
    echo "--------------------------"
}

# Main script execution
echo "Gathering System Information..."
display_system_info
display_cpu_info
display_memory_info
display_disk_usage
display_docker_info # Call the new function
echo "Information gathering complete."
