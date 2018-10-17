import argparse
import pandas as pd
import matplotlib.pyplot as plt


def make_plot(infile):
    with open(infile) as csvfile:
        # load the data
        df = pd.read_csv(csvfile)

        # index the dataframe
        df_multindex = df.set_index(['predictor', 'set'])

        # calculate the standard deviation for each set
        df_set_std = df_multindex.groupby(['predictor', 'set']).std()

        # calculate the mean of the sets and the mean across the sets
        df_set_mean = df_multindex.groupby(['predictor', 'set']).mean()

        # calculate the 'total' standard deviation, i.e. the standard deviation
        # across all the samples, regardless of the set
        df_total_std = df_multindex.groupby(['predictor']).std()

        # calculate the 'total' mean, i.e. the mean across all the samples,
        # regardless of the set
        df_total_mean = df_multindex.groupby(['predictor']).mean()

        # 'rearrange' the dataframes so that the predictor names are columns
        set_std_unstk = df_set_std.unstack(level=0)
        set_data_unstk = df_set_mean.unstack(level=0)
        # total_std_data = df_total_std.transpose()
        # total_mean_data = df_total_mean.transpose()

        # remove the top-level column index of the set-wise dataframes as that
        # index is no longer needed
        set_std_cols = set_std_unstk.copy()
        set_std_cols.columns = set_std_unstk.columns.droplevel(level=0)
        set_data_cols = set_data_unstk.copy()
        set_data_cols.columns = set_data_unstk.columns.droplevel(level=0)

        # plot the set-wise data with error-bars
        plt.figure(1)
        fig, ax = plt.subplots()
        set_data_cols.plot(fmt='.', yerr=set_std_cols, ax=ax)

        # plot the set-wise data, excluding 'always-taken' for a smaller y-scale
        plt.figure(2)
        fig, ax = plt.subplots()
        set_data_cols.drop('always-taken', axis=1)\
            .plot(fmt='.', yerr=set_std_cols.drop('always-taken', axis=1), ax=ax)

        # plot the 'total' data, i.e. the data across all the sets
        plt.figure(3)
        fig, ax = plt.subplots()
        df_total_mean.plot.bar(yerr=df_total_std, ax=ax)

        # plot the 'total' data, excluding 'always-taken' for a smaller y-scale
        plt.figure(4)
        fig, ax = plt.subplots()
        df_total_mean.drop('always-taken', axis=0)\
            .plot.bar(yerr=df_total_std.drop('always-taken', axis=0), ax=ax)

        # show the plots
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="The path to the csv-file containing the data.")
    args = parser.parse_args()

    if not args.infile.endswith(".csv"):
        raise argparse.ArgumentTypeError("infile must be a .csv-file")

    make_plot(args.infile)
