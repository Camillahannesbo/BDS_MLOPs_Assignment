---
title: Electricity Price
emoji: 🦀
colorFrom: yellow
colorTo: indigo
sdk: streamlit
sdk_version: 1.34.0
app_file: app.py
pinned: false
---

# <span style="font-width:bold; font-size: 3rem; color:#2656a3;">**BDS MODULE 4 - DATA ENGINEERING AND MACHINE LEARNING OPERATIONS IN BUSINESS (MLOPs)** </span> <span style="font-width:bold; font-size: 3rem; color:#333;">- EXAM ASSIGMENT</span>

## Expectation for the Assignment:
What is expected for technical part of project:

-	A form of prediction system. 
-	Should be able to be retrained over time.
-	Should be able to add on new data.
-	Should be able to end up in a dashboard/interface.

## Group members
| Name                     | Student ID |
|--------------------------|------------|
| Camilla Dyg Hannesbo     | 20202923   |
| Benjamin Ly              | 20205432   |
| Tobias Moesgård Jensen   | 20231658   |

---

## Objectives:
This repository contains all notebooks and local datafiles for the final assignment in the module data engineering and machine learning operations in business (*"MLOPs" in short*).

The objective of this assignment is to build a prediction system that predicts the electricity prices in Denmark (area DK1) based on weather conditions, previous prices, and the Danish holidays.

## Structure:
There are four notebooks in the folder "*notebooks*":

1. **Feature Backfill**: Data is loaded and we engineer and create feature groups.
2. **Feature Pipeline**: New data are parsed and inserted into feature groups.
3. **Training Pipeline**: Building feature view,  training dataset split, training a model, and saving it in the Model Registry.
4. **Inference Pipeline**: The trained model is retrieved from the model registry and used for batch inference.

The structure of the notebooks is largely inspired by [Hopsworks tutorials](https://github.com/logicalclocks/hopsworks-tutorials).
Inspiration for code snippets has been taken from the following advanced tutorials [air_quality](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/advanced_tutorials/air_quality), [electricity](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/advanced_tutorials/electricity), and [timeseries](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/advanced_tutorials/timeseries)

## Data Pipeline:
Electricity Pipeline

![electricity_pipeline.png](images/electricity_pipeline.png)

## Data:
The data used comes from the following sources:

- Hourly electricity prices in Denmark per day from [Energinet](https://www.energidataservice.dk).
- Different meteorological observations based on Aalborg Denmark from [Open meteo](https://www.open-meteo.com).
- Danish calendar that categorizes dates into types based on whether it is a weekday or not. This file is made manually by the group and is located in the "*data*" folder inside this repository.
- Forecast Renewable Energy next day from [Energinet](https://www.energidataservice.dk).
- Weather Forecast based on Aalborg Denmark from [Open Meteo](https://www.open-meteo.com).

See corresponding functions in the folder [features](https://github.com/Camillahannesbo/MLOPs-Assignment-/tree/main/features).

## Frontend application
A functional frontend application that visually demonstrates the project’s effectiveness in real-world scenarios (e.g. streamlit, gradio, Github pages)