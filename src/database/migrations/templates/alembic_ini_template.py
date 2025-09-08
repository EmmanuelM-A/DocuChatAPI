"""
Stores the template to create an Alembic ini file.
"""

ALEMBIC_INI_TEMPLATE = """# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = src/database/migrations

# template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
prepend_sys_path = .

# timezone to use when rendering the date
timezone = UTC

# max length of characters to apply to the "slug" field
truncate_slug_length = 40

# set to 'true' to run the environment during the 'revision' command
revision_environment = false

# set to 'true' to allow .pyc and .pyo files without a source .py file
sourceless = false

# version number format
version_num_format = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s

# line length limit to use in the automatically generated revision files
# Default is 120, setting to None removes the limit
line_length = 120

# the output encoding used when revision files are written
output_encoding = utf-8

# Database URL (placeholder - will be set dynamically by MigrationManager)
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/db

[post_write_hooks]
# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
