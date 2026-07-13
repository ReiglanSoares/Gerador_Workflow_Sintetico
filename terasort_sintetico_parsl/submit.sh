#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH -p sequana_cpu_bigmem
#SBATCH --job-name=TeraSortSynthetic
#SBATCH --time=01:30:00
#SBATCH -e slurm-%j.err
#SBATCH -o slurm-%j.out

module load anaconda3/2024.02_sequana
eval "$(conda shell.bash hook)"

CONDA_ENV="/scratch/<usuario>/RNA-seq/conda_envs/parsl_env/"
conda activate "${CONDA_ENV}"

export PATH=/usr/bin:$PATH

PROJECT_DIR="/scratch/usuario/parsl-pattern-workflow-builder"
APP_DIR="${PROJECT_DIR}"
MAIN_SCRIPT="${APP_DIR}/main_terasort.py"

export PYTHONPATH="${PROJECT_DIR}:${APP_DIR}:${PYTHONPATH}"

cd "${APP_DIR}"

python "${MAIN_SCRIPT}" \
  --files 256 \
  --buckets 256 \
  --filter-time 3.04 \
  --sort-time 65.11 \
  --verify-time 10.04 \
  --finalize-time 0.04 \
  --time-scale 1.00 \
  --export-pdf \
  --monitor \
  --work-mode cpu \
  --onslurm
