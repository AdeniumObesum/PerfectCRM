from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

# Create your models here.


class Customer(models.Model):
    '''客户信息表'''
    name = models.CharField(max_length=32, blank=True, null=True,verbose_name='姓名')
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    id_num = models.CharField(max_length=64, blank=True, null=True,verbose_name='证件号')
    email = models.CharField(max_length=64, blank=True, null=True,verbose_name='常用邮箱')
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '官网'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),
                      (6, '市场推广'))
    status_choices = ((0,'未报名'),
                      (1,'已报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices,default=0)
    derive = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(verbose_name="转介绍人QQ", max_length=64, null=True,blank=True)
    consult_course = models.ForeignKey("Course", verbose_name="咨询课程", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="咨询详情",null=True,blank=True)
    consultant = models.ForeignKey("UserProfile", verbose_name="咨询顾问", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag",blank=True)
    remark = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户信息表"
        verbose_name_plural = "客户信息表"

    pass


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class CustomerFollowUp(models.Model):
    '''客户记录跟进'''
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile", verbose_name="跟进人", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    intention_choices = ((0, '2周内报名'),
                         (1, '1个月内报名'),
                         (2, '近期无报名计划'),
                         (3, '已在其他机构报名'),
                         (4, '已报名'),
                         (5, '已拉黑'),
                         )
    intention = models.SmallIntegerField(choices=intention_choices)

    def __str__(self):
        return "<%s : %s>" % (self.customer, self.intention)

    class Meta:
        verbose_name = "客户记录跟进表"
        verbose_name_plural = "客户记录跟进表"

    pass


# class UserProfile(models.Model):
#     ''' 用户表 '''
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=32)
#     roles = models.ManyToManyField('Role', blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "用户表"
#         verbose_name_plural = "用户表"
#
#     pass


class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField('Menu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = "角色表"

    pass


class Course(models.Model):
    '''课程'''
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="周期（月）")
    outline = models.TextField(verbose_name="大纲")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = "课程表"

    pass


class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    class Meta:
        verbose_name = "校区表"
        verbose_name_plural = "校区表"
    def __str__(self):
        return self.name

class Cls(models.Model):
    '''班级'''
    branch = models.ForeignKey("Branch", verbose_name="校区", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    contract = models.ForeignKey("ContractTemplate", on_delete=models.CASCADE,blank=True,null=True)
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    cls_type_choices = ((0, "面授（脱产）"),
                        (1, "面授（周末）"),
                        (2, "网络班"),
                        )
    cls_type = models.SmallIntegerField(choices=cls_type_choices, verbose_name="班级类型")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="毕业日期", blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester')
        verbose_name = "班级表"
        verbose_name_plural = "班级表"

    pass


class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    cls = models.ForeignKey('Cls', verbose_name='报名班级', on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问', on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False, verbose_name='学员已同意条款')
    contract_approved = models.BooleanField(default=False, verbose_name='合同已审核')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.customer, self.cls)

    class Meta:
        unique_together = ('customer', 'cls')
        verbose_name = "报名表"
        verbose_name_plural = "报名表"

    pass

class ContractTemplate(models.Model):
    '''合同模板'''
    name = models.CharField('合同名称',max_length=64,unique=True)
    template = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '合同模板'
        verbose_name_plural = '合同模板'
    pass


class Payment(models.Model):
    '''缴费记录'''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='金额', default=500)
    consultant = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('Course', verbose_name='所报课程', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)

    class Meta:
        verbose_name = "缴费记录表"
        verbose_name_plural = "缴费记录表"


class CourseRecord(models.Model):
    '''上课记录'''
    cls = models.ForeignKey('Cls', verbose_name='班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='节次')
    teacher = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.cls, self.day_num)

    class Meta:
        unique_together = ('cls', 'day_num')

        verbose_name = "上课记录表"
        verbose_name_plural = "上课记录表"


pass


class StudyRecord(models.Model):
    '''学习记录'''
    student = models.ForeignKey("Enrollment", on_delete=models.CASCADE)
    course_record = models.ForeignKey("CourseRecord", on_delete=models.CASCADE)
    attendance_choices = (
        (0, '已签到'),
        (1, '迟到'),
        (2, '缺勤'),
        (3, '早退'),
    )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0)
    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (-100, 'COPY'),
        (0, 'N/A'),
    )
    score = models.SmallIntegerField(choices=score_choices)
    remark = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.student, self.course_record, self.score)
    class Meta:
        unique_together = ('student','course_record')
        verbose_name = "学习记录表"
        verbose_name_plural = "学习记录表"

    pass
class Menu(models.Model):
    '''菜单'''
    name = models.CharField(max_length=32)
    url_type_choice = ((1,'alias'),
                       (2,'abslute_url'),)
    url_type = models.SmallIntegerField(choices=url_type_choice,default=2)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = '菜单表'

class UserProfileManager(BaseUserManager):
    '''创建和保存用户与给定的电子邮件，日期出生和密码。'''
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name = name,
        )
        # user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''用户表'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    roles = models.ManyToManyField("Role",blank=True)
    name = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(_('password'), max_length=128,help_text='''<a href="password/">点我改密码</a>''')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    stu_account = models.ForeignKey("Customer",verbose_name='关联学员帐号',blank=True,null=True,help_text='报名缴费后方可为其申请帐号',on_delete=models.CASCADE)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # def __str__(self):
    #
    #     return self.name

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"
