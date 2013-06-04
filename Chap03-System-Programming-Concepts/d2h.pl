#!/usr/bin/env perl
# Convert list of decimal numbers into hex
for ($i = 0; $i < @ARGV; $i++) {
	printf("%d\t= 0x%08x\n", $ARGV[$i], $ARGV[$i]);
}
