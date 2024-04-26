# <span style="font-width:bold; font-size: 3rem; color:#2656a3;">**BDS MODULE 4 - DATA ENGINEERING AND MACHINE LEARNING OPERATIONS IN BUSINESS (MLOPs)** </span> <span style="font-width:bold; font-size: 3rem; color:#333;">- EXAM ASSIGMENT</span>
Report file elaborating on the process

# Topic title: Electricity Price Predicter for Denmark DK1 
## Business Problem
In recent times, energy prices have experienced a notable surge, prompting consumers and businesses alike to scrutinize their energy consumption patterns more closely than ever before. This surge in energy prices has not only heightened awareness regarding energy usage but has also sparked a renewed interest in identifying the optimal times for energy consumption. As consumers seek to navigate this landscape of rising energy costs, understanding when the best times are for utilizing energy becomes paramount. By pinpointing these optimal periods, individuals and organizations can strategically adjust their energy usage patterns to minimize costs while maximizing efficiency.

### Objectives
The objective is to build a prediction system that predicts the electricity prices in Denmark (area DK1) based on weather conditions, previous prices, and the Danish holidays. This will end up in an frontend application there ultimately can help the user decide when is the best time to charge the electric vehicle or have production running - leading to potential cost savings or profit maximization. 
The application can be relevent both individual client and in larger business perspective.  

# Data Pipeline 

    mangler billede 

## Feature Backfill
The notebook is divided into the following sections:
1. Loading data and process features
2. Connecting to Hopsworks Feature Store
3. Creating feature groups and uploading them to the feature store

**The data used comes from different sources:**

- Electricity prices in Denmark on hourly basis per day from [Energinet](https://www.energidataservice.dk).
- > Historical electricity prices for area DK1 starting from January 1, 2022, up until present day of yesterday. 

- Different meteorological observations based on Aalborg Denmark from [Open Meteo](https://www.open-meteo.com). 
- > Historical weather measurements based on the location of Aalborg, Denmark starting from January 1, 2022, up until present day of yesterday. 

- Danish calendar that categorizes dates into types based on whether it is a weekday or not. This files is made manually by the group. 
- > The calendar data stretches from 2022-01-01 until 2024-12-31.

- Forecast Renewable Energy next day from [Energinet](https://www.energidataservice.dk). 
- > Historical forecast of renewable energy data for area DK1 from January 1, 2022, up until present day of yesterday.  

Creating feature groups for the four datasets and uploading them to the Feature Store that have been connected in Hopsworks.

## Feature Pipeline
The notebook is divided into the following sections:
1. Parsing new data of today of hourly electricity prices and forecast weather measurements
2. Inserting the new data into the Feature Store.

Same API calls for the respective datasets as in Feature Backfill, just changing the historical setting to `false` so the fetched data is from real time of today.

Uploading the new data to the feature groups created previously in Feature Backfill.

## Training Pipeline
This notebook is divided into the following sections:
1. Feature selection.
2. Feature transformations.
3. Training datasets creation - splitting into train, validation and test sets.
4. Loading the training data.
5. Training the model.
6. Register the model to Hopsworks Model Registry.

## Inference Pipeline
This notebook is divided into the following sections:
1. Loading batch data.
2. Predicting using the model from Model Registry.

