# Generated by Django 5.0.6 on 2025-03-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='软删除标志')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('email', models.EmailField(max_length=100, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=20, verbose_name='电话')),
                ('message', models.TextField(verbose_name='留言内容')),
            ],
            options={
                'verbose_name': '联系我们',
                'verbose_name_plural': '联系我们',
                'db_table': 'djs_contact',
            },
        ),
        migrations.AddField(
            model_name='about',
            name='metrics',
            field=models.JSONField(default=dict, verbose_name='关键数据'),
        ),
        migrations.AddField(
            model_name='about',
            name='milestones',
            field=models.JSONField(default=list, verbose_name='发展历程'),
        ),
        migrations.AddField(
            model_name='about',
            name='values',
            field=models.JSONField(default=list, verbose_name='价值观'),
        ),
    ]
