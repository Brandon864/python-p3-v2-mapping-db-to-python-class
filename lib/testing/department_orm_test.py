# testing/department_orm_test.py
import pytest
from lib.department import Department
from lib.__init__ import CONN, CURSOR

@pytest.fixture(scope="module")
def db_setup():
    Department.drop_table()
    Department.create_table()
    Department.create("Payroll", "Building A, 5th Floor")
    Department.create("Human Resources", "Building C, East Wing")
    yield
    Department.drop_table()

def test_instance_from_db(db_setup):
    row = CURSOR.execute("SELECT * FROM departments WHERE id = 1").fetchone()
    department = Department.instance_from_db(row)
    assert department.id == 1
    assert department.name == "Payroll"
    assert department.location == "Building A, 5th Floor"

def test_get_all(db_setup):
    departments = Department.get_all()
    assert len(departments) == 2
    assert departments[0].name == "Payroll"
    assert departments[1].name == "Human Resources"

def test_find_by_id(db_setup):
    department = Department.find_by_id(1)
    assert department is not None
    assert department.id == 1
    assert department.name == "Payroll"
    assert Department.find_by_id(999) is None

def test_find_by_name(db_setup):
    department = Department.find_by_name("Human Resources")
    assert department is not None
    assert department.id == 2
    assert department.name == "Human Resources"
    assert Department.find_by_name("Nonexistent") is None

def test_delete(db_setup):
    department = Department.find_by_id(1)
    department_id = department.id
    department.delete()
    assert Department.find_by_id(department_id) is None
    assert department.id is None
    assert department_id not in Department.all