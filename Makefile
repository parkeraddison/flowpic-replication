# Default parameter values
username ?= pgaddiso
platform ?= linux
interface ?= enp2s0	# See list_interface.py
csvmode ?= e 		# {'c' for normal csv | 'e' for extended} 
# Internal
_pythonpath = /home/parker/miniconda3/envs/via/bin/python
_datapath = ./data/collected/
# Functional
date = $(shell date +'%Y%m%d')

# Collects data using network stats and saves a csv to the data directory.
# 
# Example call:
# ```
# make collect-data provider=youtube speed=2x vpn=vpn clean=noisy
# ```
#
# TODO: Automatically interrupt the script if given a time argument.
#
collect-data:
	# Requires:
	# - provider
	# - speed
	# - vpn/novpn
	# - clean/noisy
	$(_pythonpath) \
	network-stats/network_stats.py \
	-i $(interface) \
	-$(csvmode) $(_datapath)$(username)-$(provider)-$(speed)-$(vpn)-$(platform)-$(clean)-$(date).csv

# Takes all .csv files in the data directory and individually compresses each
# file to a .csv.zip, then moves the files to the zipped data sub-directory.
zip-data:
	for i in $(_datapath)*.csv; do zip "$${i%/}.zip" "$$i"; done
	mv $(_datapath)*.zip $(_datapath)zipped

# Runs data collection and compression. See `collect-data` and `zip-data`.
data: collect-data zip-data
