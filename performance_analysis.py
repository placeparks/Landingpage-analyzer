import subprocess
import json

def analyze_performance_directly(url):
    lighthouse_cmd_path = r'C:\Users\place\AppData\Roaming\npm\lighthouse.cmd'
    
    result = subprocess.run([lighthouse_cmd_path, url, '--quiet', '--no-update-notifier', '--output=json', '--output-path=stdout'], capture_output=True, text=True, encoding='utf-8')
    if result.stderr:
        print("Error in Lighthouse analysis:", result.stderr)
        return None
    # Parse the JSON output directly from stdout
    performance_results = json.loads(result.stdout)
    return performance_results
 

