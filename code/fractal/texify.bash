cat results-q0-h.txt | sed -e 's/\.None//g' -e 's/\.datapoints//g' -e 's/\s*y\_intcpt=.*//g' -e 's/slope=\s*\-//g' -e 's/\([^0-9]\)$/\1\&/g' -e 's/[0-9]$/\\\\\^/g' -e 's/\s*//g' -e 's/\_/\\\_/g' | tr '\n' ' ' | tr '^' '\n' > tmp.txt
sort -t\& -k2 -r tmp.txt