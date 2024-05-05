# <span style="font-width:bold; font-size: 3rem; color:#2656a3;">**BDS MODULE 4 - DATA ENGINEERING AND MACHINE LEARNING OPERATIONS IN BUSINESS (MLOPs)** </span> <span style="font-width:bold; font-size: 3rem; color:#333;">- EXAM ASSIGMENT</span>
Report file elaborating on the process

# Topic title: Electricity Price Predicter for Denmark DK1 
## Business Problem
In recent times, energy prices have experienced a notable surge, prompting consumers and businesses alike to scrutinize their energy consumption patterns more closely than ever before. This surge in energy prices has not only heightened awareness regarding energy usage but has also sparked a renewed interest in identifying the optimal times for energy consumption. As consumers seek to navigate this landscape of rising energy costs, understanding when the best times are for utilizing energy becomes paramount. By pinpointing these optimal periods, individuals and organizations can strategically adjust their energy usage patterns to minimize costs while maximizing efficiency.

   > Mangler noget reference?

### Objectives
The objective is to build a prediction system that predicts the daily electricity prices per hour in Denmark (area DK1) based on weather conditions, previous prices, and the Danish calendar. This will end up in a frontend application there ultimately can help the user decide when is the best time to charge the electric vehicle or have production running - leading to potential cost savings or profit maximization. 
The application can be relevant for both individual clients and in a larger business perspective.  

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

- Hourly electricity spot prices in DKK per day from [Energinet](https://www.energidataservice.dk).
   - Historical electricity prices for area DK1 starting from January 1, 2022, up until the present day. Today is not included since it is not historical data. 

- Different meteorological observations based on Aalborg Denmark from [Open Meteo](https://www.open-meteo.com). 
   - Historical weather measurements based on the location of Aalborg, Denmark starting from January 1, 2022, up until the present day. 

- Danish calendar that categorizes dates into types based on whether it is a workday or not. This file is made manually by the group. 
   - The calendar data stretches from 2022-01-01 until 2024-12-31. 
   - Workday is represented by 1 and not a workday is represented by 0.

Creating feature groups for the three datasets defining a `primary_key` as `date` and `timestamp`, so we can join them when we create a dataset for training in part 03 training_pipeline. The feature groups are uploaded to the Feature Store that has been connected in Hopsworks.

## Feature Pipeline
Implemented in [notebooks/2_feature_pipeline.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/2_feature_pipeline.ipynb). 

The notebook is divided into the following sections:
1. Parsing new data of today of hourly electricity prices and forecast weather measurements.
2. Inserting the new data into the Feature Store.

The same API call for the electricity prices as in Feature Backfill, just changing the historical setting to `false` so the fetched data is from real time. To provide real-time weather measures, a weather forecast measure for the next 5 days is being fetched.

Uploading the new data to the feature groups created previously in Feature Backfill.

## Training Pipeline
Implemented in [notebooks/3_training_pipeline.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/3_training_pipeline.ipynb). 

This notebook is divided into the following sections:
1. Feature selection.
2. Creating a Feature View.
3. Training datasets creation - splitting into train and test sets.
4. Training the model.
5. Register the model to the Hopsworks Model Registry.

We first select the features that we want to include for model training and based on the specified `primary_key`, `date`, and `timestamp`, in part 01_feature_backfill we can now join features together for the `electricity_fg`, `weather_fg`, and `Danish_holiday_fg`. For `electricity_fg` and `Danish_holiday_fg` all columns are selected. For `weather_fg`, "timestamp", "datetime", and "hour" is not selected since they do not directly contribute to predicting electricity prices now that we have joined the feature groups based on the `primary_key`. Сombining **Feature Groups** we can then create a **Feature View** which stores a metadata of our data. Having the **Feature View** we can create a **Training Dataset**.

Creating the training/test split data is first retrieved from the Hopsworks Feature Store where we stored the feature view. The training data is then split into 80% assigned to training and the remaining 20% is left out for testing and evaluating the performance of the model.

From the xgboost Python Package, we initialize the XGBoost Regressor as the model used for training and prediction. The model is fitted to the train data and further evaluated using validation metric functions from the sklearn library. The results are illustrated below and indicate that the model has a fairly good performance when it comes to predicting new electricity prices. 

| Validation metrics       |  |
|----------------------|----------|
| ⛳️ MSE               | 0.0022   |
| ⛳️ RMSE              | 0.0471   |
| ⛳️ R^2               | 0.9708   |
| ⛳️ MAE               | 0.04100  |

We further look into the feature importances using the plot_importance function from XGBoost, here ....

A schema of the model's input and output is specified from training examples using the features (X_train) and target variable (y_train). An entry of the specified details is then created and the model is uploaded to the Hopsworks Model Registry.

## Inference Pipeline
Implemented in [notebooks/4_batch_inference.ipynb](https://github.com/Camillahannesbo/MLOPs-Assignment-/blob/main/notebooks/4_batch_inference.ipynb).

This notebook is divided into the following sections:
1. Load new batch data.
2. Predict using the model from the Model Registry.

Our objective is to predict the electricity prices for the upcoming days, therefore we load a weather forecast as batch data to generate predictions. This dataframe is merged with the calendar dataframe. 
This batch obtains daily weather measures forecast for the upcoming 5 days after the run (e.g., a run on May 7th will fetch values 5 days ahead including May 12th).

The saved XGBmodel is retrieved and used on the new merged data to predict the electricity prices in the upcoming 5 days. 

Along with a prediction matrix on hourly intervals, the batch pipeline also includes a time-series plot visualizing the trend of the spot price (in DKK) for DK1 over the prediction time. An interactive version of this in the form of a line chart with points is also created enabling users to explore the data and gain insights interactively.

The feature pipeline and batch inference run daily as a scheduled function using Github Actions. 
A script is set up to run the feature and batch inference pipeline and a Github Action workflow is scheduled to run the script at 23:50 everyday. Another workflow is scheduled to run at 23:59 everyday to sync the features and predictions made daily up to Huggingface Spaces. 
