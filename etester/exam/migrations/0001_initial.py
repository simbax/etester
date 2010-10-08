# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'QuestionBank'
        db.create_table('exam_questionbank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('question_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question_checked_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('paper_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('paper_checked_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('paper_publish_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('exam', ['QuestionBank'])

        # Adding model 'Question'
        db.create_table('exam_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exam.QuestionBank'])),
            ('qcon', self.gf('django.db.models.fields.TextField')()),
            ('qask', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('qkey', self.gf('django.db.models.fields.TextField')()),
            ('qscore', self.gf('django.db.models.fields.IntegerField')()),
            ('qchapter', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('qlevel', self.gf('django.db.models.fields.IntegerField')()),
            ('qtype', self.gf('django.db.models.fields.IntegerField')()),
            ('qexp', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('exam', ['Question'])

        # Adding model 'ExamPaper'
        db.create_table('exam_exampaper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('set_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('set_no', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('paper_type', self.gf('django.db.models.fields.IntegerField')()),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exam.QuestionBank'])),
            ('is_checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('exam', ['ExamPaper'])

        # Adding model 'ExamConfig'
        db.create_table('exam_examconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exam.ExamPaper'], null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exam.Question'], null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('exam', ['ExamConfig'])


    def backwards(self, orm):
        
        # Deleting model 'QuestionBank'
        db.delete_table('exam_questionbank')

        # Deleting model 'Question'
        db.delete_table('exam_question')

        # Deleting model 'ExamPaper'
        db.delete_table('exam_exampaper')

        # Deleting model 'ExamConfig'
        db.delete_table('exam_examconfig')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exam.examconfig': {
            'Meta': {'object_name': 'ExamConfig'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exam.ExamPaper']", 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exam.Question']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'exam.exampaper': {
            'Meta': {'ordering': "['-updated_time']", 'object_name': 'ExamPaper'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exam.QuestionBank']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paper_type': ('django.db.models.fields.IntegerField', [], {}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['exam.Question']", 'null': 'True', 'through': "'ExamConfig'", 'blank': 'True'}),
            'set_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'set_no': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'exam.question': {
            'Meta': {'ordering': "['-updated_time']", 'object_name': 'Question'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exam.QuestionBank']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'qask': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'qchapter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'qcon': ('django.db.models.fields.TextField', [], {}),
            'qexp': ('django.db.models.fields.TextField', [], {}),
            'qkey': ('django.db.models.fields.TextField', [], {}),
            'qlevel': ('django.db.models.fields.IntegerField', [], {}),
            'qscore': ('django.db.models.fields.IntegerField', [], {}),
            'qtype': ('django.db.models.fields.IntegerField', [], {}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exam.questionbank': {
            'Meta': {'ordering': "['-updated_time']", 'object_name': 'QuestionBank'},
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper_checked_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paper_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paper_publish_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question_checked_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['exam']
