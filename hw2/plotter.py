#!/usr/bin/env python
import csv
import matplotlib.pyplot as plt
import math
import sys, re, os
import argparse

def sortcoords(xvals, yvals):
    return zip(*sorted(zip(xvals, yvals), key=lambda xy: float((xy[0]))))

def _main(argv):
    parser = argparse.ArgumentParser(usage="Plots runtime of algorithms.")
    parser.add_argument('timefiles', nargs='*')
    parser.add_argument('-x', '--x-axis', nargs=1, dest='xaxis_name', default='Input Size (n)')

    args = parser.parse_args()

    colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w')
    csv_pattern = re.compile('\.csv$')

    csv_count = len(args.timefiles)
    if csv_count not in range(1, len(colors)): raise Exception('Must specify between 1 and 8 csv filenames')
    
    for i, csv_path in enumerate(args.timefiles):
        if not os.path.exists(csv_path) or not csv_pattern.search(csv_path):
            raise Exception('File argument %s is not a valid .csv file' % str(i + 1))

    filename_one, filename_two = args.timefiles[0], args.timefiles[1] if csv_count == 2 else None

    # label the axes
    plt.ylabel('Time')
    plt.xlabel(args.xaxis_name[0])

    handles = []
    for i, fname in enumerate(args.timefiles):
        xvals, yvals = [], []
        # read csv
        with open(fname, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
            #         print row
                xvals.append(row[0]); yvals.append(row[1])

        xvals, yvals = sortcoords(xvals, yvals)

        # plot the times
        xpts = [math.sqrt(float(xval)) for xval in xvals]
        line = plt.plot(xvals, yvals, colors[i] + 'o-', label=fname.replace('.csv', ''))
        handles.append(line[0])

        """
    if csv_count == 2:
        xvals_two, yvals_two = [], []
        with open(filename_two, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                xvals_two.append(row[0])
                yvals_two.append(row[1])


        xvals_two, yvals_two = sortcoords(xvals_two, yvals_two)
        second_csv = plt.plot(xvals_two, yvals_two, 'ro-', label=argv[1].replace('.csv', ''))
        """
    
    #handles = [first_csv[0]] + ([second_csv[0]] if csv_count == 2 else [])
    # calculate legend based on csv_count; 2 csv's means two handles
    plt.legend(loc=0, handles=handles)

    #plotfile_name = filename_one + (' vs. ' + filename_two if filename_two else '')
    plotfile_name = ' vs. '.join((name for name in args.timefiles))

    if not os.path.exists('graphs'):
        os.makedirs('graphs')

    outfile_path = os.path.join('graphs', plotfile_name.replace('.csv', '') + '.png')

    plt.savefig(outfile_path)
    plt.show()


if __name__ == '__main__':
    _main(sys.argv[1:])
