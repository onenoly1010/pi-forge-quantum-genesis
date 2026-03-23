# Stale PR Management Workflow

## Overview

The Stale PR Management workflow automatically monitors and manages pull requests that have become inactive, helping maintain a clean and active repository.

## Features

### 🔍 Automatic Inactivity Detection

The workflow tracks PR activity including:
- Commits pushed to the PR branch
- Comments on the PR (excluding bot comments)
- Review submissions and comments
- PR updates

### 📅 Three-Tier Management System

#### Day 7: First Reminder
- **Trigger**: No activity for 7 days
- **Action**: Posts a comment tagging assignees and reviewers
- **Message**: Includes timeline and instructions to keep PR active

#### Day 14: Stale Label
- **Trigger**: No activity for 14 days
- **Action**: Applies the `stale` label to the PR
- **Message**: Posts a comment explaining the label and next steps

#### Day 30: Auto-Close
- **Trigger**: No activity for 30 days
- **Action**: Closes the PR with a comment
- **Reopening**: PR can be reopened at any time with clear instructions provided

### 🎯 Smart Activity Tracking

The workflow:
- Only counts human activity (excludes bot comments)
- Tracks the most recent activity across all types
- Automatically removes the stale label if activity resumes
- Prevents duplicate reminder notifications

## Schedule

- **Automatic**: Runs daily at 2:00 AM UTC via cron schedule
- **Manual**: Can be triggered via workflow_dispatch with optional dry-run mode

## Usage

### Manual Workflow Trigger

You can manually trigger the workflow from the GitHub Actions tab:

1. Go to **Actions** → **Stale PR Management**
2. Click **Run workflow**
3. (Optional) Enable **Dry run mode** to see what would happen without taking action
4. Click **Run workflow**

### Dry Run Mode

When enabled, the workflow will:
- Analyze all open PRs
- Log what actions would be taken
- Not post any comments, apply labels, or close PRs
- Provide a summary of actions that would occur

This is useful for:
- Testing the workflow configuration
- Understanding what PRs would be affected
- Validating the workflow before enabling automatic runs

## Keeping PRs Active

To prevent a PR from being marked as stale or closed, contributors can:

1. **Add a comment** with a status update
2. **Push new commits** to the PR branch
3. **Request a review** from team members
4. **Submit or respond to reviews**

Any of these actions will reset the inactivity timer.

## Configuration

The workflow configuration is defined in `.github/workflows/stale-pr-management.yml`.

### Adjustable Parameters

You can modify these constants in the workflow file:

```javascript
const INACTIVE_DAYS_FIRST_REMINDER = 7;  // Days until first reminder
const INACTIVE_DAYS_STALE_LABEL = 14;    // Days until stale label
const INACTIVE_DAYS_AUTO_CLOSE = 30;     // Days until auto-close
const STALE_LABEL = 'stale';             // Label name
```

### Required Permissions

The workflow requires:
- `pull-requests: write` - To add labels and close PRs
- `issues: write` - To post comments

## Reopening Closed PRs

If a PR is automatically closed:

1. Navigate to the closed PR
2. Click **Reopen pull request**
3. Add a comment explaining your plan to continue work
4. The PR will be active again and the timer resets

## Notifications

When the workflow takes action:

- **Assignees** and **reviewers** are mentioned in reminder comments
- Clear instructions are provided for keeping the PR active
- All comments include a note that they are automated

## Workflow Summary

After each run, the workflow provides a summary showing:
- Number of PRs processed
- First reminders sent
- Stale labels added
- PRs closed

View the summary in the **Actions** tab under the workflow run.

## Best Practices

### For Contributors

- Update your PR regularly, even if just to add a comment about progress
- Respond to reviews and feedback promptly
- If you need more time, add a comment explaining the situation
- Don't let PRs sit idle - either complete them or close them

### For Maintainers

- Review stale PRs before they auto-close
- Consider adjusting the timeframes if needed for your project
- Use dry-run mode to test configuration changes
- Monitor the workflow summaries to understand PR activity patterns

## Troubleshooting

### PR was marked stale but shouldn't be

If a PR was incorrectly marked as stale:
1. Add a comment to explain the situation
2. The stale label will be automatically removed
3. Consider if the timeframes need adjustment

### Workflow not running

Check that:
1. The workflow file is in `.github/workflows/`
2. The cron schedule is valid
3. GitHub Actions is enabled for the repository
4. The workflow has the required permissions

### Bot comments not appearing

Ensure:
1. The workflow has `pull-requests: write` permission
2. The GitHub token has access to the repository
3. Check the workflow run logs for errors

## Canon Alignment

This workflow embodies the Quantum Pi Forge principles:

- **Clarity**: Transparent process with clear communication
- **Autonomy**: Self-managing without hierarchical intervention
- **Coordination**: Helps contributors stay synchronized
- **Improvement**: Continuously maintains repository health

The workflow serves as a gentle coordinator, not a command structure, guiding contributors with helpful reminders while respecting their autonomy to reopen and continue work at any time.
