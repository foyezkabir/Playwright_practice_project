# CI/CD Setup Guide

## Overview
This project includes a complete GitHub Actions workflow for automated testing with Playwright. The CI/CD pipeline runs tests automatically on every push and pull request, generates comprehensive reports, and publishes them to GitHub Pages.

## What's Included

### Automated Workflows
- **Playwright Tests CI** (`.github/workflows/playwright-tests.yml`)
  - Runs on: Push to `master`/`main`/`develop` branches, Pull Requests, Manual trigger
  - Platform: Windows (can be changed to ubuntu-latest or macos-latest)
  - Browser: Chromium (configurable for Firefox, WebKit)

### CI/CD Features

#### ✅ Automated Test Execution
- Runs all Playwright tests in headless mode
- Executes on every push and pull request
- Supports manual workflow dispatch
- Matrix strategy for multiple browser testing

#### 📊 Report Generation
- **Allure Reports**: Interactive HTML reports with detailed test results
- **HTML Reports**: Basic pytest-html reports
- **Screenshots**: Automatic capture on test failures
- **Test Results**: Raw Allure results for analysis

#### 📦 Artifact Upload
- Test reports stored for 30 days
- Screenshots available for failed tests
- Allure results for historical tracking
- HTML reports for quick review

#### 🌐 GitHub Pages Deployment
- Allure reports automatically published to GitHub Pages
- Accessible at: `https://<username>.github.io/<repository>/allure-report`
- Historical test results preserved (last 20 reports)
- Updates on every master branch push

## Setup Instructions

### 1. Enable GitHub Actions (Already Done)
The workflow file is already created at `.github/workflows/playwright-tests.yml`

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. Click **Save**

### 3. Set Repository Permissions

1. Go to **Settings** → **Actions** → **General**
2. Scroll to "Workflow permissions"
3. Select **"Read and write permissions"**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**

### 4. Trigger First Run

**Option 1: Automatic (On Next Push)**
```powershell
git add .
git commit -m "feat: Add CI/CD pipeline with GitHub Actions"
git push origin master
```

**Option 2: Manual Trigger**
1. Go to **Actions** tab on GitHub
2. Select "Playwright Tests CI" workflow
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"**

### 5. View Results

#### View Test Execution
1. Go to **Actions** tab
2. Click on the latest workflow run
3. View logs, test results, and download artifacts

#### View Allure Report (GitHub Pages)
After first successful run with Pages enabled:
- URL: `https://<your-username>.github.io/<repository-name>/allure-report`
- Example: `https://foyezkabir.github.io/Playwright_practice_project/allure-report`

#### Download Artifacts
1. Go to completed workflow run
2. Scroll to "Artifacts" section
3. Download:
   - `allure-report-chromium` - Complete Allure report
   - `html-report-chromium` - Basic HTML report
   - `test-screenshots-chromium` - Screenshots from failures
   - `allure-results-chromium` - Raw test results

## Workflow Configuration

### Current Settings
```yaml
Browser: chromium
Platform: windows-latest
Timeout: 60 minutes
Artifact Retention: 30 days
Report History: 20 reports
```

### Customization Options

#### Change Browser
Edit `.github/workflows/playwright-tests.yml`:
```yaml
matrix:
  browser: [chromium, firefox, webkit]  # Test on multiple browsers
```

#### Change Platform
```yaml
runs-on: ubuntu-latest  # or macos-latest
```

#### Adjust Timeouts
```yaml
timeout-minutes: 60  # Change to your needs
```

#### Run on Different Branches
```yaml
on:
  push:
    branches: [ master, develop, feature/* ]
```

#### Change Artifact Retention
```yaml
retention-days: 30  # Change to your needs (max 90 days)
```

## CI Environment Configuration

### Automatic Headless Mode
The project automatically detects CI environment and runs in headless mode:

```python
# In utils/config.py
HEADLESS = os.getenv("CI", "false").lower() == "true"
```

No manual configuration needed!

### Environment Variables
Currently, test credentials are hardcoded for QA environment. For production or sensitive data:

1. Add secrets in GitHub:
   - Go to **Settings** → **Secrets and variables** → **Actions**
   - Click **"New repository secret"**
   - Add: `TEST_EMAIL`, `TEST_PASSWORD`, etc.

2. Use in workflow:
```yaml
- name: Run tests
  env:
    TEST_EMAIL: ${{ secrets.TEST_EMAIL }}
    TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
  run: pytest
```

3. Access in tests:
```python
import os
email = os.getenv("TEST_EMAIL", "default@example.com")
```

## Monitoring & Notifications

### Email Notifications
GitHub automatically sends email notifications for:
- Workflow failures
- First workflow success after failures

Configure in: **GitHub Settings** → **Notifications** → **Actions**

### Slack Integration (Optional)
Add to workflow:
```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Test Results: ${{ job.status }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

### Status Badge
Add to README.md:
```markdown
[![Playwright Tests](https://github.com/<username>/<repo>/actions/workflows/playwright-tests.yml/badge.svg)](https://github.com/<username>/<repo>/actions/workflows/playwright-tests.yml)
```

## Troubleshooting

### Workflow Not Running
- Check if Actions are enabled in repository settings
- Verify workflow file syntax (use GitHub's workflow editor)
- Check branch name matches workflow configuration

### Tests Failing in CI but Passing Locally
- Check timeout values (CI might be slower)
- Verify all dependencies in requirements.txt
- Check for environment-specific issues
- Review CI logs for specific error messages

### GitHub Pages Not Updating
- Ensure workflow has write permissions
- Check if gh-pages branch exists
- Verify Pages settings point to gh-pages branch
- Wait 2-3 minutes after workflow completes

### Artifacts Not Uploading
- Check artifact paths in workflow
- Ensure files exist after test run
- Verify artifact names are unique
- Check workflow permissions

### Allure Report Empty
- Verify pytest runs with `--alluredir=allure-results`
- Check allure-results directory contains JSON files
- Ensure Allure generates report successfully
- Review workflow logs for errors

## Cost Considerations

### GitHub Actions Minutes
- **Free tier**: 2,000 minutes/month for private repos
- **Public repos**: Unlimited
- **Current workflow**: ~10-15 minutes per run

### Storage
- **Free tier**: 500 MB for artifacts
- **Current usage**: ~50-100 MB per run
- **Retention**: 30 days (adjustable)

### Optimization Tips
1. Run on pull requests only (not every push)
2. Reduce artifact retention days
3. Run fewer browser combinations
4. Use caching for dependencies
5. Run critical tests first, full suite nightly

## Advanced Features

### Scheduled Runs (Nightly Tests)
Add to workflow:
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2 AM UTC daily
```

### Parallel Test Execution
```yaml
- name: Run tests in parallel
  run: pytest -n 4  # 4 parallel workers
```

### Test Sharding (For Large Test Suites)
```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: pytest --shard-id=${{ matrix.shard }} --num-shards=4
```

### Conditional Execution
```yaml
- name: Run only smoke tests on PR
  if: github.event_name == 'pull_request'
  run: pytest -m smoke

- name: Run full suite on push
  if: github.event_name == 'push'
  run: pytest
```

## Next Steps

1. ✅ Push the CI/CD workflow to GitHub
2. ✅ Enable GitHub Pages in repository settings
3. ✅ Set repository permissions for Actions
4. ✅ Trigger first workflow run
5. ✅ Monitor execution in Actions tab
6. ✅ Access Allure report on GitHub Pages
7. ✅ Add status badge to README
8. 🔄 Customize workflow as needed

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Playwright CI Guide](https://playwright.dev/docs/ci)
- [Allure GitHub Pages](https://github.com/simple-elf/allure-report-action)
- [GitHub Pages Setup](https://docs.github.com/en/pages)

---

**Status**: ✅ Fully Configured and Ready to Use
