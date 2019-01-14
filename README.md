# Occurrence aggregation example

This Python script aggregates biologging (machine) observations as a demonstration of a possible way to summarize such data before supplying it to GBIF.

The dataset used is [the example from the TDWG dwc-for-biologging group](https://github.com/tdwg/dwc-for-biologging/wiki/Terrestrial-mammal-GPS-and-ACC-data-from-Movebank), it's description from there is:

> This dataset is a subset of GPS and acceleration data from collared mammals described in [Mahoney and Young (2016)](https://doi.org/10.1111/2041-210X.12658) Uncovering behavioural states from animal activity and site fidelity patterns. Methods in Ecology and Evolution 8(2): 174–183. The data are stored on Movebank in the study ["Site fidelity in cougars and coyotes, Utah/Idaho USA (data from Mahoney et al. 2016)"](https://www.movebank.org/panel_embedded_movebank_webapp?gwt_fragment=page=studies,path=study193545363) and have been published in the Movebank Data Repository with DOI [10.5441/001/1.7d8301h2](https://doi.org/10.5441/001/1.7d8301h2).

## Usage

1. (Optional) Set up a Python virtual environment, so you can throw all this away later:
   `python3 -m venv cougars`
   `source cougars/bin/activate`

2. Install necessary Python modules
   `pip install -r requirements.txt`

3. Run the script:
   `python summarize.py`

4. Zip the result:
   `zip mahoney.zip meta.xml eml-Mahoney-data-DwC-A.xml event.txt occurrence.txt extendedmeasurementorfact.txt`

5. Send to GBIF!

The dataset is registered on GBIF's test environment as [Cougar and coyote GPS telemetry, Utah/Idaho USA (OBIS-ENV-DATA example)](https://www.gbif-uat.org/dataset/c8a94e02-54a2-4eed-a8bf-d5216bbe0cc9) (the test environment is reset occasionally, so the dataset may disappear).
