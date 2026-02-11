"""List all Flask routes"""
from web_frontend import app

print("All registered routes:")
print("=" * 60)
for rule in app.url_map.iter_rules():
    print(f"{rule.rule:40} {str(rule.methods):30}")
print("=" * 60)
