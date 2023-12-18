with open("license/license.json", "r") as f: license_data = __import__("json").loads(f.read())

APP_NAME = license_data["app_name"]
CATEGORY = license_data["category"]
WEB_APP = license_data["web_app"]
STATUS = license_data["status"]
CO_FOUNDER = license_data["co_founder"]
TEAM_LEADER = license_data["team_leader"]
TEAM = license_data["team"]
COPYRIGHT_HOLDER = license_data["copyright_holder"]
VERSION = license_data["version"]
DATE_CREATED = license_data["date_created"]
