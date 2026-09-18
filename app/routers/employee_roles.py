from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.models.employee_roles import EmployeeRole
from app.models.employees import Employees
from app.models.roles import Role
from app.schemas.employee_roles import EmployeeRolesCreate, EmployeeRolesResponse
from app.utils.checked import check_ident

router = APIRouter(tags=['Employee_Roles'], prefix="/employee_roles")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_employee_role(employee_role: EmployeeRolesCreate, db: MyDb):

    result = await db.scalar(select(EmployeeRole).
                              where(
        EmployeeRole.employee_id == employee_role.employee_id,
        EmployeeRole.branch_id == employee_role.branch_id,
        EmployeeRole.role_id == employee_role.role_id
    ))

    if result:
        raise HTTPException(409, "Employee role already exists")


    await check_ident(db, Employees, employee_role.employee_id)
    await check_ident(db, Role, employee_role.role_id)
    await check_ident(db, Branch, employee_role.branch_id)

    obj = EmployeeRole(
        **employee_role.model_dump()
    )
    db.add(obj)
    await db.commit()
    return {"msg": "Employee role created successfully"}


@router.get('/', response_model=list[EmployeeRolesResponse])
async def list_employee_roles(db: MyDb):

    result = await db.execute(select(EmployeeRole))

    return result.scalars().all()
