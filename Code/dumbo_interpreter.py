import sys

if __name__ == '__main__':
    if len(sys.argv) == 4:
        # On lance le programme avec 3 argument(data, template et output), on va donc recuperer les 3 arguments
        arg1 = sys.argv[0]
        arg2 = sys.argv[1]
        arg3 = sys.argv[2]

        data = open(arg1, "r")
        template = open(arg2, "r")
        output = open(arg3, "r")

        #Puis on lance la fonction avec els 3 arguments et qui va permettre d'interpreter le data et template et d'ecrire ca dans output


    else:
        print("Erreur, il faut 3 arguments pour faire fonctionner le programme")
