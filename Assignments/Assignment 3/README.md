# CSCI 5930 Assignment 3
###
In this assignment, we explored linear regression, and the different strategies to calculate the betas in order to predict an accurate y value.  
  
The first model I submitted was the closed form solution to linear regression. I chose this model because close form yielded the lowest RMSLE value (~.14) in task 15. Compared to the other techniques which all yield values (~.22)  
The RMSLE value on the final dataset was 0.2491. This is a good result, but closed form can sometimes suffer from overfitting the data, so other solutions can be tried for a better prediction.
  
Next, I tried mini-batch gradient descent using alpha = .05 and batch size = 128, since these were the ideal parameters found in task 16. The RMSLE value for this submission was better than closed form at 0.2487.  
I wanted to further tune the hyper-pararmeters for mini-batch. I decided to pick alpha, and batch sizes around the ideal values from task 16. I chose to test the below values.  
  
alphas_judge = [0.03, 0.04, 0.045, 0.05, 0.055, 0.06]  
batch_sizes_judge = [96, 128, 160, 192]  
  
I calculated the betas and predicted y values for each pair (alpha, batch_size). I did these calculations 5 times for each pair and compute the average RMSLE and standard deviation. I chose the alpha and batch size pair which yielded the lowest average RMSLE.  
The fine tuning gave an even better result with RMSLE = .2473.  
  
Next, I tried full batch gradient. In a similar fashion to the fine tuning for mini-batch, I chose a few alpha values, and number epochs, and found which pair yield the lowest average RMSLE. The best pair of values was alpha = .05 and epochs = 50. This was actually the worst performing model with an RMSLE = .2516
  
alphas_full = [0.03, 0.04, 0.05, 0.055, 0.06]  
epochs_full = [50, 100]  
  
So the overall, my best performing model used mini-batch gradient descent with an alpha = .05 and a batch size = 192.  