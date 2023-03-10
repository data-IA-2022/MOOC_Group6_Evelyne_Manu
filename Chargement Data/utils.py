from colorama import Fore, Back, Style

def factorielle(n):
    if n==1:
        return 1
    result = n * factorielle(n-1)
    print(f"{n}! = {result}")
    return result

def recur_message(msg, f, parent_id=None):
    '''
    Cette fonction fait un traitement messages de l'objet JSON passé
    :param obj: objet JSON contiens un MESSAGE
    :param f: fonctions à appeler
    :return:
    '''
    #print("Recurse ", obj['id'], obj['depth'] if 'depth' in obj else '-')
    f(msg, parent_id)
    
    # try:
    if 'children' in msg:
        for child in msg['children']:
            recur_message(child, f, parent_id=msg['id'])
    if 'non_endorsed_responses' in msg:
        for child in msg['non_endorsed_responses']:
            recur_message(child, f, parent_id=msg['id'])
    if 'endorsed_responses' in msg:
        for child in msg['endorsed_responses']:
            recur_message(child, f, parent_id=msg['id'])
    # except:
    #     print("----------------------------------------------------------------------")  
    #     print(f"error recur_message --> {msg['id']}  !!!!")  
    #     print("----------------------------------------------------------------------")   

def nombre_messages(obj):
    '''
    Cette fonction doit retourner le nombre de messages de l'objet JSON passé
    :param obj: objet JSON contiens un MESSAGE
    :return: Nombre de messages trouvés
    '''
    cumul = 1
    depth = obj['depth'] if 'depth' in obj else -1
    print(f"{'  ' * (depth+1)}id: {Fore.RED}{obj['id']}{Style.RESET_ALL}, depth: {depth}, count: {obj['comments_count'] if 'comments_count' in obj else '-'}")
    if 'children' in obj:
        for msg in obj['children']:
            cumul += nombre_messages(msg)
    if 'non_endorsed_responses' in obj:
        for msg in obj['non_endorsed_responses']:
            cumul += nombre_messages(msg)
    if 'endorsed_responses' in obj:
        for msg in obj['endorsed_responses']:
            cumul += nombre_messages(msg)
    print(f"id: {obj['id']} : {cumul} messages")
    return cumul