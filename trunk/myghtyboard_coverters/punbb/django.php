<?PHP
define('PUN_ROOT', './'); // ścieżka do skryptu forum
require PUN_ROOT.'include/common.php';
ob_start();
echo '# -*- coding: utf-8 -*-
from os import environ
environ[\'DJANGO_SETTINGS_MODULE\'] = \'settings\'
from django.contrib.auth.models import User, Group
from settings import *
';
IF($result = $db->query("SELECT * FROM ".$db->prefix."users WHERE id > 2 AND num_posts > 10 ORDER BY last_post DESC"))
	{
	echo 'User.objects.filter(id__gt=1).delete()'."\n";
	while ($row = $db->fetch_assoc($result))
		{
		echo 'us = User(username="'.$row['username'].'", first_name="'.$row['username'].'", last_name="'.$db->escape($row['username']).'", email="'.$row['email'].'", password="sha1$$'.$row['password'].'", is_staff="0", is_active="1", is_superuser="0", last_login="2006-08-29 20:00:34", date_joined="2006-08-29 20:00:34")'."\n";
		echo 'us.save()'."\n";
		echo 'us.groups.add(Group.objects.get(name=\'users\'))'."\n";
		}
	}


IF($result = $db->query("SELECT * FROM ".$db->prefix."categories"))
	{
	echo "\n\n".'from myghtyboard.models import *',"\n".'Category.objects.all().delete()'."\n";
	while ($row = $db->fetch_assoc($result))
		{
echo 'mc = Category(cat_name=\'\'\''.$row['cat_name'].'\'\'\', cat_order=\'\'\''.$row['disp_position'].'\'\'\')
mc.save()'."\n";
		}
	}

IF($result = $db->query("SELECT * FROM ".$db->prefix."forums"))
	{
	echo "\n\n".'Forum.objects.all().delete()'."\n";
	while ($row = $db->fetch_assoc($result))
		{
echo 'mf = Forum(id = \'\'\''.$row['id'].'\'\'\', forum_category = Category.objects.get(id='.$row['cat_id'].'), forum_name = \'\'\''.$row['forum_name'].'\'\'\', forum_description =\'\'\''.$row['forum_desc'].'\'\'\', forum_order=\'\'\''.$row['disp_position'].'\'\'\', forum_posts=\'\'\''.$row['num_posts'].'\'\'\', forum_topics = \'\'\''.$row['num_topics'].'\'\'\')
mf.save()'."\n";
		}
	}
	
IF($result = $db->query("SELECT * FROM ".$db->prefix."topics"))
	{
	echo "\n\n".'Topic.objects.all().delete()'."\n";
	while ($row = $db->fetch_assoc($result))
		{
echo 'mt = Topic(id = \'\'\''.$row['id'].'\'\'\', topic_forum = Forum.objects.get(id='.$row['forum_id'].'), topic_name = \'\'\''.$row['subject'].'\'\'\', topic_author =  \'\'\''.$row['poster'].'\'\'\', topic_posts =  \'\'\''.$row['num_replies'].'\'\'\', topic_modification_date =  \'\'\''.date("Y-m-d H:i:s", $res['posted']).'\'\'\')
mt.save()'."\n";
		}
	}

IF($result = $db->query("SELECT * FROM ".$db->prefix."posts"))
	{
	echo "\n\n".'Post.objects.all().delete()'."\n";
	while ($row = $db->fetch_assoc($result))
		{
		$row['message'] = nl2br($row['message']);
		$row['message'] = str_replace("\n", '', $row['message']);
		$row['message'] = $db->escape(str_replace("\n\r", '', $row['message']));
echo 'mp = Post(post_topic = Topic.objects.get(id='.$row['topic_id'].'), post_text = \'\'\''.$row['message'].'\'\'\', post_author = \'\'\''.$row['poster'].'\'\'\', post_date = \'\'\''.date("Y-m-d H:i:s", $res['posted']).'\'\'\', post_ip = \'1.2.3.4\')
mp.save()'."\n";
		}
	}
$wynik = ob_get_contents();
ob_end_clean();
file_put_contents('install_1.py', $wynik);
echo '<h1>install_1.py should be ready</h1>';
?>