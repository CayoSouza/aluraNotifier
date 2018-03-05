import urllib.request
from bs4 import BeautifulSoup
import ctypes
import time
import webbrowser
import sys
import re

SECTIONS_TO_VERIFY = {'JAVA':'https://cursos.alura.com.br/forum/subcategoria-java/sem-resposta/',
                      'JAVASCRIPT':'https://cursos.alura.com.br/forum/subcategoria-javascript/sem-resposta/',
                      'JQUERY':'https://cursos.alura.com.br/forum/subcategoria-jquery/sem-resposta/',
                      'SQL':'https://cursos.alura.com.br/forum/subcategoria-sql/sem-resposta/',
                      'GERAL':'https://cursos.alura.com.br/forum/sem-resposta/'}

def checkForDoubtsWithOutAnswer(seconds):
    while True:
        for secao, url in SECTIONS_TO_VERIFY.copy().items():
            result = urllib.request.urlopen(url)
            print('Verificando: '+url)

            soup = BeautifulSoup(result, 'html.parser')

            alert_message = soup.find('p', attrs={'class':'alert-message'})

            if not(alert_message):
                forumListItems = soup.find_all('li', attrs={'class':'forumList-item'})
                itemIds = ''
                for item in forumListItems:
                    m = re.search("-([a-zA-z-]+)-", item.get('itemid'))
                    itemIds += "\u00BB"+m.groups()[0] + "\n"

                ret_value = ctypes.windll.user32.MessageBoxW(0, "Existe(m) " + str(len(forumListItems)) +" dúvida(s) "
                                                             + "sem resposta na seção "+secao+".\n\n"
                                                             + itemIds
                                                             + "\n\nGostaria de abrir o link?"
                                                             , "Alura Notifier", 3)
                # 6 = YES
                if (ret_value == 6):
                    webbrowser.open(r"https://cursos.alura.com.br"+str(forumListItems[0].get('itemid'))) if ( (len(forumListItems)) == 1 ) else webbrowser.open(url)
                # 2 = CANCEL or EXIT
                elif (ret_value == 2):
                    sys.exit(0)
                # NO
                else:
                    SECTIONS_TO_VERIFY.pop(secao, None)
                    print('Próxima verificação: '+str(SECTIONS_TO_VERIFY))

                
    time.sleep(seconds)

checkForDoubtsWithOutAnswer(10)
