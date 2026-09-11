import urllib.request, json
try:
    resp = urllib.request.urlopen('https://api.github.com/repos/Doppler2u/doppler-inference-node/actions/runs')
    data = json.loads(resp.read())
    runs = data.get('workflow_runs', [])
    if not runs:
        print("No workflow runs found!")
    for run in runs:
        print(f"Run {run['id']}: status={run['status']}, conclusion={run['conclusion']}, created={run['created_at']}, name={run['name']}")
except Exception as e:
    print(e)
