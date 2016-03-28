def protectQuote(s):
    return s.replace("'",r"\'")

class Button:
    """
    Définition d'un bouton actif pour commander les expériences
    """
    def __init__(self,**kw):
        """
        Le constructeur
        param kw un dictionnaire permettant de contruire l'objet ;
        les clés utiles sont name, html, action
        """
        self.name=kw.get("name","Sans_Nom")
        self.html=kw.get("html","???")
        self.action="$.ajax(\"{0}\").done(function(data){{message(\"Succès : {0} --> \"+data,document.success)}}).fail(function(data){{message(\"Échec : {0}\",document.failure)}})".format(kw.get("action","action0"))

    def __str__(self):
        return "<button name='{name}' onclick='{action}'>{html}</button>".format(**self.__dict__)
    
