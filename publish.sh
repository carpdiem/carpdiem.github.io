#!/bin/bash

publish () {
	sitedir="$HOME/github_projects/carpdiem.github.io"
	if [[ $# -le 2 ]]; then
		if [[ -n $2 ]]; then
			fname="/$2"
		else
			case "$1" in
				blog)
					fname="/drafts/blog/draft_blog.markdown"
					;;
				essay)
					fname="/drafts/essays/draft_essay.markdown"
					;;
				list)
					fname="/drafts/lists/draft_list.markdown"
					;;
				misc)
					fname="/drafts/misc/draft_misc.markdown"
					;;
				project)
					fname="/drafts/projects/draft_project.markdown"
					;;
			esac
		fi
		case "$1" in
			blog)
				d=$(grep date: "$sitedir$fname" | cut -d' ' -f2)
				t=$(grep title: "$sitedir$fname" | cut -d' ' -f1 --complement | tr ' ' '-')
				mv "$sitedir$fname" "$sitedir/_blog/$d-$t.markdown"
				;;
			essay)
				t=$(grep title: "$sitedir$fname" | cut -d' ' -f1 --complement | tr ' ' '-')
				mv "$sitedir$fname" "$sitedir/_essays/$t.markdown"
				;;
			list)
				t=$(grep title: "$sitedir$fname" | cut -d' ' -f1 --complement | tr ' ' '-')
				mv "$sitedir$fname" "$sitedir/_lists/$t.markdown"
				;;
			misc)
				t=$(grep title: "$sitedir$fname" | cut -d' ' -f1 --complement | tr ' ' '-')
				mv "$sitedir$fname" "$sitedir/_misc/$t.markdown"
				;;
			project)
				t=$(grep title: "$sitedir$fname" | cut -d' ' -f1 --complement | tr ' ' '-')
				mv "$sitedir$fname" "$sitedir/_projects/$t.markdown"
				;;
			*)
				echo "Argument is not an existing category to publish."
				;;
		esac
	fi
}
