import time
from create_project_daily_report import create_new_daily_report
from get_template import get_template_by_id
from create_status_page import create_status_page

SECONDS_IN_ONE_DAY = 86400

STATUS_PAGE_TEMPLATE_ID = 811401235
STATUS_PAGE_PARENT_PAGE_ID = 811368466
STATUS_PAGE_SPACE_KEY = 'SR'

PROJECTS = {
    'Dungeon': {
        'ParentPageID': 808648705,
        'TemplateID': 808616025,
        'SpaceKeyID': 'DC'
    },
    'HOPA': {
        'ParentPageID': 811368459,
        'TemplateID': 808616025,
        'SpaceKeyID': 'KB'
    }
}


def create_daily_reports():
    for project_name, project_data in PROJECTS.items():
        template_id = project_data.get('TemplateID')
        parent_page_id = project_data.get('ParentPageID')
        space_key = project_data.get('SpaceKeyID')

        template = get_template_by_id(template_id)
        value_storage = template.get('body').get('storage').get('value')
        page_id = create_new_daily_report(parent_page_id, space_key, value_storage, project_name)
        print(page_id)


def create_daily_status():
    template = get_template_by_id(STATUS_PAGE_TEMPLATE_ID)
    value_storage = template.get('body').get('storage').get('value')
    page_id = create_status_page(STATUS_PAGE_PARENT_PAGE_ID, STATUS_PAGE_SPACE_KEY, value_storage)

    print(page_id)


def main_function():
    while True:
        create_daily_reports()
        create_daily_status()
        time.sleep(SECONDS_IN_ONE_DAY)


if __name__ == '__main__':
    main_function()
