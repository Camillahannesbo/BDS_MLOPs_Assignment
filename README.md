# <span style="font-width:bold; font-size: 3rem; color:#2656a3;">**BDS MODULE 4 - DATA ENGINEERING AND MACHINE LEARNING OPERATIONS IN BUSINESS (MLOPs)** </span> <span style="font-width:bold; font-size: 3rem; color:#333;">- EXAM ASSIGMENT</span>

## Expectation for the Assignment:
What is expected for project:

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

## Data Pipeline:
Electricity Pipeline

    mangler billede

## Data:
The data used comes from three different sources:

- Electricity prices in Denmark per day from [Energinet](https://www.energidataservice.dk).
- Different meteorological observations from [Open meteo](https://www.open-meteo.com).
- Danish Calendar with the type if the date is a national holiday or not. This file is made manually by the group and is located in the "*data*" folder inside this repository.

See corresponding functions in the folder [features](https://github.com/Camillahannesbo/MLOPs-Assignment-/tree/main/features).

## Frontend application
A functional frontend application that visually demonstrates the project’s effectiveness in real-world scenarios (e.g. streamlit, gradio, Github pages)