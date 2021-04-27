Gets hospital bed availability for given city. Currently supported cities:

* `ahmedabad` ([source](https://ahna.org.in/covid19.html))
* `hyderabad` ([source](http://164.100.112.24/SpringMVC/Hospital_Beds_Statistic_Bulletin_citizen.html))
* `vadodara` ([source](https://vmc.gov.in/Covid19VadodaraApp/Default.aspx))

#### Installation:

```shell script
pip3 install hydbedscraper
```

#### Usage

```python
from hydbedscraper.main import work

hospital_type_to_dataframe = work("name_of_city")
for hospital_type, dataframe in hospital_type_to_dataframe.items():
    ...
```

In your python project, import the `work` method and call it with the name of the city. It returns a dictionary.

* Keys of the dictionary: Hospital types (e.g. "government", "private", etc.)
* Values of the dictionary: A `DataFrame` object from the `pandas` package containing information about hospitals. Contents of `DataFrame` vary from source-to-source, column information stored in first row.
