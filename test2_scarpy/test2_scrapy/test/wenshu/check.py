
import time

cookies = '_gscu_2116842793=45290230pz5s0i39; ' \
          'Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545290231,1545298274,1545356434,1545716938; ' \
          '_gscbrs_2116842793=1; ' \
          'Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545720079; ' \
          '_gscs_2116842793=t457200630bgno783|pv:2; ' \
          'vjkl5=053498ff1be46b013f1806393895926eda85e44c'

cookies_2 = '_gscu_2116842793=45290230pz5s0i39; ' \
            'Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545290231,1545298274,1545356434,1545716938; ' \
            '_gscbrs_2116842793=1; ' \
            'Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545720294; ' \
            '_gscs_2116842793=t457200630bgno783|pv:3; ' \
            'vjkl5=20f470298ff1ce440014118310f7bbd44087b275'

print(cookies==cookies_2)
print(int(time.time()))