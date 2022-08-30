'''
In this function we can generate the sample size for the dataset that we need to analyse
 N: The total number of the dataset eg)2058 for our case
 
 p: Population Proportion eg)  50%
 
 z: The z-score is the number of standard deviations a given proportion is away from the mean. 
 To find the right z-score to use, refer to the table below:
 -----------------------------------------------------
|Desired confidence level   |    Z score              |
 -----------------------------------------------------
|     80%                   | 1.28                    |
|     85%                   | 1.44                    |
|     90%                   | 1.65                    |
|     95%                   | 1.96                    |
|     99%                   | 2.58                    |
 -----------------------------------------------------
 Desired Confidence level is A percentage that reveals how confident you can be that the population would select an answer within a certain range. For example, 
 a 95% confidence level means that you can be 95% certain the results lie between x and y numbers.
 
 e: Margin of error: A percentage that tells you how much you can expect your survey results to reflect the views of the overall population. 
 The smaller the margin of error, the closer you are to having the exact answer at a given confidence level.
'''


def sample_size(N, p=0.5, z= 1.96,  e = 0.05):
    num = ((z*z)*(p*(1-p)))/(e*e)
    if N==0:
        deno = 0
    else:
        deno = 1+(((z*z)*(p*(1-p)))/(e*e*N))
    if deno!=0:
        sams= num/deno
        return round(sams)
    else:
        return 0


if __name__ == '__main__':

    dataset_size = 2058 # define your dataset size for custom generation
    sample_set_size = sample_size(dataset_size)