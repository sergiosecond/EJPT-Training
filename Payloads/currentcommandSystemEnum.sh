function ctrl_c(){
	echo -e "\n\n[!] Saliendo...\n"
	tput cnorm: exit 1 #Recuperar cursor
}

# HAbilitar Ctrl+c
trap ctrl_c SIGINT

old_process=$(ps -eo user,command)

tput civis # Ocultar cursor

while true; do
	new_process=$(ps -eo user,command)
	diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -vE "command|kworker|procmon"
	old_process=$new_process
done