#!/bin/bash

#SBATCH --job-name=spock_toi_5126
#SBATCH --array=0-9 # Request N jobs with IDs equal to 0, ..., N
#SBATCH -t 2-00:00  # Request runtime of 2 hours DD-HH:MM
#SBATCH -C centos7  # Request only Centos7 nodes
#SBATCH -p sched_mit_mki # Run on sched_engaging_default partition To run on MKI partition: sched_mit_mki
#SBATCH --mem-per-cpu=500  # Request 50MB of memory per CPU
#SBATCH -o spockarr_%j.txt   # Redirect output to output_JOBID_TASKID.txt
#SBATCH -e spockerror_%j.txt  # Redirect errors to error_JOBID_TASKID.txt
#SBATCH --mail-type=BEGIN,END  # Mail when job starts and ends
#SBATCH --mail-user=ofoo@mit.edu # Email recipient

## list of integers
declare -a arr=(1  2  3  4  5  6  7  8  9  10)

## load modules
module add anaconda3/2021.11

## install rebound
pip install --user rebound

## move to directory of this batch submit file
# cd /home/ofoo/v${arr[$SLURM_ARRAY_TASK_ID]}

## execute code 
python toi_5126_spock_extra_planet.py $SLURM_ARRAY_TASK_ID
