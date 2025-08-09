#!/bin/bash

publish () {
    sitedir="$HOME/github_projects/carpdiem.github.io"
    if [[ $# -eq 0 ]]; then
        echo "Usage: publish <category>"
        echo "Categories: blog, essay, list, misc, project"
        return 1
    fi

    local category=$1
    local draft_dir
    local publish_dir

    case "$category" in
        blog) draft_dir="$sitedir/drafts/blog"; publish_dir="$sitedir/_blog";;
        essay) draft_dir="$sitedir/drafts/essays"; publish_dir="$sitedir/_essays";;
        list) draft_dir="$sitedir/drafts/lists"; publish_dir="$sitedir/_lists";;
        misc) draft_dir="$sitedir/drafts/misc"; publish_dir="$sitedir/_misc";;
        project) draft_dir="$sitedir/drafts/projects"; publish_dir="$sitedir/_projects";;
        *) echo "Error: '$category' is not a valid category."; return 1;;
    esac

    # Find drafts, handling the case where the directory might be empty
    local drafts_found=()
    while IFS= read -r line; do
        drafts_found+=("$line")
    done < <(find "$draft_dir" -maxdepth 1 -type f -name '*.markdown')

    if [[ ${#drafts_found[@]} -eq 0 ]]; then
        echo "No drafts found in $draft_dir."
        return 0
    fi

    local selected_draft
    if [[ ${#drafts_found[@]} -eq 1 ]]; then
        selected_draft="${drafts_found[0]}"
        echo "Found one draft. Selecting: $(basename "$selected_draft")"
    else
        echo "Please choose a draft to publish:"
        select draft_path in "${drafts_found[@]}"; do
            if [[ -n "$draft_path" ]]; then
                selected_draft="$draft_path"
                break
            else
                echo "Invalid selection. Please try again."
            fi
        done
    fi

    local title_line=$(grep -m 1 "^title:" "$selected_draft")
    if [[ -z "$title_line" || "$title_line" == *"--title here--"* ]]; then
        echo "Warning: The draft '$(basename "$selected_draft")' has a placeholder title."
        read -p "Publishing it will result in a generic filename. Continue? (y/N) " confirm
        if [[ "${confirm,,}" != "y" ]]; then
            echo "Publishing aborted."
            return 1
        fi
    fi

    local t=$(echo "$title_line" | sed 's/^title: *//' | tr ' ' '-' | tr -d '*."/\[]:;|=,?')
    local final_path

    if [[ "$category" == "blog" ]]; then
        local d=$(grep -m 1 "^date:" "$selected_draft" | cut -d' ' -f2)
        final_path="$publish_dir/$d-$t.markdown"
    else
        final_path="$publish_dir/$t.markdown"
    fi

    echo "Publishing to: $final_path"
    mv "$selected_draft" "$final_path"
}
