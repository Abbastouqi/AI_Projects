"""
System Control Skill
Handles desktop applications and system tasks
"""

import os
import subprocess
import platform
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemControl:
    def __init__(self):
        self.os_type = platform.system()
        self.scheduled_tasks = []
        
    def open_application(self, app_name: str, **kwargs) -> Dict[str, Any]:
        """Open a desktop application"""
        try:
            logger.info(f"Opening: {app_name}")
            
            app_map = {
                'chrome': 'start chrome' if self.os_type == 'Windows' else 'google-chrome',
                'chromium': 'start chrome' if self.os_type == 'Windows' else 'chromium',
                'firefox': 'start firefox' if self.os_type == 'Windows' else 'firefox',
                'word': 'start winword' if self.os_type == 'Windows' else 'libreoffice --writer',
                'excel': 'start excel' if self.os_type == 'Windows' else 'libreoffice --calc',
                'notepad': 'start notepad' if self.os_type == 'Windows' else 'gedit',
                'calculator': 'start calc' if self.os_type == 'Windows' else 'gnome-calculator',
                'terminal': 'start cmd' if self.os_type == 'Windows' else 'terminal',
                'explorer': 'start explorer' if self.os_type == 'Windows' else 'nautilus',
                'powershell': 'start powershell' if self.os_type == 'Windows' else 'bash'
            }
            
            app_cmd = app_map.get(app_name.lower(), app_name)
            logger.info(f"Executing command: {app_cmd}")
            
            if self.os_type == 'Windows':
                subprocess.Popen(app_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(app_cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return {
                'status': 'success',
                'application': app_name,
                'message': f'Opened {app_name}',
                'command_executed': app_cmd
            }
            
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return {'status': 'error', 'message': str(e), 'application': app_name}
    
    def schedule_task(self, task: str, time: str = None, date: str = None, **kwargs) -> Dict[str, Any]:
        """Schedule a task"""
        task_info = {
            'task': task,
            'time': time,
            'date': date,
            'created': datetime.now().isoformat()
        }
        self.scheduled_tasks.append(task_info)
        
        return {
            'status': 'success',
            'message': f'Task "{task}" scheduled',
            'details': task_info
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system info"""
        return {
            'os': self.os_type,
            'platform': platform.platform(),
            'scheduled_tasks': len(self.scheduled_tasks)
        }

if __name__ == "__main__":
    sc = SystemControl()
    print(sc.get_system_info())
