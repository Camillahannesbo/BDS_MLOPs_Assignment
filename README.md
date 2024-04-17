# <span style="font-width:bold; font-size: 3rem; color:#2656a3;">**BDS MODULE 4 - DATA ENGINEERING AND MACHINE LEARNING OPERATIONS IN BUSINESS (MLOPs)** </span> <span style="font-width:bold; font-size: 3rem; color:#333;">- EXAM ASSIGMENT</span>

## Group members
| Name                     | Student ID |
|--------------------------|------------|
| Camilla Dyg Hannesbo     | 20202923   |
| Benjamin Ly              | 20205432   |
| Tobias Moesgård Jensen   | 20231658   |

---

## Objektives:
This repository contains all notebooks and local datafiles for the final assigment in the module data engineering and machine learning operations in business (*"MLOPs" in short*)

The objektives for this assigment is to build a predicting system the electricity prices in Denmark based on weather conditions, previous prices, and the Danish holidays.

## Structure:
There is four notebooks in the folder "*notebooks*":

1. **Feature Backfill**: How to load, engineer and create feature groups.
2. **Feature Pipeline**: How to parse new data and insert into feature groups.
3. **Training Pipeline**: How to build a feature view, training dataset split, train a model and save it in the Model Registry.
4. **Inference Pipeline**: How to retrieve a trained model from the model registry and use it for batch inference.

### Feature Backfill

API: 

### Feature Pipeline

### Training Pipeline

### Inference Pipeline

## Data:
The data you will use comes from three different sources:

- Electricity prices in Denmark per day from [Energinet](https://www.energidataservice.dk).
- Different meteorological observations from [Open meteo](https://www.open-meteo.com).
- Danish Calendar with the type if the date is a national holiday or not. This files is made manually by the group and is located in the "*data*" folder inside this repository.

See corresponding functions in the folder [features](https://github.com/Camillahannesbo/MLOPs-Assignment-/tree/main/features).
