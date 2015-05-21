if exists('g:fastmatcher_loaded') || v:version < 700 || &compatible
    finish
else
      let g:fastmatcher_loaded = 1
endif

if has("python3")
	let g:fastmatcher_script = "py3 "
elseif has("python")
	let g:fastmatcher_script = "py "
elseif has("lua")
	let g:fastmatcher_script = "lua"
else
	echo "Error: LeaderF requires vim compiled with +python or +python3"
	finish
endif
