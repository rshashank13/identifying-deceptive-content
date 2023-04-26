### Contents:

This folder contains all the code related to fakenews detection experiments.

1. `Generate Embeddings.ipynb` -> code used to pre-generate RoBERTa embeddings of all the datasets
2. `CombinedDatasetEmbeddings.ipynb` -> code used to generate combined dataset's RoBERTa embeddings.
3. `RoBERTa-LIAR-3.ipynb` -> code for RoBERTa + FC model trained on LIAR dataset
4. `RoBERTa-Siamese-LIAR-2.ipynb` -> code for RoBERTa based Siamese BERT model trained on LIAR dataset
5. `SplittingFnewsDataset.ipynb` -> code for extracting useful datapoints from the fake news corpus
6. `TrainModel.ipynb` -> code for training the RoBERTa + FC model on all the datasets