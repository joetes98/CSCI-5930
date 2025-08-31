import pandas as pd


def main():

    dfA = pd.read_csv('week-01/datasets/A.csv')
    dfB = pd.read_csv('week-01/datasets/B.txt', delim_whitespace=True, header=None)
    dfC = pd.read_csv('week-01/datasets/C.csv', sep=';')
    dfD = pd.read_csv('week-01/datasets/D.txt', delim_whitespace=True, header=None)

    lengthA = len(dfA)
    lengthB = len(dfB)
    lengthC = len(dfC)
    lengthColumnsA = len(dfA.columns)
    lengthColumnsB = len(dfB.columns)
    lengthColumnsC = len(dfC.columns)

    dfC.iloc[1:, -1] = pd.to_numeric(dfC.iloc[1:, -1], errors='coerce')
    meanC = dfC.iloc[1:, -1].mean()
    meanA = dfA.iloc[:, 2].mean()
    distinctA = dfA.iloc[:,3].unique()

    print(f"Number of rows in A: {lengthA}")
    print(f"Number of rows in B: {lengthB}")
    print(f"Number of rows in C: {lengthC}")
    print('\n')
    print(f"Number of columns in A: {lengthColumnsA}")
    print(f"Number of columns in B: {lengthColumnsB}")
    print(f"Number of columns in C: {lengthColumnsC}")
    print('\n')
    print(f"Mean of the last column in C: {meanC:.2f}")
    print('\n')
    
    dfCompare = dfB.compare(dfD)
    print(dfCompare)
    print(dfB.iloc[[112589]])
    print(dfD.iloc[[112589]])
    print('\n')
    print(f"Mean Credit Score in Dataset A: {meanA:.2f}")
    print(f"Number of distinct countires in Dataset A: {len(distinctA)}")


if __name__ =="__main__":
    main()