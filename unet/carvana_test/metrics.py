import numpy as np

#class to calculate metrics (IoU, Dice, etc.)
class Metrics:
    def __init__(self):
        super(Metrics, self).__init__()

    #function to calculate relevant metrics on data
    def calculateMetrics(self, gt, pred):
        iou = self.__jaccardIndex(gt, pred) #avg iou per batch
        dice = self.__diceCoefficient(gt, pred) #avg dice coefficient
        return iou, dice


    #function to calculate the average jaccard index (IoU) over a batch of preds
    @staticmethod
    def __jaccardIndex(gt, pred):
        batch_size = pred.shape[0] 
        avg_iou = 0

        #looping over each image in batch
        for i in range(batch_size):
            pred_mask = pred[i]
            gt_mask = gt[i]

            intersection = np.logical_and(pred_mask, gt_mask)
            union = np.logical_or(pred_mask, gt_mask)
            
            #if both pred and GT are all BG
            if union.sum() == 0: 
                avg_iou += 1 #rewarding with max IoU (should we do this???)
                continue 

            avg_iou += intersection.sum() / union.sum()

        avg_iou /= batch_size #diving by batch size to obtain average
        return avg_iou

    #function to calculate the Dice coefficient 
    @staticmethod
    def __diceCoefficient(gt, pred):
        batch_size = pred.shape[0] 
        avg_dice = 0

        for i in range(batch_size):
            pred_mask = pred[i]
            gt_mask = gt[i]

            intersection = np.logical_and(pred_mask, gt_mask)
            totals = pred_mask.sum() + gt_mask.sum()

            #checking if all BG
            if totals == 0: 
                avg_dice += 1 #(should we do this???)
                continue

            avg_dice += (2 * intersection.sum()) / totals

        avg_dice /= batch_size
        return avg_dice

    def __sensitivity(gt, pred):
        pass
    
    @staticmethod
    def __specificity(gt, pred):
        pass

    def __accuracy(gt, pred):
        pass

    def __fScore(gt, pred):
        pass
