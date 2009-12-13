''' Tags usados para verificar las conecciones entre los usuarios
'''
from django import template

from microblog.models import Conexion

register = template.Library()

@register.filter_function
def tiene_conexion(user, amigo):
    return Conexion.objects.filter(
            user=user,
            amigo=amigo,
            ).count() >= 1

def do_get_microblog_connection(parser, token):
    """
    Example:
    {% get_microblog_connection between user and user_item as connection %}
    """
    try:
        tag_name, _between, vuser1, _and, vuser2, _as, vconnection = token.split_contents()
    except ValueError, e:
        raise template.TemplateSyntaxError, "%s requires arguments 'between', 'and' and 'as'" % token.split_contents()[0]

    return GetMicroblogConnection(vuser1, vuser2, vconnection)

class GetMicroblogConnection(template.Node):
    vuser1 = None
    vuser2 = None
    vconnection = None

    def __init__(self, vuser1, vuser2, vconnection):
        self.vuser1 = template.Variable(vuser1)
        self.vuser2 = template.Variable(vuser2)
        self.vconnection = vconnection

    def render(self, context):
        try:
            user1 = self.vuser1.resolve(context)
            user2 = self.vuser2.resolve(context)

            connection = Connection.objects.get(
                    user=user1,
                    friend=user2,
                    )
        except template.VariableDoesNotExist, e:
            connection = None
        except Connection.DoesNotExist, e:
            connection = None

        context[self.vconnection] = connection

        return ''

register.tag('get_microblog_connection', do_get_microblog_connection)
