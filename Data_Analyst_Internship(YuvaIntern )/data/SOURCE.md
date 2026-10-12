# Dataset source and interpretation
Source: scikit-learn diabetes dataset, distributed with the installed package.
https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html
https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
Original study: Efron, Hastie, Johnstone and Tibshirani (2004), Least Angle Regression, Annals of Statistics.
442 records, 10 baseline predictors, and a quantitative progression target measured one year later.
Data are loaded with scaled=False. Predictors therefore use raw dataset units. The sex field is a coded category, not a continuous measurement. Serum feature meanings should be interpreted using the source documentation.
Columns: age, sex, bmi, bp, s1, s2, s3, s4, s5, s6, target.
This is an educational analysis of an existing research cohort. It is not a clinical decision tool. No patient names or contact information are included.
The dirty lab example is an intentionally modified 12-record copy, not an issue found in the real source.
