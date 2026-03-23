# How to run the link checker locally or in CI

## Run locally

1. Create a venv and install deps:

   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
   pip install requests beautifulsoup4 tqdm

2. Run the checker:

   python tools/link_check.py https://quantumpiforge.com/ --workers 16 --output results.csv

## CI / GitHub Actions

- A workflow template is included at `infra/link-check.yml`. Copy it to `.github/workflows/link-check.yml` (or request an admin to enable it) to run daily and on-demand via `workflow_dispatch`.

## Notes
- The workflow uploads `link_check_results.csv` as an artifact called `link-check-results`.
- To change the site, set env `LINK_CHECK_SITE` in the workflow or pass as the action input.
