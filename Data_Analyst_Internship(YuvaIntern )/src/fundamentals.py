"""Task 1: runnable Python and statistics exercises."""
import json
from pathlib import Path
from statistics import mean, median, stdev

def numeric_summary(values):
    if len(values)<2:
        raise ValueError('At least two values are required')
    return {'mean':mean(values),'median':median(values),'sample_std':stdev(values)}

def main():
    values=[10,20,20,30,40]
    output={'types':{k:type(v).__name__ for k,v in {'age':25,'score':8.5,'name':'Analyst','active':True,'marks':[10,20],'point':(1,2),'unique':{1,2},'record':{'id':1}}.items()},'summary':numeric_summary(values),'squares':[x*x for x in range(1,6)],'above_mean':[x for x in values if x>mean(values)],'probability_above_20':sum(x>20 for x in values)/len(values)}
    target=Path(__file__).resolve().parents[1]/'outputs/fundamentals.json'
    target.write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
