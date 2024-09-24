from tortoise import fields, models

class Manager(models.Model):
    id = fields.IntField(pk=True)
    manager = fields.CharField(max_length=20)
    password = fields.CharField(max_length=20)
    create_time = fields.DatetimeField(auto_now_add=True)
    score = fields.FloatField(default=0.0)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = "manager"

class LegymCustomer(models.Model):
    id = fields.IntField(pk=True)
    create_time = fields.DatetimeField(auto_now_add=True)
    manager = fields.CharField(max_length=20)
    username = fields.CharField(max_length=20)
    password = fields.CharField(max_length=20)
    schoolName = fields.CharField(max_length=20)
    runType = fields.CharField(max_length=20)
    total_goals = fields.FloatField(default=0.0)
    day_goals = fields.FloatField(default=0.0)
    day_in_week = fields.IntField(default=5)
    rounds = fields.IntField(default=0)
    #开刷设置
    begin_state = fields.BooleanField(default=True)
    runTime = fields.CharField(max_length=20) # 跑步时间(8~12,13~18,19~21,22~24)
    
    # 任务统计
    is_run = fields.BooleanField(default=False)
    complete_goals = fields.FloatField(default=0.0)
    complete_day_in_week = fields.IntField(default=0)

    class Meta:
        table = "legym_customer"
