from django.contrib.auth.models import AbstractUser
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from crum import get_current_request

class User(AbstractUser):
    imagen=models.ImageField(upload_to='users/%Y/%m/%d',null=True,blank=True)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/usuario.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions ', 'last_login']) #Me permite obtener un diccionario a partir del modelo que se le enví
        if self.last_login:
            item['last_login']=self.last_login.strftime('%Y-%m-%d')
        item['date_joined']=self.date_joined.strftime('%Y-%m-%d')
        item['imagen']=self.get_image()
        item['full_name']=self.get_full_name()
        item['groups']=[{'id':g.id, 'name':g.name}for g  in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0] #Seleecionar el primer perfil de usuario
        except:
            pass


        

