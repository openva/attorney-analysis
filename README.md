# Attorney Analysis

An analysis of the disposition of criminal cases in which defendants lack representation.

## The Task
The task here is to use the data that drives the [VA Circuit Court Statewide Search](https://github.com/Code4HR/va-circuit-court-search) project to deanonymize [our case data](https://github.com/openva/attorney-analysis/tree/master/cases). Our case data is a list of criminal cases in which the accused, charged with a felony, was not represented by an attorney. But the case data does not include the name of the accused.

## The Data

Here's an example record (with header row):

FIPS | CASE_TYPE | ATTORNEY_TYPE | FILE_DATE | OFFENSE_CLASS_CODE | FINAL_DISP_DATE
---- | --------- | ------------- | --------- | ------------------ | ---------------
7 | F | N | 11/26/12 | O | 1/15/13

Here's what each field means:

* `FIPS`: This is the [FIPS code](http://www2.census.gov/geo/docs/reference/codes/files/st51_va_cou.txt) that identifies the locality in Virginia. In our example, `7` means Amelia County.
* `CASE_TYPE`: In theory, this can represent a range of offenses. In practice, in our data, it will always be `F`, meaning felony.
* `ATTORNEY_TYPE`: In theory, this can have a range of values. In practice, in our data, it will always be `N`, meaning that the accused has no attorney.
* `FILE_DATE`: The date that the case was taken up by the courts (or so it appears)—the start date. In `MM/DD/YY` format. In our example, it's November 26, 2012.
* `OFFENSE_CLASS_CODE`: The nature of the felony. In our example data, `O` means "other," but other possible values exist, such as numbers 1–6 for the class of the felony.
* `FINAL_DISP_DATE`: The date that the case was concluded by the court—the end date. In `MM/DD/YY` format. In our example, it's January 15, 2013.

## The Challenge

Use court data to find the case that matches these anonymized records. In practice, that means matching the locality (via `FIPS`), the type of case (a felony), that the accused was without an attorney (a `NULL` value in the court records), that the offense class was the same, and that the start and end dates are identical. That is likely to be enough data points that there won't be multiple possible matches.

## The Result

Matching up these records will make it possible for the ACLU of Virginia to determine whether criminal defendants in Virginia are being denied their constitutional right to counsel.
