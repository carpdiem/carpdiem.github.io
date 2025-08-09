#!/bin/bash

new () {
    cd ~/github_projects/carpdiem.github.io || { echo "You need to clone your website into the proper directory structure, first."; return 1; }

    if [[ $# -lt 1 ]]; then
        echo "Usage: new <category> [slug]"
        echo "Categories: blog, essay, list, misc, project"
        return 1
    fi

    local category=$1
    local slug=$2
    local dir_path
    local layout

    case "$category" in
        blog) dir_path="drafts/blog"; layout="blog_post";; 
        essay) dir_path="drafts/essays"; layout="essay";;
        list) dir_path="drafts/lists"; layout="list";;
        misc) dir_path="drafts/misc"; layout="misc";;
        project) dir_path="drafts/projects"; layout="project";;
        *) echo "Error: '$category' is not a valid category."; return 1;;
    esac

    if [[ -z "$slug" ]]; then
        slug=$(date +%Y-%m-%d-%H%M%S)
        echo "No slug provided. Using timestamp: $slug"
    fi

    local fname="$dir_path/$slug.markdown"

    if [[ -e $fname ]]; then
        echo "Error: A draft named '$slug.markdown' already exists in '$dir_path'."
        return 1
    fi

    local d=$(date +%Y-%m-%d)
    
    echo "Creating new draft: $fname"
    touch "$fname"
    echo "---" > "$fname"
    {
        echo "layout: $layout";
        echo "title: --title here--";
        echo "date: $d";
        echo "last_modified: $d";
        echo "---";
        echo "<!--more-->";
    } >> "$fname"

    vim "$fname"
}
