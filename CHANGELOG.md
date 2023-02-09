# Changelog

## 0.4.2.1

### Changes

- Tkinter GUI.
- Use ydata_profiling (formerly pandas_profiling).
- Fixed bug in the data categorisation. Columns (observables) with mixed
  int and float values were rejected as bad columns. It was a bug.
- Fixed bug related to missing data values.
  Tests were preformed for pairs well-defined values and missing values.
  Now test are preformed only when are at least two rows with well-defined
  values for given columns.
- *Can* be frozen by pyinstaller. With a little help of a copy-paste magic.
  Not as a single file.

## 0.4.0.0

### Changes

- fixed p-value meaning.
- simplified, streamlined.
- unit tests via doctest and unittest.
- simplified i/o.
- frequency tables etc. moved from statquest_tests.
- statquest_tests.py should now contain only statistical tests,

### Restart

- A big restart of the project as a direct continuation (branch/fork) of *ProQuest*.
- Numbering will be continued, thus 0.4.0.0 instead 0.1.0.0.
- Project name has been renamed from *ProQuest* to *StatQuest*.
  The name reflects the change of the domain. *ProQuest* was
  dedicated to a very specific domain. *StatQuest* is planned
  to be usable more widely as a general tool.
- Files has been renamed.

## 0.3.2.2

- The last (and successful) version of *ProQuest* 
  written by Sławomir Marczyński.
