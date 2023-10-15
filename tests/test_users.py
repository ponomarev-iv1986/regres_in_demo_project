import allure
import jsonschema
import pytest
from allure_commons.types import Severity

from regres_in_demo_project import utils


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.NORMAL)
@allure.step('verify status code')
def test_list_users_status_code():
    response = utils.request('get', '/api/users')

    assert response.status_code == 200


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.CRITICAL)
@allure.step('validate json schema')
def test_list_users_validate_json_schema():
    response = utils.request('get', '/api/users')

    jsonschema.validate(
        response.json(),
        utils.load_schema('list_users_json_schema.json')
    )


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.NORMAL)
@allure.step('verify pagination')
@pytest.mark.parametrize('page, per_page', [(1, 6), (2, 6), (1, 2),
                                            (2, 2), (3, 2), (1, 3),
                                            (2, 3), (3, 3), (4, 3)])
def test_list_users_pagination(page, per_page):
    params = {
        'page': page,
        'per_page': per_page
    }
    response = utils.request('get', '/api/users', params=params)
    body = response.json()

    assert body['page'] == page
    assert body['per_page'] == per_page
    assert len(body['data']) == per_page


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.NORMAL)
@allure.step('verify status code')
def test_single_user_status_code():
    response = utils.request('get', f'/api/users/1')

    assert response.status_code == 200


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.CRITICAL)
@allure.step('validate json schema')
def test_single_user_validate_json_schema():
    response = utils.request('get', f'/api/users/1')

    jsonschema.validate(
        response.json(),
        utils.load_schema('single_user_json_schema.json')
    )


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.CRITICAL)
@allure.step('verify user data')
@pytest.mark.parametrize('user_id, email, first_name, last_name',
                         [
                             (1, 'george.bluth@reqres.in', 'George', 'Bluth'),
                             (2, 'janet.weaver@reqres.in', 'Janet', 'Weaver'),
                             (3, 'emma.wong@reqres.in', 'Emma', 'Wong')
                         ])
def test_user_data(user_id, email, first_name, last_name):
    response = utils.request('get', f'/api/users/{user_id}')
    data = response.json()['data']

    assert data['id'] == user_id
    assert data['email'] == email
    assert data['first_name'] == first_name
    assert data['last_name'] == last_name


@allure.tag('reqres.in')
@allure.label('owner', 'ponomarev-iv1986')
@allure.severity(Severity.NORMAL)
@allure.step('verify user not found error')
def test_single_user_not_found():
    response = utils.request('get', f'/api/users/23')

    assert response.status_code == 404
    assert not response.json()
