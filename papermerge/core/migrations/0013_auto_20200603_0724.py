# Generated by Django 3.0.6 on 2020-06-03 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200603_0607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kvstorecompitem',
            name='id',
        ),
        migrations.AddField(
            model_name='kvstorecompitem',
            name='kvstore_ptr',
            field=models.OneToOneField(auto_created=True, default='', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.KVStore'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kvstorecompitem',
            name='comp_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kvstore', to='core.KVStoreCompNode'),
        ),
        migrations.AlterField(
            model_name='kvstorecompnode',
            name='node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kvstorecomp', to='core.BaseTreeNode'),
        ),
    ]
