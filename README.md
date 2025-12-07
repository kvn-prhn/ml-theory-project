# Resources
- [Deportation Data Project](https://deportationdata.org/)
- [ICE data](https://deportationdata.org/data/ice.html)
- [ICE data Documentation](https://deportationdata.org/docs/ice.html#codebook)
- [ICE data Codebook](https://deportationdata.org/docs/ice/codebook.html): description of each table and their fields
- [Frequently Asked Questions](https://deportationdata.org/docs/ice.html#sec-faq)
- [A Close Look at ICE Arrest Data from the Deportation Data Project (Part 1)](https://austinkocher.substack.com/p/a-close-look-at-ice-arrest-data-from). Austin Kocher. Blog post background of the dataset

# Setup
- Download the 5 raw Excel files from https://deportationdata.org/data/ice.html
- Place them in a directory named ice_data in the root of this repository

# Repository Structure
Data structure
- `arrests_columns.py`
- `detainers_columns.py`
- `detentions_columns.py`
- `encounters_columns.py`
- `removals_columns.py`

Data cleaning
- `clean_arrests.py`
- `clean_detainers.py`
- `clean_detentions.py`
- `clean_encounters.py`
- `clean_removals.py`
- `clean_all.py`

Supervised classification:
- `encounters_decision_tree_train.py`
- `encounters_decision_tree_analyze.py`
- `encounters_random_forest_train.py`
- `encounters_random_forest_analyze.py`
- `encounters_logistic_regression_train.py`
- `encounters_logistic_regression_analyze.py`
- `notebooks/bag_knn_classify_deport_criminality.ipynb`

Supervised regression
- `subsequent_removal_train.py`
- `subsequent_removal_tree_analyze.py`
- `subsequent_removal_forest_analyze.py`
- `subsequent_removal_lasso_analyze.py`
- `subsequent_removal_grad_boost_analyze.py`

Unsupervised Learning
- `notebooks/rule_association_mining.ipynb`
- `notebooks/unsupervised.ipynb`

# Data overview

## ENCOUNTERS

Records every time ICE Enforcement and Removal Operations encounters a person, i.e. considers whether to take enforcement action against a person.  This need not mean a physical encounter. Most notably, every time ICE processes a match between FBI book-in information (i.e. to a jail or prison) and ICE database information, that match is logged as an ICE encounter.  Generally, if an individual appears in the detainers or arrests table, that individual should appear in this table. An individual might appear in the removals or detentions tables without appearing in the encounters data if Customs and Border Protection initially encounters the person. This is both the largest and the sparsest of the tables, and in many cases, encounters lack a unique ID because the individual lacked an A number (A numbers are generally only given to people with immigrant visas or when they are processed for deportation proceedings).

Notes: 
- 1.2 million rows
- $~18%$ of rows are deported. Non-null values for 'Departed Date' indicates this
- 'Departed Date' and 'Departure Country' are non-null together
- 'Case Status' and 'Case Category' are non-null together
- 'Final Order Date' is a "subset" of 'Final Order Yes No'
- 'Departed Date' is a subset of 'Final Order Date' (maybe not tbd)

by "subset" I mean if the other columns value is non-null this one is too

# Observations

- One strong predictor of whether an encounter leads to a deportation is the encounter date, and if that date is right before the end of the data collection period. i.e., they were encountered right before the last day of data collection.
- Trying to create a dummy variable for each of 100s of categorical varibles made training a basic decision tree incredibly slow.