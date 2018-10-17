import argparse
import pandas as pd
import os.path as path
import matplotlib.pyplot as plt
from math import ceil


def savefig(figure, directory, infile, figname):
    if directory.endswith('/'):
        file_path = "{:s}{:s}-{:s}.png"
    else:
        file_path = "{:s}/{:s}-{:s}.png"
    if '/' in infile:
        infile = infile.split('/')[-1]
    infile = infile.split('.')[0]
    file_path = file_path.format(directory, infile,
                                 figname.replace(' ', '-')
                                 .replace('\'', '')
                                 .replace('(', '')
                                 .replace(')', ''))
    figure.savefig(file_path)


def make_plot(infile, outdir=None):
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

        # remove the top-level column index of the set-wise dataframes as that
        # index is no longer needed
        set_std_cols = set_std_unstk.copy()
        set_std_cols.columns = set_std_unstk.columns.droplevel(level=0)
        set_data_cols = set_data_unstk.copy()
        set_data_cols.columns = set_data_unstk.columns.droplevel(level=0)

        # plot the set-wise data with error-bars
        ylabel = "Accuracy (%)"
        plt.figure(1)
        fig, ax = plt.subplots()
        set_data_cols.plot(fmt='.', yerr=set_std_cols, ax=ax)
        title = "Set-wise Accuracy"
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        ax.legend(loc='lower left', bbox_to_anchor=(1.01, 0))
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, infile, title)

        # plot the set-wise data, excluding 'always-taken' for a smaller y-scale
        set_data_excl_at = set_data_cols.drop('always-taken', axis=1)
        set_std_excl_at = set_std_cols.drop('always-taken', axis=1)
        plt.figure(2)
        fig, ax = plt.subplots()
        set_data_excl_at.plot(fmt='.', yerr=set_std_excl_at, ax=ax)
        title = "Set-wise Accuracy (excluding 'always-taken')"
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        ax.legend(loc='lower left', bbox_to_anchor=(1.01, 0))
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, infile, title)

        # plot the 'total' data, i.e. the data across all the sets
        plt.figure(3)
        fig, ax = plt.subplots()
        df_total_mean.plot.bar(yerr=df_total_std, ax=ax)
        title = "Average Accuracy for all Predictors"
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, infile, title)

        # plot the 'total' data, excluding 'always-taken' for a smaller y-scale
        excl_at = df_total_mean.drop('always-taken', axis=0)
        y_low = min(excl_at.values)
        y_high = max(excl_at.values)
        y_margin = 0.7 * (y_high - y_low)
        plt.figure(4)
        fig, ax = plt.subplots()
        excl_at.plot.bar(yerr=df_total_std.drop('always-taken', axis=0), ax=ax)
        title = "Average Accuracy for all Predictors (excluding 'always-taken')"
        plt.ylim([ceil(y_low - y_margin),
                  100])
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, infile, title)

        # if we haven't saved the plots, show them
        if outdir is None:
            plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="The path to the csv-file containing the data.")
    parser.add_argument("-o", "--outdir", type=str, default=None,
                        help="The path to the directory to save the plots to.")
    args = parser.parse_args()

    if not args.infile.endswith(".csv"):
        raise argparse.ArgumentTypeError("infile must be a .csv-file")
    if args.outdir is not None:
        if not path.isdir(args.outdir):
            raise argparse.ArgumentTypeError("-d/--outdir must be the path to a directory")

    make_plot(args.infile, outdir=args.outdir)
