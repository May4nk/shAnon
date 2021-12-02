from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self,name,email,username,password=None):
        if not email:
            raise ValueError('User must have an email.')
        if not username:
            raise ValueError('User must have an username.')
        if not name:
            raise ValueError('User must have an name.')
        user = self.model(
                email=self.normalize_email(email),
                name=name,
                username=username,
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,password,name):
        user = self.create_user(
                email=self.normalize_email(email),
                name=name,
                username=username,
                password=password,
                    )
        user.is_staff = True    
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
            

class Suser(AbstractBaseUser):
    name = models.TextField(max_length=20)
    usrname_validator = RegexValidator(regex='[a-zA-Z0-9_]+')
    username = models.CharField(max_length=30,unique=True,validators=[usrname_validator])
    birth_date = models.DateField(null=True,blank=True)
    email = models.EmailField(max_length=50,unique=True)
    psswd_validator = RegexValidator(regex='[a-zA-Z0-9_@#!$,]{7,}')
    password = models.CharField(max_length=30,validators=[psswd_validator])
    contact = models.IntegerField(blank=True,null=True)
    pic = models.CharField(max_length=500,blank=True)
    reset_link = models.CharField(max_length=50,blank=True,null=True)
    status = models.CharField(max_length=255,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','email']
    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Post(models.Model):
    owner = models.ForeignKey(Suser,on_delete=models.CASCADE)
    pic = models.CharField(max_length=500)
    caption = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    tag = models.CharField(max_length=50,blank=True,null=True)
    likes = models.ManyToManyField(Suser,related_name='suser_likes')
    saved = models.ManyToManyField(Suser,related_name='suser_saved')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(Suser,on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(Suser,on_delete=models.CASCADE,related_name='following')
    perm = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
   

class Comments(models.Model):
    owner = models.ForeignKey(Suser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    cmnt = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Chat(models.Model):
    first = models.ForeignKey(Suser,on_delete=models.CASCADE,blank=True, null=True,related_name='first')
    second = models.ForeignKey(Suser,on_delete=models.CASCADE,blank=True, null=True,related_name='second')
    updated = models.DateTimeField(auto_now =True)
    created = models.DateTimeField(auto_now_add =True)
    
    class Meta:
        unique_together = ['first','second']

class Messages(models.Model):
    thread = models.ForeignKey(Chat,on_delete=models.CASCADE,blank=True, null=True,related_name='chatmsg')
    usr = models.ForeignKey(Suser,on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add =True)
