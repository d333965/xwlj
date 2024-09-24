import schedule
import time
from tortoise import Tortoise, run_async
from datetime import datetime
from method.login import LoginGetInfo, getsemesterId, Oct_SecretKey
from method.routeLine import getRouteLine
from method.runUpLoad import runTask
import sys
import os

# 获取当前文件所在目录的上一级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))

# 将项目根目录添加到 sys.path
sys.path.append(root_dir)

from app.mysql.models import LegymCustomer
from app.mysql.settings import get_tortoise_config

async def initialize():
    # 初始化数据库连接
    await Tortoise.init(config=get_tortoise_config())
    await Tortoise.generate_schemas()

async def process_customer(customer):
    try:
        # 检查是否完成总目标
        if customer.complete_goals >= customer.total_goals:
            await customer.delete()
            print(f"用户 {customer.username} 已完成总目标,已从数据库中删除")
            return
        # 检查今天是否为周一
        if datetime.now().weekday() == 0:
            customer.complete_day_in_week = 0
            await customer.save()
            print(f"用户 {customer.username} 周一重置")
            return
        # 检查本周任务是否完成day_in_week
        if customer.complete_day_in_week >= customer.day_in_week:
            customer.is_run = True
            await customer.save()
            print(f"用户 {customer.username} 本周任务已完成,已重置")
            return

        # 检查当前时间是否在跑步时间内
        current_hour = datetime.now().hour
        run_times = customer.runTime.split(',')
        is_run_time = any(start <= current_hour < end for time_range in run_times for start, end in [map(int, time_range.split('~'))])

        if not is_run_time:
            print(f"用户 {customer.username} 当前不在跑步时间内")
            return

        # 登录获取信息
        accessToken, schoolId, userId = LoginGetInfo(customer.username, customer.password)
        OctSecretKey = Oct_SecretKey(userId, schoolId)
        routine_line = getRouteLine(customer.schoolName, customer.rounds)
        semesterId = getsemesterId(accessToken, schoolId)

        # 执行跑步任务
        max_attempts = 11
        attempt = 0
        while attempt < max_attempts:
            message = runTask(customer.day_goals, accessToken, semesterId, routine_line, customer.runType, OctSecretKey)
            
            if message == None:
                customer.complete_goals += customer.day_goals
                customer.complete_day_in_week += 1
                customer.is_run = True
                await customer.save()
                print(f"用户 {customer.username} 成功完成跑步任务")
                break
            elif message == "success":
                attempt += 1
                print(f"用户 {customer.username} 跑步请求失败,message返回success。尝试第 {attempt} 次")
                if attempt == max_attempts:
                    print(f"用户 {customer.username} 已达到最大尝试次数,跳过此用户")
            else:
                print(f"用户 {customer.username} 未知错误")
                break

    except Exception as e:
        print(f"处理用户 {customer.username} 时发生错误：{str(e)}")
        # 可以在这里添加更多的错误处理逻辑，比如标记用户状态或发送通知
        return

async def main():
    await initialize()
    # 如果现在时间在01:00~06:00之间，则重置is_run=False
    if datetime.now().hour >= 1 and datetime.now().hour < 6:
        customers = await LegymCustomer.filter(is_run=True)
        for customer in customers:
            customer.is_run = False
            await customer.save()
            print(f"用户 {customer.username} 已重置")
    else:
        # 获取所有begin_state为True且is_run为False的用户
        customers = await LegymCustomer.filter(begin_state=True, is_run=False)

        for customer in customers:
            await process_customer(customer)

    # 关闭数据库连接
    await Tortoise.close_connections()

def run_main():
    run_async(main())

if __name__ == "__main__":
    # 设置定时任务，每2分钟执行一次
    schedule.every(2).minutes.do(run_main)

    # 运行定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)