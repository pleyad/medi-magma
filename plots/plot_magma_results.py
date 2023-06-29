import csv
import seaborn as sns
import pandas as pd
import numpy as np
from bokeh.palettes import Category20c
from matplotlib import style
from matplotlib import pyplot as plt

def scale_array(df: pd.DataFrame, x: float, y: float):
    min_val = df.min()
    max_val = df.max()
    scaled_df = ((y - x) * (df - min_val) / (max_val - min_val)) + x
    return scaled_df

def create_plot(eval_csv: str, metrics_csv: str, run_name: str, ax: plt.Axes):
    my_palette = Category20c[20]

    eval = pd.read_csv(eval_csv)
    metrics = pd.read_csv(metrics_csv)

    eval_loss = eval[f'{run_name} - eval/loss']
    eval_color = my_palette[0]
    
    # First plot (left)
    sns.lineplot(
        x=eval['Step'],
        y=eval_loss,
        color=eval_color,
        label='Eval Loss',
        ax=ax
    )
    
    sns.scatterplot(
        x=eval['Step'],
        y=eval_loss,
        color=eval_color,
        s=15,
        ax=ax
    )
    
    smoothed_data = pd.Series(eval[f'{run_name} - eval/loss']).rolling(10, min_periods=1, center=True).mean()
    smooth_color = my_palette[1]
    
    sns.lineplot(
        x=eval['Step'],
        y=smoothed_data,
        linestyle='dashed',
        color=smooth_color,
        label='Smoothed Eval Loss',
        ax=ax
    )
    
    # Second plot (right)
    metrics_labels = ['mean_bleu', 'mean_bertscore', 'mean_sembscore', 'mean_radgraphcombined', 'mean_cxrmetric']
    metrics_std_labels = ['std_bleu', 'std_bertscore', 'std_sembscore', 'std_radgraphcombined', 'std_cxrmetric']
    metrics_colors = [my_palette[8], my_palette[9], my_palette[10], my_palette[11], my_palette[6]]
    metrics_scales = [3, 3.5, 4, 4.5, 5, 5.5]
    metrics_labels_legend = ['Mean BLEU', 'Mean BERTScore', 'Mean CheXbert Similarity', 'Mean RadGraph F1', 'Mean RadCliQ']
    
    for i, metric_label in enumerate(metrics_labels):
        sns.lineplot(
            x=metrics['step'],
            y=scale_array(metrics[metric_label], metrics_scales[i], metrics_scales[i+1]),
            color=metrics_colors[i],
            label=metrics_labels_legend[i],
            ax=ax
        )
        
        ax.fill_between(
            metrics['step'],
            scale_array(metrics[metric_label] - metrics[metrics_std_labels[i]], metrics_scales[i], metrics_scales[i+1]),
            scale_array(metrics[metric_label] + metrics[metrics_std_labels[i]], metrics_scales[i], metrics_scales[i+1]),
            alpha=0.5,
            color=metrics_colors[i]
        )
        
        sns.scatterplot(
            x=metrics['step'],
            y=scale_array(metrics[metric_label], metrics_scales[i], metrics_scales[i+1]),
            color=metrics_colors[i],
            s=15,
            ax=ax
        )
        
    plt.tight_layout()
    return fig

def get_best_metrics(metrics_csv: str, run_name: str):
    print(f'Run name: {run_name}:')

    max_metrics = ['mean_bleu', 'mean_bertscore', 'mean_sembscore', 'mean_radgraphcombined']
    min_metrics = ['mean_cxrmetric']
    
    # Read in metrics csv
    metrics = pd.read_csv(metrics_csv)
    
    # Get max values of all max_metrices and correspending step value
    max_values = []
    max_steps = []
    for metric in max_metrics:
        max_value = metrics[metric].max()
        max_values.append(max_value)
        max_row = metrics[metrics[metric] == max_value].iloc[0]
        step = max_row['step']
        max_steps.append(step)
        
    min_values = []
    min_steps = []
    for metric in min_metrics:
        min_value = metrics[metric].min()
        min_values.append(min_value)
        min_row = metrics[metrics[metric] == min_value].iloc[0]
        step = min_row['step']
        min_steps.append(step)
        
    # Print out max values and corresponding steps
    for metric, value, step in zip(max_metrics, max_values, max_steps):
        print(f'\tMax {metric}: {value} at step {step}')
    
    # Print out min values and corresponding steps
    for metric, value, step in zip(min_metrics, min_values, min_steps):
        print(f'\tMin {metric}: {value} at step {step}')


def get_best_eval_model(eval_csv: str, run_name: str):
    print(f'Run name: {run_name}:')
    eval = pd.read_csv(eval_csv)
    min_eval_loss = eval[f'{run_name} - eval/loss'].min()
    min_eval_loss_step = eval[eval[f'{run_name} - eval/loss'] == min_eval_loss].iloc[0]['Step']
    print(f'\tMin eval loss: {min_eval_loss} at step {min_eval_loss_step}')

if __name__ == "__main__":

    eval_csv_train1 = 'training1_evaluation.csv'
    metrics_csv_train1 = 'training1_metrics.csv'
    run_name1 = 'vibrant-mountain-58'
    
    
    eval_csv_train2 = 'training2_evaluation.csv'
    metrics_csv_train2 = 'training2_metrics.csv'
    run_name2 = 'denim-sound-65'
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    y_tick_positions = np.arange(0, 5.5, 0.5)
    ax1.set_yticks(y_tick_positions)
    ax2.set_yticks(y_tick_positions)
        
    ax1.set_xlabel('Training Steps')
    ax1.set_ylabel('Evaluation Loss')
    ax2.set_xlabel('Training Steps')

    ax1.set_title('1. Training:  MIMIC-CXR')
    ax2.set_title('2. Training: MIMIC-CXR & IU Chest X-Ray')
    
    # Add title
    fig.suptitle('Evaluation Loss vs. Evaluation Metrics Trends', fontsize=16)

    
    create_plot(eval_csv_train1, metrics_csv_train1, run_name1, ax=ax1)
    fig = create_plot(eval_csv_train2, metrics_csv_train2, run_name2, ax=ax2)
    
    ax1.legend().remove()
    ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    
    fig.figure.savefig('train1_train2_combined.png', bbox_inches='tight')
    
    
    get_best_metrics(metrics_csv_train1, run_name1)
    get_best_metrics(metrics_csv_train2, run_name2)
    
    get_best_eval_model(eval_csv_train1, run_name1)
    get_best_eval_model(eval_csv_train2, run_name2)