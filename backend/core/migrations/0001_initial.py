# Generated by Django 5.0.2 on 2024-02-10 02:00

import core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('business_value', models.CharField(blank=True, max_length=200, verbose_name='business value')),
                ('type', models.CharField(choices=[('PR', 'Primary'), ('SP', 'Support')], default='SP', max_length=2, verbose_name='type')),
                ('is_published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
            },
        ),
        migrations.CreateModel(
            name='ComplianceAssessment',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('version', models.CharField(blank=True, default='1.0', help_text='Version of the compliance assessment (eg. 1.0, 2.0, etc.)', max_length=100, null=True, verbose_name='Version')),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('in_progress', 'In progress'), ('in_review', 'In review'), ('done', 'Done'), ('deprecated', 'Deprecated')], default='planned', max_length=100, verbose_name='Status')),
                ('eta', models.DateField(blank=True, help_text='Estimated time of arrival', null=True, verbose_name='ETA')),
                ('due_date', models.DateField(blank=True, help_text='Due date', null=True, verbose_name='Due date')),
                ('result', models.CharField(blank=True, choices=[('compliant', 'Compliant'), ('non_compliant_minor', 'Non compliant (minor)'), ('non_compliant_major', 'Non compliant (major)'), ('not_applicable', 'Not applicable')], max_length=100, null=True, verbose_name='Result')),
            ],
            options={
                'verbose_name': 'Compliance assessment',
                'verbose_name_plural': 'Compliance assessments',
            },
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('attachment', models.FileField(blank=True, help_text='Attachment for evidence (eg. screenshot, log file, etc.)', null=True, upload_to='', validators=[core.validators.validate_file_size, core.validators.validate_file_name], verbose_name='Attachment')),
                ('link', models.URLField(blank=True, help_text='Link to the evidence (eg. Jira ticket, etc.)', null=True, verbose_name='Link')),
            ],
            options={
                'verbose_name': 'Evidence',
                'verbose_name_plural': 'Evidences',
            },
        ),
        migrations.CreateModel(
            name='Framework',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('provider', models.CharField(blank=True, max_length=200, null=True, verbose_name='Provider')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
            ],
            options={
                'verbose_name': 'Framework',
                'verbose_name_plural': 'Frameworks',
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
                ('copyright', models.CharField(blank=True, max_length=4096, null=True, verbose_name='Copyright')),
                ('version', models.IntegerField(verbose_name='Version')),
                ('provider', models.CharField(blank=True, help_text='Provider of the library', max_length=100, null=True, verbose_name='Provider')),
                ('packager', models.CharField(blank=True, help_text='Packager of the library', max_length=100, null=True, verbose_name='Packager')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('internal_reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Internal reference')),
                ('lc_status', models.CharField(choices=[('undefined', '--'), ('in_design', 'Design'), ('in_dev', 'Development'), ('in_prod', 'Production'), ('eol', 'End Of Life'), ('dropped', 'Dropped')], default='in_design', max_length=20, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='RequirementAssessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('status', models.CharField(choices=[('to_do', 'To do'), ('in_progress', 'In progress'), ('non_compliant', 'Non compliant'), ('partially_compliant', 'Partially compliant'), ('compliant', 'Compliant'), ('not_applicable', 'Not applicable')], default='to_do', max_length=100, verbose_name='Status')),
                ('observation', models.TextField(blank=True, null=True, verbose_name='Observation')),
            ],
            options={
                'verbose_name': 'Requirement assessment',
                'verbose_name_plural': 'Requirement assessments',
            },
        ),
        migrations.CreateModel(
            name='RequirementLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('provider', models.CharField(blank=True, max_length=200, null=True, verbose_name='Provider')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
                ('level', models.IntegerField(verbose_name='Level')),
            ],
            options={
                'verbose_name': 'Requirements level',
                'verbose_name_plural': 'Requirements levels',
            },
        ),
        migrations.CreateModel(
            name='RequirementNode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('provider', models.CharField(blank=True, max_length=200, null=True, verbose_name='Provider')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
                ('parent_urn', models.CharField(blank=True, max_length=100, null=True, verbose_name='Parent URN')),
                ('order_id', models.IntegerField(null=True, verbose_name='Order ID')),
                ('level', models.IntegerField(null=True, verbose_name='Level')),
                ('maturity', models.IntegerField(null=True, verbose_name='Maturity')),
                ('assessable', models.BooleanField(verbose_name='Assessable')),
            ],
            options={
                'verbose_name': 'RequirementNode',
                'verbose_name_plural': 'RequirementNodes',
            },
        ),
        migrations.CreateModel(
            name='RiskAcceptance',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('state', models.CharField(choices=[('created', 'Created'), ('submitted', 'Submitted'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('revoked', 'Revoked')], default='created', max_length=20, verbose_name='State')),
                ('expiry_date', models.DateField(help_text='Specify when the risk acceptance will no longer apply', null=True, verbose_name='Expiry date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('accepted_at', models.DateTimeField(blank=True, null=True, verbose_name='Acceptance date')),
                ('rejected_at', models.DateTimeField(blank=True, null=True, verbose_name='Rejection date')),
                ('revoked_at', models.DateTimeField(blank=True, null=True, verbose_name='Revocation date')),
                ('justification', models.CharField(blank=True, max_length=500, null=True, verbose_name='Justification')),
            ],
            options={
                'verbose_name': 'Risk acceptance',
                'verbose_name_plural': 'Risk acceptances',
                'permissions': [('approve_riskacceptance', 'Can validate/rejected risk acceptances')],
            },
        ),
        migrations.CreateModel(
            name='RiskAssessment',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('version', models.CharField(blank=True, default='1.0', help_text='Version of the compliance assessment (eg. 1.0, 2.0, etc.)', max_length=100, null=True, verbose_name='Version')),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('in_progress', 'In progress'), ('in_review', 'In review'), ('done', 'Done'), ('deprecated', 'Deprecated')], default='planned', max_length=100, verbose_name='Status')),
                ('eta', models.DateField(blank=True, help_text='Estimated time of arrival', null=True, verbose_name='ETA')),
                ('due_date', models.DateField(blank=True, help_text='Due date', null=True, verbose_name='Due date')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Risk assessment',
                'verbose_name_plural': 'Risk assessments',
            },
        ),
        migrations.CreateModel(
            name='RiskMatrix',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
                ('json_definition', models.JSONField(default=dict, help_text='JSON definition of the risk matrix.         See the documentation for more information.', verbose_name='JSON definition')),
                ('is_enabled', models.BooleanField(default=True, help_text='If the risk matrix is set as disabled, it will not be available for selection for new risk assessments.', verbose_name='enabled')),
                ('provider', models.CharField(blank=True, max_length=200, null=True, verbose_name='Provider')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RiskScenario',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('existing_measures', models.TextField(blank=True, help_text='The existing security measures to manage this risk. Edit the risk scenario to add extra security measures.', max_length=2000, verbose_name='Existing measures')),
                ('current_proba', models.SmallIntegerField(default=-1, verbose_name='Current probability')),
                ('current_impact', models.SmallIntegerField(default=-1, verbose_name='Current impact')),
                ('current_level', models.SmallIntegerField(default=-1, help_text='The risk level given the current measures. Automatically updated on Save, based on the chosen risk matrix', verbose_name='Current level')),
                ('residual_proba', models.SmallIntegerField(default=-1, verbose_name='Residual probability')),
                ('residual_impact', models.SmallIntegerField(default=-1, verbose_name='Residual impact')),
                ('residual_level', models.SmallIntegerField(default=-1, help_text='The risk level when all the extra measures are done. Automatically updated on Save, based on the chosen risk matrix', verbose_name='Residual level')),
                ('treatment', models.CharField(choices=[('open', 'Open'), ('mitigate', 'Mitigate'), ('accept', 'Accept'), ('avoid', 'Avoid'), ('transfer', 'Transfer')], default='open', max_length=20, verbose_name='Treatment status')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('strength_of_knowledge', models.CharField(choices=[('--', '--'), ('0', 'Low'), ('1', 'Medium'), ('2', 'High')], default='--', max_length=20, verbose_name='Strength of Knowledge')),
                ('justification', models.CharField(blank=True, max_length=500, null=True, verbose_name='Justification')),
            ],
            options={
                'verbose_name': 'Risk scenario',
                'verbose_name_plural': 'Risk scenarios',
            },
        ),
        migrations.CreateModel(
            name='SecurityFunction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('provider', models.CharField(blank=True, max_length=200, null=True, verbose_name='Provider')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
                ('category', models.CharField(blank=True, choices=[('policy', 'Policy'), ('process', 'Process'), ('technical', 'Technical'), ('physical', 'Physical')], max_length=20, null=True, verbose_name='Category')),
                ('typical_evidence', models.JSONField(blank=True, null=True, verbose_name='Typical evidence')),
                ('is_published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'verbose_name': 'Security function',
                'verbose_name_plural': 'Security functions',
            },
        ),
        migrations.CreateModel(
            name='SecurityMeasure',
            fields=[
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(blank=True, choices=[('policy', 'Policy'), ('process', 'Process'), ('technical', 'Technical'), ('physical', 'Physical')], max_length=20, null=True, verbose_name='Category')),
                ('status', models.CharField(blank=True, choices=[('planned', 'Planned'), ('active', 'Active'), ('inactive', 'Inactive')], max_length=20, null=True, verbose_name='Status')),
                ('eta', models.DateField(blank=True, help_text='Estimated Time of Arrival', null=True, verbose_name='ETA')),
                ('expiry_date', models.DateField(blank=True, help_text='Date after which the security measure is no longer valid', null=True, verbose_name='Expiry date')),
                ('link', models.CharField(blank=True, help_text='External url for action follow-up (eg. Jira ticket)', max_length=1000, null=True, verbose_name='Link')),
                ('effort', models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra-Large')], help_text='Relative effort of the measure (using T-Shirt sizing)', max_length=2, null=True, verbose_name='Effort')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Security measure',
                'verbose_name_plural': 'Security measures',
            },
        ),
        migrations.CreateModel(
            name='Threat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('urn', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='URN')),
                ('ref_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference ID')),
                ('locale', models.CharField(default='en', max_length=100, verbose_name='Locale')),
                ('default_locale', models.BooleanField(default=True, verbose_name='Default locale')),
                ('provider', models.CharField(blank=True, max_length=200, null=True, verbose_name='Provider')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('annotation', models.TextField(blank=True, null=True, verbose_name='Annotation')),
                ('is_published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'verbose_name': 'Threat',
                'verbose_name_plural': 'Threats',
            },
        ),
    ]
