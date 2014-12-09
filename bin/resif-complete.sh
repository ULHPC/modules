_resif_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _RESIF_COMPLETE=complete $1 ) )
    return 0
}

complete -F _resif_completion -o default resif;
