#!/usr/bin/perl

# creates .ts files from master translation file
#
# usage:
# run this executable from the root directory of the repo
# it requires a tab-delimited datafile in Unix format
# src/main/resources/base/ayab/translations/ayab-translation-master.tsv
#
# @author Tom Price
# @date   June 2020

use strict;
use warnings;
use List::Util qw(first);
use File::Spec::Functions;

my $master = "ayab-translation-master.tsv";
my $folder = catfile("src", "main", "resources", "base", "ayab", "translations");
chdir($folder);
open(FILE, "<", $master);
chomp(my $line = <FILE>);
my @headers = split(/\t/, $line);
close(FILE);

my $index = (first { $headers[$_] eq "Context" } 0 .. $#headers) + 1;
my $filename = "ayab_trans_context.txt";
system("cut -f$index $master > $filename");
open(FILE, "<", $filename);
chomp(my @context = <FILE>);
close(FILE);
system("rm $filename");

$index += 1;
$filename = "ayab_trans_base.txt";
system("cut -f$index $master > $filename");
open(FILE, "<", $filename);
chomp(my @base = <FILE>);
close(FILE);
system("rm $filename");

foreach my $column ($index .. $#headers){
        my $lang = $headers[$column-1];
        my $filename = "ayab_trans_$lang.txt";
	system("cut -f$column $master > $filename");
	open(FILE, "<", $filename);
	chomp(my @file = <FILE>);
	close(FILE);
	system("rm $filename");
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
chdir(catfile("..", "..", "..", "..", "..", ".."));
system("lrelease " . catfile($folder, "*.ts"));
system("rm -f " . catfile($folder, "*.ts"));
