import pandas as pd
import yake


def keyword_extraction(description):

    # defining yake parameters
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.8
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 50

    kw_extractor = yake.KeywordExtractor(lan=language, 
                                          n=max_ngram_size, 
                                          dedupLim=deduplication_thresold, 
                                          dedupFunc=deduplication_algo, 
                                          windowsSize=windowSize, 
                                          top=numOfKeywords)
    
    yake_keywords_with_score = kw_extractor.extract_keywords(description)
    yake_keywords = [yake_keyword[0] for yake_keyword in yake_keywords_with_score]

    return yake_keywords

if __name__ == '__main__':

    input_file = 'get_description.csv' # we are using sample sports apps their title and description to generate apps

    df = pd.read_csv(input_file) 
    description = df['description']
    keywords = keyword_extraction(description)





