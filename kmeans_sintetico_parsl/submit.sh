#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH -p sequana_cpu_bigmem
#SBATCH --job-name=KMeansSynthetic
#SBATCH --time=04:20:00
#SBATCH -e slurm-%j.err
#SBATCH -o slurm-%j.out

module load anaconda3/2024.02_sequana
eval "$(conda shell.bash hook)"

CONDA_ENV="/scratch/<usuario>/RNA-seq/conda_envs/parsl_env/"
conda activate "${CONDA_ENV}"

export PATH=/usr/bin:$PATH

PROJECT_DIR="/scratch/<usuario>/parsl-pattern-workflow-builder"
APP_DIR="${PROJECT_DIR}"
MAIN_SCRIPT="${APP_DIR}/main_kmeans.py"

export PYTHONPATH="${PROJECT_DIR}:${APP_DIR}:${PYTHONPATH}"

cd "${APP_DIR}"

python "${MAIN_SCRIPT}" \
  --fragments 1056 \
  --iterations 10 \
  --init-time 5.12 \
  --fragment-time 54.82 \
  --reduce-time 0.29 \
  --finalize-time 0.05 \
  --time-scale 1.00 \
  --monitor \
  --export-pdf \
  --work-mode cpu \
  --onslurm
