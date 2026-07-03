#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH -p sequana_cpu_dev
#SBATCH --job-name=WordCountSynthetic
#SBATCH --time=00:20:00
#SBATCH -e slurm-%j.err
#SBATCH -o slurm-%j.out

module load anaconda3/2024.02_sequana
eval "$(conda shell.bash hook)"

CONDA_ENV="/scratch/<usuario>/conda_envs/parsl_env/"
conda activate "${CONDA_ENV}"

export PATH=/usr/bin:$PATH

PROJECT_DIR="/scratch/<usuario>/parsl-pattern-workflow-builder"
APP_DIR="${PROJECT_DIR}"
MAIN_SCRIPT="${PROJECT_DIR}/main_WordCount.py"

export PYTHONPATH="${PROJECT_DIR}:${APP_DIR}:${PYTHONPATH}"

cd "${APP_DIR}"

python "${MAIN_SCRIPT}" \
  --files 4 \
  --buckets 4 \
  --wordcount-time 206.95 \
  --reduce-time 15.29 \
  --merge-time 886.03 \
  --time-scale 1.00 \
  --onslurm \
  --monitor \
  --export-pdf \
  --work-mode cpu
