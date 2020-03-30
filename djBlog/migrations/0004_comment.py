# Generated by Django 3.0.4 on 2020-03-28 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djBlog', '0003_auto_20200328_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djBlog.Comment', verbose_name='Parent Comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='djBlog.Post', verbose_name='Comment')),
            ],
        ),
    ]