# Default parameter values
username ?= pgaddiso
platform ?= linux
interface ?= enp2s0	# See list_interface.py
csvmode ?= e 		# {'c' for normal csv | 'e' for extended} 
# Internal
_pythonpath = /home/parker/miniconda3/envs/via/bin/python
_datapath = ./data/
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
	# - quality
	# - vpn/novpn
	# - clean/noisy
	# Optional:
	# - extension (like 'a' 'b' 'c')
	$(_pythonpath) \
	network-stats/network_stats.py \
	-i $(interface) \
	-$(csvmode) $(_datapath)collected/$(username)-$(provider)-$(speed)-$(quality)-$(vpn)-$(platform)-$(clean)-$(date)$(extension).csv

# Uses shell commands $${...} to get the filename without path... not sure how
# good that is for portability.
zip-data:
	for i in $(_datapath)collected/*.csv ; do \
		zip "$(_datapath)zipped/$${i##*/}.zip" "$$i" ; \
		# mv "$$i" $(_datapath)unzipped/ ; \
	done

echo-names:
	for i in $(_datapath)collected/*.csv ; do \
		echo $${i##*/} ; \
	done

# Runs data collection and compression. See `collect-data` and `zip-data`.
# data: collect-data zip-data
