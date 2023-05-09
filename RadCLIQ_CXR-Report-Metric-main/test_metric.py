import config
from CXRMetric.run_eval import calc_metric

gt_reports = config.GT_REPORTS
predicted_reports = config.PREDICTED_REPORTS
out_file = config.OUT_FILE

if __name__ == "__main__":
    calc_metric(gt_reports, predicted_reports, out_file)
