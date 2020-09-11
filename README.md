# Data and scripts for the paper
This repository contains the main data and scripts used in 'A First Look at Good First Issues on GitHub '



## dataset
The folder `dataset` contains the following files.

* project_attributes.csv
    *  It contains the data of 816 projects used in this study.
    *  `id` is the ghtorrent-bq.ght_2018_04_01.projects `id`
* gfi.csv
    *  It contains all the good first issues identified in this study.
    *  `id` is the ghtorrent-bq.ght_2018_04_01.issues `id`
    *  `issue_id` is the ghtorrent-bq.ght_2018_04_01.issues `issue_id`
* issue_character.csv
    *  It contains the issues used to compare the resolution process of good first issues and others (Section 5.1.1). 
* random_issue_manual_analysis.csv
    *  It contains the good first issues for manual analysis (Section 5.2.1).
* Results of Thematic Analysis.pdf
    *  It shows the thematic analysis results for RQ4 (Section 7.1.1).
* coding guide.pdf
    *  It shows the coding_guide for thematic analysis results for RQ4 (Section 7.1.1).

* Because the codes we obtained for extracting the problems of GFI mechanism are very similar, we do not provide the detail of this step (Section 6.1.2). 

## scripts
The folder `scripts` contains the following files.

* model
    *  This folder contains the scripts to bulid logstic regression model.
* key_information
    *  This folder contains the scripts to extract the key information of good first issue descriptions.
* get_issue_report
    *  Because ghtorrent dataset doesn't contain descriptions of issue reports, it used to download the issue reports from GitHub.
* process_report.py
    * It used to process the markdown style of issue reports to obtain the related fields.
* gfi_description_attributes.py
    * It used to get the attributes of good first issue descriptions.
* get_issue_label_time.py
    * It used to get the events of good first issues, i.e., who and when label the issue.
