#!/bin/bash

new () {
	cd ~/github_projects/carpdiem.github.io || echo "You need to clone your website into the proper director structure, first."
	if [[ $# -lt 1 ]]; then
		echo "No arguments provided, what would you like to write?"
		return 1
	fi
	
	case "$1" in
		list)
			fname="_lists/draft_list.markdown"
			if [[ ! -e $fname ]]; then
				touch $fname
				d=$(date --rfc-3339=s)
				d=${d:0:10}
				echo "---" > $fname
				echo "layout: default" >> $fname
				echo "title: --title here--" >> $fname
				echo "subtitle: --subtitle here--" >> $fname
				echo "date: $d" >> $fname
				echo "last_modified: $d" >> $fname
				echo "---" >> $fname
				vim $fname
			else
				echo "Error: you already have a draft in progress. Stash it somewhere and try again."
				return 1
			fi
			;;
		esac
}
					
