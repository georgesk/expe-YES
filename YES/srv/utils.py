from django.utils.translation import ugettext as _

class Element:
    """
    defines some active HTML element to drive experiments
    """
    def __init__(self,**kw):
        """
        Constructor
        @param kw a dictionnary to build the object;
        useful keys are: name, label, action, description
        """
        self.name=kw.get("name",_("No_name"))
        self.label=kw.get("label",_("No_label"))
        self.description=kw.get("description",_("no description"))
        self.action="""$.ajax("{0}?"+elParams("{1}")).done(function(data){{message("Succès : {0} --> "+JSON.stringify(data, null, 2).replace(/\\n/g,"<br/>").replace(/ /g,"&nbsp;"), document.success)}}).fail(function(data){{message("Échec : {0}",document.failure)}})""".format(kw.get("action","action0"),self.name)

class Button(Element):
    """
    Defines an active button to drive experiments
    """
        
    def __init__(self,**kw):
        """
        Constructor
        @param kw a dictionnary to build the object;
        useful keys are: name, label, action, description
        """
        Element.__init__(self,**kw)
        # no more attributes
        return
    
    def __str__(self):
        return "<button name='{name}' onclick='{action}'>{label}</button> {description}".format(**self.__dict__)
    
class Range:
    """
    Defines an active range input to drive experiments
    """
    def __init__(self,**kw):
        """
        Constructor
        @param kw a dictionary to build the object;
        useful keys are:
        name, label, action, description, minval, maxval, step, value
        """
        Element.__init__(self,**kw)
        self.minval=int(kw.get("minval","0"))
        self.maxval=int(kw.get("maxval","10"))
        self.value=int(kw.get("value","5"))
        self.step=int(kw.get("step","1"))

    def __str__(self):
        return """
<div class="range">
  <div class="description">
    <strong>{label}</strong> {description}
  </div>
  <div class="range_input">
    <input type="range" name='{name}'
           min='{minval}' max='{maxval}' value='{value}' step='{step}'
           onchange='{action}'/>
  </div>
</div>
""".format(**self.__dict__)
    
