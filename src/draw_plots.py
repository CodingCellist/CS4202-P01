import argparse
import pandas as pd
import os.path as path
import matplotlib.pyplot as plt
from math import ceil


def savefig(figure, directory, figname):
    if directory.endswith('/'):
        file_path = "{:s}{:s}.png"
    else:
        file_path = "{:s}/{:s}.png"
    file_path = file_path.format(directory,
                                 figname.replace(' ', '-')
                                 .replace('\'', '')
                                 .replace('(', '')
                                 .replace(')', ''))
    figure.savefig(file_path)


def make_plot(infile, sem, outdir=None):
    with open(infile) as csvfile:
        # load the data
        df = pd.read_csv(csvfile)

        # index the dataframe
        df_multindex = df.set_index(['predictor', 'set'])

        # calculate the standard deviation or error mean for each set
        if sem:
            df_set_std = df_multindex.groupby(['predictor', 'set']).sem()
        else:
            df_set_std = df_multindex.groupby(['predictor', 'set']).std()

        # calculate the mean of the sets and the mean across the sets
        df_set_mean = df_multindex.groupby(['predictor', 'set']).mean()

        # calculate the 'total' standard deviation or error mean, i.e. the
        # standard deviation or mean error of all the samples, across all the
        # sets
        if sem:
            df_total_std = df_multindex.groupby(['predictor']).sem()
        else:
            df_total_std = df_multindex.groupby(['predictor']).std()

        # calculate the 'total' mean, i.e. the mean across all the samples,
        # and all the sets
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

        # constant parts of the plots
        ylabel = "Accuracy (%)"
        program = "[{:s}]".format((infile.split('/')[-1]).split('.')[0])

        # plot the set-wise data with error-bars
        plt.figure(1)
        fig, ax = plt.subplots()
        set_data_cols.plot(fmt='.', yerr=set_std_cols, ax=ax)
        title = program + " Set-wise Accuracy"
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        ax.legend(loc='lower left', bbox_to_anchor=(1.01, 0))
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, title)

        # plot the set-wise data, excluding 'always-taken' for a smaller y-scale
        set_data_excl_at = set_data_cols.drop('always-taken', axis=1)
        set_std_excl_at = set_std_cols.drop('always-taken', axis=1)
        plt.figure(2)
        fig, ax = plt.subplots()
        set_data_excl_at.plot(fmt='.', yerr=set_std_excl_at, ax=ax)
        title = program + " Set-wise Accuracy (excluding 'always-taken')"
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        ax.legend(loc='lower left', bbox_to_anchor=(1.01, 0))
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, title)

        # plot the 'total' data, i.e. the data across all the sets
        plt.figure(3)
        fig, ax = plt.subplots()
        df_total_mean.plot.bar(yerr=df_total_std, ax=ax)
        title = program + " Average Accuracy for all Predictors"
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, title)

        # plot the 'total' data, excluding 'always-taken' for a smaller y-scale
        excl_at = df_total_mean.drop('always-taken', axis=0)
        y_low = min(excl_at.values)
        y_high = max(excl_at.values)
        y_margin = 0.7 * (y_high - y_low)
        plt.figure(4)
        fig, ax = plt.subplots()
        excl_at.plot.bar(yerr=df_total_std.drop('always-taken', axis=0), ax=ax)
        title = program + " Average Accuracy for all Predictors (excluding 'always-taken')"
        plt.ylim([ceil(y_low - y_margin),
                  100])
        plt.title(title)
        plt.ylabel(ylabel, rotation=90)
        plt.tight_layout()
        if outdir is not None:
            savefig(fig, outdir, title)

        # if we haven't saved the plots, show them
        if outdir is None:
            plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="The path to the csv-file containing the data.")
    parser.add_argument("--sem", action='store_true', dest='sem',
                        help="Use Standard Error Mean for error-bars."
                             " [Note: either --sem OR --std must be used]")
    parser.add_argument("--std", action='store_true', dest='std',
                        help="Use Standard Deviation for error-bars."
                             " [Note: either --sem OR --std must be used]")
    parser.set_defaults(sem=False)
    parser.set_defaults(std=False)
    parser.add_argument("-o", "--outdir", type=str, default=None,
                        help="The path to the directory to save the plots to.")
    args = parser.parse_args()

    if not args.infile.endswith(".csv"):
        raise argparse.ArgumentTypeError("infile must be a .csv-file")
    if not args.sem ^ args.std:
        raise argparse.ArgumentTypeError("please pass --sem OR --std")
    if args.outdir is not None:
        if not path.isdir(args.outdir):
            raise argparse.ArgumentTypeError("-d/--outdir must be the path to a directory")

    make_plot(args.infile, args.sem, outdir=args.outdir)
