import urllib.request
from bs4 import BeautifulSoup
import ctypes
import time
import webbrowser
import sys
import re

SECTIONS_TO_VERIFY = {#'JAVA':'https://cursos.alura.com.br/forum/subcategoria-java/sem-resposta/',
                      #'JAVASCRIPT':'https://cursos.alura.com.br/forum/subcategoria-javascript/sem-resposta/',
                      #'JQUERY':'https://cursos.alura.com.br/forum/subcategoria-jquery/sem-resposta/',
                      #'SQL':'https://cursos.alura.com.br/forum/subcategoria-sql/sem-resposta/',
                      #'GERAL':'https://cursos.alura.com.br/forum/sem-resposta/',
                      'FRONT-END':'https://cursos.alura.com.br/forum/categoria-front-end/sem-resposta/',
                      'OFF-TOPIC':'https://cursos.alura.com.br/forum/categoria-offtopic/sem-resposta/',
                      'INFRAESTRUTURA':'https://cursos.alura.com.br/forum/categoria-infraestrutura/sem-resposta/',
                      'PROGRAMACAO':'https://cursos.alura.com.br/forum/categoria-programacao/sem-resposta/',
                      'MOBILE':'https://cursos.alura.com.br/forum/categoria-mobile/sem-resposta/',
                      'DESIGN & UX':'https://cursos.alura.com.br/forum/categoria-design-ux/sem-resposta/',
                      'BUSINESS':'https://cursos.alura.com.br/forum/categoria-business/sem-resposta/'}

def checkForDoubtsWithOutAnswer(seconds):
    topicosVistos = []
    topicoNovo = True
    while ( len(SECTIONS_TO_VERIFY) > 0 ):
        for secao, url in SECTIONS_TO_VERIFY.copy().items():
            result = urllib.request.urlopen(url)
            print('>>Verificando '+ secao +'<<')

            soup = BeautifulSoup(result, 'html.parser')

            alert_message = soup.find('p', attrs={'class':'alert-message'})

            if not(alert_message):
                forumListItems = soup.find_all('li', attrs={'class':'forumList-item'})
                itemIds = ''
                for item in forumListItems:
                    match = re.search("-([a-zA-z-]+)-", item.get('itemid')).groups()[0]
                    itemIds += "\u00BB"+ match + "\n"

                    if match not in topicosVistos:
                        topicosVistos.append(match)
                        topicoNovo = True

                if (topicoNovo == False):
                    continue
                
                topicoNovo = False
                
                print(topicosVistos)
                ret_value = ctypes.windll.user32.MessageBoxW(0, "Existe(m) " + str(len(forumListItems)) +" dúvida(s) "
                                                             + "sem resposta na seção "+ secao +".\n\n"
                                                             + itemIds
                                                             + "\n\nGostaria de abrir o link?"
                                                             , "Alura Notifier", 3)
                print('Foram encontradas %s dúvidas em %s' % (len(forumListItems), secao))
                
                # 6 = YES
                if (ret_value == 6):
                    webbrowser.open(r"https://cursos.alura.com.br"+ str(forumListItems[0].get('itemid'))) if ( (len(forumListItems)) == 1 ) else webbrowser.open(url)
                    print('=>Seção %s acessada' % secao)
                # 2 = CANCEL or EXIT
                elif (ret_value == 2):
                    finalizarPrograma('Cancel clicado, terminando programa.')
                # NO
                else:
                    #SECTIONS_TO_VERIFY.pop(secao, None)
                    #print('->%s foi removido da lista de monitoramento' % secao)
                    print('Próxima verificação: %s' % SECTIONS_TO_VERIFY.keys())
            else:
                print('Nenhuma dúvida sem resposta na seção %s' % secao)
        
        print('Esperando %s segundos para executar a próxima busca...\n' % seconds)        
        time.sleep(seconds)
    finalizarPrograma('Nada para verificar, terminando programa.')

def finalizarPrograma(msg):
    print(msg)
    sys.exit(0)

checkForDoubtsWithOutAnswer(5)
