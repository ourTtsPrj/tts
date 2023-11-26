# Generated by Django 4.2.5 on 2023-11-26 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='classModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=128)),
                ('classDes', models.CharField(max_length=128)),
                ('classPass', models.CharField(max_length=32)),
                ('classCode', models.IntegerField()),
                ('classOwner', models.IntegerField()),
                ('classMakeTime', models.IntegerField()),
                ('classMemberLen', models.IntegerField()),
                ('classHasActiveSession', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='classSessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classSessionClassCode', models.IntegerField()),
                ('classSessionSessionCode', models.IntegerField()),
                ('classSessionStutus', models.CharField(max_length=10)),
                ('classSessionOpenTime', models.IntegerField()),
                ('classSessionOpenUntil', models.IntegerField()),
                ('classSessionHowManyUserDetect', models.IntegerField()),
                ('classSessionHowManyUserRecord', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='sessionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionImageClassCode', models.IntegerField()),
                ('sessionImageSessionCode', models.IntegerField()),
                ('sessionImageImage', models.CharField(max_length=30)),
                ('sessionImageFaceJson', models.TextField(default='', max_length=65535)),
                ('sessionImageTime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='sessionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionLogClassCode', models.IntegerField()),
                ('sessionLogSessionCode', models.IntegerField()),
                ('sessionLogStdCode', models.IntegerField()),
                ('sessionLogFaceCode', models.IntegerField()),
                ('sessionLogFaceDes', models.CharField(max_length=6000)),
                ('sessionLogTime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='whoWhereModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whoWhereFirstName', models.CharField(max_length=70)),
                ('whoWhereLastName', models.CharField(max_length=70)),
                ('whoWhereStdCode', models.IntegerField()),
                ('whoWhereClassCode', models.IntegerField()),
                ('whoWhereJoinedTime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('stdcode', models.IntegerField(unique=True)),
                ('firstName', models.CharField(max_length=70)),
                ('lastName', models.CharField(max_length=70)),
                ('joinTime', models.IntegerField()),
                ('lastLogin', models.IntegerField()),
                ('rank', models.CharField(max_length=50)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
