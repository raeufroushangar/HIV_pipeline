# Configuration Files

This directory contains configuration files for the project.

1. `extracting_seq_within_pol_region.py`: Algorithm to extract the HIV-I pol-region within the query sequence.
   - Algorithm workflow summary:
   
   ![Workflow Summary](../figures/pol_region_finder_extractor.png)

---

2. `mafft_caller.py`: Python script to call the MAFFT alignment tool.
3. `db_caller.py`: Python script to interact with the database.
4. `mafft_mac_installer.py`: Python script to install MAFFT on macOS.
5. `db_data_uploader.py`: Python script to upload data to the database.
6. `db_tables_operations.py`: Python script to perform operations on database tables.
7. `multistate_character_cleaner.py`: Python script to clean multistate characters from sequences.
8. `muscle_mac_linux_installer.py`: Python script to install MUSCLE on macOS and Linux.
9. `end_characters_cleaner.py`: Python script to clean end characters from sequences.
10. `parallel_alignment_processor.py`: Python script to process alignments in parallel.
11. `file_reader.py`: Python script to read files.
12. `pol_region_coordinates_finder.py`: Python script to find coordinates in the pol region.
13. `hiv_subtyping_alignment_worker.py`: Python script for HIV subtyping alignment.
14. `qc.py`: Python script for quality control.
15. `hiv_typing_alignment_worker.py`: Python script for HIV typing alignment.
16. `similarity_calculator.py`: Python script to calculate similarity.
17. `stats_plotter.py`: Python script to plot statistics.
