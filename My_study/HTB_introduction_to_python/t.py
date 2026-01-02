from colorama import Fore
# print("\033[38;5;45m[-] Please specify a target, use --help for more info.\033[0m")
# print("\033[38;5;51m[-] Please specify a target, use --help for more info.\033[0m")
reset_all='\033[0m'
c='\033[38;5;'
cyan_45=f'{c}45m'
cyan_51=f'{c}51m'
color_155=f'{c}155m'
d='\033[38;5;251m'


underline='\033[4m'
remove_underline='\033[24m'

color_block='\033[38;5;'
color_45=f'{color_block}45m'
color_51=f'{color_block}51m'
color_160=f'{color_block}160m'
color_122=f'{color_block}122m'
color_123=f'{color_block}123m'
color_124=f'{color_block}196m'
color_251=f'{color_block}251m'
reset_colors='\033[0m'

victim_ip='192.168.1.86'
gateway_ip='192.168.1.1'

gateway_ip='192.168.1.1'
print(f"{color_251}Spoofing {color_123}{underline}{gateway_ip}{remove_underline}{color_251} pretending to be {color_124}{underline}{victim_ip}{remove_underline}{color_251}...{reset_colors}")
print(f"{color_251}Spoofing {color_124}{underline}{victim_ip}{remove_underline}{color_251} pretending to be {color_123}{underline}{gateway_ip}{remove_underline}{color_251}...{reset_colors}")

print(f'\r{color_251}Restoring {color_123}{underline}{gateway_ip}{remove_underline}{color_251} to its original state...{reset_colors}',flush=True,end='')
print(f'\n{color_block}34mDone.')
print(f'\r{color_251}Restoring {color_124}{underline}{victim_ip}{remove_underline}{color_251} to its original state...{reset_colors}',flush=True,end='')
print(f'\n{color_block}34mDone.')

raise SystemExit(1)
print(3333)