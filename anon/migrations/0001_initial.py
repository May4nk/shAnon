# Generated by Django 3.2.6 on 2021-09-20 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.TextField(max_length=20)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('contact', models.IntegerField(blank=True, null=True)),
                ('pic', models.CharField(blank=True, max_length=500)),
                ('reset_link', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('first', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first', to=settings.AUTH_USER_MODEL)),
                ('second', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('first', 'second')},
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.CharField(max_length=500)),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('tag', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('likes', models.ManyToManyField(related_name='suser_likes', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('saved', models.ManyToManyField(related_name='suser_saved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatmsg', to='anon.chat')),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmnt', models.CharField(max_length=300)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='anon.post')),
            ],
        ),
    ]
