# Generated by Django 4.2.1 on 2023-06-18 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_comentario_post_comentarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_relacionados', to='core.post'),
        ),
    ]
