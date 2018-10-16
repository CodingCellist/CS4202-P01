import argparse
import pandas as pd
import matplotlib.pyplot as plt


def make_plot(infile):
    with open(infile) as csvfile:
        df = pd.read_csv(csvfile)
        # index the dataframe
        df_multindex = df.set_index(['predictor', 'set'])
        # calculate the standard deviation
        df_std = df_multindex.groupby(['predictor', 'set']).std()
        # now that we have the standard deviation, calculate the mean
        df_mean = df_multindex.groupby(['predictor', 'set']).mean()
        # 'rearrange' the dataframes so that the predictor names are columns
        std_unstk = df_std.unstack(level=0)
        data_unstk = df_mean.unstack(level=0)
        # remove the top-level column index as it is no longer needed
        std_cols = std_unstk.copy()
        std_cols.columns = std_unstk.columns.droplevel(level=0)
        data_cols = data_unstk.copy()
        data_cols.columns = data_unstk.columns.droplevel(level=0)
        # plot the data with error-bars
        plt.figure(1)
        fig, ax = plt.subplots()
        data_cols.plot(fmt='.', yerr=std_cols, ax=ax)
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="The path to the csv-file containing the data.")
    args = parser.parse_args()

    if not args.infile.endswith(".csv"):
        raise argparse.ArgumentTypeError("infile must be a .csv-file")

    make_plot(args.infile)
