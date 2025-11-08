#show link: set text(fill: blue)
#show link: underline

/*
TODO
- Come up with list of questions
- write "derivation" script
  - detainers[entry date] - removals[departure date]

For meeting 11/5/25
- I noticed that in detainers we remove any columns with >75% missing data. In removals for example only 20% of the individuals are "removed" (deported) so it is expected that most of the data is missing. Want to confirm we aren't missing anything like that with a blanket remove >75%
- Do other data sets have repeat unique IDs? if so, we need to decide how to collapse them. What i did for removals was to combine them and create a new column with the count. I keep only the most recent deportation. and the num deportations is actually a useful thing.
*/

= Resources
- [Deportation Data Project](https://deportationdata.org/)
- [ICE data](https://deportationdata.org/data/ice.html)
- [ICE data Documentation](https://deportationdata.org/docs/ice.html#codebook)
- [ICE data Codebook](https://deportationdata.org/docs/ice/codebook.html): description of each table and their fields
- [Frequently Asked Questions](https://deportationdata.org/docs/ice.html#sec-faq)
- [A Close Look at ICE Arrest Data from the Deportation Data Project (Part 1)](https://austinkocher.substack.com/p/a-close-look-at-ice-arrest-data-from). Austin Kocher. Blog post background of the dataset

= Setup
- Download the 5 raw Excel files from https://deportationdata.org/data/ice.html
- Place them in a directory named ice_data in the root of this repository

= Data overview

== ENCOUNTERS

Records every time ICE Enforcement and Removal Operations encounters a person, i.e. considers whether to take enforcement action against a person.  This need not mean a physical encounter. Most notably, every time ICE processes a match between FBI book-in information (i.e. to a jail or prison) and ICE database information, that match is logged as an ICE encounter.  Generally, if an individual appears in the detainers or arrests table, that individual should appear in this table. An individual might appear in the removals or detentions tables without appearing in the encounters data if Customs and Border Protection initially encounters the person. This is both the largest and the sparsest of the tables, and in many cases, encounters lack a unique ID because the individual lacked an A number (A numbers are generally only given to people with immigrant visas or when they are processed for deportation proceedings).

Notes: 
- 1.2 million rows
- $~18%$ of rows are deported. Non-null values for 'Departed Date' indicates this
- 'Departed Date' and 'Departure Country' are non-null together
- 'Case Status' and 'Case Category' are non-null together
- 'Final Order Date' is a "subset" of 'Final Order Yes No'
- 'Departed Date' is a subset of 'Final Order Date' (maybe not tbd)

by "subset" I mean if the other columns value is non-null this one is too

= Examples of Bad Data

The unique ID `e324d5dceb0f735544c0757b983433458ef7b707` is the most common in the encounters dataset, appearing 45 times. In each occurence, the birthyear, citizenship, and gender are the same. However, the encounter criminality is inconsistent:

```txt
Encounter Criminality
2 Pending Criminal Charges      21
1 Convicted Criminal            12
3 Other Immigration Violator    12
```

This makes me have less faith in the validity of this column.

= Prediction questions