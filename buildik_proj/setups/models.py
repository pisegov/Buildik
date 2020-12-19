from django.db import models
from pccomponents.models import Item
from users.models import User

class Setup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f'{self.name}'
        # return f'{self.user.username} : {self.name}'

class SetupItem(models.Model):
    setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ['setup', 'item']
    
    def __str__(self):
        return f'{self.setup.name} : {str(self.item)} : {self.number}'
        # user = User.objects.get(setup=self.setup)
        # return f'{user.username} : {self.setup.name} : {str(self.item)} : {self.number}'