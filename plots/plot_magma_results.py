import csv
import seaborn as sns
import pandas as pd
import numpy as np
from bokeh.palettes import Category20c
from matplotlib import style

def scale_array(df: pd.DataFrame, x: float, y: float):
    min_val = df.min()
    max_val = df.max()
    scaled_df = ((y - x) * (df - min_val) / (max_val - min_val)) + x
    return scaled_df

def create_plot(eval_csv: str, metrics_csv: str):
    style.use('ggplot')
    my_palette = Category20c[20]

    eval = pd.read_csv('eval_vibrant_mountain.csv')
    metrics = pdf   = pd.read_csv('metrics.csv')
    
    eval_loss = eval['vibrant-mountain-58 - eval/loss']
    eval_color = my_palette[0]        
    plot = sns.lineplot(
        x=eval['Step'], 
        y=eval_loss, 
        color=eval_color,
        label='Eval Loss'
        )

    # Add dots for each data point
    sns.scatterplot(
        x=eval['Step'],
        y=eval_loss,
        color=eval_color,
        s=15
    )

    smoothed_data = pd.Series(eval['vibrant-mountain-58 - eval/loss']).rolling(10, min_periods=1, center=True).mean()
    smooth_color = my_palette[1]
    plot = sns.lineplot(
        x=eval['Step'],
        y=smoothed_data, 
        linestyle='dashed', 
        color=smooth_color, 
        label='Smoothed Eval Loss'
    )

    metrics_labels = ['mean_bleu', 'mean_bertscore', 'mean_sembscore', 'mean_radgraphcombined', 'mean_cxrmetric']
    metrics_std_labels = ['std_bleu', 'std_bertscore', 'std_sembscore', 'std_radgraphcombined', 'std_cxrmetric']
    metrics_colors = [my_palette[8], my_palette[9], my_palette[10], my_palette[11], my_palette[6]]
    metrics_scales = [3, 3.5, 4, 4.5, 5, 5.5]
    metrics_labels_legend = ['Mean Bleu', 'Mean Bert Score', 'Mean Semb Score', 'Mean Radgraph', 'Mean CXR']

    for i, metric_label in enumerate(metrics_labels):
        plot = sns.lineplot(
            x=metrics['step'],
            y=scale_array(metrics[metric_label], metrics_scales[i], metrics_scales[i+1]),
            color=metrics_colors[i],
            label=metrics_labels_legend[i]
        )
        
        plot.fill_between(
            metrics['step'],
            scale_array(metrics[metric_label] - metrics[metrics_std_labels[i]], metrics_scales[i], metrics_scales[i+1]),
            scale_array(metrics[metric_label] + metrics[metrics_std_labels[i]], metrics_scales[i], metrics_scales[i+1]),
            alpha=0.5,
            color=metrics_colors[i]
        )
        
        # Add dots for each data point
        sns.scatterplot(
            x=metrics['step'],
            y=scale_array(metrics[metric_label], metrics_scales[i], metrics_scales[i+1]),
            color=metrics_colors[i],
            s=15
        )

    # Move the legend box to the right outside of the plot
    plot.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)


    # X-label
    plot.set_xlabel('Training Steps')
    # Y-label
    plot.set_ylabel('Evaluation Loss')

    # Title
    plot.set_title('Evaluation Loss vs Evaluation Metrics Trends')
            
    # show plot
    plot.figure.savefig('eval_vibrant_mountain.png', bbox_inches='tight')


if __name__ == "__main__":

    eval_csv = 'training1_evaluation.csv'
    metrics_csv = 'training1_metrics.csv'
    
    create_plot(eval_csv, metrics_csv)