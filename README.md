# Computational Pipeline for HIV Outbreak Monitoring

## Project Description
This pipeline runs natively on public health departments' network systems to predict HIV transmission and outbreak progression, guiding public health mitigation efforts.

### Pipeline Workflow Summary:
![Workflow Summary](pipline_workflow.png)
## Directory Structure
- `assets`: Contains description files of accepted data.
- `bin`: Contains database and external applications.
- `config`: Contains configuration files.
- `tests`: Contains test scripts.

## External Tools
- MAFFT version 7
- PostgreSQL 16.2

## System Requirements
- macOS 14.4.1 
- Python 3.9.6
- pip3 24
- *May work with similar versions.

**Installation Instructions:**

1. Clone the repository: `git clone https://github.com/MolEvolEpid/HIV_pipeline.git`
2. Change to the 'HIV_pipeline' directory: `cd HIV_pipeline`
3. Run setup.sh: `./setup.sh`
   - Jupyter Notebook will open, allowing you to execute different cells.
4. Run deactivate_env.sh: `./deactivate_env.sh`

*Note: Jupyter Notebook is used here to demonstrate user prompting for "data upload" and "header matching". Once the software is fully developed, all scripts in this repository should run natively, with no changes, on any operating system using Docker.*