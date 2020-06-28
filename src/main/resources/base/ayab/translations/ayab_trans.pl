#!/usr/bin/perl

# creates .ts files from master translation file
#
# usage: run this executable from the directory it is in
# it requires a tab-delimited datafile `ayab-translation-master.tsv`
# in Unix format
#
# after the `.ts` files have been generated
# then run `lrelease *.ts` to create binary `.qm` files
# 
#
# @author Tom Price
# @date   June 2020

$master = "ayab-translation-master.tsv";
open(FILE, "<", $master);
chomp($line = <FILE>);
@headers = split(/\t/, $line);
$columns = scalar @headers;
close(FILE);

$filename = "ayab_trans_context.txt";
system("cut -f4 $master > $filename");
open(FILE, "<", $filename);
chomp(@context = <FILE>);
close(FILE);
system("rm $filename");

$filename = "ayab_trans_base.txt";
system("cut -f5 $master > $filename");
open(FILE, "<", $filename);
chomp(@base = <FILE>);
close(FILE);
system("rm $filename");

foreach my $column (5 .. $columns){
        $lang = $headers[$column-1]; 
        $filename = "ayab_trans_$lang.txt";
	system("cut -f$column $master > $filename");
	open(FILE, "<", $filename);
	chomp(@file = <FILE>);
	close(FILE);
	system("rm $filename");
        $filename = "ayab_trans.$lang.ts";
	open(FILE, ">", $filename);
	print FILE <<'HEADER';
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
HEADER
	print FILE '<TS version="2.1" language="' . $lang . '">' . "\n";
        $last_context = "";
        foreach my $index (1 .. scalar @context - 1) {
		$context = $context[$index];
		print FILE "</context>\n" if ($last_context ne "" && $last_context ne $context);
		print FILE "<context>\n    <name>$context</name>\n" if ($last_context ne $context);
		$last_context = $context;
		print FILE "    <message>\n";
		$src = $base[$index];
		print FILE "        <source>$src</source>\n";
		$trans = $file[$index];
		print FILE "        <translation>$trans</translation>\n" if ($trans ne "");
		print FILE '        <translation type="unfinished"></translation>' . "\n" if ($trans eq "");
		print FILE "    </message>\n";
        }
	print FILE "</context>\n";
	print FILE "</TS>\n";
	close(FILE);
}

