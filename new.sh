#!/bin/bash

new () {
	cd ~/github_projects/carpdiem.github.io || echo "You need to clone your website into the proper director structure, first."
	if [[ $# -lt 1 ]]; then
		echo "No arguments provided, what would you like to write?"
		return 1
	fi
	
	case "$1" in
		blog)
			fname="drafts/blog/draft_blog.markdown"
			if [[ ! -e $fname ]]; then
				touch $fname
				d=$(date --rfc-3339=s)
				d=${d:0:10}
				echo "---" > $fname
				{
					echo "layout: blog_post";
					echo "title: --title here--";
					echo "date: $d";
					echo "last_modified: $d";
					echo "---";
				} >> $fname
				vim $fname
			else
				echo "Error: you already have a draft in progress. Stash it somewhere and try again."
				return 1
			fi
			;;
		essay)
			fname="drafts/essays/draft_essay.markdown"
			if [[ ! -e $fname ]]; then
				touch $fname
				d=$(date --rfc-3339=s)
				d=${d:0:10}
				echo "---" > $fname
				{
					echo "layout: essay";
					echo "title: --title here--";
					echo "date: $d";
					echo "last_modified: $d";
					echo "---";
				} >> $fname
				vim $fname
			else
				echo "Error: you already have a draft in progress. Stash it somewhere and try again."
				return 1
			fi
			;;
		list)
			fname="drafts/lists/draft_list.markdown"
			if [[ ! -e $fname ]]; then
				touch $fname
				d=$(date --rfc-3339=s)
				d=${d:0:10}
				echo "---" > $fname
				{
					echo "layout: list";
					echo "title: --title here--";
					echo "date: $d";
					echo "last_modified: $d";
					echo "---";
				} >> $fname
				vim $fname
			else
				echo "Error: you already have a draft in progress. Stash it somewhere and try again."
				return 1
			fi
			;;
		misc)
			fname="drafts/misc/draft_misc.markdown"
			if [[ ! -e $fname ]]; then
				touch $fname
				d=$(date --rfc-3339=s)
				d=${d:0:10}
				echo "---" > $fname
				{
					echo "layout: misc";
					echo "title: --title here--";
					echo "date: $d";
					echo "last_modified: $d";
					echo "---";
				} >> $fname
				vim $fname
			else
				echo "Error: you already have a draft in progress. Stash it somewhere and try again."
				return 1
			fi
			;;
		project)
			fname="drafts/projects/draft_project.markdown"
			if [[ ! -e $fname ]]; then
				touch $fname
				d=$(date --rfc-3339=s)
				d=${d:0:10}
				echo "---" > $fname
				{
					echo "layout: project";
					echo "title: --title here--";
					echo "date: $d";
					echo "last_modified: $d";
					echo "---";
				} >> $fname
				vim $fname
			else
				echo "Error: you already have a draft in progress. Stash it somewhere and try again."
				return 1
			fi
			;;

	esac
}
					
