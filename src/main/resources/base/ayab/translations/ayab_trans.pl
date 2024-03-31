#!/usr/bin/perl

# creates .ts files from master translation file
#
# usage:
# run this executable the same directory of the repo
# as a tab-delimited datafile in Unix format called
# ayab-translation-master.tsv
#
# @author Tom Price
# @date   June 2020

use strict;
use warnings;
use List::Util qw(first);
use File::Spec::Functions;

#index, infile, outfile
sub cut{
open(my $infile, "<",$_[1]);
open(my $outfile, ">",$_[2]);
while (my $line = <$infile>) {
	my @b = split(/\t/,$line);
	print $outfile @b[$_[0]-1],"\n";
}
}

#filenames
sub rm{
    unlink(@_)
}

my $master = "ayab-translation-master.tsv";
open(FILE, "<", $master);
chomp(my $line = <FILE>);
my @headers = split(/\t/, $line);
close(FILE);

my $index = (first { $headers[$_] eq "Context" } 0 .. $#headers) + 1;
my $filename = "ayab_trans_context.txt";
cut($index, $master, $filename);
open(FILE, "<", $filename);
chomp(my @context = <FILE>);
close(FILE);
rm($filename);

$index += 1;
$filename = "ayab_trans_base.txt";
cut($index, $master, $filename);
open(FILE, "<", $filename);
chomp(my @base = <FILE>);
close(FILE);
rm($filename);

foreach my $column ($index .. $#headers){
        my $lang = $headers[$column-1];
        my $filename = "ayab_trans_$lang.txt";
	cut($column, $master, $filename);
	open(FILE, "<", $filename);
	chomp(my @file = <FILE>);
	close(FILE);
	rm($filename);
    $filename = "ayab_trans.$lang.ts";
	open(FILE, ">", $filename);
	print FILE <<'HEADER';
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
HEADER
	print FILE '<TS version="2.1" language="' . $lang . '">' . "\n";
        my $last_context = "";
        foreach my $index (1 .. $#context) {
		my $context = $context[$index];
		print FILE "</context>\n" if ($last_context ne "" && $last_context ne $context);
		print FILE "<context>\n    <name>$context</name>\n" if ($last_context ne $context);
		$last_context = $context;
		print FILE "    <message>\n";
		my $src = $base[$index];
		print FILE "        <source>$src</source>\n";
		my $trans = $file[$index];
		print FILE "        <translation>$trans</translation>\n" if ($trans ne "");
		print FILE '        <translation type="unfinished"></translation>' . "\n" if ($trans eq "");
		print FILE "    </message>\n";
        }
	print FILE "</context>\n";
	print FILE "</TS>\n";
	close(FILE);
}

# now that the `.ts` files have been generated
# run `lrelease *.ts` to create binary `.qm` files
open(FILE, "<", $master);
system("lrelease *.ts");
unlink glob "*.ts";
