Gets hospital bed availability for given city. Currently supported cities:

* `ahmedabad` ([source](https://ahna.org.in/covid19.html))
* `hyderabad` ([source](http://164.100.112.24/SpringMVC/Hospital_Beds_Statistic_Bulletin_citizen.html))
* `pune` ([source](https://www.divcommpunecovid.com/ccsbeddashboard/hsr))
* `vadodara` ([source](https://vmc.gov.in/Covid19VadodaraApp/Default.aspx))

#### Installation:

```shell script
pip3 install hydbedscraper
```

#### Usage

```python
from hydbedscraper.main import work

dataframe = work("name_of_city")
```

In your python project, import the `work` method and call it with the name of the city. It returns a pandas `DataFrame` object with tabulated data.
