# livestreamer.bash
# =================
#
# Bash completion support for Livestreamer (http://livestreamer.tanuki.se/)
#
# See README.md for install instructions.
#

# Will complete URLs from these files if they exist.
URL_SOURCES=$(ls ~/.config/livestreamer/favorites* 2>/dev/null)

_livestreamer()
{
    local cur prev words cword
    _init_completion || return

    case $prev in
        -h|--help|-V|--version|--plugins)
            return
            ;;
    esac

    if [[ $cur == -* ]]; then
        COMPREPLY=($(compgen -W '$(_parse_help "$1")' -- "$cur"))
        return
    fi

    local valid_sources=""
    for wordlist in $URL_SOURCES; do
    	if [[ -f $wordlist ]]; then
            valid_sources="$valid_sources $wordlist"
    	fi
    done


    COMPREPLY=($(compgen -W '$(cat $valid_sources)' -- "$cur"))
} &&
complete -F _livestreamer livestreamer

# ex: ts=4 sw=4 et filetype=sh
