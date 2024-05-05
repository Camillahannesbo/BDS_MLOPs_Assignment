# <span style="font-width:bold; font-size: 3rem; color:#2656a3;">**BDS MODULE 4 - DATA ENGINEERING AND MACHINE LEARNING OPERATIONS IN BUSINESS (MLOPs)** </span> <span style="font-width:bold; font-size: 3rem; color:#333;">- EXAM ASSIGMENT</span>
Report file elaborating on the process

# Topic title: Electricity Price Predicter for Denmark DK1 
## Business Problem
In recent times, energy prices have experienced a notable surge, prompting consumers and businesses alike to scrutinize their energy consumption patterns more closely than ever before. This surge in energy prices has not only heightened awareness regarding energy usage but has also sparked a renewed interest in identifying the optimal times for energy consumption. As consumers seek to navigate this landscape of rising energy costs, understanding when the best times are for utilizing energy becomes paramount. By pinpointing these optimal periods, individuals and organizations can strategically adjust their energy usage patterns to minimize costs while maximizing efficiency.

   > Mangler noget reference?

### Objectives
The objective is to build a prediction system that predicts the daily electricity prices per hour in Denmark (area DK1) based on weather conditions, previous prices, and the Danish calendar. This will end up in an frontend application there ultimately can help the user decide when is the best time to charge the electric vehicle or have production running - leading to potential cost savings or profit maximization. 
The application can be relevent for both individual client and in larger business perspective.  

# Data Pipeline 
The prediction system is built using several features, training, and inference pipelines. [Hopsworks](https://www.hopsworks.ai) is used as the platform to store features in the **Hopworks Feature Store** and save the trained model in **Hopworks Model Registry**. The overall architecture of the Electricity Pipeline is illustrated below. Inspiration is taken from [MLOPs Lecture 2](https://github.com/saoter/SDS24_MLOps_L1/blob/main//MLOps_Lecture_2_slides.pdf).

![electricity_pipeline.png](images/electricity_pipeline.png)

## Feature Backfill
Implemented in [notebooks/1_feature_backfill.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/1_feature_backfill.ipynb). 

The notebook is divided into the following sections:
1. Loading historical data and process features
2. Connecting to Hopsworks Feature Store
3. Creating feature groups and uploading them to the feature store

**The data used comes from different sources:**

- Hourly electricity spot price in kwh per day from [Energinet](https://www.energidataservice.dk).
   - Historical electricity prices for area DK1 starting from January 1, 2022, up until present day. Today is not included since it is not historical data. 

- Different meteorological observations based on Aalborg Denmark from [Open Meteo](https://www.open-meteo.com). 
   - Historical weather measurements based on the location of Aalborg, Denmark starting from January 1, 2022, up until present day. 

- Danish calendar that categorizes dates into types based on whether it is a workday or not. This files is made manually by the group. 
   - The calendar data stretches from 2022-01-01 until 2024-12-31. 
   - Workday is represented by 1 and not a workday is represented by 0.

Creating feature groups for the three datasets defining a `primary_key` as `date` and `timestamp`, so we are able to join them when we create a dataset for training in part 03 the training_pipeline. The feature groups are uploaded to the Feature Store that have been connected in Hopsworks.

We specify a `primary_key` as `date` and `timestamp`, so we are able to join them when we create a dataset for training later in part 03 the training_pipeline.

## Feature Pipeline
Implemented in [notebooks/2_feature_pipeline.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/2_feature_pipeline.ipynb). 

The notebook is divided into the following sections:
1. Parsing new data of today of hourly electricity prices and forecast weather measurements.
2. Inserting the new data into the Feature Store.

Same API calls for the electricity prices as in Feature Backfill, just changing the historical setting to `false` so the fetched data is from real time. In order to provide real time weather measures, a weather forecast measure for the next 5 days is being fetched.

Uploading the new data to the feature groups created previously in Feature Backfill.

## Training Pipeline
Implemented in [notebooks/3_training_pipeline.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/3_training_pipeline.ipynb). 

This notebook is divided into the following sections:
1. Feature selection.
2. Creating a Feature View.
3. Training datasets creation - splitting into train and test sets.
4. Training the model.
5. Register the model to Hopsworks Model Registry.

The selected features for training data is based on select all feature of the electricitry and calendar feature grup.

We first select the features that we want to include for model training and based on the specified `primary_key`as `date` and `timestamp` in part 01_feature_backfill we can now join them together for the `electricity_fg`, `weather_fg` and `danish_holiday_fg`. "timestamp", "datetime", and "hour" is not selected from the `weather_fg`since they not directly contribute to predicting electricity prices now that we have joined based on the `primary_key`.

From the xgboost Python Package we initialize the XGBoost Regressor as the model used for training and predition. The model is trained on the 


## Inference Pipeline
Implemented in [notebooks/4_batch_inference.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/4_batch_inference.ipynb).

This notebook is divided into the following sections:
1. Load new batch data.
2. Predict using the model from Model Registry.
