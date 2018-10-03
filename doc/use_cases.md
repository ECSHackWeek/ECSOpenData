# Use cases (incomplete):
Some prior art for example: https://github.com/ECSHackDay/MetaData_RDE/blob/master/RDEtest_100mV.yaml

* Upload a data set
  * Metadata required:
    * Data DOI
    * Reference
      * Authors
      * Paper
      * DOI
      * Journal
      * Year
    * Experiment class
      * Battery Cycling
        * Instrument (Arbin/MACCOR/etc.)
        * Something about chemistry/materials used
        * Commercial or research
  * Auto parse upload and show user extracted columns (confirm type and units)
  * Data cleaning / preprocessing / standardization
* Download a data set
  * From data set landing page?
  * In bulk? E.g. all of some type - displayed files, as they are sorted/filtered, have a checkbox “download,” have a button for “Select all displayed.”  Sort of like a “shopping cart.”  As data sets are selected, they are visualized.  Can click on a legend entry in the visualization to “deselect it.”
  * Standardize units? Give flexibility but match all of the units
  * Download will include a citation manager file containing references
  * Choose format of data that is being downloaded (.xlsx, .txt, .csv)
  * Download comes as a tarball that includes both the data table and the metadata (in a yaml file, for instance).  We give the user a reader tool for importing this into python.
* Search and filter for data sets
  * Fields available for searching / filtering:
  * Experiment class
    * Reference information including Authors, Papers, DOI
* Preview data
* Use of data metrics - upvote or something 
  * ECS best data award, badges, etc. 
  * Incentive to put good metadata in 


### Flask App Deliverables:
* Base app
  * Table / filters
  * Preview / cross-selection
  * Pop-up window for adding metadata
