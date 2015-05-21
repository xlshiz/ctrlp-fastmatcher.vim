if g:fastmatcher_script =~? "py"
	exec g:fastmatcher_script "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
	exec g:fastmatcher_script "sys.path.insert(0, cwd)"
	exec g:fastmatcher_script "from pymatcher.matcher import *"
	let g:fastmatcher_command = g:fastmatcher_script." py_matcher()"
elseif g:fastmatcher_script == 'lua'
	let s:cwd = eval('expand(\"<sfile>:p:h\")')
	exec g:fastmatcher_script "require ".s:cwd.'/luamatcher/matcher'
	let g:fastmatcher_command = g:fastmatcher_script." lua_matcher()"
else
	let g:fastmatcher_command = ''

endif

function! fastmatcher#matcher(items, str, limit, mmode, ispath, crfile, regex)

	if g:fastmatcher_command == ''
		return
	endif

	call clearmatches()

	let s:rez = []
	let s:regex = ''

	if a:str != ''
		exec g:fastmatcher_command
		let s:matchregex = '\v\c'
		if a:mmode == 'filename-only'
			let s:matchregex .= '[\^\/]*'
		endif
		let s:matchregex .= s:regex
		call matchadd('CtrlPMatch', s:matchregex)
	else
		let s:rez = a:items[0:a:limit]
	endif

	return filter(s:rez, 'v:val != a:crfile')
endfunction
