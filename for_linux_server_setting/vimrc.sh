#!/bin/bash

# .vimrc 파일 경로
vimrc_path="$HOME/.vimrc"

# .vimrc 파일이 이미 존재하는지 확인
if [ -e "$vimrc_path" ]; then
  echo ".vimrc 파일이 이미 존재합니다. 스크립트를 종료합니다."
  exit 1
fi

# .vimrc 파일 생성
cat << EOF > "$vimrc_path"
set hlsearch
set nu
set autoindent
set scrolloff=2
set wildmode=longest,list
set ts=4
set sts=4
set sw=1
set autowrite
set autoread
set cindent
set bs=eol,start,indent
set history=256
set laststatus=2
set paste
set shiftwidth=4
set showmatch
set smartcase
set expandtab
set smarttab
set smartindent
set softtabstop=4
set tabstop=4
set ruler
set incsearch
set statusline=\ %<%l:%v\ [%P]%=%a\ %h%m%r\ %F
:hi CursorLine cterm=NONE ctermfg=white guibg=yellow guifg=white

autocmd BufWritePre * %s/\s\+$//e

augroup CursorLine
  au!
  au VimEnter,WinEnter,BufWinEnter * setlocal cursorline
  au WinLeave * setlocal nocursorline
augroup END
EOF

echo ".vimrc 파일이 생성되었습니다."

