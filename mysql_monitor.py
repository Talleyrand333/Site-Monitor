from replication_monitor import DatabaseMonitor
from text_color import DatabaseMonitor_T

moni = DatabaseMonitor_T()
moni.send_mail()
# moni.check_database_uptime_status()

