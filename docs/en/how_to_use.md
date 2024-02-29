# How to Use

## Overview
This guide provides step-by-step instructions on how to use the Python scripts in the `PetaBencana.id_BulkDownloader` repository to download and process disaster data from the PetaBencana.id API.

## Prerequisites
- Ensure you have Python 3.x installed on your system.
- Install necessary Python libraries with `pip install -r requirements.txt`.

## Steps

1. **Setting Up Your Environment**
   - Clone the repository using `git clone https://github.com/your-username/PetaBencana.id_BulkDownloader.git`.
   - Navigate to the cloned repository folder.
   - Install the required Python packages: `pip install -r requirements.txt`.

2. **Configuring the Scripts**
   - Open the `config.json` file in the `src` directory.
   - Set the API key and other configuration parameters as needed.

3. **Running the Scripts**
   - Execute the main script to start the downloading process: `python Main.py`.
   - For specific tasks, run the corresponding script, e.g., `python Main_Combine_n_FlattenJSON.py`.

4. **Post-Processing**
   - After downloading, you may run `Main_Flatten_Json.py` to flatten the JSON structure.
   - Use `Main_Json_to_Geojson.py` to convert the data to GeoJSON format.

5. **Data Analysis**
   - With the data in the desired format, you can now proceed with your analysis using tools like QGIS, ArcGIS, or any other data analysis software that supports GeoJSON.

For more detailed information, refer to the individual script documentation within the `src` directory.

Thank you for using `PetaBencana.id_BulkDownloader`.
