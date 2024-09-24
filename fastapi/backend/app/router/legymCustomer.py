from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.mysql.models import Manager, LegymCustomer
from tortoise.exceptions import DoesNotExist
from app.runTask.method.login import LoginGetInfo

router = APIRouter()

# 创建用户
@router.post("/create")
async def create(request: Request):
    # 获取请求体数据
    data = await request.json()
    manager = data.get("manager")
    username = data.get("username")
    password = data.get("password")
    runType = data.get("runType")
    schoolName = data.get("schoolName")
    runTime = data.get("runTime")
    total_goals = data.get("total_goals")
    day_goals = data.get("day_goals")
    day_in_week = data.get("day_in_week")
    rounds = data.get("rounds")
    print(manager, username, password, runType, schoolName, runTime, total_goals, day_goals, day_in_week, rounds)
    # 验证账号密码
    if LoginGetInfo(username, password) == "账号密码错误":
        return JSONResponse(content={"message": "账号密码错误"}, status_code=400)
    
    try:
        manager_obj = await Manager.get(manager=manager)
        
        # 检查Manager的score是否足够
        if manager_obj.score < total_goals:
            return JSONResponse(content={"message": "您的乐点不足，请充值"}, status_code=400)
        if total_goals < day_goals:
            return JSONResponse(content={"message": "总km数不能小于每天km数"}, status_code=400)
        # 创建新的 LegymCustomer 记录
        new_customer = await LegymCustomer.create(
            manager=manager,
            username=username,
            password=password,
            schoolName=schoolName,
            runType=runType,
            total_goals=total_goals,
            day_goals=day_goals,
            day_in_week=day_in_week,
            rounds=rounds,
            runTime=runTime,
        )
        
        # 扣除Manager的score
        manager_obj.score -= total_goals
        await manager_obj.save()
        
        return JSONResponse(content={"message": f"创建成功,扣除{total_goals}乐点"}, status_code=201)
    
    except DoesNotExist:
        print("创建者不存在")
        return JSONResponse(content={"message": "创建者不存在"}, status_code=404)
    except Exception as e:
        print(f"创建失败: {str(e)}")
        return JSONResponse(content={"message": f"创建失败: {str(e)}"}, status_code=400)

# 更新开始状态
@router.post("/begin_state")
async def begin_state(request: Request):
    data = await request.json()
    id = data.get("id")
    manager = data.get("manager")
    username = data.get("username")
    
    try:
        customer = await LegymCustomer.get(id=id,manager=manager, username=username)
        customer.begin_state = not customer.begin_state
        await customer.save()
        return JSONResponse(content={"message": "开始状态更新成功", "begin_state": customer.begin_state}, status_code=200)
    except DoesNotExist:
        return JSONResponse(content={"message": "用户不存在"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": f"更新失败: {str(e)}"}, status_code=400)

# 删除用户
@router.post("/delete")
async def delete(request: Request):
    data = await request.json()
    id = data.get("id")
    manager = data.get("manager")
    username = data.get("username")

    try:
        customer = await LegymCustomer.get(id=id,manager=manager, username=username)
        
        # 计算未完成的积分
        remaining_goals = customer.total_goals - customer.complete_goals
        
        if remaining_goals > 0:
            # 获取对应的 Manager
            manager_obj = await Manager.get(manager=manager)
            
            # 将未完成的积分加到 Manager 的 score 中
            manager_obj.score += remaining_goals
            await manager_obj.save()
        
        # 删除客户
        await customer.delete()
        return JSONResponse(content={"message": f"删除成功,返还 {remaining_goals} 积分给管理员"}, status_code=200)
    except DoesNotExist:
        return JSONResponse(content={"message": "用户不存在"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": f"删除失败: {str(e)}"}, status_code=400)

# 获取manager相关的所有用户信息
@router.post("/get_info")
async def get_info(request: Request):
    data = await request.json()
    manager = data.get("manager")
    
    try:
        customers = await LegymCustomer.filter(manager=manager)
        
        if not customers:
            return JSONResponse(content={"message": "该管理员下没有用户"}, status_code=404)
        
        customers_info = []
        for customer in customers:
            customers_info.append({
                "id": customer.id,
                "create_time": customer.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "manager": customer.manager,
                "username": customer.username,
                "password": customer.password,
                "schoolName": customer.schoolName,
                "runType": customer.runType,
                "total_goals": customer.total_goals,
                "day_goals": customer.day_goals,
                "day_in_week": customer.day_in_week,
                "rounds": customer.rounds,
                "begin_state": customer.begin_state,
                "runTime": customer.runTime,
                "is_run": customer.is_run,
                "complete_goals": customer.complete_goals,
                "complete_day_in_week": customer.complete_day_in_week
            })
        
        return JSONResponse(content={"customers": customers_info}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"获取信息失败: {str(e)}"}, status_code=400)
