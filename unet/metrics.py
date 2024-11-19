import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from tqdm import tqdm

#class to calculate metrics (IoU, Dice, etc.)
class Metrics:
    def __init__(self):
        super(Metrics, self).__init__()

    #function to calculate relevant metrics on data
    def calculateMetrics(self, gt, pred):
        iou = self.__jaccardIndex(gt, pred) #iou
        dice = self.__diceCoefficient(gt, pred) #dice coefficient
        sensitivity = self.__sensitivity(gt, pred)
        specificity = self.__specificity(gt, pred)
        precision = self.__precision(gt, pred)
        accuracy = self.__accuracy(gt, pred)

        return iou, dice, sensitivity, specificity, precision, accuracy

    #function to calculate the jaccard index (IoU)
    @staticmethod
    def __jaccardIndex(gt, pred):
        intersection = np.logical_and(pred, gt)
        union = np.logical_or(pred, gt)
        iou = intersection.sum() / union.sum()
        return iou

    #function to calculate the Dice coefficient 
    @staticmethod
    def __diceCoefficient(gt, pred):
        intersection = np.logical_and(pred, gt)
        totals = pred.sum() + gt.sum()
        dice = (2 * intersection.sum()) / totals
        return dice

    #function to calculate the sensitivity 
    @staticmethod
    def __sensitivity(gt, pred): #aka recall
        tp = np.logical_and(gt, pred).sum() #true positives
        fn = ((gt - pred) == 1).sum()
        sensitivity = tp / (tp + fn)
        return sensitivity #ability to detect true positives (white pixels)

    #function to calculate the specificity 
    @staticmethod
    def __specificity(gt, pred):
        not_gt = np.logical_not(gt)
        not_pred = np.logical_not(pred)
        tn = np.logical_and(not_gt, not_pred).sum()
        fp = ((pred - gt) == 1).sum()
        specficity = tn / (tn + fp)
        return specficity #ability to detect true negatives (background)
    
    #function to calculate precision
    @staticmethod
    def __precision(gt, pred):
        tp = np.logical_and(gt, pred).sum() #true positives
        fp = ((pred - gt) == 1).sum()
        precision = tp / (tp + fp)
        return precision #positive predictive value
    
    #function to calculate overall accuracy
    @staticmethod
    def __accuracy(gt, pred):
        true = (gt == pred).sum()
        accuracy = true / (gt.shape[0] * gt.shape[1])
        return accuracy

def main():
    #pred/gt directories
    pred_mask_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/mask_images"
    gt_mask_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset/test_masks"
    
    #directory to save figures w/ metrics
    metrics_mask_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/metrics_masks"
    os.makedirs(metrics_mask_dir, exist_ok=True)

    avg_metrics = {"iou": 0, "dice": 0, "sensitivity": 0, "specificity": 0, "precision": 0, "accuracy": 0}

    for i, pred_mask_file in enumerate(tqdm(os.listdir(pred_mask_dir))):
        pred_base_name = pred_mask_file.split(".")[0]

        gt_mask_name = pred_base_name + "_mask.gif"

        #loading gt mask
        # gt_mask = np.array(Image.open(os.path.join(gt_mask_dir, os.listdir(gt_mask_dir)[i])).convert("L"), dtype=np.uint8)
        gt_mask = np.array(Image.open(os.path.join(gt_mask_dir, gt_mask_name)).convert("L"), dtype=np.uint8)
        (thresh, gt_mask) = cv2.threshold(gt_mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gt_mask[gt_mask == 255] = 1.0

        #loading pred mask
        pred_mask = np.array(Image.open(os.path.join(pred_mask_dir, pred_mask_file)).convert("L"), dtype=np.uint8)
        (thresh, pred_mask) = cv2.threshold(pred_mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        pred_mask[pred_mask == 255] = 1.0 

        #calculating relevant metrics
        metrics_obj = Metrics()
        iou, dice, sensitivity, specificity, precision, accuracy = metrics_obj.calculateMetrics(gt_mask, pred_mask)
        
        #sanity check
        if iou < 0.6:
            breakpoint()

        #plotting pred masks with metrics 
        metric_text = f"IOU = %.2f\nDice = %.2f\nSensitivity = %.2f\nSpecificity = %.2f\nPrecision = %.2f\nAccuracy = %.2f" % (iou, dice, sensitivity, specificity, precision, accuracy)
        plt.imshow(pred_mask)
        plt.text(-1200, 1000, metric_text, fontsize=14)
        plt.subplots_adjust(left=0.35)
        plt.title(pred_base_name)
        plt.savefig(os.path.join(metrics_mask_dir, pred_base_name + "_metrics.png"))
        plt.clf()

        #updating average metrics
        avg_metrics["iou"] += iou
        avg_metrics["dice"] += dice
        avg_metrics["sensitivity"] += sensitivity
        avg_metrics["specificity"] += specificity
        avg_metrics["precision"] += precision
        avg_metrics["accuracy"] += accuracy

    #averaging the metrics over the number of files
    for metric in avg_metrics:
        avg_metrics[metric] /= len(os.listdir(pred_mask_dir))
        print(f"Avg. {metric}: {avg_metrics[metric]}")

if __name__ == "__main__":
    main()