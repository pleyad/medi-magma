import csv
import seaborn as sns
import pandas as pd
import numpy as np
from bokeh.palettes import Category20c
from matplotlib import style

style.use('ggplot')
my_palette = Category20c[20]

with open('eval_vibrant_mountain.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    eval_losses = []
    steps = []
    for row in reader:
        eval_losses.append(float(row['vibrant-mountain-58 - eval/loss']))
        steps.append(int(row['Step']))
        
        
    # Draw from a normal distribution to create vector lenth of eval_losses
    some_random = np.random.normal(size=len(eval_losses))
    # Add an offset to the random vector
    some_random = some_random + 4
    
    some_random2 = np.random.normal(size=len(eval_losses)) + 4
    some_random3 = np.random.normal(size=len(eval_losses)) + 4

    plot = sns.lineplot(
        x=steps, 
        y=eval_losses, 
        color=my_palette[0],
        label='Eval Loss'
        )
    plot = sns.lineplot(
        x=steps, 
        y=pd.Series(eval_losses).rolling(10, min_periods=1, center=True).mean(), linestyle='dashed', 
        color=my_palette[1], 
        label='Smoothed Eval Loss'
    )
    
    plot = sns.lineplot(
        x=steps, 
        y=some_random, 
        color=my_palette[4], 
        label='Random')
    
    plot = sns.lineplot(
        x=steps,
        y=some_random2,
        color = my_palette[5],
        label = 'Random2'
    )
    
    plot = sns.lineplot(
        x=steps,
        y=some_random3,
        color = my_palette[6],
        label = 'Random3'
    )
    
    # X-label
    plot.set_xlabel('Steps')
    # Y-label
    plot.set_ylabel('Eval Loss')
    
    # Title
    plot.set_title('Evaluation Loss vs Evaluation Metrics Trends')
    
            
    # show plot
    plot.figure.savefig('eval_vibrant_mountain.png')

