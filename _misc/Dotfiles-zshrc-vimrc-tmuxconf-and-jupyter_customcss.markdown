---
layout: misc
title: "Dotfiles: .zshrc, .vimrc, .tmux.conf, and jupyter_custom.css"
date: 2020-06-10
last_modified: 2020-06-10
---

These are my dotfiles. There are many like them, but these ones are mine.

[.zshrc](https://www.dropbox.com/s/903zu61w1o5mxnv/.zshrc?dl=0)
{% highlight shell linenos %}
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
setopt autocd notify
unsetopt beep extendedglob
bindkey -v
bindkey '^R' history-incremental-search-backward
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename $HOME/.zshrc

autoload -Uz compinit
compinit
# End of lines added by compinstall

## Custom additions:

# useful aliases
alias ll='ls -alFh'
alias lr='ls -alFhR'
alias dc='cd'
alias bc='bc -l'
alias ls='ls -F'
alias jnote='jupyter notebook'
alias jlab='jupyter lab'
alias ip3='ipython3'
export GP=$HOME/github_projects

# useful scripts
source $HOME/.config/broot/launcher/bash/br
source $HOME/Dropbox/backups/utility\ scripts/mkcd
source $HOME/Dropbox/backups/utility\ scripts/todo
source ~/Dropbox/backups/utility\ scripts/marco.sh
source ~/Dropbox/backups/utility\ scripts/polo.sh
source ~/Dropbox/backups/utility\ scripts/new.sh
source ~/Dropbox/backups/utility\ scripts/publish.sh

export PATH=$HOME/anaconda3/bin:$PATH
export PATH=$HOME/.cargo/bin:$PATH

# enable autocompletion
# ## TODO: dig into exactly what this lets you do
autoload -Uz compinit
compinit

# enable prompt themes
autoload -Uz promptinit
promptinit

prompt walters

# force terminal backgrounds to make vim work with gruvbox
export TERM=xterm-256color

# Autostart tmux if tmux is installed
if command -v tmux &> /dev/null; then 
# There's something funny going on here with the "=="... 
# see: https://www.zsh.org/mla/users/2011/msg00161.html "Re: string equal problem" 
	if [ "$TMUX" "==" "" ]; then
		if [ $TERM != "screen-256color" ] && [ $TERM != "screen" ]; then
			tmux
		fi
	fi
fi

# Install Ruby Gems to ~/gems
export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"

# attempt to reduce timeouts on ESC key
KEYTIMEOUT=1

# function expand-alias() {
# 	zle _expand_alias
# 	zle self-insert
# }
# zle -N expand-alias
# bindkey -M main '	' expand-alias
{% endhighlight %}

---

[.vimrc](https://www.dropbox.com/s/1gkz8tsyygp7ea8/.vimrc?dl=0)
{% highlight viml linenos %}
" Comments in Vimscript start with a `"`.

" If you open this file in Vim, it'll be syntax highlighted for you.

" Vim is based on Vi. Setting `nocompatible` switches from the default
" Vi-compatibility mode and enables useful Vim functionality. This
" configuration option turns out not to be necessary for the file named
" '~/.vimrc', because Vim automatically enters nocompatible mode if that file
" is present. But we're including it here just in case this config file is
" loaded some other way (e.g. saved as `foo`, and then Vim started with
" `vim -u foo`).
set nocompatible

" Turn on syntax highlighting.
syntax on

" Disable the default Vim startup message.
set shortmess+=I

" Show line numbers.
set number

" set tab-spacing = 4 spaces
set ts=4
set shiftwidth=4

" This enables relative line numbering mode. With both number and
" relativenumber enabled, the current line shows the true line number, while
" all other lines (above and below) are numbered relative to the current line.
" This is useful because you can tell, at a glance, what count is needed to
" jump up or down to a particular line, by {count}k to go up or {count}j to go
" down.
set relativenumber

" Always show the status line at the bottom, even if you only have one window open.
set laststatus=2

" The backspace key has slightly unintuitive behavior by default. For example,
" by default, you can't backspace before the insertion point set with 'i'.
" This configuration makes backspace behave more reasonably, in that you can
" backspace over anything.
set backspace=indent,eol,start

" By default, Vim doesn't let you hide a buffer (i.e. have a buffer that isn't
" shown in any window) that has unsaved changes. This is to prevent you from "
" forgetting about unsaved changes and then quitting e.g. via `:qa!`. We find
" hidden buffers helpful enough to disable this protection. See `:help hidden`
" for more information on this.
set hidden

" This setting makes search case-insensitive when all characters in the string
" being searched are lowercase. However, the search becomes case-sensitive if
" it contains any capital letters. This makes searching more convenient.
set ignorecase
set smartcase

" Enable searching as you type, rather than waiting till you press enter.
set incsearch

" Unbind some useless/annoying default key bindings.
nmap Q <Nop> " 'Q' in normal mode enters Ex mode. You almost never want this.

" Disable audible bell because it's annoying.
set noerrorbells visualbell t_vb=

" Enable mouse support. You should avoid relying on this too much, but it can
" sometimes be convenient.
set mouse+=a

" Try to prevent bad habits like using the arrow keys for movement. This is
" not the only possible bad habit. For example, holding down the h/j/k/l keys
" for movement, rather than using more efficient movement commands, is also a
" bad habit. The former is enforceable through a .vimrc, while we don't know
" how to prevent the latter.
" Do this in normal mode...
nnoremap <Left>  :echoe "Use h"<CR>
nnoremap <Right> :echoe "Use l"<CR>
nnoremap <Up>    :echoe "Use k"<CR>
nnoremap <Down>  :echoe "Use j"<CR>
" ...and in insert mode
inoremap <Left>  <ESC>:echoe "Use h"<CR>
inoremap <Right> <ESC>:echoe "Use l"<CR>
inoremap <Up>    <ESC>:echoe "Use k"<CR>
inoremap <Down>  <ESC>:echoe "Use j"<CR>

filetype plugin indent on
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'

" enable gruvbox colorscheme
set background=dark
colorscheme gruvbox

" enable adding newlines in normal mode in a way that lets them work with
" number prefixes
nnoremap <silent> oo :<C-u>call append(line("."), repeat([""], v:count1))<CR>
nnoremap <silent> OO :<C-u>call append(line(".")-1, repeat([""], v:count1))<CR>
nnoremap ooo o<CR>
nnoremap OOO O<ESC>O

" set default split pane behavior
set splitbelow
set splitright

" set easier split pane movement
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" attempt to keep the cursor in the middle of the screen when scrolling in
" .txt or .md files
au BufNewFile,BufRead *.txt,*.markdown
	\ setlocal scrolloff=99999

" attempt to remove timeout delays when using ESC kep
set timeoutlen=1000 ttimeoutlen=0

" try making indentLine plugin ignore both tex and markdown files
autocmd FileType markdown,tex,json let g:indentLine_enabled=0

" make vim stop breaking words in half to wrap lines
set linebreak
{% endhighlight %}

---

[.tmux.conf](https://www.dropbox.com/s/a3vtx5be888f5b0/.tmux.conf?dl=0)
{% highlight plaintext linenos %}
# remap prefix from 'C-b' to 'C-a'
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# enable vim mode-keys
setw -g mode-keys vi

# split panes using | and -
bind | split-window -c "#{pane_current_path}" -h
bind - split-window -c "#{pane_current_path}" -v
unbind '"'
unbind %

# reload config file (assuming default location)
bind r source-file ~/.tmux.conf

# switch panes using Alt-arrow without prefix
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# switch panes using vim hjkl
bind -n M-h select-pane -L
bind -n M-l select-pane -R
bind -n M-k select-pane -U
bind -n M-j select-pane -D

# don't rename windows automatically
set-option -g allow-rename off

# attempt to reduce ESC key timeouts
set -s escape-time 0
# above (and similar lines in .vimrc and .zshrc) come from the following post
# https://www.johnhawthorn.com/2012/09/vi-escape-delays/
{% endhighlight %}

---

[jupyter_custom.css](https://www.dropbox.com/s/qejaf5n1cc0tnwx/jupyter_custom.css?dl=0)
{% highlight css linenos %}
/*This file contains any manual css for this page that needs to override the global styles.
This is only required when different pages style the same element differently. This is just
a hack to deal with our current css styles and no new styling should be added in this file.*/

#ipython-main-app {
    position: relative;
}
#jupyter-main-app {
    position: relative;
}

div#notebook p, div#notebook{
	font-family: "Crimson Pro Light";
    font-size: 110%;
    line-height: 115%;
}
.rendered_html pre, .rendered_html table{
	font-family: "Crimson Pro Light";
    font-size: 110%;
    line-height: 115%;
}
.CodeMirror, .CodeMirror pre, .CodeMirror-dialog, .CodeMirror-dialog .CodeMirror-search-field, .terminal-app .terminal {
	font-family: "Iosevka Term Slab Light" !important;
    font-size: 100%;
    line-height: 115%;
}

pre {
	font-family: "Crimson Pro Light";
	font-size: 110%;
	line-height: 110%;
	word-break: break-word;
}

.prompt {
	font-family: "Iosevka Term Slab Light";
}

.cm-keyword, .cm-operator {
	font-weight: normal !important;
}

.cm-header {
	font-family: "Iosevka Term Slab Light" !important;
	font-weight: normal ! important;
}
{% endhighlight %}

#### Why do I post these here with dropbox links, rather than hosting them in a github repo?

Frankly, I'm too lazy to bother *git add*-ing and *git commit*-ing them every time I make a change. In practice, I keep them synced to my Dropbox account, and have a setupNewUbuntu.sh script that I run on all of my personal systems to symlink them into ~/ after I get my local Dropbox folder synced.

So far this has worked well, though I might adjust the setup as I need to in the future.

#### Anything particularly interesting?

Lines 116-117 of my .vimrc were critical to fixing an issue I had of extremely annoying pauses whenever I would tap the Caps-Lock key (I have my Caps-Lock set to act as ESC when you tap it, but CTRL when you hold it). this was coupled with lines 71-72 of my .zshrc, and lines 33-36 of my .tmux.conf.

Lines 119-120 of my .vimrc were needed to fix a crazy-annoying bug where due to a particular vim plugin (indentLine), various characters would not be displayed when editing .markdown and .tex files. This included single asterisks, but not double asterisks! So \* would not be displayed, but \*\* would be displayed.

Finally, I include my jupyter_custom.css file. It's not a true dotfile—no "." at the beginning!—but it serves a similar role for adjusting the default display properties of my Jupyter installation make my time using that software more enjoyable. And given just how often I fire that up, it's well worth it.
