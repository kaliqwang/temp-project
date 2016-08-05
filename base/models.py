from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator

################################################################################

mobile_validator = RegexValidator(
    regex=r'^\d{10}$', message='Enter a valid phone number')
student_id_validator = RegexValidator(
    regex=r'^\d{10}$', message='Enter a valid student id')
youtube_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_-]{11}$', message='Invalid YouTube video id')

class GetOrNoneManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

################################################################################

first_names = [
    # 70 male first names
    'Adam','Adrian','Alan','Alexander','Andrew','Anthony','Austin','Benjamin','Blake','Boris',
    'Brandon','Brian','Cameron','Charles','Christian','Christopher','Colin','Connor','Dan','David',
    'Dominic','Dylan','Edward','Eric','Evan','Frank','Gavin','Gordon','Harry','Ian',
    'Isaac','Jack','Jacob','Jake','James','Jason','Joe','John','Jonathan','Joseph',
    'Julian','Justin','Keith','Kevin','Leonard','Liam','Lucas','Luke','Matt','Max',
    'Michael','Nathan','Nicholas','Oliver','Paul','Peter','Phil','Richard','Robert','Ryan',
    'Sam','Sean','Sebastian','Stephen','Steven','Stewart','Thomas','Tim','Trevor','William',
    # 70 female first names
    'Abigail','Alexandra','Alison','Amanda','Amelia','Amy','Andrea','Angela','Anna','Anne',
    'Audrey','Ava','Bella','Caroline','Carolyn','Chloe','Claire','Diana','Dorothy','Elizabeth',
    'Ella','Emily','Emma','Faith','Felicity','Gabrielle','Grace','Hannah','Heather','Irene',
    'Jane','Jasmine','Jennifer','Jessica','Joan','Julia','Karen','Katherine','Kimberly','Kylie',
    'Lauren','Leah','Lillian','Lily','Lisa','Madeleine','Maria','Mary','Megan','Melanie',
    'Michelle','Molly','Natalie','Nicola','Olivia','Penelope','Rachel','Rebecca','Rose','Samantha',
    'Sarah','Sonia','Sophie','Stephanie','Theresa','Vanessa','Victoria','Virginia','Wendy','Zoe',
]

last_names = [
    # 140 last names
    'Abraham','Allan','Anderson','Arnold','Avery','Bailey','Baker','Ball','Bell', 'Berry',
    'Black','Blake','Bower','Brown','Buckland','Burgess','Butler','Cameron','Campbell','Chapman',
    'Churchill','Clark','Clarkson','Coleman','Davidson','Davies','Dickens','Dowd','Duncan','Dyer',
    'Edmunds','Ellison','Ferguson','Fisher','Forsyth','Fraser','Gibson','Gill','Glover','Graham',
    'Grant','Gray','Greene','Hamilton','Harris','Hart','Hemmings','Henderson','Hill','Howard',
    'Hudson','Hughes','Hunter','Jackson','James','Johnston','Jones','Kelly','Kerr','King',
    'Knox','Lambert','Lawrence','Lee','Lewis','Lyman','MacDonald','Mackay','Mackenzie','Manning',
    'Marshall','Martin','Mathis','May','McDonald','McLean','McGrath','Metcalfe','Miller','Mills',
    'Mitchell','Morgan','Morrison','Murray','Nash','Newman','Nolan','North','Ogden','Oliver',
    'Paige','Parr','Parsons','Paterson','Payne','Peake','Peters','Piper','Poole','Powell',
    'Pullman','Quinn','Rampling','Randall','Rees','Reid','Roberts','Robertson','Ross','Russell',
    'Rutherford','Sanderson','Scott','Sharp','Short','Simpson','Skinner','Slater','Smith','Springer',
    'Stewart','Sutherland','Taylor','Terry','Thomson','Tucker','Turner','Underwood','Vance','Vaughan',
    'Walker','Wallace','Walsh', 'Watson','Welch','White','Wilkins','Wilson','Wright','Young',
]

lorem_random = [
    # First 100 words are capitalized
    'Lorem','Ipsum','Dolor','Sit','Amet','Consectetur','Adipiscing','Elit','Donec','Vel',
    'Facilisis','Mi','Imperdiet','Hendrerit','Est','Nam','Venenatis','Magna','Semper','Libero',
    'Pretium','A','Lacinia','Nisl','Varius','Ut','Velit','Vitae','Viverra','Nibh',
    'Sed','Eleifend','Volutpat','Placerat','Duis','Eu','Tortor','Nec','Mauris','Aliquam',
    'Ac','Urna','In','Metus','Augue','Ultrices','At','Felis','Gravida','Fermentum',
    'Etiam','Fringilla','Purus','Congue','Eget','Turpis','Condimentum','Id','Luctus','Lacus',
    'Commodo','Porta','Lectus','Vehicula','Nulla','Odio','Erat','Maximus','Et','Sodales',
    'Tellus','Sapien','Duis','Integer','Dictum','Rhoncus','Nunc','Neque','Dui','Suscipit',
    'Aliquet','Rutrum','Vestibulum','Tristique','Sem','Enim','Accumsan','Eros','Non','Curabitur',
    'Laoreet','Quis','Sagittis','Nisi','Efficitur','Auctor','Fusce','Blandit','Pharetra','Leo',
     # Second 100 words are lowercase
    'lorem','ipsum','dolor','sit','amet','consectetur','adipiscing','elit','integer','felis',
    'in','egestas','vitae','malesuada','nisi','proin','pellentesque','est','nec','luctus',
    'vestibulum','et','metus','at','dui','efficitur','iaculis','a','eleifend','massa',
    'morbi','elementum','eget','leo','ornare','vel','nunc','placerat','odio','ut',
    'tincidunt','pulvinar','curabitur','mauris','viverra','eu','id','laoreet','mattis','donec',
    'erat','facilisis','porttitor','nibh','fringilla','turpis','arcu','sem','molestie','quis',
    'libero','sed','euismod','fermentum','ultrices','porta','accumsan','neque','nam','quam',
    'posuere','quisque','dapibus','nisl','ac','nulla','facilisi','nullam','ligula','bibendum',
    'diam','dapibus','augue','varius','maecenas','risus','semper','dignissim','aliquam','sodales',
    'pretium','ante','ullamcorper','suscipit','condimentum','tortor','cursus','praesent','non','eros',
]

random_videos = [
    # 20 total
    "mT0DpuAlJbs", "_yhf_PvRGIE", "LKiDgFySXg8", "zMN9otsaZ80", "cb1Jp-rFJDI",
    "gGrXEewfz34", "6QdOI4zZC0g", "LWgqWuJG5Jg", "Z1lpZRe7-R8", "Kkr9hf9d8Fo",
    "s1exvkLxQi8", "T7iiwsT5hWg", "eZ5C7dfU6-A", "pmhqMajav8Y", "8SF1Wt__W6g",
    "oQq9vDU4IfU", "wLXVDzM8Tnk", "V3i0eOfchxg", "BG9rW-hYikw", "4SxWtQzL6js",
]

################################################################################

# CURRENTLY UNUSED
#
# periods = (
#     ('1', 'Period 1'),
#     ('2', 'Period 2'),
#     ('3', 'Period 3'),
#     ('4', 'Period 4'),
#     ('5a','Period 5A'),
#     ('5b','Period 5B'),
#     ('6', 'Period 6'),
#     ('7', 'Period 7'),
# )
#
# class Subject(models.Model):
#     subject = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.subject
#
# class Class(models.Model):
#     subject = models.ForeignKey('Subject', related_name='classes', blank=True, null=True, on_delete=models.SET_NULL)
#     teacher = models.ForeignKey('TeacherProfile', related_name='classes', blank=True, null=True)
#     room = models.CharField('Room Number', max_length=6)
#     period = models.CharField(max_length=2, choices=periods)
#     is_honors = models.BooleanField(default=False)
#     is_ap = models.BooleanField(default=False)
#     is_dual = models.BooleanField(default=False)
#
#     def __str__(self):
#         return '%s - %s' % (self.subject, self.teacher)
#
#     class Meta:
#         unique_together = ('teacher', 'period')
#
# class Schedule(models.Model):
#     #TODO: validate overlapping classes by period
#     classes = models.ManyToManyField(Class, related_name='schedules_included')
#
#     def __str__(self):
#         return '%s\'s Schedule' % self.user
