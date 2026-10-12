"""Run Tasks 2-6 using an offline, real-world regression dataset."""
from pathlib import Path
import json, sqlite3, platform
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'outputs'; figs=out/'figures'; figs.mkdir(parents=True,exist_ok=True)
    dataset=load_diabetes(as_frame=True,scaled=False)
    df=dataset.frame
    df.to_csv(ROOT/'data/diabetes_raw.csv',index=False)
    (ROOT/'data/DATASET_DESCRIPTION.txt').write_text(dataset.DESCR)
    quality={'rows':len(df),'columns':len(df.columns),'missing_cells':int(df.isna().sum().sum()),'duplicate_rows':int(df.duplicated().sum())}
    # No source records are modified if they already pass the audit.
    clean=df.drop_duplicates().copy()
    clean.to_csv(ROOT/'data/diabetes_clean.csv',index=False)
    clean.describe().to_csv(out/'descriptive_statistics.csv')
    correlations=clean.corr(numeric_only=True)['target'].drop('target').sort_values(ascending=False)
    correlations.to_csv(out/'target_correlations.csv')
    q1=clean.quantile(.25); q3=clean.quantile(.75); iqr=q3-q1
    flags=((clean<q1-1.5*iqr)|(clean>q3+1.5*iqr)).sum()
    flags.to_csv(out/'outlier_flags.csv')
    # Deliberately damaged COPY for Task 2; source data remains untouched.
    lab=clean.head(12).copy(); lab.loc[0,'bmi']=np.nan
    lab=pd.concat([lab,lab.iloc[[1]]],ignore_index=True)
    lab.to_csv(ROOT/'data/lab_dirty_example.csv',index=False)
    lab=lab.drop_duplicates(); lab['bmi']=lab['bmi'].fillna(lab['bmi'].median())
    lab.to_csv(ROOT/'data/lab_clean_example.csv',index=False)
    plt.figure(figsize=(7,4)); clean.target.hist(bins=20,color='#237a9f'); plt.xlabel('Progression score'); plt.ylabel('Records'); plt.title('Target distribution'); plt.tight_layout(); plt.savefig(figs/'target_histogram.png',dpi=150); plt.close()
    plt.figure(figsize=(7,4)); plt.scatter(clean.bmi,clean.target,alpha=.5,s=15); plt.xlabel('BMI'); plt.ylabel('Progression score'); plt.title('BMI and target'); plt.tight_layout(); plt.savefig(figs/'bmi_scatter.png',dpi=150); plt.close()
    plt.figure(figsize=(7,4)); correlations.sort_values().plot.barh(color='#237a9f'); plt.xlabel('Pearson correlation with target'); plt.title('Feature associations'); plt.tight_layout(); plt.savefig(figs/'correlations.png',dpi=150); plt.close()
    plt.figure(figsize=(7,4)); clean.boxplot(column=['bmi','bp']); plt.title('BMI and blood pressure distributions'); plt.tight_layout(); plt.savefig(figs/'boxplot.png',dpi=150); plt.close()
    # No time column exists, so no invented time-series chart is produced.
    X=clean.drop(columns='target'); y=clean.target
    Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,test_size=.2,random_state=42)
    cv=KFold(n_splits=5,shuffle=True,random_state=42)
    candidates={'Mean baseline':DummyRegressor(),'Linear regression':LinearRegression(),'Ridge regression':Ridge(alpha=10),'Random forest':RandomForestRegressor(n_estimators=200,min_samples_leaf=5,random_state=42,n_jobs=1)}
    trained={}; rows=[]
    for name,model in candidates.items():
        pipeline=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),model)
        scores=-cross_val_score(pipeline,Xtrain,ytrain,cv=cv,scoring='neg_mean_absolute_error')
        pipeline.fit(Xtrain,ytrain); trained[name]=pipeline
        rows.append({'model':name,'cv_mae_mean':scores.mean(),'cv_mae_std':scores.std()})
    results=pd.DataFrame(rows).sort_values('cv_mae_mean'); results.to_csv(out/'cross_validation.csv',index=False)
    # Select only on training folds; evaluate held-out test exactly once.
    best=results.iloc[0]['model']; pred=trained[best].predict(Xtest)
    metrics={'selected_model':best,'train_rows':len(Xtrain),'test_rows':len(Xtest),'test_mae':float(mean_absolute_error(ytest,pred)),'test_rmse':float(np.sqrt(mean_squared_error(ytest,pred))),'test_r2':float(r2_score(ytest,pred))}
    pd.DataFrame({'row_index':Xtest.index,'actual':ytest.values,'predicted':pred,'residual':ytest.values-pred}).to_csv(out/'test_predictions.csv',index=False)
    plt.figure(figsize=(7,4)); plt.scatter(pred,ytest-pred,alpha=.7,s=18); plt.axhline(0,color='black'); plt.xlabel('Predicted score'); plt.ylabel('Actual minus predicted'); plt.title('Held-out residuals'); plt.tight_layout(); plt.savefig(figs/'residuals.png',dpi=150); plt.close()
    with sqlite3.connect(out/'analysis.sqlite') as con:
        clean.to_sql('diabetes',con,if_exists='replace',index=False)
        for name,query in {'summary':'SELECT COUNT(*) AS records, AVG(target) AS mean_target, AVG(bmi) AS mean_bmi FROM diabetes','bmi_groups':'SELECT CASE WHEN bmi < 25 THEN "below_25" WHEN bmi < 30 THEN "25_to_30" ELSE "30_plus" END AS bmi_group, COUNT(*) AS records, AVG(target) AS mean_target FROM diabetes GROUP BY bmi_group'}.items():
            pd.read_sql_query(query,con).to_csv(out/f'sql_{name}.csv',index=False)
    summary={'quality':quality,'target_mean':float(y.mean()),'target_median':float(y.median()),'bmi_target_correlation':float(correlations['bmi']),'outlier_flags':{k:int(v) for k,v in flags.items()},'metrics':metrics,'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__}}
    (out/'results.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
